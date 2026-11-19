"""Empirical Phase E: execute the future probes with REAL measured subagent correctness (probe_answers.json from calibrate.py)
plus the controlled profile corruption; verification catches wrong answers w.p. q and falls back to the specialist."""
import json
import ctb, agents


class ProbeExec:
    def __init__(self, path, d=ctb.DESIGN):
        self.pa = json.load(open(path)); self.d = d
        self.by_id = {ag: {k: {x["id"]: x["base_ok"] for x in v} for k, v in kk.items()} for ag, kk in self.pa.items()}

    def run(self, ep, dT):
        d = self.d; tot_u = tot_or = succ = 0.0
        for idx, (j, role) in enumerate(ep.probes):
            tasks = list(self.by_id[ep.agent][j].keys())
            if not tasks: return {}
            tid = tasks[ctb.hseed("probe", ep.id, idx) % len(tasks)]
            weak = ep.skill if ep.cause == "persistent_reasoning" else None
            ok_s = self.by_id[ep.agent][j][tid] and not agents.draw_corrupt(ep.agent, tid, j, weak, "probe")
            spec = ctb.AGENT_OF[j]; ok_b = self.by_id[spec][j].get(tid, False) and not agents.draw_corrupt(spec, tid, j, None, "probe")
            belief = ctb.clip(ep.r_pre[j] + ctb.clip(dT[j], -1, .5), 0, 1)
            def outcome(a):
                if a == "delegate": return float(ok_s), 0.0
                if a == "verify":
                    q = (ctb.hseed("ver", ep.id, idx) % 1000) / 1000 < d["q_verify"]
                    return float(ok_s or (q and ok_b)), d["c_verify"]
                return float(ok_b), d["c_reroute"]
            s1, c1 = outcome(ctb.best_action(belief, d)); s0, c0 = outcome(ctb.best_action(ep.r_post[j], d))
            tot_u += s1 - c1; tot_or += s0 - c0; succ += s1
        n = len(ep.probes)
        return dict(emp_success=succ / n, emp_utility=tot_u / n, emp_regret=(tot_or - tot_u) / n)
