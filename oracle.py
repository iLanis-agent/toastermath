#!/usr/bin/env python3
"""Oracle mirror of engine.js for Toaster math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def article(n):
    s = str(int(n)) if isinstance(n, float) and n == int(n) else str(n)
    return "an" if s.startswith(("8", "11", "18")) else "a"

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def queuePlan(slices, slots, cycleSec):
    if not (slices > 0) or not (slots > 0) or not (cycleSec > 0):
        return {"error": "slices, slots and cycle time must be positive"}
    batches = math.ceil(slices / slots)
    totalMin = r1(batches * cycleSec / 60)
    return {"slices": jsnum(float(slices)), "slots": jsnum(float(slots)), "cycleSec": jsnum(float(cycleSec)),
            "batches": batches, "totalMin": jsnum(totalMin)}

def energyPlan(watts, minutesDay, tariff):
    if not (watts > 0) or not (minutesDay > 0) or not (tariff > 0):
        return {"error": "watts, minutes and tariff must be positive"}
    kwhYear = r2(watts * minutesDay / 60 / 1000 * 365)
    costYear = r2(kwhYear * tariff)
    return {"watts": jsnum(float(watts)), "minutesDay": jsnum(float(minutesDay)), "tariff": jsnum(float(tariff)),
            "kwhYear": jsnum(kwhYear), "costYear": jsnum(costYear)}

def shadePlan(shade):
    if not (shade > 0):
        return {"error": "shade must be positive"}
    if shade > 6:
        return {"error": "shade must be between 1 and the labeled 6 steps"}
    seconds = 60 + 30 * shade
    return {"shade": jsnum(float(shade)), "seconds": jsnum(seconds), "minutes": jsnum(r1(seconds / 60))}

def renderQueue(r):
    return (fmt(r["slices"]) + " slice" + ("" if r["slices"] == 1 else "s") + " through " + article(r["slots"]) + " " + fmt(r["slots"]) +
            "-slot toaster at a labeled " + fmt(r["cycleSec"]) + " seconds a cycle is " + str(r["batches"]) + " batch" +
            ("" if r["batches"] == 1 else "es") + " - about " + fmt(r["totalMin"]) + " minutes at the counter.")

def renderEnergy(r):
    return (article(r["watts"]) + " " + fmt(r["watts"]) + " W toaster running " + fmt(r["minutesDay"]) + " minutes a day uses about " + fmt(r["kwhYear"]) +
            " kWh a year - about " + fmt(r["costYear"]) + " at your labeled " + fmt(r["tariff"]) + " per kWh tariff.")

def renderShade(r):
    return ("Shade " + fmt(r["shade"]) + " on a labeled 6-step dial is about " + str(r["seconds"]) +
            " seconds - a labeled 60 seconds plus 30 a step. Your toaster's own dial decides.")

CASES = []
CASES.append({"fn": "queuePlan", "args": [9, 2, 150]})
CASES.append({"fn": "queuePlan", "args": [4, 4, 120]})
CASES.append({"fn": "queuePlan", "args": [1, 2, 150]})
CASES.append({"fn": "queuePlan", "args": [12, 2, 180]})
CASES.append({"fn": "queuePlan", "args": [7, 4, 90]})
CASES.append({"fn": "queuePlan", "args": [2, 2, 200]})
CASES.append({"fn": "queuePlan", "args": [0, 2, 150]})
CASES.append({"fn": "queuePlan", "args": [9, 0, 150]})
CASES.append({"fn": "queuePlan", "args": [9, 2, 0]})
CASES.append({"fn": "queuePlan", "args": [18, 4, 140]})
CASES.append({"fn": "queuePlan", "args": [3, 1, 160]})
CASES.append({"fn": "queuePlan", "args": [11, 2, 130]})
CASES.append({"fn": "energyPlan", "args": [850, 7.5, 0.15]})
CASES.append({"fn": "energyPlan", "args": [1200, 10, 0.25]})
CASES.append({"fn": "energyPlan", "args": [700, 5, 0.4]})
CASES.append({"fn": "energyPlan", "args": [1000, 12, 0.12]})
CASES.append({"fn": "energyPlan", "args": [800, 3, 0.55]})
CASES.append({"fn": "energyPlan", "args": [1800, 8, 0.22]})
CASES.append({"fn": "energyPlan", "args": [0, 7.5, 0.15]})
CASES.append({"fn": "energyPlan", "args": [850, 0, 0.15]})
CASES.append({"fn": "energyPlan", "args": [850, 7.5, 0]})
CASES.append({"fn": "energyPlan", "args": [1100, 6.5, 0.3]})
CASES.append({"fn": "energyPlan", "args": [900, 15, 0.18]})
CASES.append({"fn": "energyPlan", "args": [750, 4, 0.65]})
CASES.append({"fn": "shadePlan", "args": [4]})
CASES.append({"fn": "shadePlan", "args": [1]})
CASES.append({"fn": "shadePlan", "args": [6]})
CASES.append({"fn": "shadePlan", "args": [3]})
CASES.append({"fn": "shadePlan", "args": [2]})
CASES.append({"fn": "shadePlan", "args": [5]})
CASES.append({"fn": "shadePlan", "args": [0]})
CASES.append({"fn": "shadePlan", "args": [7]})
CASES.append({"fn": "shadePlan", "args": [8]})
CASES.append({"fn": "shadePlan", "args": [2.5]})
CASES.append({"fn": "shadePlan", "args": [4.5]})
CASES.append({"fn": "shadePlan", "args": [11]})

out = []
for c in CASES:
    fn = {"queuePlan": queuePlan, "energyPlan": energyPlan, "shadePlan": shadePlan}[c["fn"]]
    r = fn(*c["args"])
    is_err = "error" in r
    if is_err:
        render = r["error"]
    else:
        render = {"queuePlan": renderQueue, "energyPlan": renderEnergy, "shadePlan": renderShade}[c["fn"]](r)
    out.append({"fn": c["fn"], "args": c["args"], "result": r, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
    f.write("\n")
print("wrote", len(out), "cases")
