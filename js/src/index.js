/**
 * VeriSigil AI — JavaScript SDK
 * ================================
 * npm install @verisigil/sdk
 *
 * @example
 * const { VeriSigil } = require('@verisigil/sdk');
 * const vs = new VeriSigil({ apiKey: 'demo' });
 * const passport = await vs.issuePassport({
 *   agentName: 'my-agent',
 *   owner: 'dev@mycompany.com',
 * });
 * console.log(passport.did);
 */

'use strict';

const crypto = require('crypto');

const DEFAULT_BASE_URL    = 'https://api.verisigilai.com/v1';
const DEMO_BASE_URL       = 'https://api-demo.verisigilai.com/v1';
const DEFAULT_EXPIRY_DAYS = 365;
const SDK_VERSION         = '0.1.0';

const PassportStatus = Object.freeze({
  ISSUED: 'ISSUED', ACTIVE: 'ACTIVE',
  SUSPENDED: 'SUSPENDED', REVOKED: 'REVOKED', EXPIRED: 'EXPIRED',
});

const EURiskClass = Object.freeze({
  UNACCEPTABLE: 'UNACCEPTABLE_RISK', HIGH: 'HIGH_RISK',
  LIMITED: 'LIMITED_RISK', MINIMAL: 'MINIMAL_RISK',
});

class VeriSigil {
  constructor({ apiKey = 'demo', baseUrl, timeout = 30000 } = {}) {
    this.apiKey  = apiKey || process.env.VERISIGIL_API_KEY || 'demo';
    this.baseUrl = baseUrl || (this.apiKey === 'demo' ? DEMO_BASE_URL : DEFAULT_BASE_URL);
    this.timeout = timeout;
  }

  async issuePassport({ agentName, owner, framework = 'unknown', runtime = 'node', version = '1.0.0', tags = [], expiryDays = DEFAULT_EXPIRY_DAYS } = {}) {
    if (!agentName) throw new Error('agentName is required');
    if (!owner)     throw new Error('owner is required');
    if (this.apiKey === 'demo') return this._demoPassport({ agentName, owner, framework, runtime, version, tags, expiryDays });
    return this._post('/passport/issue', { agent_name: agentName, owner, framework, runtime, version, tags, expiry_days: expiryDays });
  }

  async verify(agentId) {
    if (this.apiKey === 'demo') return true;
    try { const data = await this._get(`/passport/verify/${agentId}`); return data.verified === true; }
    catch { return false; }
  }

  async getPassport(agentId) {
    if (this.apiKey === 'demo') return this._demoPassport({ agentName: `agent-${agentId.slice(0, 8)}`, owner: 'demo@verisigilai.com' });
    return this._get(`/passport/${agentId}`);
  }

  async revoke(agentId, reason = 'manual_revocation') {
    if (this.apiKey === 'demo') { console.log(`[DEMO] Revoked ${agentId}`); return true; }
    const data = await this._post('/passport/revoke', { agent_id: agentId, reason });
    return data.revoked === true;
  }

  async scan(code, agentId = null) {
    if (this.apiKey === 'demo') return this._demoScan(code);
    return this._post('/security/scan', { code, agent_id: agentId });
  }

  async checkCompliance(agentId, regulations = ['eu_ai_act', 'gdpr', 'hipaa', 'soc2']) {
    if (this.apiKey === 'demo') return {
      eu_ai_act: { compliant: true,  risk_class: 'LIMITED_RISK' },
      gdpr:      { compliant: true,  lawful_basis: 'legitimate_interest' },
      hipaa:     { compliant: false, reason: 'BAA required' },
      soc2:      { compliant: false, reason: 'Audit pending' },
    };
    return this._post('/compliance/check', { agent_id: agentId, regulations });
  }

