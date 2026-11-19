DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Anomaly Guard — Transaction Risk Console</title>
  <style>
    :root {
      --bg: #f4f5f7;
      --surface: #ffffff;
      --border: #d8dce3;
      --border-soft: #eaedf2;
      --text: #111827;
      --muted: #5b6472;
      --accent: #111827;
      --ok-bg: #eef7f1;
      --ok-text: #14532d;
      --ok-border: #bbf7d0;
      --bad-bg: #fef2f2;
      --bad-text: #991b1b;
      --bad-border: #fecaca;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      font-size: 14px;
      line-height: 1.45;
    }

    .topbar {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .brand {
      display: flex;
      align-items: baseline;
      gap: 10px;
    }
    .brand h1 {
      margin: 0;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    .brand span {
      font-size: 12px;
      color: var(--muted);
    }
    .top-meta {
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 12px;
      color: var(--muted);
    }
    .top-meta a {
      color: var(--text);
      text-decoration: none;
      border-bottom: 1px solid var(--border);
      font-weight: 500;
    }
    .top-meta a:hover { border-color: var(--text); }
    .status-inline {
      font-family: var(--mono);
      font-size: 12px;
      color: var(--text);
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px 24px 40px;
    }

    /* Flat stat strip */
    .stat-strip {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      margin-bottom: 20px;
    }
    .stat-cell {
      padding: 14px 18px;
      border-right: 1px solid var(--border-soft);
    }
    .stat-cell:last-child { border-right: none; }
    .stat-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted);
      margin-bottom: 4px;
    }
    .stat-val {
      font-family: var(--mono);
      font-size: 22px;
      font-weight: 600;
      color: var(--text);
    }
    .stat-val.danger { color: var(--bad-text); }
    .stat-sub {
      font-size: 11px;
      color: var(--muted);
      margin-top: 2px;
    }

    .grid {
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }
    @media (max-width: 900px) {
      .stat-strip { grid-template-columns: repeat(2, 1fr); }
      .grid { grid-template-columns: 1fr; }
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
    }
    .panel-head {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-soft);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .panel-head h2 {
      margin: 0;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .panel-body { padding: 16px; }

    .preset-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border-soft);
    }
    .btn {
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 500;
      padding: 6px 10px;
      border-radius: 3px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      cursor: pointer;
    }
    .btn:hover { background: #f9fafb; border-color: #9ca3af; }
    .btn:disabled { opacity: 0.55; cursor: not-allowed; }
    .btn-primary {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      padding: 8px 14px;
      font-weight: 600;
    }
    .btn-primary:hover { background: #1f2937; }
    .btn-active {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }
    @media (max-width: 600px) {
      .form-grid { grid-template-columns: 1fr; }
    }
    .field label {
      display: block;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      margin-bottom: 4px;
    }
    .field input, .field select {
      width: 100%;
      padding: 7px 9px;
      font-size: 13px;
      font-family: var(--mono);
      border: 1px solid var(--border);
      border-radius: 3px;
      background: #fff;
      color: var(--text);
    }
    .field select { font-family: var(--sans); }
    .field input:focus, .field select:focus {
      outline: none;
      border-color: var(--text);
    }

    .form-actions {
      margin-top: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .verdict-box {
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 14px;
      background: #fafafa;
      margin-bottom: 14px;
    }
    .verdict-box.ok {
      background: var(--ok-bg);
      border-color: var(--ok-border);
      color: var(--ok-text);
    }
    .verdict-box.bad {
      background: var(--bad-bg);
      border-color: var(--bad-border);
      color: var(--bad-text);
    }
    .verdict-title {
      font-size: 15px;
      font-weight: 700;
      margin: 0 0 2px;
      font-family: var(--mono);
    }
    .verdict-sub { font-size: 12px; margin: 0; }

    .kv-list {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 14px;
      font-size: 12px;
    }
    .kv-list td {
      padding: 6px 0;
      border-bottom: 1px solid var(--border-soft);
    }
    .kv-list td:first-child { color: var(--muted); }
    .kv-list td:last-child {
      text-align: right;
      font-family: var(--mono);
      font-weight: 600;
    }

    .signal-box {
      border-top: 1px solid var(--border-soft);
      padding-top: 10px;
      font-size: 12px;
    }
    .signal-box ul {
      margin: 6px 0 0;
      padding-left: 18px;
      color: var(--muted);
    }

    .threshold-bar {
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--border-soft);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 12px;
    }
    .threshold-bar input[type="range"] { flex: 1; }

    .err-banner {
      display: none;
      margin-bottom: 12px;
      padding: 8px 12px;
      font-size: 12px;
      font-family: var(--mono);
      background: var(--bad-bg);
      color: var(--bad-text);
      border: 1px solid var(--bad-border);
      border-radius: 3px;
    }

    .table-wrap { overflow-x: auto; }
    table.ledger {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    table.ledger th {
      text-align: left;
      padding: 9px 12px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--muted);
      background: #fafafa;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    table.ledger td {
      padding: 8px 12px;
      border-bottom: 1px solid var(--border-soft);
      white-space: nowrap;
    }
    table.ledger tr:hover td { background: #f9fafb; }
    .num { text-align: right; font-family: var(--mono); }
    .mono { font-family: var(--mono); }

    .tag {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 2px;
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 600;
    }
    .tag-ok { background: var(--ok-bg); color: var(--ok-text); border: 1px solid var(--ok-border); }
    .tag-bad { background: var(--bad-bg); color: var(--bad-text); border: 1px solid var(--bad-border); }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <h1>Anomaly Guard</h1>
      <span>Mobile Money Risk &amp; Velocity Scoring Console (PaySim-KES Prototype)</span>
    </div>
    <div class="top-meta">
      <span id="healthText" class="status-inline">status: checking...</span>
      <span>DPA 2019: synthetic telemetry only</span>
      <a href="/docs" target="_blank">OpenAPI /docs</a>
    </div>
  </header>

  <main class="container">
    <section class="stat-strip">
      <div class="stat-cell">
        <div class="stat-label">Transactions Scored</div>
        <div id="kpiTotal" class="stat-val">0</div>
        <div class="stat-sub">SQLite audit records</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Flagged Fraud</div>
        <div id="kpiFlagged" class="stat-val danger">0</div>
        <div id="kpiRate" class="stat-sub">0.0% flag rate</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Last Scoring Latency</div>
        <div id="kpiLatency" class="stat-val">--</div>
        <div class="stat-sub">Target &le; 1,500 ms</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Decision Threshold</div>
        <div id="kpiThreshold" class="stat-val">0.50</div>
        <div id="kpiModel" class="stat-sub">Checking model...</div>
      </div>
    </section>

    <div id="errBanner" class="err-banner"></div>

    <section class="grid">
      <!-- Left: Simulator & Input -->
      <div class="panel">
        <div class="panel-head">
          <h2>Transaction Input &amp; Test Cases</h2>
          <span style="font-size:11px;color:var(--muted);">POST /score</span>
        </div>
        <div class="panel-body">
          <div class="preset-bar">
            <button type="button" class="btn" onclick="runPreset('normal')">Normal Till (KES 250.50)</button>
            <button type="button" class="btn" onclick="runPreset('sim_swap')">SIM-Swap 02:30 Drain (KES 185k)</button>
            <button type="button" class="btn" onclick="runPreset('high_value')">Mule Transfer (KES 540k)</button>
            <button type="button" class="btn" onclick="runPreset('smurfing')">Smurfing Burst (6&times; KES 900)</button>
            <button type="button" class="btn" id="streamBtn" onclick="runMixedStream()">Mixed Stream (8 Tx)</button>
          </div>

          <form id="txForm">
            <div class="form-grid">
              <div class="field">
                <label for="txType">Channel / Type</label>
                <select id="txType">
                  <option value="PAYMENT">Lipa na M-Pesa / Till (PAYMENT)</option>
                  <option value="TRANSFER">Send Money P2P (TRANSFER)</option>
                  <option value="CASH_OUT">Agent Withdrawal (CASH_OUT)</option>
                </select>
              </div>
              <div class="field">
                <label for="amountKes">Amount (KES)</label>
                <input id="amountKes" type="number" step="0.01" min="0" value="1200.00" required />
              </div>
              <div class="field">
                <label for="originAccount">Origin Account ID</label>
                <input id="originAccount" type="text" value="KE_ACC_254712345678" required />
              </div>
              <div class="field">
                <label for="vendorHash">Recipient / Till / Agent ID</label>
                <input id="vendorHash" type="text" value="TILL_NAIVAS_4021" required />
              </div>
              <div class="field">
                <label for="oldBalanceOrg">Sender Old Balance (KES)</label>
                <input id="oldBalanceOrg" type="number" step="0.01" min="0" value="15000.00" required />
              </div>
              <div class="field">
                <label for="newBalanceOrig">Sender New Balance (KES)</label>
                <input id="newBalanceOrig" type="number" step="0.01" min="0" value="13800.00" required />
              </div>
              <div class="field">
                <label for="newBalanceDest">Receiver New Balance (KES)</label>
                <input id="newBalanceDest" type="number" step="0.01" min="0" value="48200.00" required />
              </div>
              <div class="field">
                <label for="txTimestamp">Timestamp (Local)</label>
                <input id="txTimestamp" type="datetime-local" />
              </div>
            </div>

            <div class="form-actions">
              <span style="font-size:11px;color:var(--muted);">Scores transaction and writes to SQLite audit store.</span>
              <button type="submit" id="submitBtn" class="btn btn-primary">Score Transaction</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Right: Verdict & SOC Controls -->
      <div class="panel">
        <div class="panel-head">
          <h2>Inference Result</h2>
          <span id="verdictTxId" class="mono" style="font-size:11px;color:var(--muted);">--</span>
        </div>
        <div class="panel-body">
          <div id="verdictBox" class="verdict-box">
            <p id="verdictLabel" class="verdict-title">NO TRANSACTION SCORED</p>
            <p id="verdictSub" class="verdict-sub">Run a test case or submit the form to evaluate risk.</p>
          </div>

          <table class="kv-list">
            <tr>
              <td>Risk Score</td>
              <td id="scoreValue">--</td>
            </tr>
            <tr>
              <td>End-to-End Latency</td>
              <td id="lastLatencyDetail">--</td>
            </tr>
            <tr>
              <td>Time Since Previous Tx</td>
              <td id="velTimeSince">--</td>
            </tr>
            <tr>
              <td>Account Tx Count (15 min)</td>
              <td id="velCount15">--</td>
            </tr>
            <tr>
              <td>Account Tx Count (24 hr)</td>
              <td id="velCount24">--</td>
            </tr>
          </table>

          <div class="signal-box">
            <strong>Triggering Signals</strong>
            <ul id="signalList">
              <li>Awaiting payload evaluation.</li>
            </ul>
          </div>

          <div class="threshold-bar">
            <label for="thresholdSlider"><strong>SOC Threshold:</strong> <span id="thresholdReadout" class="mono">0.50</span></label>
            <input id="thresholdSlider" type="range" min="0.10" max="0.90" step="0.05" value="0.50" />
            <button type="button" class="btn" onclick="applyThreshold()">Apply</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Audit Ledger -->
    <section class="panel">
      <div class="panel-head">
        <h2>Inference Audit Log (SQLite)</h2>
        <div style="display:flex;gap:6px;">
          <button type="button" id="filterAllBtn" class="btn btn-active" onclick="setFilter('all')">All</button>
          <button type="button" id="filterFlaggedBtn" class="btn" onclick="setFilter('flagged')">Flagged Only</button>
          <button type="button" class="btn" onclick="refreshAll()">Refresh</button>
        </div>
      </div>
      <div class="table-wrap">
        <table class="ledger">
          <thead>
            <tr>
              <th>Tx ID</th>
              <th>Timestamp</th>
              <th>Origin Account</th>
              <th>Recipient / Vendor</th>
              <th class="num">Amount (KES)</th>
              <th class="num">Risk Score</th>
              <th>Verdict</th>
            </tr>
          </thead>
          <tbody id="txTableBody">
            <tr><td colspan="7" style="text-align:center;color:var(--muted);padding:20px;">Loading records...</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>

  <script>
    let currentFilter = 'all';
    let cachedTransactions = [];

    function showError(msg) {
      const el = document.getElementById('errBanner');
      if (!msg) {
        el.style.display = 'none';
        el.textContent = '';
      } else {
        el.style.display = 'block';
        el.textContent = msg;
      }
    }

    function escapeHtml(str) {
      return String(str ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    function makeTxId(prefix) {
      const rand = Math.random().toString(36).slice(2, 6).toUpperCase();
      return `${prefix}-${Date.now().toString(36).toUpperCase()}-${rand}`;
    }

    function toNaiveIso(date) {
      const pad = (n) => String(n).padStart(2, '0');
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
    }

    function toLocalInputValue(date) {
      return toNaiveIso(date).slice(0, 16);
    }

    function formatKes(val) {
      return Number(val || 0).toLocaleString('en-KE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function setFilter(mode) {
      currentFilter = mode;
      document.getElementById('filterAllBtn').className = mode === 'all' ? 'btn btn-active' : 'btn';
      document.getElementById('filterFlaggedBtn').className = mode === 'flagged' ? 'btn btn-active' : 'btn';
      renderTable();
    }

    async function checkHealth() {
      try {
        const res = await fetch('/health');
        const data = await res.json();
        document.getElementById('healthText').textContent = 'status: online';
        document.getElementById('kpiModel').textContent = data.model_loaded ? 'model.joblib loaded' : 'fallback mode';
        if (data.threshold !== undefined) {
          const t = Number(data.threshold).toFixed(2);
          document.getElementById('kpiThreshold').textContent = t;
          document.getElementById('thresholdSlider').value = t;
          document.getElementById('thresholdReadout').textContent = t;
        }
      } catch (err) {
        document.getElementById('healthText').textContent = 'status: offline';
      }
    }

    async function applyThreshold() {
      showError('');
      const val = parseFloat(document.getElementById('thresholdSlider').value);
      try {
        const res = await fetch('/settings/threshold', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ threshold: val }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        document.getElementById('kpiThreshold').textContent = Number(data.threshold).toFixed(2);
      } catch (err) {
        showError(`Threshold update failed: ${err.message}`);
      }
    }

    document.getElementById('thresholdSlider').addEventListener('input', (e) => {
      document.getElementById('thresholdReadout').textContent = Number(e.target.value).toFixed(2);
    });

    async function refreshStats() {
      const res = await fetch('/stats');
      const data = await res.json();
      document.getElementById('kpiTotal').textContent = data.total_scored ?? 0;
      document.getElementById('kpiFlagged').textContent = data.flagged_fraud ?? 0;
      document.getElementById('kpiRate').textContent = `${((data.flag_rate || 0) * 100).toFixed(1)}% flag rate`;
    }

    async function refreshTransactions() {
      const res = await fetch('/transactions?limit=50');
      const data = await res.json();
      cachedTransactions = data.transactions || [];
      renderTable();
    }

    function renderTable() {
      const tbody = document.getElementById('txTableBody');
      const rows = currentFilter === 'flagged'
        ? cachedTransactions.filter((t) => Number(t.verdict) === 1)
        : cachedTransactions;

      if (!rows.length) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:20px;">No matching transactions.</td></tr>';
        return;
      }

      tbody.innerHTML = rows.map((tx) => {
        const isFraud = Number(tx.verdict) === 1;
        const badge = isFraud
          ? '<span class="tag tag-bad">FLAGGED</span>'
          : '<span class="tag tag-ok">CLEARED</span>';
        const scorePct = ((Number(tx.score) || 0) * 100).toFixed(1) + '%';
        const ts = tx.timestamp ? tx.timestamp.replace('T', ' ').slice(0, 19) : '--';
        return `
          <tr>
            <td class="mono">${escapeHtml(tx.tx_id)}</td>
            <td class="mono" style="color:var(--muted);">${escapeHtml(ts)}</td>
            <td class="mono">${escapeHtml(tx.origin_account_id)}</td>
            <td>${escapeHtml(tx.vendor_hash)}</td>
            <td class="num">${formatKes(tx.amount_kes)}</td>
            <td class="num">${scorePct}</td>
            <td>${badge}</td>
          </tr>
        `;
      }).join('');
    }

    function buildSignals(payload, result) {
      const signals = [];
      const f = result.features || {};
      if (payload.oldbalance_org >= 50000 && payload.newbalance_orig === 0) {
        signals.push('Sender balance drained to KES 0.00 on high-value movement.');
      }
      if (payload.oldbalance_org > 0 && payload.amount_kes > payload.oldbalance_org) {
        signals.push('Transfer amount exceeds pre-transaction account balance.');
      }
      if ((f.tx_count_15min || 0) >= 3) {
        signals.push(`High short-window velocity: ${f.tx_count_15min} prior tx within 15 minutes (structuring/smurfing).`);
      }
      const hour = parseInt(String(payload.timestamp).slice(11, 13), 10);
      if (!isNaN(hour) && hour <= 4) {
        signals.push(`Off-hours / ghost-hour activity (${String(hour).padStart(2, '0')}:xx local time).`);
      }
      if (payload.amount_kes >= 50000) {
        signals.push(`Elevated transfer value: KES ${formatKes(payload.amount_kes)}.`);
      }
      if (!signals.length) {
        signals.push('Amount, balance change, and velocity are consistent with normal account activity.');
      }
      return signals;
    }

    function renderVerdict(payload, result, latencyMs) {
      const isFraud = Number(result.verdict) === 1;
      const scorePct = ((Number(result.score) || 0) * 100).toFixed(2);

      document.getElementById('verdictTxId').textContent = result.tx_id;
      document.getElementById('kpiLatency').textContent = `${latencyMs.toFixed(1)} ms`;
      document.getElementById('lastLatencyDetail').textContent = `${latencyMs.toFixed(1)} ms`;
      document.getElementById('scoreValue').textContent = `${scorePct}%`;

      const box = document.getElementById('verdictBox');
      const label = document.getElementById('verdictLabel');
      const sub = document.getElementById('verdictSub');

      if (isFraud) {
        box.className = 'verdict-box bad';
        label.textContent = 'FLAGGED — SUSPECTED FRAUD';
        sub.textContent = 'Action: Hold settlement & escalate to SOC review.';
      } else {
        box.className = 'verdict-box ok';
        label.textContent = 'CLEARED — LEGITIMATE';
        sub.textContent = 'Action: Allow transaction.';
      }

      const f = result.features || {};
      document.getElementById('velTimeSince').textContent =
        f.time_since_last_tx !== undefined && f.time_since_last_tx !== null
          ? `${Number(f.time_since_last_tx).toFixed(1)} min`
          : '--';
      document.getElementById('velCount15').textContent = f.tx_count_15min ?? 0;
      document.getElementById('velCount24').textContent = f.tx_count_24h ?? 0;

      const signals = buildSignals(payload, result);
      document.getElementById('signalList').innerHTML = signals.map((s) => `<li>${escapeHtml(s)}</li>`).join('');
    }

    async function scorePayload(payload) {
      showError('');
      const start = performance.now();
      const res = await fetch('/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const latencyMs = performance.now() - start;
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text}`);
      }
      const data = await res.json();
      renderVerdict(payload, data, latencyMs);
      return data;
    }

    function fillForm(cfg) {
      document.getElementById('txType').value = cfg.type || 'PAYMENT';
      document.getElementById('amountKes').value = cfg.amount_kes;
      document.getElementById('originAccount').value = cfg.origin_account_id;
      document.getElementById('vendorHash').value = cfg.vendor_hash;
      document.getElementById('oldBalanceOrg').value = cfg.oldbalance_org;
      document.getElementById('newBalanceOrig').value = cfg.newbalance_orig;
      document.getElementById('newBalanceDest').value = cfg.newbalance_dest;
      if (cfg.timestamp) {
        document.getElementById('txTimestamp').value = cfg.timestamp.slice(0, 16);
      }
    }

    async function runPreset(kind) {
      try {
        const now = new Date();
        if (kind === 'normal') {
          const payload = {
            tx_id: makeTxId('TILL'),
            origin_account_id: 'KE_ACC_254712345678',
            vendor_hash: 'TILL_NAIVAS_4021',
            amount_kes: 250.50,
            timestamp: toNaiveIso(now),
            oldbalance_org: 12500.00,
            newbalance_orig: 12249.50,
            newbalance_dest: 45250.50,
          };
          fillForm({ ...payload, type: 'PAYMENT' });
          await scorePayload(payload);
        } else if (kind === 'sim_swap') {
          const ghost = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 2, 30, 0);
          const payload = {
            tx_id: makeTxId('SIMSWP'),
            origin_account_id: 'KE_ACC_254722889911',
            vendor_hash: 'AGENT_CASHOUT_991',
            amount_kes: 185000.00,
            timestamp: toNaiveIso(ghost),
            oldbalance_org: 185000.00,
            newbalance_orig: 0.00,
            newbalance_dest: 0.00,
          };
          fillForm({ ...payload, type: 'CASH_OUT' });
          await scorePayload(payload);
        } else if (kind === 'high_value') {
          const ghost = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 3, 15, 0);
          const payload = {
            tx_id: makeTxId('MULE'),
            origin_account_id: 'KE_ACC_254700445566',
            vendor_hash: 'MULE_WALLET_8842',
            amount_kes: 540000.00,
            timestamp: toNaiveIso(ghost),
            oldbalance_org: 540000.00,
            newbalance_orig: 0.00,
            newbalance_dest: 0.00,
          };
          fillForm({ ...payload, type: 'TRANSFER' });
          await scorePayload(payload);
        } else if (kind === 'smurfing') {
          const acct = `KE_SMURF_${Math.floor(1000 + Math.random() * 9000)}`;
          let bal = 5400.00;
          for (let i = 0; i < 6; i++) {
            const ts = new Date(now.getTime() + i * 15000);
            const nextBal = Math.max(0, bal - 900.00);
            const payload = {
              tx_id: makeTxId(`SMRF${i + 1}`),
              origin_account_id: acct,
              vendor_hash: `PROXY_ACC_00${i + 1}`,
              amount_kes: 900.00,
              timestamp: toNaiveIso(ts),
              oldbalance_org: bal,
              newbalance_orig: nextBal,
              newbalance_dest: 0.00,
            };
            bal = nextBal;
            fillForm({ ...payload, type: 'TRANSFER' });
            await scorePayload(payload);
          }
        }
        await refreshAll();
      } catch (err) {
        showError(`Scoring failed: ${err.message}`);
      }
    }

    async function runMixedStream() {
      const btn = document.getElementById('streamBtn');
      btn.disabled = true;
      btn.textContent = 'Running stream...';
      try {
        const now = new Date();
        const cases = [
          { prefix: 'TILL', acct: 'KE_ACC_254711001122', vendor: 'TILL_CARREFOUR_102', amt: 1450.00, oldB: 24000, newB: 22550, destB: 120450 },
          { prefix: 'KPLC', acct: 'KE_ACC_254722334455', vendor: 'PAYBILL_KPLC_888880', amt: 2000.00, oldB: 18500, newB: 16500, destB: 980000 },
          { prefix: 'P2P',  acct: 'KE_ACC_254733998877', vendor: 'AIRTEL_254733112233', amt: 650.00, oldB: 5400, newB: 4750, destB: 3200 },
          { prefix: 'SIM',  acct: 'KE_ACC_254701999888', vendor: 'AGENT_KAWANGWARE_77', amt: 245000.00, oldB: 245000, newB: 0, destB: 0, hour: 2 },
          { prefix: 'TILL', acct: 'KE_ACC_254798123456', vendor: 'TILL_JAVA_WESTLANDS', amt: 1850.00, oldB: 31000, newB: 29150, destB: 64200 },
          { prefix: 'P2P',  acct: 'KE_ACC_254710556677', vendor: 'MPESA_254720998811', amt: 3500.00, oldB: 19000, newB: 15500, destB: 11200 },
          { prefix: 'MULE', acct: 'KE_ACC_254745001199', vendor: 'MULE_SYN_4412', amt: 420000.00, oldB: 420000, newB: 0, destB: 0, hour: 3 },
          { prefix: 'TILL', acct: 'KE_ACC_254712345678', vendor: 'TILL_QUICKMART_305', amt: 820.00, oldB: 11800, newB: 10980, destB: 87320 },
        ];
        for (let i = 0; i < cases.length; i++) {
          const c = cases[i];
          const ts = c.hour !== undefined
            ? new Date(now.getFullYear(), now.getMonth(), now.getDate(), c.hour, 10 + i, 0)
            : new Date(now.getTime() + i * 2000);
          await scorePayload({
            tx_id: makeTxId(c.prefix),
            origin_account_id: c.acct,
            vendor_hash: c.vendor,
            amount_kes: c.amt,
            timestamp: toNaiveIso(ts),
            oldbalance_org: c.oldB,
            newbalance_orig: c.newB,
            newbalance_dest: c.destB,
          });
        }
        await refreshAll();
      } catch (err) {
        showError(`Stream error: ${err.message}`);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Mixed Stream (8 Tx)';
      }
    }

    document.getElementById('txForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.disabled = true;
      btn.textContent = 'Scoring...';
      try {
        const tsVal = document.getElementById('txTimestamp').value;
        const tsNaive = tsVal ? `${tsVal}:00` : toNaiveIso(new Date());
        const payload = {
          tx_id: makeTxId(document.getElementById('txType').value.slice(0, 4)),
          origin_account_id: document.getElementById('originAccount').value.trim(),
          vendor_hash: document.getElementById('vendorHash').value.trim(),
          amount_kes: parseFloat(document.getElementById('amountKes').value),
          timestamp: tsNaive,
          oldbalance_org: parseFloat(document.getElementById('oldBalanceOrg').value),
          newbalance_orig: parseFloat(document.getElementById('newBalanceOrig').value),
          newbalance_dest: parseFloat(document.getElementById('newBalanceDest').value),
        };
        await scorePayload(payload);
        await refreshAll();
      } catch (err) {
        showError(`Scoring failed: ${err.message}`);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Score Transaction';
      }
    });

    async function refreshAll() {
      await Promise.all([checkHealth(), refreshStats(), refreshTransactions()]);
    }

    document.getElementById('txTimestamp').value = toLocalInputValue(new Date());
    refreshAll();
  </script>
</body>
</html>
"""
