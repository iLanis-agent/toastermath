# Toaster math

What nine slices through two slots really costs in minutes, what the toaster costs the grid in a year, and what the mystery dial means in seconds. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/toastermath/

## The three tools

- **Queue plan** - `queuePlan(slices, slots, cycleSec)`: the pile becomes batches and minutes at the counter.
- **Energy plan** - `energyPlan(watts, minutesDay, tariff)`: daily minutes become kWh and cost per year.
- **Shade plan** - `shadePlan(shade)`: the dial step becomes labeled seconds (a labeled 60 plus 30 a step).

## Labeled norms (illustrative references, not rules)

- Cycle: about 150 seconds for a medium toast. Slots: 2.
- Dial: 6 steps at a labeled 60 seconds plus 30 a step - your toaster's own dial decides.
- Tariff: 0.15 per kWh reference; put in your own.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (36 cases, 108 checks)

Regenerate the oracle expectations: `python3 oracle.py`
