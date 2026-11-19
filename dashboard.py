DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Anomaly Guard — Mobile Money Fraud Screening Console</title>
  <style>
    :root {
      --bg: #f4f5f7;
      --surface: #ffffff;
      --subtle: #f9fafb;
      --border: #d8dce3;
      --border-soft: #eaedf2;
      --text: #111827;
      --muted: #5b6472;
      --accent: #111827;
      --focus: #1d4ed8;
      --ok-bg: #eef7f1;
      --ok-text: #14532d;
      --ok-border: #bbf7d0;
      --warn-bg: #fffbeb;
      --warn-text: #92400e;
      --warn-border: #fde68a;
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
      line-height: 1.48;
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
    .brand { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
    .brand h1 { margin: 0; font-size: 16px; font-weight: 700; letter-spacing: -0.01em; }
    .brand span { font-size: 12px; color: var(--muted); }
    .top-meta { display: flex; align-items: center; gap: 16px; font-size: 12px; color: var(--muted); flex-wrap: wrap; }
    .top-meta a { color: var(--text); text-decoration: none; border-bottom: 1px solid var(--border); font-weight: 500; }
    .top-meta a:hover { border-color: var(--text); }
    .mono { font-family: var(--mono); }

    .container { max-width: 1220px; margin: 0 auto; padding: 18px 24px 44px; }

    /* Context intro bar */
    .context-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      border-radius: 4px;
      padding: 12px 16px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      flex-wrap: wrap;
    }
    .context-bar p { margin: 0; font-size: 13px; color: #374151; max-width: 820px; }
    .context-bar strong { color: var(--text); }
    .context-pills { display: flex; gap: 8px; flex-wrap: wrap; }
    .pill {
      font-size: 11px;
      font-family: var(--mono);
      padding: 3px 8px;
      border-radius: 2px;
      background: var(--subtle);
      border: 1px solid var(--border);
      color: var(--muted);
    }

    /* Mode Selector Cards */
    .mode-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }
    .mode-card {
      text-align: left;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 13px 15px;
      cursor: pointer;
      transition: border-color 0.15s, background 0.15s;
      font-family: var(--sans);
    }
    .mode-card:hover { border-color: #6b7280; background: var(--subtle); }
    .mode-card.active {
      border: 2px solid var(--accent);
      background: var(--surface);
      padding: 12px 14px;
    }
    .mode-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 4px;
    }
    .mode-title { font-size: 14px; font-weight: 700; color: var(--text); }
    .mode-badge {
      font-size: 10px;
      font-family: var(--mono);
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 2px;
      background: var(--subtle);
      border: 1px solid var(--border);
      color: var(--muted);
    }
    .mode-card.active .mode-badge {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }
    .mode-desc { font-size: 12px; color: var(--muted); margin: 0; }

    /* Flat stat strip */
    .stat-strip {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      margin-bottom: 18px;
    }
    .stat-cell { padding: 12px 16px; border-right: 1px solid var(--border-soft); }
    .stat-cell:last-child { border-right: none; }
    .stat-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); margin-bottom: 2px; }
    .stat-val { font-family: var(--mono); font-size: 20px; font-weight: 600; color: var(--text); }
    .stat-val.danger { color: var(--bad-text); }
    .stat-sub { font-size: 11px; color: var(--muted); margin-top: 2px; }

    .grid {
      display: grid;
      grid-template-columns: 1.3fr 1fr;
      gap: 18px;
      margin-bottom: 18px;
    }
    @media (max-width: 920px) {
      .mode-grid { grid-template-columns: 1fr; }
      .stat-strip { grid-template-columns: repeat(2, 1fr); }
      .grid { grid-template-columns: 1fr; }
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
    }
    .panel-head {
      padding: 11px 16px;
      border-bottom: 1px solid var(--border-soft);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .panel-head h2 { margin: 0; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; }
    .panel-body { padding: 16px; }

    .btn {
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 500;
      padding: 7px 11px;
      border-radius: 3px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      cursor: pointer;
    }
    .btn:hover { background: var(--subtle); border-color: #9ca3af; }
    .btn:disabled { opacity: 0.55; cursor: not-allowed; }
    .btn-primary {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      padding: 9px 15px;
      font-weight: 600;
    }
    .btn-primary:hover { background: #1f2937; }
    .btn-active { background: var(--accent); color: #fff; border-color: var(--accent); }

    /* Demo Mode scenario list */
    .scenario-list {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-bottom: 14px;
    }
    @media (max-width: 600px) { .scenario-list { grid-template-columns: 1fr; } }
    .scenario-item {
      text-align: left;
      background: var(--subtle);
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 10px 12px;
      cursor: pointer;
      font-family: var(--sans);
    }
    .scenario-item:hover { border-color: #6b7280; }
    .scenario-item.selected {
      background: var(--surface);
      border: 2px solid var(--accent);
      padding: 9px 11px;
    }
    .scenario-top { display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 3px; }
    .scenario-name { font-size: 13px; font-weight: 600; color: var(--text); }
    .scenario-tag {
      font-size: 10px;
      font-family: var(--mono);
      padding: 1px 6px;
      border-radius: 2px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: var(--surface);
    }
    .scenario-tag.risk { background: var(--bad-bg); color: var(--bad-text); border-color: var(--bad-border); }
    .scenario-tag.ok { background: var(--ok-bg); color: var(--ok-text); border-color: var(--ok-border); }
    .scenario-tag.pat { background: var(--warn-bg); color: var(--warn-text); border-color: var(--warn-border); }
    .scenario-sub { font-size: 11px; color: var(--muted); }

    .scenario-brief {
      background: var(--subtle);
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 13px;
      margin-bottom: 14px;
    }
    .scenario-brief h3 { margin: 0 0 6px; font-size: 14px; }
    .scenario-brief p { margin: 0 0 8px; font-size: 12px; color: #374151; }
    .payload-preview {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      background: var(--surface);
      border: 1px solid var(--border-soft);
      margin-top: 8px;
    }
    .payload-preview td {
      padding: 5px 8px;
      border-bottom: 1px solid var(--border-soft);
    }
    .payload-preview td:first-child { color: var(--muted); width: 42%; }
    .payload-preview td:last-child { font-family: var(--mono); font-weight: 500; }

    /* Guided Mode */
    .progress-head {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 6px;
    }
    .progress-track {
      width: 100%;
      height: 6px;
      background: var(--border-soft);
      border-radius: 3px;
      overflow: hidden;
      margin-bottom: 14px;
    }
    .progress-fill {
      height: 100%;
      background: var(--accent);
      transition: width 0.2s ease;
    }
    .guided-card {
      border: 2px solid var(--accent);
      border-radius: 4px;
      padding: 15px;
      background: var(--surface);
      margin-bottom: 12px;
    }
    .guided-card h3 { margin: 0 0 4px; font-size: 15px; }
    .guided-explain { margin: 0 0 10px; font-size: 13px; color: #374151; }
    .guided-meta {
      background: var(--subtle);
      border: 1px solid var(--border-soft);
      border-radius: 3px;
      padding: 9px 11px;
      font-size: 12px;
      margin-bottom: 12px;
    }
    .guided-meta div { margin-bottom: 4px; }
    .guided-meta div:last-child { margin-bottom: 0; }
    .example-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px solid var(--border-soft);
      flex-wrap: wrap;
    }
    .guided-input {
      width: 100%;
      padding: 9px 10px;
      font-size: 14px;
      font-family: var(--mono);
      border: 1px solid #6b7280;
      border-radius: 3px;
      background: #fff;
      color: var(--text);
    }
    .guided-input:focus { outline: 2px solid rgba(17, 24, 39, 0.15); border-color: var(--accent); }
    .guided-hint { font-size: 11px; color: var(--muted); margin-top: 6px; }
    .guided-err { font-size: 12px; color: var(--bad-text); margin-top: 6px; font-weight: 500; display: none; }
    .guided-nav { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-top: 12px; }
    .guided-result-note {
      display: none;
      margin-top: 12px;
      padding: 10px 12px;
      border-radius: 3px;
      background: var(--subtle);
      border: 1px solid var(--border);
      font-size: 12px;
    }

    /* Manual Form */
    .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 11px; }
    @media (max-width: 600px) { .form-grid { grid-template-columns: 1fr; } }
    .field label { display: block; font-size: 11px; font-weight: 600; color: var(--muted); margin-bottom: 3px; }
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
    .field input:focus, .field select:focus { outline: none; border-color: var(--text); }
    .field-help { font-size: 10px; color: var(--muted); margin-top: 2px; }
    .form-actions { margin-top: 14px; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }

    /* Verdict & Explainability Panel */
    .verdict-box {
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 13px;
      background: var(--subtle);
      margin-bottom: 12px;
    }
    .verdict-box.ok { background: var(--ok-bg); border-color: var(--ok-border); color: var(--ok-text); }
    .verdict-box.warn { background: var(--warn-bg); border-color: var(--warn-border); color: var(--warn-text); }
    .verdict-box.bad { background: var(--bad-bg); border-color: var(--bad-border); color: var(--bad-text); }
    .verdict-title { font-size: 14px; font-weight: 700; margin: 0 0 3px; font-family: var(--mono); }
    .verdict-sub { font-size: 12px; margin: 0; }

    .kv-list { width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 12px; }
    .kv-list td { padding: 6px 0; border-bottom: 1px solid var(--border-soft); }
    .kv-list td:first-child { color: var(--muted); }
    .kv-list td:last-child { text-align: right; font-family: var(--mono); font-weight: 600; }

    .signal-box {
      border-top: 1px solid var(--border-soft);
      padding-top: 10px;
      font-size: 12px;
    }
    .signal-box ul { margin: 6px 0 0; padding-left: 18px; color: #374151; }
    .signal-box li { margin-bottom: 4px; }

    .score-disclaimer {
      margin-top: 8px;
      font-size: 11px;
      color: var(--muted);
      background: var(--subtle);
      padding: 7px 9px;
      border-radius: 3px;
      border: 1px solid var(--border-soft);
    }

    .threshold-bar {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--border-soft);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 12px;
      flex-wrap: wrap;
    }
    .threshold-bar input[type="range"] { flex: 1; min-width: 110px; }

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

    /* Audit Ledger */
    .table-wrap { overflow-x: auto; }
    table.ledger { width: 100%; border-collapse: collapse; font-size: 12px; }
    table.ledger th {
      text-align: left;
      padding: 9px 12px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--muted);
      background: var(--subtle);
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    table.ledger td { padding: 8px 12px; border-bottom: 1px solid var(--border-soft); white-space: nowrap; }
    table.ledger tr:hover td { background: var(--subtle); }
    .num { text-align: right; font-family: var(--mono); }
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
    .hidden { display: none !important; }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <h1>Anomaly Guard</h1>
      <span>B2B Mobile Money Fraud Screening Console (PaySim-KES Prototype)</span>
    </div>
    <div class="top-meta">
      <span id="healthText" class="mono">status: checking...</span>
      <span>Synthetic telemetry only (Kenya DPA 2019)</span>
      <a href="/docs" target="_blank">OpenAPI /docs</a>
    </div>
  </header>

  <main class="container">
    <!-- Plain-English Product Context -->
    <section class="context-bar">
      <p>
        <strong>What Anomaly Guard does:</strong> Screens mobile money transactions in real time for Kenyan SACCOs, micro-lenders, and fintech risk teams before settlement. In production, a payment switch streams transactions automatically to <span class="mono">POST /score</span>; choose a mode below to explore fraud scenarios, walk through the input schema step by step, or test custom payloads.
      </p>
      <div class="context-pills">
        <span class="pill">B2B Risk API</span>
        <span class="pill">Target &le; 1,500 ms</span>
        <span class="pill">SQLite Audit Store</span>
      </div>
    </section>

    <!-- Immediately Visible 3-Mode Selector -->
    <section class="mode-grid" aria-label="Choose an experience">
      <button type="button" id="tabDemo" class="mode-card active" onclick="switchMode('demo')">
        <div class="mode-head">
          <span class="mode-title">Demo Mode</span>
          <span class="mode-badge">Explore</span>
        </div>
        <p class="mode-desc">Select a Kenyan fraud scenario (SIM-swap, mule transfer, smurfing), inspect its data, and score it live with the ML engine.</p>
      </button>

      <button type="button" id="tabGuided" class="mode-card" onclick="switchMode('guided')">
        <div class="mode-head">
          <span class="mode-title">Guided Mode</span>
          <span class="mode-badge">Learn</span>
        </div>
        <p class="mode-desc">First time here? Walk through every transaction field step by step with plain-English definitions, data sources, and validation.</p>
      </button>

      <button type="button" id="tabManual" class="mode-card" onclick="switchMode('manual')">
        <div class="mode-head">
          <span class="mode-title">Manual Mode</span>
          <span class="mode-badge">Developer</span>
        </div>
        <p class="mode-desc">Direct analyst &amp; developer console for entering custom transaction payloads and testing balance or velocity edge cases.</p>
      </button>
    </section>

    <!-- KPI Strip -->
    <section class="stat-strip">
      <div class="stat-cell">
        <div class="stat-label">Transactions Scored</div>
        <div id="kpiTotal" class="stat-val">0</div>
        <div class="stat-sub">Persisted in SQLite</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Flagged Suspicious</div>
        <div id="kpiFlagged" class="stat-val danger">0</div>
        <div id="kpiRate" class="stat-sub">0.0% flag rate</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Last Inference Latency</div>
        <div id="kpiLatency" class="stat-val">--</div>
        <div class="stat-sub">SLA target &le; 1,500 ms</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Risk Cutoff Threshold</div>
        <div id="kpiThreshold" class="stat-val">0.80</div>
        <div id="kpiModel" class="stat-sub">Checking model...</div>
      </div>
    </section>

    <div id="errBanner" class="err-banner"></div>

    <!-- Main Workspace -->
    <section class="grid">
      <!-- Left: Mode-Driven Workspace -->
      <div class="panel">
        <!-- 1. DEMO MODE -->
        <div id="panelDemo">
          <div class="panel-head">
            <h2>Demo Mode — Choose a Fraud Scenario</h2>
            <span class="mono" style="font-size:11px;color:var(--muted);">Real ML Scoring (POST /score)</span>
          </div>
          <div class="panel-body">
            <div id="demoCards" class="scenario-list"></div>

            <div class="scenario-brief">
              <h3 id="demoDetailTitle">Select a scenario</h3>
              <p id="demoDetailDesc"></p>
              <p id="demoDetailSource" style="font-size:11px;color:var(--muted);"></p>
              <table class="payload-preview" id="demoPayloadPreview"></table>
            </div>

            <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;">
              <span style="font-size:11px;color:var(--muted);">Sends synthetic data to the live backend — verdicts are never hardcoded.</span>
              <div style="display:flex;gap:8px;">
                <button type="button" class="btn" onclick="copyScenarioToManual()">Edit in Manual Mode</button>
                <button type="button" id="runDemoBtn" class="btn btn-primary" onclick="runSelectedScenario()">Run Scenario Through ML Engine</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. GUIDED MODE -->
        <div id="panelGuided" class="hidden">
          <div class="panel-head">
            <h2>Guided Mode — Step-by-Step Transaction Walkthrough</h2>
            <button type="button" class="btn" onclick="resetGuided()">Restart Tour</button>
          </div>
          <div class="panel-body">
            <div class="progress-head">
              <span id="guidedStepLabel">Step 1 of 8</span>
              <span id="guidedPctLabel" class="mono">13% complete</span>
            </div>
            <div class="progress-track">
              <div id="guidedProgressFill" class="progress-fill" style="width:13%;"></div>
            </div>

            <div id="guidedStepCard" class="guided-card">
              <h3 id="guidedFieldTitle">Channel / Transaction Type</h3>
              <p id="guidedFieldDesc" class="guided-explain"></p>
              <div class="guided-meta">
                <div><strong>Where this comes from in production:</strong> <span id="guidedFieldSource"></span></div>
                <div class="example-row">
                  <span><strong>Example:</strong> <span id="guidedExampleVal" class="mono"></span></span>
                  <button type="button" class="btn" onclick="fillGuidedExample()">Use Example</button>
                </div>
              </div>
              <div id="guidedInputWrap"></div>
              <div id="guidedLiveMath" class="guided-hint"></div>
              <div id="guidedError" class="guided-err"></div>
            </div>

            <div id="guidedSummaryBox" class="scenario-brief hidden">
              <h3>Review Your Transaction Before Scoring</h3>
              <p>Confirm the synthetic transaction below, then submit it to the real-time scoring API to see how Anomaly Guard evaluates it.</p>
              <table class="payload-preview" id="guidedSummaryTable"></table>
            </div>

            <div class="guided-nav">
              <button type="button" id="guidedPrevBtn" class="btn" onclick="guidedPrev()">&larr; Back</button>
              <button type="button" id="guidedNextBtn" class="btn btn-primary" onclick="guidedNext()">Next Field &rarr;</button>
            </div>

            <div id="guidedResultNote" class="guided-result-note"></div>
          </div>
        </div>

        <!-- 3. MANUAL MODE -->
        <div id="panelManual" class="hidden">
          <div class="panel-head">
            <h2>Manual Mode — Developer &amp; Analyst Testing Form</h2>
            <span class="mono" style="font-size:11px;color:var(--muted);">POST /score</span>
          </div>
          <div class="panel-body">
            <p style="margin:0 0 12px;font-size:12px;color:var(--muted);">
              Enter custom transaction attributes directly. Try changing Sender New Balance so it does not equal <span class="mono">Old Balance - Amount</span> to test ledger reconciliation checks.
            </p>
            <form id="txForm">
              <div class="form-grid">
                <div class="field">
                  <label for="txType">Channel / Type</label>
                  <select id="txType">
                    <option value="PAYMENT">Lipa na M-Pesa / Till (PAYMENT)</option>
                    <option value="TRANSFER">Send Money P2P (TRANSFER)</option>
                    <option value="CASH_OUT">Agent Withdrawal (CASH_OUT)</option>
                  </select>
                  <div class="field-help">Payment rail category from switch payload</div>
                </div>
                <div class="field">
                  <label for="amountKes">Amount (KES)</label>
                  <input id="amountKes" type="number" step="0.01" min="0" value="1200.00" required />
                  <div class="field-help">Transaction value in Kenya Shillings</div>
                </div>
                <div class="field">
                  <label for="originAccount">Origin Account ID (Pseudonymised)</label>
                  <input id="originAccount" type="text" value="KE_ACC_254712345678" required />
                  <div class="field-help">Sender account token used for velocity lookup</div>
                </div>
                <div class="field">
                  <label for="vendorHash">Recipient / Till / Agent ID</label>
                  <input id="vendorHash" type="text" value="TILL_NAIVAS_4021" required />
                  <div class="field-help">Destination wallet, till, or agent identifier</div>
                </div>
                <div class="field">
                  <label for="oldBalanceOrg">Sender Old Balance (KES)</label>
                  <input id="oldBalanceOrg" type="number" step="0.01" min="0" value="15000.00" required />
                  <div class="field-help">Sender ledger balance before transaction</div>
                </div>
                <div class="field">
                  <label for="newBalanceOrig">Sender New Balance (KES)</label>
                  <input id="newBalanceOrig" type="number" step="0.01" min="0" value="13800.00" required />
                  <div class="field-help">Expected consistent balance: Old - Amount</div>
                </div>
                <div class="field">
                  <label for="oldBalanceDest">Receiver Old Balance (KES, optional)</label>
                  <input id="oldBalanceDest" type="number" step="0.01" min="0" placeholder="Optional (e.g. 47000)" />
                  <div class="field-help">Enables receiver-side balance validation</div>
                </div>
                <div class="field">
                  <label for="newBalanceDest">Receiver New Balance (KES)</label>
                  <input id="newBalanceDest" type="number" step="0.01" min="0" value="48200.00" required />
                  <div class="field-help">Recipient balance recorded after movement</div>
                </div>
                <div class="field" style="grid-column: 1 / -1;">
                  <label for="txTimestamp">Transaction Timestamp (Local)</label>
                  <input id="txTimestamp" type="datetime-local" />
                  <div class="field-help">Used for ghost-hour detection and 15m / 24h velocity windows</div>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" class="btn" onclick="autoBalanceManual()">Auto-Calculate Consistent New Balance</button>
                <button type="submit" id="submitBtn" class="btn btn-primary">Score Transaction</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Right: Explain This Transaction & SOC Threshold -->
      <div class="panel">
        <div class="panel-head">
          <h2>Explain This Transaction</h2>
          <span id="verdictTxId" class="mono" style="font-size:11px;color:var(--muted);">Awaiting run</span>
        </div>
        <div class="panel-body">
          <div id="verdictBox" class="verdict-box">
            <p id="verdictLabel" class="verdict-title">NO TRANSACTION SCORED YET</p>
            <p id="verdictSub" class="verdict-sub">Select a scenario in Demo Mode, complete Guided Mode, or submit a custom payload to inspect live results.</p>
          </div>

          <table class="kv-list">
            <tr>
              <td>Risk Score Index (0.00 – 1.00)</td>
              <td id="scoreValue">--</td>
            </tr>
            <tr>
              <td>Recommended Policy Action</td>
              <td id="actionValue">--</td>
            </tr>
            <tr>
              <td>End-to-End API Latency</td>
              <td id="lastLatencyDetail">--</td>
            </tr>
            <tr>
              <td>Time Since Previous Tx <span style="font-size:10px;">(auto)</span></td>
              <td id="velTimeSince">--</td>
            </tr>
            <tr>
              <td>Account Tx Count — 15 min <span style="font-size:10px;">(auto)</span></td>
              <td id="velCount15">--</td>
            </tr>
            <tr>
              <td>Account Tx Count — 24 hr <span style="font-size:10px;">(auto)</span></td>
              <td id="velCount24">--</td>
            </tr>
          </table>

          <div class="signal-box">
            <strong>Detected Signals &amp; Reasoning</strong>
            <ul id="signalList">
              <li>Run any scenario or transaction to view the specific signals that drove the decision.</li>
            </ul>
            <div class="score-disclaimer" id="thresholdNote">
              A score at or above the configured threshold flags the transaction for analyst review or settlement hold; it is a risk index rather than a raw certainty percentage.
            </div>
          </div>

          <div class="threshold-bar">
            <label for="thresholdSlider"><strong>SOC Cutoff:</strong> <span id="thresholdReadout" class="mono">0.80</span></label>
            <input id="thresholdSlider" type="range" min="0.10" max="0.90" step="0.05" value="0.80" />
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
    let currentMode = 'demo';
    let currentFilter = 'all';
    let cachedTransactions = [];
    let selectedScenarioKey = 'normal';
    let activeThreshold = 0.80;

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

    function switchMode(mode) {
      currentMode = mode;
      ['demo', 'guided', 'manual'].forEach((m) => {
        const cap = m.charAt(0).toUpperCase() + m.slice(1);
        document.getElementById(`tab${cap}`).classList.toggle('active', m === mode);
        document.getElementById(`panel${cap}`).classList.toggle('hidden', m !== mode);
      });
      if (mode === 'guided') renderGuidedStep();
    }

    // ---------------- DEMO MODE SCENARIOS ----------------
    const SCENARIOS = {
      normal: {
        name: 'Normal M-Pesa Payment',
        tag: 'Legitimate',
        tagClass: 'ok',
        short: 'KES 250.50 — Ordinary merchant till payment.',
        desc: 'Simulates an everyday Lipa na M-Pesa payment to a supermarket till during business hours. Sender balance reconciles cleanly (12,500.00 - 250.50 = 12,249.50) with normal account velocity.',
        source: 'In production, streamed automatically from the institution\'s core mobile money ledger at checkout.',
        buildPayloads: () => {
          const now = new Date();
          return [{
            tx_id: makeTxId('TILL'),
            tx_type: 'PAYMENT',
            origin_account_id: 'KE_ACC_254712345678',
            vendor_hash: 'TILL_NAIVAS_4021',
            amount_kes: 250.50,
            timestamp: toNaiveIso(now),
            oldbalance_org: 12500.00,
            newbalance_orig: 12249.50,
            oldbalance_dest: 45000.00,
            newbalance_dest: 45250.50,
          }];
        },
        preview: [
          ['Channel / Type', 'Lipa na M-Pesa / Till (PAYMENT)'],
          ['Amount', 'KES 250.50'],
          ['Origin Account', 'KE_ACC_254712345678'],
          ['Recipient', 'TILL_NAIVAS_4021'],
          ['Sender Balance', 'KES 12,500.00 → KES 12,249.50 (reconciled)'],
          ['Time Window', 'Current local time'],
        ],
      },
      sim_swap: {
        name: 'SIM-Swap Drain',
        tag: 'High Risk',
        tagClass: 'risk',
        short: 'KES 185,000 — Ghost-hour (02:30) agent withdrawal.',
        desc: 'Simulates a classic Kenyan SIM-swap account takeover: an attacker hijacks the victim\'s number and empties the entire KES 185,000 balance to KES 0.00 via an agent cash-out at 2:30 AM.',
        source: 'Demonstrates combined ghost-hour timing + full account-drain detection prior to cash settlement.',
        buildPayloads: () => {
          const now = new Date();
          const ghost = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 2, 30, 0);
          return [{
            tx_id: makeTxId('SIMSWP'),
            tx_type: 'CASH_OUT',
            origin_account_id: 'KE_ACC_254722889911',
            vendor_hash: 'AGENT_CASHOUT_991',
            amount_kes: 185000.00,
            timestamp: toNaiveIso(ghost),
            oldbalance_org: 185000.00,
            newbalance_orig: 0.00,
            newbalance_dest: 0.00,
          }];
        },
        preview: [
          ['Channel / Type', 'Agent Withdrawal (CASH_OUT)'],
          ['Amount', 'KES 185,000.00'],
          ['Origin Account', 'KE_ACC_254722889911'],
          ['Recipient', 'AGENT_CASHOUT_991'],
          ['Sender Balance', 'KES 185,000.00 → KES 0.00 (100% drain)'],
          ['Time Window', '02:30 AM (ghost hour)'],
        ],
      },
      high_value: {
        name: 'Mule Transfer',
        tag: 'High Risk',
        tagClass: 'risk',
        short: 'KES 540,000 — Suspicious full-balance P2P sweep.',
        desc: 'Simulates a high-value transfer moving KES 540,000 in one sweep to a mule account at 03:15 AM, leaving the origin wallet empty while the destination balance shows zero reconciliation.',
        source: 'Tests detection of large syndicate fund-layering movements across proxy mobile wallets.',
        buildPayloads: () => {
          const now = new Date();
          const ghost = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 3, 15, 0);
          return [{
            tx_id: makeTxId('MULE'),
            tx_type: 'TRANSFER',
            origin_account_id: 'KE_ACC_254700445566',
            vendor_hash: 'MULE_WALLET_8842',
            amount_kes: 540000.00,
            timestamp: toNaiveIso(ghost),
            oldbalance_org: 540000.00,
            newbalance_orig: 0.00,
            newbalance_dest: 0.00,
          }];
        },
        preview: [
          ['Channel / Type', 'Send Money P2P (TRANSFER)'],
          ['Amount', 'KES 540,000.00'],
          ['Origin Account', 'KE_ACC_254700445566'],
          ['Recipient', 'MULE_WALLET_8842'],
          ['Sender Balance', 'KES 540,000.00 → KES 0.00 (full sweep)'],
          ['Time Window', '03:15 AM (ghost hour)'],
        ],
      },
      smurfing: {
        name: 'Smurfing Burst',
        tag: 'Pattern',
        tagClass: 'pat',
        short: '6× KES 900 rapid transfers to evade static thresholds.',
        desc: 'Simulates structuring ("smurfing"): instead of one large transfer that a static KES 50,000 rule would catch, the same account fires six KES 900 transfers within 90 seconds. Watch SQLite 15-minute velocity climb and trigger an alert.',
        source: 'Proves why behavioral velocity tracking outperforms static single-transaction thresholds.',
        buildPayloads: () => {
          const now = new Date();
          const acct = `KE_SMURF_${Math.floor(1000 + Math.random() * 9000)}`;
          let bal = 5400.00;
          const batch = [];
          for (let i = 0; i < 6; i++) {
            const ts = new Date(now.getTime() + i * 15000);
            const nextBal = Math.max(0, bal - 900.00);
            batch.push({
              tx_id: makeTxId(`SMRF${i + 1}`),
              tx_type: 'TRANSFER',
              origin_account_id: acct,
              vendor_hash: `PROXY_ACC_00${i + 1}`,
              amount_kes: 900.00,
              timestamp: toNaiveIso(ts),
              oldbalance_org: bal,
              newbalance_orig: nextBal,
              newbalance_dest: 0.00,
            });
            bal = nextBal;
          }
          return batch;
        },
        preview: [
          ['Batch Size', '6 sequential transfers (15s apart)'],
          ['Amount per Tx', 'KES 900.00 (far below KES 50,000 static limit)'],
          ['Origin Account', 'Generated unique account per run (KE_SMURF_XXXX)'],
          ['Recipients', 'PROXY_ACC_001 → PROXY_ACC_006'],
          ['Key Signal', 'Account Tx Count (15 min) climbs 0 → 5'],
        ],
      },
      mixed: {
        name: 'Mixed Transaction Stream',
        tag: 'Batch (8 Tx)',
        tagClass: 'pat',
        short: '8 transactions mixing legitimate payments & fraud.',
        desc: 'Dispatches a realistic mini-stream of 8 Kenyan mobile money transactions (Carrefour till, KPLC paybill, Airtel P2P, Java House, Quickmart, plus a 2:10 AM SIM-swap drain and a 3:16 AM mule transfer) to test throughput and audit logging.',
        source: 'Simulates live multi-account traffic arriving at a SACCO or fintech scoring gateway.',
        buildPayloads: () => {
          const now = new Date();
          const cases = [
            { prefix: 'TILL', type: 'PAYMENT', acct: 'KE_ACC_254711001122', vendor: 'TILL_CARREFOUR_102', amt: 1450.00, oldB: 24000, newB: 22550, destB: 120450 },
            { prefix: 'KPLC', type: 'PAYMENT', acct: 'KE_ACC_254722334455', vendor: 'PAYBILL_KPLC_888880', amt: 2000.00, oldB: 18500, newB: 16500, destB: 980000 },
            { prefix: 'P2P',  type: 'TRANSFER', acct: 'KE_ACC_254733998877', vendor: 'AIRTEL_254733112233', amt: 650.00, oldB: 5400, newB: 4750, destB: 3200 },
            { prefix: 'SIM',  type: 'CASH_OUT', acct: 'KE_ACC_254701999888', vendor: 'AGENT_KAWANGWARE_77', amt: 245000.00, oldB: 245000, newB: 0, destB: 0, hour: 2 },
            { prefix: 'TILL', type: 'PAYMENT', acct: 'KE_ACC_254798123456', vendor: 'TILL_JAVA_WESTLANDS', amt: 1850.00, oldB: 31000, newB: 29150, destB: 64200 },
            { prefix: 'P2P',  type: 'TRANSFER', acct: 'KE_ACC_254710556677', vendor: 'MPESA_254720998811', amt: 3500.00, oldB: 19000, newB: 15500, destB: 11200 },
            { prefix: 'MULE', type: 'TRANSFER', acct: 'KE_ACC_254745001199', vendor: 'MULE_SYN_4412', amt: 420000.00, oldB: 420000, newB: 0, destB: 0, hour: 3 },
            { prefix: 'TILL', type: 'PAYMENT', acct: 'KE_ACC_254712345678', vendor: 'TILL_QUICKMART_305', amt: 820.00, oldB: 11800, newB: 10980, destB: 87320 },
          ];
          return cases.map((c, i) => {
            const ts = c.hour !== undefined
              ? new Date(now.getFullYear(), now.getMonth(), now.getDate(), c.hour, 10 + i, 0)
              : new Date(now.getTime() + i * 2000);
            return {
              tx_id: makeTxId(c.prefix),
              tx_type: c.type,
              origin_account_id: c.acct,
              vendor_hash: c.vendor,
              amount_kes: c.amt,
              timestamp: toNaiveIso(ts),
              oldbalance_org: c.oldB,
              newbalance_orig: c.newB,
              newbalance_dest: c.destB,
            };
          });
        },
        preview: [
          ['Stream Composition', '6 legitimate Kenyan transactions + 2 fraud attacks'],
          ['Legitimate Samples', 'Carrefour, KPLC Paybill, Airtel P2P, Java, Quickmart'],
          ['Fraud Samples', 'KES 245k 02:13 SIM-swap drain + KES 420k 03:16 mule sweep'],
          ['Audit Output', 'All 8 scored live and logged to SQLite below'],
        ],
      },
    };

    function renderDemoCards() {
      const container = document.getElementById('demoCards');
      container.innerHTML = Object.entries(SCENARIOS).map(([key, sc]) => `
        <button type="button" class="scenario-item ${key === selectedScenarioKey ? 'selected' : ''}" onclick="selectScenario('${key}')">
          <div class="scenario-top">
            <span class="scenario-name">${escapeHtml(sc.name)}</span>
            <span class="scenario-tag ${sc.tagClass}">${escapeHtml(sc.tag)}</span>
          </div>
          <div class="scenario-sub">${escapeHtml(sc.short)}</div>
        </button>
      `).join('');

      const active = SCENARIOS[selectedScenarioKey];
      document.getElementById('demoDetailTitle').textContent = active.name;
      document.getElementById('demoDetailDesc').textContent = active.desc;
      document.getElementById('demoDetailSource').textContent = active.source;
      document.getElementById('demoPayloadPreview').innerHTML = active.preview
        .map(([k, v]) => `<tr><td>${escapeHtml(k)}</td><td>${escapeHtml(v)}</td></tr>`)
        .join('');
    }

    function selectScenario(key) {
      selectedScenarioKey = key;
      renderDemoCards();
    }

    function copyScenarioToManual() {
      const payloads = SCENARIOS[selectedScenarioKey].buildPayloads();
      const first = payloads[0];
      fillManualForm(first);
      switchMode('manual');
    }

    async function runSelectedScenario() {
      const btn = document.getElementById('runDemoBtn');
      const sc = SCENARIOS[selectedScenarioKey];
      const payloads = sc.buildPayloads();
      btn.disabled = true;
      showError('');
      try {
        for (let i = 0; i < payloads.length; i++) {
          btn.textContent = payloads.length > 1
            ? `Scoring ${i + 1} of ${payloads.length}...`
            : 'Scoring via /score...';
          fillManualForm(payloads[i]);
          await scorePayload(payloads[i]);
        }
        await refreshAll();
      } catch (err) {
        showError(`Scoring failed: ${err.message}`);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Run Scenario Through ML Engine';
      }
    }

    // ---------------- GUIDED MODE (8 STEPS + REVIEW) ----------------
    const GUIDED_STEPS = [
      {
        key: 'tx_type',
        title: 'Channel / Transaction Type',
        desc: 'Select how the money is moving across the mobile money network.',
        source: 'Provided automatically by the mobile money switch (e.g., Paybill/Till checkout, P2P Send Money, or Agent Cash-Out).',
        exampleLabel: 'Lipa na M-Pesa / Till (PAYMENT)',
        exampleValue: 'PAYMENT',
        type: 'select',
        options: [
          ['PAYMENT', 'Lipa na M-Pesa / Till (PAYMENT)'],
          ['TRANSFER', 'Send Money P2P (TRANSFER)'],
          ['CASH_OUT', 'Agent Withdrawal (CASH_OUT)'],
        ],
        validate: (v) => v ? '' : 'Please choose a transaction type.',
      },
      {
        key: 'amount_kes',
        title: 'Transaction Amount (KES)',
        desc: 'Enter how much money is being moved in Kenya Shillings.',
        source: 'Captured directly from the transaction request payload before settlement.',
        exampleLabel: 'KES 1,200.00',
        exampleValue: '1200.00',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) > 0) ? '' : 'Enter a valid amount greater than 0 KES.',
      },
      {
        key: 'origin_account_id',
        title: 'Origin Account ID (Pseudonymised)',
        desc: 'Identifier of the account sending the money. Anomaly Guard uses this to query 15-minute and 24-hour transaction velocity.',
        source: 'In production, a hashed or pseudonymised account token from the SACCO or wallet ledger — never raw personal data in this prototype.',
        exampleLabel: 'KE_ACC_254712345678',
        exampleValue: 'KE_ACC_254712345678',
        type: 'text',
        validate: (v) => String(v || '').trim().length >= 3 ? '' : 'Enter an account identifier (at least 3 characters).',
      },
      {
        key: 'vendor_hash',
        title: 'Recipient / Till / Agent ID',
        desc: 'Identifier of the merchant till, agent float, or wallet receiving the funds.',
        source: 'Populated automatically from the destination till number, paybill, or recipient wallet hash.',
        exampleLabel: 'TILL_NAIVAS_4021',
        exampleValue: 'TILL_NAIVAS_4021',
        type: 'text',
        validate: (v) => String(v || '').trim().length >= 3 ? '' : 'Enter a recipient identifier (at least 3 characters).',
      },
      {
        key: 'oldbalance_org',
        title: 'Sender Old Balance (KES)',
        desc: 'The sender\'s account balance immediately before this transaction is processed.',
        source: 'Read from the institution\'s core ledger before debiting the sender account.',
        exampleLabel: 'KES 15,000.00',
        exampleValue: '15000.00',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) >= 0) ? '' : 'Enter a valid balance of 0 or more.',
      },
      {
        key: 'newbalance_orig',
        title: 'Sender New Balance (KES)',
        desc: 'The sender\'s account balance immediately after this transaction. Anomaly Guard checks whether Old Balance minus Amount reconciles cleanly and detects full drains to KES 0.',
        source: 'Calculated by the core banking/mobile money ledger post-debit. Mismatches indicate ledger tampering or anomalous balance manipulation.',
        exampleLabel: 'Consistent: Old - Amount',
        exampleValue: '__CALC_NEW_ORIG__',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) >= 0) ? '' : 'Enter a valid post-transaction balance of 0 or more.',
      },
      {
        key: 'newbalance_dest',
        title: 'Receiver New Balance (KES)',
        desc: 'The recipient\'s recorded account balance after receiving the funds.',
        source: 'Recorded from the destination account ledger (often 0 for unpopulated merchant accounts or rapid cash-out mule wallets in PaySim).',
        exampleLabel: 'KES 48,200.00',
        exampleValue: '48200.00',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) >= 0) ? '' : 'Enter a valid receiver balance of 0 or more.',
      },
      {
        key: 'timestamp',
        title: 'Transaction Timestamp',
        desc: 'When the transaction occurred. Used to detect off-hours ("ghost-hour") attacks between 00:00 and 04:59 and compute rolling velocity windows.',
        source: 'Generated automatically by the transaction gateway server clock.',
        exampleLabel: 'Current local date & time',
        exampleValue: '__NOW__',
        type: 'datetime-local',
        validate: (v) => v ? '' : 'Select a valid date and time.',
      },
    ];

    let guidedStepIdx = 0;
    let guidedState = {
      tx_type: 'PAYMENT',
      amount_kes: '',
      origin_account_id: '',
      vendor_hash: '',
      oldbalance_org: '',
      newbalance_orig: '',
      newbalance_dest: '',
      timestamp: toLocalInputValue(new Date()),
    };

    function resetGuided() {
      guidedStepIdx = 0;
      guidedState = {
        tx_type: 'PAYMENT',
        amount_kes: '',
        origin_account_id: '',
        vendor_hash: '',
        oldbalance_org: '',
        newbalance_orig: '',
        newbalance_dest: '',
        timestamp: toLocalInputValue(new Date()),
      };
      document.getElementById('guidedResultNote').style.display = 'none';
      renderGuidedStep();
    }

    function getGuidedExampleValue(step) {
      if (step.exampleValue === '__CALC_NEW_ORIG__') {
        const oldB = parseFloat(guidedState.oldbalance_org || '15000');
        const amt = parseFloat(guidedState.amount_kes || '1200');
        return Math.max(0, oldB - amt).toFixed(2);
      }
      if (step.exampleValue === '__NOW__') {
        return toLocalInputValue(new Date());
      }
      return step.exampleValue;
    }

    function renderGuidedStep() {
      const total = GUIDED_STEPS.length;
      const isReview = guidedStepIdx >= total;
      const pct = isReview ? 100 : Math.round(((guidedStepIdx + 1) / total) * 100);

      document.getElementById('guidedStepLabel').textContent = isReview
        ? 'Review & Submit'
        : `Step ${guidedStepIdx + 1} of ${total}`;
      document.getElementById('guidedPctLabel').textContent = `${pct}% complete`;
      document.getElementById('guidedProgressFill').style.width = `${pct}%`;

      const stepCard = document.getElementById('guidedStepCard');
      const summaryBox = document.getElementById('guidedSummaryBox');
      const prevBtn = document.getElementById('guidedPrevBtn');
      const nextBtn = document.getElementById('guidedNextBtn');

      prevBtn.disabled = guidedStepIdx === 0;

      if (isReview) {
        stepCard.classList.add('hidden');
        summaryBox.classList.remove('hidden');
        nextBtn.textContent = 'Submit & Score Transaction';
        const oldB = parseFloat(guidedState.oldbalance_org);
        const amt = parseFloat(guidedState.amount_kes);
        const newB = parseFloat(guidedState.newbalance_orig);
        const expected = oldB - amt;
        const mathStatus = Math.abs(expected - newB) <= 1.0
          ? 'Reconciled cleanly'
          : `Mismatch (expected KES ${formatKes(expected)})`;

        document.getElementById('guidedSummaryTable').innerHTML = [
          ['Channel / Type', guidedState.tx_type],
          ['Amount', `KES ${formatKes(amt)}`],
          ['Origin Account', guidedState.origin_account_id],
          ['Recipient', guidedState.vendor_hash],
          ['Sender Balance', `KES ${formatKes(oldB)} → KES ${formatKes(newB)} (${mathStatus})`],
          ['Receiver New Balance', `KES ${formatKes(guidedState.newbalance_dest)}`],
          ['Timestamp', guidedState.timestamp.replace('T', ' ')],
        ].map(([k, v]) => `<tr><td>${escapeHtml(k)}</td><td>${escapeHtml(v)}</td></tr>`).join('');
        return;
      }

      stepCard.classList.remove('hidden');
      summaryBox.classList.add('hidden');
      nextBtn.textContent = guidedStepIdx === total - 1 ? 'Review Transaction →' : 'Next Field →';

      const step = GUIDED_STEPS[guidedStepIdx];
      document.getElementById('guidedFieldTitle').textContent = step.title;
      document.getElementById('guidedFieldDesc').textContent = step.desc;
      document.getElementById('guidedFieldSource').textContent = step.source;
      document.getElementById('guidedExampleVal').textContent = step.key === 'newbalance_orig'
        ? `KES ${formatKes(getGuidedExampleValue(step))}`
        : step.exampleLabel;

      const wrap = document.getElementById('guidedInputWrap');
      const val = guidedState[step.key] ?? '';
      if (step.type === 'select') {
        wrap.innerHTML = `<select id="guidedActiveInput" class="guided-input">${step.options.map(
          ([ov, ol]) => `<option value="${ov}" ${ov === val ? 'selected' : ''}>${escapeHtml(ol)}</option>`
        ).join('')}</select>`;
      } else {
        const extra = step.type === 'number' ? 'step="0.01" min="0"' : '';
        wrap.innerHTML = `<input id="guidedActiveInput" class="guided-input" type="${step.type}" ${extra} value="${escapeHtml(val)}" placeholder="Enter ${escapeHtml(step.title)}" />`;
      }

      const mathEl = document.getElementById('guidedLiveMath');
      if (step.key === 'newbalance_orig') {
        const oldB = parseFloat(guidedState.oldbalance_org || '0');
        const amt = parseFloat(guidedState.amount_kes || '0');
        mathEl.textContent = `Ledger math check: KES ${formatKes(oldB)} − KES ${formatKes(amt)} = KES ${formatKes(oldB - amt)}. Entering a different balance lets you test tampering detection.`;
      } else {
        mathEl.textContent = '';
      }

      const errEl = document.getElementById('guidedError');
      errEl.style.display = 'none';
      errEl.textContent = '';
    }

    function fillGuidedExample() {
      const step = GUIDED_STEPS[guidedStepIdx];
      const ex = getGuidedExampleValue(step);
      guidedState[step.key] = ex;
      const input = document.getElementById('guidedActiveInput');
      if (input) input.value = ex;
      document.getElementById('guidedError').style.display = 'none';
    }

    function guidedPrev() {
      if (guidedStepIdx > 0) {
        if (guidedStepIdx < GUIDED_STEPS.length) {
          const inp = document.getElementById('guidedActiveInput');
          if (inp) guidedState[GUIDED_STEPS[guidedStepIdx].key] = inp.value;
        }
        guidedStepIdx -= 1;
        renderGuidedStep();
      }
    }

    async function guidedNext() {
      const total = GUIDED_STEPS.length;
      if (guidedStepIdx < total) {
        const step = GUIDED_STEPS[guidedStepIdx];
        const inp = document.getElementById('guidedActiveInput');
        const val = inp ? inp.value : '';
        const err = step.validate(val);
        const errEl = document.getElementById('guidedError');
        if (err) {
          errEl.textContent = err;
          errEl.style.display = 'block';
          return;
        }
        guidedState[step.key] = val;
        guidedStepIdx += 1;
        renderGuidedStep();
        return;
      }

      // Submit guided transaction to real /score endpoint
      const nextBtn = document.getElementById('guidedNextBtn');
      nextBtn.disabled = true;
      nextBtn.textContent = 'Scoring via /score...';
      try {
        const payload = {
          tx_id: makeTxId('GUID'),
          tx_type: guidedState.tx_type,
          origin_account_id: guidedState.origin_account_id.trim(),
          vendor_hash: guidedState.vendor_hash.trim(),
          amount_kes: parseFloat(guidedState.amount_kes),
          timestamp: `${guidedState.timestamp}:00`,
          oldbalance_org: parseFloat(guidedState.oldbalance_org),
          newbalance_orig: parseFloat(guidedState.newbalance_orig),
          newbalance_dest: parseFloat(guidedState.newbalance_dest),
        };
        const result = await scorePayload(payload);
        await refreshAll();
        const note = document.getElementById('guidedResultNote');
        const isFlag = Number(result.verdict) === 1;
        note.innerHTML = `<strong>Understanding your result:</strong> Your transaction received a risk score of <span class="mono">${Number(result.score).toFixed(2)}</span> against the active SOC cutoff of <span class="mono">${Number(result.threshold ?? activeThreshold).toFixed(2)}</span>, so Anomaly Guard marked it <strong>${isFlag ? 'FLAGGED' : 'CLEARED'}</strong>. Check the <em>Explain This Transaction</em> panel on the right for the exact signals detected and scroll down to see it recorded in SQLite.`;
        note.style.display = 'block';
      } catch (err) {
        showError(`Guided scoring failed: ${err.message}`);
      } finally {
        nextBtn.disabled = false;
        nextBtn.textContent = 'Submit & Score Transaction';
      }
    }

    // ---------------- MANUAL MODE & API CALLS ----------------
    function fillManualForm(cfg) {
      if (cfg.tx_type) document.getElementById('txType').value = cfg.tx_type;
      document.getElementById('amountKes').value = cfg.amount_kes;
      document.getElementById('originAccount').value = cfg.origin_account_id;
      document.getElementById('vendorHash').value = cfg.vendor_hash;
      document.getElementById('oldBalanceOrg').value = cfg.oldbalance_org;
      document.getElementById('newBalanceOrig').value = cfg.newbalance_orig;
      document.getElementById('oldBalanceDest').value = cfg.oldbalance_dest ?? '';
      document.getElementById('newBalanceDest').value = cfg.newbalance_dest;
      if (cfg.timestamp) document.getElementById('txTimestamp').value = cfg.timestamp.slice(0, 16);
    }

    function autoBalanceManual() {
      const oldB = parseFloat(document.getElementById('oldBalanceOrg').value) || 0;
      const amt = parseFloat(document.getElementById('amountKes').value) || 0;
      document.getElementById('newBalanceOrig').value = Math.max(0, oldB - amt).toFixed(2);
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
          activeThreshold = Number(data.threshold);
          const t = activeThreshold.toFixed(2);
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
        activeThreshold = Number(data.threshold);
        document.getElementById('kpiThreshold').textContent = activeThreshold.toFixed(2);
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
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:20px;">No matching transactions logged yet.</td></tr>';
        return;
      }

      tbody.innerHTML = rows.map((tx) => {
        const isFraud = Number(tx.verdict) === 1;
        const badge = isFraud
          ? '<span class="tag tag-bad">FLAGGED</span>'
          : '<span class="tag tag-ok">CLEARED</span>';
        const scoreStr = Number(tx.score || 0).toFixed(2);
        const ts = tx.timestamp ? tx.timestamp.replace('T', ' ').slice(0, 19) : '--';
        return `
          <tr>
            <td class="mono">${escapeHtml(tx.tx_id)}</td>
            <td class="mono" style="color:var(--muted);">${escapeHtml(ts)}</td>
            <td class="mono">${escapeHtml(tx.origin_account_id)}</td>
            <td>${escapeHtml(tx.vendor_hash)}</td>
            <td class="num">${formatKes(tx.amount_kes)}</td>
            <td class="num">${scoreStr}</td>
            <td>${badge}</td>
          </tr>
        `;
      }).join('');
    }

    const ACTION_LABELS = {
      ALLOW: 'Allow transaction',
      ALLOW_WITH_MONITORING: 'Allow & monitor account',
      FLAG_FOR_MANUAL_REVIEW: 'Flag for manual review / step-up verification',
      HOLD_AND_ESCALATE_SOC: 'Hold settlement & escalate to SOC analyst',
    };

    function renderVerdict(result, latencyMs) {
      const isFraud = Number(result.verdict) === 1;
      const scoreVal = Number(result.score || 0);
      const thr = Number(result.threshold ?? activeThreshold);
      const actionKey = result.recommended_action || (isFraud ? 'FLAG_FOR_MANUAL_REVIEW' : 'ALLOW');

      document.getElementById('verdictTxId').textContent = result.tx_id;
      document.getElementById('kpiLatency').textContent = `${latencyMs.toFixed(1)} ms`;
      document.getElementById('lastLatencyDetail').textContent = `${latencyMs.toFixed(1)} ms`;
      document.getElementById('scoreValue').textContent = `${scoreVal.toFixed(2)} (cutoff ${thr.toFixed(2)})`;
      document.getElementById('actionValue').textContent = ACTION_LABELS[actionKey] || actionKey;

      const box = document.getElementById('verdictBox');
      const label = document.getElementById('verdictLabel');
      const sub = document.getElementById('verdictSub');

      if (actionKey === 'HOLD_AND_ESCALATE_SOC') {
        box.className = 'verdict-box bad';
        label.textContent = 'FLAGGED — HIGH RISK (HOLD & ESCALATE)';
        sub.textContent = 'Recommended Policy: Hold settlement and route to SOC analyst for immediate review.';
      } else if (isFraud) {
        box.className = 'verdict-box warn';
        label.textContent = 'FLAGGED — SUSPICIOUS (MANUAL REVIEW)';
        sub.textContent = 'Recommended Policy: Request additional verification or queue for analyst investigation.';
      } else {
        box.className = 'verdict-box ok';
        label.textContent = 'CLEARED — LEGITIMATE';
        sub.textContent = 'Recommended Policy: Allow transaction within normal operating thresholds.';
      }

      const f = result.features || {};
      document.getElementById('velTimeSince').textContent =
        f.time_since_last_tx !== undefined && f.time_since_last_tx !== null
          ? `${Number(f.time_since_last_tx).toFixed(1)} min`
          : '--';
      document.getElementById('velCount15').textContent = f.tx_count_15min ?? 0;
      document.getElementById('velCount24').textContent = f.tx_count_24h ?? 0;

      const signals = Array.isArray(result.signals) && result.signals.length
        ? result.signals
        : ['No additional anomaly signals detected.'];
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
      renderVerdict(data, latencyMs);
      return data;
    }

    document.getElementById('txForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.disabled = true;
      btn.textContent = 'Scoring...';
      try {
        const tsVal = document.getElementById('txTimestamp').value;
        const tsNaive = tsVal ? `${tsVal}:00` : toNaiveIso(new Date());
        const oldDestRaw = document.getElementById('oldBalanceDest').value;
        const payload = {
          tx_id: makeTxId(document.getElementById('txType').value.slice(0, 4)),
          tx_type: document.getElementById('txType').value,
          origin_account_id: document.getElementById('originAccount').value.trim(),
          vendor_hash: document.getElementById('vendorHash').value.trim(),
          amount_kes: parseFloat(document.getElementById('amountKes').value),
          timestamp: tsNaive,
          oldbalance_org: parseFloat(document.getElementById('oldBalanceOrg').value),
          newbalance_orig: parseFloat(document.getElementById('newBalanceOrig').value),
          newbalance_dest: parseFloat(document.getElementById('newBalanceDest').value),
        };
        if (oldDestRaw !== '') payload.oldbalance_dest = parseFloat(oldDestRaw);
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
    renderDemoCards();
    refreshAll();
  </script>
</body>
</html>
"""