  _demoPassport({ agentName, owner, framework = 'unknown', runtime = 'node', version = '1.0.0', tags = [], expiryDays = 365, agentId }) {
    const id   = agentId || `vsa_${crypto.randomBytes(6).toString('hex')}`;
    const slug = agentName.toLowerCase().replace(/\s+/g, '-');
    const did  = `did:web:verisigilai.com:agents:${slug}-${id.slice(-6)}`;
    const sig  = `DIDSig:${crypto.createHmac('sha256', 'demo').update(id).digest('hex').slice(0, 32)}...${id.slice(-4)}`;
    const now  = new Date();
    const exp  = new Date(now.getTime() + expiryDays * 86400000);
    return {
      agentId: id, agentName, did, owner,
      status: PassportStatus.ACTIVE, trustScore: 0.97,
      euRiskClass: EURiskClass.LIMITED, compliant: true,
      signature: sig, issuedAt: now.toISOString(), expiresAt: exp.toISOString(),
      threatsDetected: 0, lastScanAt: now.toISOString(),
      metadata: { framework, runtime, version, tags },
      compliance: { euAiAct: true, gdpr: true, hipaa: false, soc2: false },
      isTrusted() { return this.status === PassportStatus.ACTIVE && this.trustScore >= 0.8 && this.compliant; },
      isExpired()  { return new Date() > new Date(this.expiresAt); },
    };
  }

  _demoScan(code) {
    const lines = code.split('\n');
    const threats = [];
    const patterns = [
      { re: /eval\s*\(/i,            sev: 'HIGH',   msg: 'Unsafe eval() — arbitrary code execution risk' },
      { re: /exec\s*\(/i,            sev: 'HIGH',   msg: 'Unsafe exec() — arbitrary code execution risk' },
      { re: /child_process/i,        sev: 'MEDIUM', msg: 'Child process usage — verify inputs are sanitised' },
      { re: /password\s*=\s*['"]/i,  sev: 'HIGH',   msg: 'Possible hardcoded password — use environment variables' },
      { re: /api_?key\s*=\s*['"]/i,  sev: 'HIGH',   msg: 'Possible hardcoded API key — use environment variables' },
      { re: /secret\s*=\s*['"]/i,    sev: 'HIGH',   msg: 'Possible hardcoded secret — use a vault or env vars' },
    ];
    lines.forEach((line, i) => {
      patterns.forEach(({ re, sev, msg }) => {
        if (re.test(line)) threats.push({ line: i + 1, severity: sev, description: msg, code: line.trim() });
      });
    });
    return {
      scanId: `scan_${crypto.randomBytes(6).toString('hex')}`,
      linesScanned: lines.length, threats, threatCount: threats.length,
      passed: threats.length === 0, scannedAt: new Date().toISOString(), demo: true,
      note: 'Demo scan. Production scanning engine in development — Q2 2026.',
    };
  }

  async _get(path) {
    const res = await fetch(`${this.baseUrl}${path}`, { headers: this._headers(), signal: AbortSignal.timeout(this.timeout) });
    return this._handle(res);
  }

  async _post(path, body) {
    const res = await fetch(`${this.baseUrl}${path}`, { method: 'POST', headers: this._headers(), body: JSON.stringify(body), signal: AbortSignal.timeout(this.timeout) });
    return this._handle(res);
  }

  async _handle(res) {
    if (res.ok) return res.json();
    const text = await res.text();
    if (res.status === 401) throw new Error('AuthenticationError: Invalid API key.');
    if (res.status === 404) throw new Error('PassportNotFoundError: Passport not found.');
    if (res.status === 429) throw new Error('RateLimitError: Rate limit exceeded.');
    throw new Error(`VeriSigilError ${res.status}: ${text}`);
  }

  _headers() {
    return { 'Authorization': `Bearer ${this.apiKey}`, 'Content-Type': 'application/json', 'User-Agent': `verisigil-js/${SDK_VERSION}` };
  }

  toString() { return `VeriSigil { mode: '${this.apiKey === 'demo' ? 'demo' : 'production'}' }`; }
}

module.exports = { VeriSigil, PassportStatus, EURiskClass };
