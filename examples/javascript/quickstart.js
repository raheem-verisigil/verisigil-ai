/**
 * VeriSigil AI — JavaScript Quick Start
 * Run: node examples/javascript/quickstart.js
 */

'use strict';

const { VeriSigil } = require('../../js/src/index');

async function main() {
  console.log('='.repeat(55));
  console.log('  VeriSigil AI — JavaScript Demo');
  console.log('='.repeat(55));

  const vs = new VeriSigil({ apiKey: 'demo' });

  console.log('\n🔐 Issuing passport...');
  const passport = await vs.issuePassport({
    agentName: 'openai-coding-agent',
    owner:     'engineering@example.com',
    framework: 'openai',
  });
  console.log('   ✅ Issued!');
  console.log(`   DID:         ${passport.did}`);
  console.log(`   Trust Score: ${passport.trustScore}`);
  console.log(`   EU Risk:     ${passport.euRiskClass}`);
  console.log(`   Expires:     ${passport.expiresAt}`);

  console.log('\n🛡️  Verifying...');
  const ok = await vs.verify(passport.agentId);
  console.log(`   ${ok ? '✅ Verified' : '⛔ NOT verified'}`);

  console.log('\n🔍 Security scan...');
  const scan = await vs.scan(`
    const apiKey = "sk-1234";
    const result = eval(userInput);
  `);
  console.log(`   Threats: ${scan.threatCount}`);
  scan.threats.forEach(t => {
    const icon = t.severity === 'HIGH' ? '🔴' : '🟡';
    console.log(`   ${icon} [${t.severity}] Line ${t.line}: ${t.description}`);
  });

  console.log('\n⚖️  Compliance...');
  const c = await vs.checkCompliance(passport.agentId);
  console.log(`   EU AI Act: ${c.eu_ai_act.compliant ? '✅' : '❌'} (${c.eu_ai_act.risk_class})`);
  console.log(`   GDPR:      ${c.gdpr.compliant ? '✅' : '❌'}`);

  console.log('\n' + '='.repeat(55));
  console.log('  🚀 verisigilai.com  |  info@verisigilai.com');
  console.log('='.repeat(55));
}

main().catch(console.error);
