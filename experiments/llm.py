"""Shared LLM client: OpenRouter (OpenAI-compatible) with disk cache, token/latency logging, retries.
`mock=True` gives an offline stand-in used ONLY to test the plumbing (never for results)."""
import hashlib, json, os, random, re, threading, time, urllib.request, urllib.error

MOCK_TRUTH = {}   # task_id -> dict(answer=..., wrong=...)   (filled by tests only)


class LLMClient:
    def __init__(self, model="openai/gpt-4o-mini", temperature=0.0, seed=0, cache_path=None, mock=False,
                 key_env="OPENROUTER_API_KEY", base_url="https://openrouter.ai/api/v1/chat/completions",
                 retries=5, max_tokens=700):
        self.model, self.temp, self.seed, self.mock = model, temperature, seed, mock
        self.key = os.environ.get(key_env); self.url = base_url; self.retries = retries; self.max_tokens = max_tokens
        self.lock = threading.Lock(); self.cache = {}; self.cache_path = cache_path
        self.stats = dict(calls=0, cached=0, prompt_tokens=0, completion_tokens=0, latency=0.0)
        if cache_path and os.path.exists(cache_path):
            for l in open(cache_path):
                try: r = json.loads(l); self.cache[r["k"]] = r
                except Exception: pass

    def _http(self, system, user):
        body = json.dumps(dict(model=self.model, temperature=self.temp, max_tokens=self.max_tokens,
                               messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])).encode()
        last = None
        for t in range(self.retries):
            try:
                req = urllib.request.Request(self.url, body, {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    j = json.loads(r.read())
                u = j.get("usage", {})
                return j["choices"][0]["message"]["content"], u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
            except Exception as e:
                last = e; time.sleep(min(30, 2 ** t))
        raise RuntimeError(f"LLM call failed after {self.retries} retries: {last}")

    def chat(self, system, user, force_text=None):
        key = hashlib.md5(f"{self.model}|{self.seed}|{self.temp}|{system}|{user}".encode()).hexdigest()
        with self.lock:
            rec = self.cache.get(key)
        cached = rec is not None
        if rec is None:
            t0 = time.time()
            if self.mock: text, pt, ct = (force_text if force_text is not None else mock_reply(system, user)), 100, 40
            else: text, pt, ct = self._http(system, user)
            rec = dict(k=key, text=text, pt=pt, ct=ct, lat=round(time.time() - t0, 3))
            with self.lock:
                self.cache[key] = rec
                if self.cache_path:
                    with open(self.cache_path, "a") as f: f.write(json.dumps(rec) + "\n")
        with self.lock:
            s = self.stats; s["calls"] += 1; s["cached"] += int(cached)
            s["prompt_tokens"] += rec["pt"]; s["completion_tokens"] += rec["ct"]; s["latency"] += rec["lat"]
        return dict(text=rec["text"], prompt_tokens=rec["pt"], completion_tokens=rec["ct"], latency=rec["lat"], cached=cached)


def extract_json(text):
    """Parse the first JSON object in a model reply. Some open models drop the closing ']' of the claims list
    (e.g. ...]},{"id":"c4",...},"answer":"X"}); we repair that, and as a last resort recover the "answer" field."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m: raise ValueError("no json found")
    t = m.group(0)
    try: return json.loads(t)
    except json.JSONDecodeError: pass
    # repair 1: unclosed claims array right before the answer key
    t2 = re.sub(r'\}\s*,\s*"answer"', '}],"answer"', t, count=1)
    try: return json.loads(t2)
    except json.JSONDecodeError: pass
    # repair 2: salvage the scalar answer field only
    a = re.search(r'"answer"\s*:\s*("(?:[^"\\]|\\.)*"|-?[0-9][0-9.,]*|true|false|null)', t)
    if a:
        try: return {"answer": json.loads(a.group(1)), "claims": [], "_repaired": True}
        except json.JSONDecodeError: pass
    raise ValueError("unparseable json")


# ---------------- offline mock (plumbing tests only) ----------------
def mock_reply(system, user):
    s = system + "\n" + user
    role = re.search(r"\[\[ROLE:(\w+)\]\]", s)
    role = role.group(1) if role else "unknown"
    rng = random.Random(int(hashlib.md5(s.encode()).hexdigest()[:8], 16))
    if role == "solve":
        tid = re.search(r"Task-ID:(\S+)", user).group(1); t = MOCK_TRUTH[tid]
        ans = t["answer"] if rng.random() < 0.9 else t["wrong"]
        return json.dumps(dict(claims=[dict(id="c1", parent=None, text="gathered evidence", evidence=["e0"]),
                                       dict(id="c2", parent="c1", text="interpreted evidence", evidence=["e0"]),
                                       dict(id="c3", parent="c2", text="reasoned", evidence=["e0"]),
                                       dict(id="c4", parent="c3", text=f"answer {ans}", evidence=["e0"])], answer=ans))
    if role == "induce":
        tgt = re.search(r"TARGET-ANSWER:(.+)", user).group(1).strip()
        return json.dumps(dict(claims=[dict(id="c1", parent=None, text="Retrieved the available evidence items.", evidence=["e0"]),
                                       dict(id="c2", parent="c1", text="Interpreted what the evidence says.", evidence=["e0"]),
                                       dict(id="c3", parent="c2", text="Combined the facts step by step.", evidence=["e0"]),
                                       dict(id="c4", parent="c3", text=f"Therefore the answer is {tgt}.", evidence=["e0"])], answer=tgt))
    if role == "provenance":
        agent = re.search(r"Agent:(\S+)", user).group(1)
        items = re.findall(r"\b(e\d+)\b", user.split("TRANSCRIPT")[-1]); items = sorted(set(items))
        body = user.split("TRANSCRIPT")[-1]
        st = "failed" if "ERROR" in body else ("empty" if "(no rows)" in body else ("stale" if "outdated" in body else "ok"))
        tool = f"retrieve:{st}"
        edges = [dict(id=f"c{i}", parent=(None if i == 1 else f"c{i-1}")) for i in range(1, 5)]
        if rng.random() < 0.1: edges[2]["parent"] = "c1"
        return json.dumps(dict(origin_agent=agent, source_evidence=items, tool_dependency=tool, claims=edges))
    return "{}"
