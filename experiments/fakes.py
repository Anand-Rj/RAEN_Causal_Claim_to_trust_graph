"""Synthetic stand-ins for HotpotQA/FEVER, used ONLY by selftest.py (offline plumbing test)."""
import random


def fake_multi(source, skill, n, offset=0, seed=0):
    rng = random.Random(seed + offset); out = []
    for i in range(n):
        a, b = rng.sample(["Ann", "Bo", "Cy", "Di", "Ed", "Flo"], 2)
        out.append(dict(source=source, skill=skill, question=f"Who is older, {a} or {b}?",
                        facts=[f"{a} is {rng.randint(20, 40)}.", f"{b} is {rng.randint(41, 60)}."], answer=b, wrong=a, base_idx=offset + i))
    return out


def install():
    import ctb
    ctb.load_hotpot = lambda n, seed=0, offset=0: fake_multi("hotpotqa", "multihop", n, offset, seed)
    ctb.load_fever = lambda n, seed=0, offset=0: fake_multi("fever", "fact", n, offset, seed)
