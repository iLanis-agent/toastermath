/* Toaster math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function article(n) { return /^(8|11|18)/.test(String(n)) ? "an" : "a"; }

  function queuePlan(slices, slots, cycleSec) {
    if (!(slices > 0) || !(slots > 0) || !(cycleSec > 0)) return { error: "slices, slots and cycle time must be positive" };
    var batches = Math.ceil(slices / slots);
    var totalMin = r1(batches * cycleSec / 60);
    return { slices: slices, slots: slots, cycleSec: cycleSec, batches: batches, totalMin: totalMin };
  }

  function energyPlan(watts, minutesDay, tariff) {
    if (!(watts > 0) || !(minutesDay > 0) || !(tariff > 0)) return { error: "watts, minutes and tariff must be positive" };
    var kwhYear = r2(watts * minutesDay / 60 / 1000 * 365);
    var costYear = r2(kwhYear * tariff);
    return { watts: watts, minutesDay: minutesDay, tariff: tariff, kwhYear: kwhYear, costYear: costYear };
  }

  function shadePlan(shade) {
    if (!(shade > 0)) return { error: "shade must be positive" };
    if (shade > 6) return { error: "shade must be between 1 and the labeled 6 steps" };
    var seconds = 60 + 30 * shade;
    return { shade: shade, seconds: seconds, minutes: r1(seconds / 60) };
  }

  function renderQueue(r) {
    return r.slices + " slice" + (r.slices === 1 ? "" : "s") + " through " + article(r.slots) + " " + r.slots + "-slot toaster at a labeled " + r.cycleSec + " seconds a cycle is " + r.batches + " batch" + (r.batches === 1 ? "" : "es") + " - about " + r.totalMin + " minutes at the counter.";
  }

  function renderEnergy(r) {
    return article(r.watts) + " " + r.watts + " W toaster running " + r.minutesDay + " minutes a day uses about " + r.kwhYear + " kWh a year - about " + r.costYear + " at your labeled " + r.tariff + " per kWh tariff.";
  }

  function renderShade(r) {
    return "Shade " + r.shade + " on a labeled 6-step dial is about " + r.seconds + " seconds - a labeled 60 seconds plus 30 a step. Your toaster's own dial decides.";
  }

  var api = { queuePlan: queuePlan, energyPlan: energyPlan, shadePlan: shadePlan,
              renderQueue: renderQueue, renderEnergy: renderEnergy, renderShade: renderShade };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ToasterMath = api;
})(typeof window !== "undefined" ? window : this);
