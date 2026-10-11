const E = require('./engine.js');
const cases = require('./expected.json');
let pass = 0, fail = 0;
function chk(name, cond) { if (cond) pass++; else { fail++; console.log('FAIL', name); } }
cases.forEach((c, i) => {
  let actual, render;
  if (c.fn === 'queuePlan') { actual = E.queuePlan(...c.args); render = actual.error || E.renderQueue(actual); }
  else if (c.fn === 'energyPlan') { actual = E.energyPlan(...c.args); render = actual.error || E.renderEnergy(actual); }
  else { actual = E.shadePlan(...c.args); render = actual.error || E.renderShade(actual); }
  chk(i + ':' + c.fn + ':result', JSON.stringify(actual) === JSON.stringify(c.result));
  chk(i + ':' + c.fn + ':render', render === c.render);
  chk(i + ':' + c.fn + ':errorflag', (!!actual.error) === c.isError);
});
console.log(cases.length + ' cases, ' + pass + ' checks green, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
