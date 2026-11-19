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
      --link: #1d4ed8;
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

    .container { max-width: 1260px; margin: 0 auto; padding: 18px 24px 48px; }

    .context-bar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      border-radius: 4px;
      padding: 12px 16px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      flex-wrap: wrap;
    }
    .context-bar p { margin: 0; font-size: 13px; color: #374151; max-width: 850px; }
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

    /* 4-Mode Selector Cards */
    .mode-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 16px;
    }
    .mode-card {
      text-align: left;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 12px 14px;
      cursor: pointer;
      font-family: var(--sans);
    }
    .mode-card:hover { border-color: #6b7280; background: var(--subtle); }
    .mode-card.active {
      border: 2px solid var(--accent);
      background: var(--surface);
      padding: 11px 13px;
    }
    .mode-head { display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-bottom: 3px; }
    .mode-title { font-size: 13px; font-weight: 700; color: var(--text); }
    .mode-badge {
      font-size: 10px;
      font-family: var(--mono);
      text-transform: uppercase;
      padding: 1px 6px;
      border-radius: 2px;
      background: var(--subtle);
      border: 1px solid var(--border);
      color: var(--muted);
    }
    .mode-card.active .mode-badge { background: var(--accent); color: #fff; border-color: var(--accent); }
    .mode-desc { font-size: 11px; color: var(--muted); margin: 0; }

    /* Stat strip */
    .stat-strip {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      margin-bottom: 16px;
    }
    .stat-cell { padding: 12px 16px; border-right: 1px solid var(--border-soft); }
    .stat-cell:last-child { border-right: none; }
    .stat-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); margin-bottom: 2px; }
    .stat-val { font-family: var(--mono); font-size: 20px; font-weight: 600; color: var(--text); }
    .stat-val.danger { color: var(--bad-text); }
    .stat-sub { font-size: 11px; color: var(--muted); margin-top: 2px; }

    .grid {
      display: grid;
      grid-template-columns: 1.28fr 1fr;
      gap: 18px;
      margin-bottom: 18px;
    }
    @media (max-width: 960px) {
      .mode-grid { grid-template-columns: repeat(2, 1fr); }
      .stat-strip { grid-template-columns: repeat(2, 1fr); }
      .grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 580px) {
      .mode-grid { grid-template-columns: 1fr; }
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
      padding: 6px 10px;
      border-radius: 3px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
    }
    .btn:hover { background: var(--subtle); border-color: #9ca3af; }
    .btn:disabled { opacity: 0.55; cursor: not-allowed; }
    .btn-primary {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      padding: 8px 14px;
      font-weight: 600;
    }
    .btn-primary:hover { background: #1f2937; }
    .btn-danger {
      background: var(--bad-bg);
      color: var(--bad-text);
      border-color: var(--bad-border);
    }
    .btn-danger:hover { background: #fee2e2; }
    .btn-xs { padding: 2px 6px; font-size: 11px; }
    .btn-active { background: var(--accent); color: #fff; border-color: var(--accent); }

    /* Demo Mode */
    .scenario-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 14px; }
    @media (max-width: 600px) { .scenario-list { grid-template-columns: 1fr; } }
    .scenario-item {
      text-align: left;
      background: var(--subtle);
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 9px 11px;
      cursor: pointer;
      font-family: var(--sans);
    }
    .scenario-item:hover { border-color: #6b7280; }
    .scenario-item.selected { background: var(--surface); border: 2px solid var(--accent); padding: 8px 10px; }
    .scenario-top { display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 2px; }
    .scenario-name { font-size: 13px; font-weight: 600; color: var(--text); }
    .scenario-tag {
      font-size: 10px;
      font-family: var(--mono);
      padding: 1px 6px;
      border-radius: 2px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: var(--surface);
      white-space: nowrap;
    }
    .scenario-tag.risk { background: var(--bad-bg); color: var(--bad-text); border-color: var(--bad-border); }
    .scenario-tag.ok { background: var(--ok-bg); color: var(--ok-text); border-color: var(--ok-border); }
    .scenario-tag.pat { background: var(--warn-bg); color: var(--warn-text); border-color: var(--warn-border); }
    .scenario-sub { font-size: 11px; color: var(--muted); }

    .scenario-brief {
      background: var(--subtle);
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 12px;
      margin-bottom: 14px;
    }
    .scenario-brief h3 { margin: 0 0 5px; font-size: 14px; }
    .scenario-brief p { margin: 0 0 7px; font-size: 12px; color: #374151; }
    .payload-preview {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      background: var(--surface);
      border: 1px solid var(--border-soft);
      margin-top: 6px;
    }
    .payload-preview td { padding: 5px 8px; border-bottom: 1px solid var(--border-soft); }
    .payload-preview td:first-child { color: var(--muted); width: 42%; }
    .payload-preview td:last-child { font-family: var(--mono); font-weight: 500; }

    /* Guided Mode */
    .progress-head { display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; margin-bottom: 6px; }
    .progress-track { width: 100%; height: 6px; background: var(--border-soft); border-radius: 3px; overflow: hidden; margin-bottom: 14px; }
    .progress-fill { height: 100%; background: var(--accent); transition: width 0.2s ease; }
    .guided-card { border: 2px solid var(--accent); border-radius: 4px; padding: 14px; background: var(--surface); margin-bottom: 12px; }
    .guided-card h3 { margin: 0 0 4px; font-size: 15px; }
    .guided-explain { margin: 0 0 10px; font-size: 13px; color: #374151; }
    .guided-meta { background: var(--subtle); border: 1px solid var(--border-soft); border-radius: 3px; padding: 9px 11px; font-size: 12px; margin-bottom: 12px; }
    .example-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: 6px; padding-top: 6px; border-top: 1px solid var(--border-soft); flex-wrap: wrap; }
    .guided-input { width: 100%; padding: 9px 10px; font-size: 14px; font-family: var(--mono); border: 1px solid #6b7280; border-radius: 3px; background: #fff; color: var(--text); }
    .guided-hint { font-size: 11px; color: var(--muted); margin-top: 6px; }
    .guided-err { font-size: 12px; color: var(--bad-text); margin-top: 6px; font-weight: 500; display: none; }
    .guided-nav { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-top: 12px; }
    .guided-result-note { display: none; margin-top: 12px; padding: 10px 12px; border-radius: 3px; background: var(--subtle); border: 1px solid var(--border); font-size: 12px; }

    /* Manual Form */
    .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 11px; }
    @media (max-width: 600px) { .form-grid { grid-template-columns: 1fr; } }
    .field label { display: block; font-size: 11px; font-weight: 600; color: var(--muted); margin-bottom: 3px; }
    .field input, .field select { width: 100%; padding: 7px 9px; font-size: 13px; font-family: var(--mono); border: 1px solid var(--border); border-radius: 3px; background: #fff; color: var(--text); }
    .field select { font-family: var(--sans); }
    .field-help { font-size: 10px; color: var(--muted); margin-top: 2px; }
    .form-actions { margin-top: 14px; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }

    /* Benchmarks & Load Test Panel */
    .bench-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 14px; }
    .bench-box { background: var(--subtle); border: 1px solid var(--border-soft); border-radius: 3px; padding: 10px; }
    .bench-box .lbl { font-size: 11px; color: var(--muted); }
    .bench-box .val { font-family: var(--mono); font-size: 16px; font-weight: 700; margin-top: 2px; }
    .load-log {
      margin-top: 10px;
      background: #111827;
      color: #e5e7eb;
      font-family: var(--mono);
      font-size: 11px;
      padding: 10px 12px;
      border-radius: 3px;
      max-height: 150px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    /* Comparison Box (Legacy Static vs Anomaly Guard) */
    .compare-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 12px;
    }
    .cmp-card {
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 10px 11px;
      background: var(--subtle);
    }
    .cmp-card.ok { background: var(--ok-bg); border-color: var(--ok-border); color: var(--ok-text); }
    .cmp-card.warn { background: var(--warn-bg); border-color: var(--warn-border); color: var(--warn-text); }
    .cmp-card.bad { background: var(--bad-bg); border-color: var(--bad-border); color: var(--bad-text); }
    .cmp-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.04em; opacity: 0.85; font-weight: 600; }
    .cmp-val { font-family: var(--mono); font-size: 13px; font-weight: 700; margin-top: 2px; }
    .cmp-sub { font-size: 11px; margin-top: 2px; opacity: 0.9; }

    .kv-list { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 12px; }
    .kv-list td { padding: 5px 0; border-bottom: 1px solid var(--border-soft); }
    .kv-list td:first-child { color: var(--muted); }
    .kv-list td:last-child { text-align: right; font-family: var(--mono); font-weight: 600; }

    .signal-box { border-top: 1px solid var(--border-soft); padding-top: 10px; font-size: 12px; }
    .signal-box ul { margin: 6px 0 0; padding-left: 18px; color: #374151; }
    .signal-box li { margin-bottom: 4px; }

    details.api-drawer {
      margin-top: 10px;
      border: 1px solid var(--border-soft);
      border-radius: 3px;
      background: var(--subtle);
      padding: 8px 10px;
      font-size: 12px;
    }
    details.api-drawer summary { cursor: pointer; font-weight: 600; color: var(--text); }
    .code-block {
      margin: 8px 0 4px;
      background: #111827;
      color: #f3f4f6;
      padding: 9px 10px;
      border-radius: 3px;
      font-family: var(--mono);
      font-size: 11px;
      overflow-x: auto;
      white-space: pre;
    }

    /* SOC Admin Box */
    .admin-box {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--border-soft);
      font-size: 12px;
    }
    .admin-row {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 6px;
    }
    .admin-row input[type="range"] { flex: 1; min-width: 90px; }
    .pin-input {
      width: 92px;
      padding: 5px 7px;
      font-family: var(--mono);
      font-size: 12px;
      border: 1px solid var(--border);
      border-radius: 3px;
    }

    /* Account Investigation Drawer */
    .acct-drawer {
      display: none;
      margin-bottom: 16px;
      background: var(--surface);
      border: 2px solid var(--accent);
      border-radius: 4px;
      padding: 14px 16px;
    }
    .acct-stats { display: flex; gap: 18px; flex-wrap: wrap; margin: 10px 0; font-size: 12px; }

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
      padding: 9px 10px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      color: var(--muted);
      background: var(--subtle);
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    table.ledger td { padding: 7px 10px; border-bottom: 1px solid var(--border-soft); white-space: nowrap; }
    table.ledger tr:hover td { background: var(--subtle); }
    .num { text-align: right; font-family: var(--mono); }
    .acct-link {
      background: none;
      border: none;
      padding: 0;
      color: var(--link);
      font-family: var(--mono);
      font-size: 12px;
      cursor: pointer;
      text-decoration: underline;
    }
    .tag {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 2px;
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 600;
    }
    .tag-ok { background: var(--ok-bg); color: var(--ok-text); border: 1px solid var(--ok-border); }
    .tag-warn { background: var(--warn-bg); color: var(--warn-text); border: 1px solid var(--warn-border); }
    .tag-bad { background: var(--bad-bg); color: var(--bad-text); border: 1px solid var(--bad-border); }
    .hidden { display: none !important; }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <h1>Anomaly Guard</h1>
      <span>B2B Mobile Money Fraud Screening Console (PaySim-KES v2.0)</span>
    </div>
    <div class="top-meta">
      <span id="healthText" class="mono">status: checking...</span>
      <span>2-Table SQLite ERD &middot; DPA 2019 Synthetic Telemetry</span>
      <a href="/docs" target="_blank">OpenAPI /docs</a>
    </div>
  </header>

  <main class="container">
    <!-- B2B Framing Banner -->
    <section class="context-bar">
      <p>
        <strong>How this works:</strong> Anomaly Guard is a B2B risk-scoring API for Kenyan SACCOs, micro-lenders, and fintechs. In production, a core payment switch streams transaction JSON to <span class="mono">POST /score</span> before settlement; this console lets assessors run live Kenyan fraud scenarios, learn the input schema step by step, inspect raw B2B API contracts, and load-test latency against the 1,500 ms SLA.
      </p>
      <div class="context-pills">
        <span class="pill">Hybrid ML + Policy Engine</span>
        <span class="pill">Sender Velocity + Mule Fan-In</span>
        <span class="pill">Static Rule Benchmark</span>
      </div>
    </section>

    <!-- 4 Immediately Visible Modes -->
    <section class="mode-grid" aria-label="Workspace modes">
      <button type="button" id="tabDemo" class="mode-card active" onclick="switchMode('demo')">
        <div class="mode-head">
          <span class="mode-title">Demo Mode</span>
          <span class="mode-badge">Explore</span>
        </div>
        <p class="mode-desc">6 Kenyan scenarios (SIM-swap, mule transfer, smurfing, syndicate fan-in) scored live by the backend.</p>
      </button>

      <button type="button" id="tabGuided" class="mode-card" onclick="switchMode('guided')">
        <div class="mode-head">
          <span class="mode-title">Guided Mode</span>
          <span class="mode-badge">Learn</span>
        </div>
        <p class="mode-desc">Step-by-step onboarding across all 8 input fields with plain-English definitions and ledger math checks.</p>
      </button>

      <button type="button" id="tabManual" class="mode-card" onclick="switchMode('manual')">
        <div class="mode-head">
          <span class="mode-title">Manual Mode</span>
          <span class="mode-badge">Developer</span>
        </div>
        <p class="mode-desc">Direct payload form for testing custom amounts, ghost hours, and sender/receiver balance tampering.</p>
      </button>

      <button type="button" id="tabBench" class="mode-card" onclick="switchMode('bench')">
        <div class="mode-head">
          <span class="mode-title">SLA &amp; Benchmarks</span>
          <span class="mode-badge">Verify</span>
        </div>
        <p class="mode-desc">Live 20-request concurrent load test, p95 latency telemetry, and ML vs. Static Rule evaluation metrics.</p>
      </button>
    </section>

    <!-- KPI Strip -->
    <section class="stat-strip">
      <div class="stat-cell">
        <div class="stat-label">Transactions Scored</div>
        <div id="kpiTotal" class="stat-val">0</div>
        <div id="kpiPending" class="stat-sub">0 pending SOC review</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Flagged Suspicious</div>
        <div id="kpiFlagged" class="stat-val danger">0</div>
        <div id="kpiStaticGain" class="stat-sub">0 caught that static rules missed</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Avg / p95 Latency</div>
        <div id="kpiLatency" class="stat-val">--</div>
        <div id="kpiSla" class="stat-sub">100% within 1,500 ms SLA</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">SOC Risk Cutoff</div>
        <div id="kpiThreshold" class="stat-val">0.80</div>
        <div id="kpiModel" class="stat-sub">Checking model...</div>
      </div>
    </section>

    <div id="errBanner" class="err-banner"></div>

    <!-- Main Two-Column Workspace -->
    <section class="grid">
      <!-- Left Panel -->
      <div class="panel">
        <!-- 1. DEMO MODE -->
        <div id="panelDemo">
          <div class="panel-head">
            <h2>Demo Mode — Live Kenyan Fraud Scenarios</h2>
            <span class="mono" style="font-size:11px;color:var(--muted);">Real Scoring via POST /score</span>
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
              <span style="font-size:11px;color:var(--muted);">Dispatches synthetic PaySim-KES payloads to live API.</span>
              <div style="display:flex;gap:8px;">
                <button type="button" class="btn" onclick="copyScenarioToManual()">Edit in Manual</button>
                <button type="button" id="runDemoBtn" class="btn btn-primary" onclick="runSelectedScenario()">Run Scenario Live</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. GUIDED MODE -->
        <div id="panelGuided" class="hidden">
          <div class="panel-head">
            <h2>Guided Mode — Step-by-Step Walkthrough</h2>
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
                <div><strong>Production data source:</strong> <span id="guidedFieldSource"></span></div>
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
              <h3>Review Synthetic Transaction Before Scoring</h3>
              <p>Confirm the inputs below, then submit to <span class="mono">POST /score</span> to inspect the live verdict and static-rule comparison.</p>
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
            <h2>Manual Mode — Analyst &amp; Developer Form</h2>
            <span class="mono" style="font-size:11px;color:var(--muted);">POST /score</span>
          </div>
          <div class="panel-body">
            <p style="margin:0 0 12px;font-size:12px;color:var(--muted);">
              Submit custom payloads directly. Test ledger tampering by setting Sender New Balance to a value other than <span class="mono">Old Balance - Amount</span>.
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
                </div>
                <div class="field">
                  <label for="amountKes">Amount (KES)</label>
                  <input id="amountKes" type="number" step="0.01" min="0" value="1200.00" required />
                </div>
                <div class="field">
                  <label for="originAccount">Origin Account ID (Pseudonymised)</label>
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
                  <label for="oldBalanceDest">Receiver Old Balance (KES, optional)</label>
                  <input id="oldBalanceDest" type="number" step="0.01" min="0" placeholder="Optional" />
                </div>
                <div class="field">
                  <label for="newBalanceDest">Receiver New Balance (KES)</label>
                  <input id="newBalanceDest" type="number" step="0.01" min="0" value="48200.00" required />
                </div>
                <div class="field" style="grid-column: 1 / -1;">
                  <label for="txTimestamp">Transaction Timestamp (Local)</label>
                  <input id="txTimestamp" type="datetime-local" />
                </div>
              </div>
              <div class="form-actions">
                <button type="button" class="btn" onclick="autoBalanceManual()">Auto-Calculate Consistent New Balance</button>
                <button type="submit" id="submitBtn" class="btn btn-primary">Score Transaction</button>
              </div>
            </form>
          </div>
        </div>

        <!-- 4. BENCHMARKS & CONCURRENT LOAD TEST -->
        <div id="panelBench" class="hidden">
          <div class="panel-head">
            <h2>Performance SLA &amp; Model Benchmarks</h2>
            <button type="button" id="loadTestBtn" class="btn btn-primary" onclick="runConcurrentLoadTest()">Run 20-Request Concurrent Load Test</button>
          </div>
          <div class="panel-body">
            <div class="bench-grid">
              <div class="bench-box">
                <div class="lbl">Avg Server Latency</div>
                <div id="benchAvgLat" class="val">--</div>
              </div>
              <div class="bench-box">
                <div class="lbl">p95 Latency (Target &le; 1500ms)</div>
                <div id="benchP95Lat" class="val">--</div>
              </div>
              <div class="bench-box">
                <div class="lbl">Max Recorded Latency</div>
                <div id="benchMaxLat" class="val">--</div>
              </div>
            </div>

            <div class="scenario-brief">
              <h3>Offline Model Validation Benchmark (PaySim-KES)</h3>
              <div id="metricsContainer" style="font-size:12px;color:var(--muted);">Loading validation metrics...</div>
            </div>

            <div>
              <strong style="font-size:12px;">Concurrent Async Load Test Output (NFR-01 &amp; NFR-02 Verification)</strong>
              <div id="loadTestLog" class="load-log">Click "Run 20-Request Concurrent Load Test" to dispatch 20 parallel HTTP POST requests against FastAPI and measure wall-clock &amp; per-request latency.</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: Explain This Transaction + B2B JSON + Authenticated SOC Controls -->
      <div class="panel">
        <div class="panel-head">
          <h2>Explain This Transaction</h2>
          <span id="verdictTxId" class="mono" style="font-size:11px;color:var(--muted);">Awaiting run</span>
        </div>
        <div class="panel-body">
          <!-- Side-by-Side Legacy Static Rule vs Anomaly Guard -->
          <div class="compare-grid">
            <div id="cmpGuardBox" class="cmp-card">
              <div class="cmp-label">Anomaly Guard (Hybrid Engine)</div>
              <div id="cmpGuardVal" class="cmp-val">AWAITING INPUT</div>
              <div id="cmpGuardSub" class="cmp-sub">ML + velocity + ledger integrity</div>
            </div>
            <div id="cmpStaticBox" class="cmp-card">
              <div class="cmp-label">Legacy Static Rule (&gt; KES 50k)</div>
              <div id="cmpStaticVal" class="cmp-val">--</div>
              <div id="cmpStaticSub" class="cmp-sub">Single-tx Boolean threshold</div>
            </div>
          </div>

          <!-- Transparent Score Breakdown -->
          <table class="kv-list">
            <tr>
              <td>Combined Risk Score / Cutoff</td>
              <td id="scoreValue">--</td>
            </tr>
            <tr>
              <td>ML Model Score vs. Policy Guardrail</td>
              <td id="scoreSplit">--</td>
            </tr>
            <tr>
              <td>Recommended Policy Action</td>
              <td id="actionValue">--</td>
            </tr>
            <tr>
              <td>Server Inference Latency</td>
              <td id="lastLatencyDetail">--</td>
            </tr>
            <tr>
              <td>Sender Velocity (15m / 24h / Gap)</td>
              <td id="velSummary">--</td>
            </tr>
            <tr>
              <td>Recipient Fan-In (Other Senders 15m)</td>
              <td id="fanInSummary">--</td>
            </tr>
          </table>

          <div class="signal-box">
            <strong>Detected Signals &amp; Reasoning</strong>
            <ul id="signalList">
              <li>Run a scenario or custom transaction to inspect detected risk signals.</li>
            </ul>
          </div>

          <!-- Collapsible B2B API Inspector -->
          <details class="api-drawer">
            <summary>B2B Integration Inspector (Raw JSON &amp; cURL Contract)</summary>
            <div style="margin-top:8px;font-size:11px;color:var(--muted);">
              Shows how a SACCO or payment gateway calls <span class="mono">POST /score</span> programmatically:
            </div>
            <div id="rawRequestBlock" class="code-block">Run any transaction to inspect the exact JSON request and response.</div>
            <div id="rawResponseBlock" class="code-block" style="display:none;"></div>
            <button type="button" class="btn btn-xs" onclick="copyCurl()">Copy cURL Command</button>
          </details>

          <!-- Authenticated SOC Admin Controls (UC-2) -->
          <div class="admin-box">
            <strong>SOC Administrator Controls (UC-2 &middot; Persisted in SQLite)</strong>
            <div class="admin-row">
              <label for="thresholdSlider">Cutoff: <span id="thresholdReadout" class="mono">0.80</span></label>
              <input id="thresholdSlider" type="range" min="0.10" max="0.90" step="0.05" value="0.80" />
            </div>
            <div class="admin-row">
              <input id="adminPin" type="password" class="pin-input" placeholder="Admin PIN" value="2026" title="Prototype SOC Admin PIN (default: 2026)" />
              <button type="button" class="btn" onclick="applyThreshold()">Apply Cutoff</button>
              <button type="button" class="btn btn-danger" onclick="clearAuditLogs()">Reset Demo Logs</button>
            </div>
            <div id="adminMsg" style="font-size:11px;color:var(--muted);margin-top:5px;">
              Requires SOC Admin PIN (prototype default: <span class="mono">2026</span>) via <span class="mono">X-Admin-Token</span>.
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Click-to-Investigate Account Drawer -->
    <section id="accountDrawer" class="acct-drawer">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
        <div>
          <strong style="font-size:14px;">Account Investigation Timeline: <span id="acctDrawerId" class="mono"></span></strong>
          <span style="font-size:11px;color:var(--muted);margin-left:8px;">Queried live from SQLite via GET /accounts/{id}</span>
        </div>
        <button type="button" class="btn btn-xs" onclick="closeAccountDrawer()">Close</button>
      </div>
      <div id="acctDrawerStats" class="acct-stats"></div>
      <div class="table-wrap">
        <table class="ledger">
          <thead>
            <tr>
              <th>Tx ID</th>
              <th>Role</th>
              <th>Counterparty</th>
              <th>Type</th>
              <th class="num">Amount (KES)</th>
              <th class="num">Score</th>
              <th>Verdict</th>
              <th>Case Status</th>
            </tr>
          </thead>
          <tbody id="acctDrawerBody"></tbody>
        </table>
      </div>
    </section>

    <!-- Live SQLite Audit Log + Case Management -->
    <section class="panel">
      <div class="panel-head">
        <h2>SQLite Inference Audit Log &amp; Case Disposition</h2>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          <button type="button" id="filterAllBtn" class="btn btn-active" onclick="setFilter('all')">All</button>
          <button type="button" id="filterFlaggedBtn" class="btn" onclick="setFilter('flagged')">Flagged Only</button>
          <button type="button" id="filterStaticMissBtn" class="btn" onclick="setFilter('static_miss')">Static Rule Missed</button>
          <a href="/export/csv" class="btn">Export CSV</a>
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
              <th class="num">Score (ML/Pol)</th>
              <th>Verdict</th>
              <th>Static Rule</th>
              <th>Analyst Disposition</th>
            </tr>
          </thead>
          <tbody id="txTableBody">
            <tr><td colspan="9" style="text-align:center;color:var(--muted);padding:20px;">Loading records...</td></tr>
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
    let lastRawRequest = null;

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
      ['demo', 'guided', 'manual', 'bench'].forEach((m) => {
        const cap = m.charAt(0).toUpperCase() + m.slice(1);
        document.getElementById(`tab${cap}`).classList.toggle('active', m === mode);
        document.getElementById(`panel${cap}`).classList.toggle('hidden', m !== mode);
      });
      if (mode === 'guided') renderGuidedStep();
      if (mode === 'bench') loadModelMetrics();
    }

    // ---------------- DEMO MODE (6 KENYAN SCENARIOS) ----------------
    const SCENARIOS = {
      normal: {
        name: 'Normal M-Pesa Payment',
        tag: 'Legitimate',
        tagClass: 'ok',
        short: 'KES 250.50 — Everyday Naivas till payment.',
        desc: 'Simulates an ordinary Lipa na M-Pesa payment during daytime hours. Sender and receiver balances reconcile cleanly with normal account velocity.',
        source: 'Baseline legitimate traffic — should clear under both Anomaly Guard and static thresholds.',
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
          ['Sender Balance', 'KES 12,500.00 → KES 12,249.50 (reconciled)'],
          ['Expected Static Rule', 'CLEARED (below KES 50,000)'],
        ],
      },
      sim_swap: {
        name: 'SIM-Swap Ghost-Hour Drain',
        tag: 'High Risk',
        tagClass: 'risk',
        short: 'KES 185,000 — 02:30 AM agent cash-out wiping wallet.',
        desc: 'Simulates a SIM-swap takeover emptying the victim\'s entire KES 185,000 balance to KES 0.00 via an agent withdrawal at 2:30 AM.',
        source: 'Combines ghost-hour timestamp, high value, and 100% balance drain prior to cash settlement.',
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
          ['Sender Balance', 'KES 185,000.00 → KES 0.00 (100% drain)'],
          ['Time Window', '02:30 AM (ghost hour)'],
        ],
      },
      high_value: {
        name: 'Mule Account Sweep',
        tag: 'High Risk',
        tagClass: 'risk',
        short: 'KES 540,000 — Full-balance P2P sweep at 03:15 AM.',
        desc: 'Simulates an illicit KES 540,000 transfer sweeping an account into a mule wallet at 03:15 AM with zero destination balance reconciliation.',
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
          ['Sender Balance', 'KES 540,000.00 → KES 0.00 (full sweep)'],
          ['Time Window', '03:15 AM (ghost hour)'],
        ],
      },
      smurfing: {
        name: 'Smurfing Burst (6× KES 900)',
        tag: 'Beats Static',
        tagClass: 'pat',
        short: '6 rapid KES 900 transfers bypassing KES 50k rules.',
        desc: 'Classic structuring attack: an attacker splits a transfer into six KES 900 bursts 15 seconds apart so every transaction stays far below the KES 50,000 static limit. Anomaly Guard catches it via 15-minute SQLite velocity.',
        source: 'Directly contrasts Legacy Static Rule (MISSED) vs. Anomaly Guard (CAUGHT).',
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
          ['Amount per Tx', 'KES 900.00 (Static Rule: MISSED)'],
          ['Key Signal', 'Sender Tx Count (15 min) climbs 0 → 5'],
          ['Anomaly Guard', 'Flags burst once velocity spikes'],
        ],
      },
      syndicate_fanin: {
        name: 'Mule-Ring Fan-In Syndicate',
        tag: 'Syndicate',
        tagClass: 'risk',
        short: '3 distinct victim accounts draining into 1 mule wallet.',
        desc: 'Simulates an organized fraud syndicate: three separate compromised accounts each send KES 18,000 (below the KES 50k static rule) into the exact same collector wallet within 3 minutes. Anomaly Guard detects recipient fan-in.',
        source: 'Addresses Section 2.2.4 organized syndicate fraud — click the mule wallet in the log to inspect all 3 senders.',
        buildPayloads: () => {
          const now = new Date();
          const muleWallet = `MULE_RING_${Math.floor(100 + Math.random() * 900)}`;
          const victims = [
            `KE_VICTIM_${Math.floor(1000 + Math.random() * 8999)}`,
            `KE_VICTIM_${Math.floor(1000 + Math.random() * 8999)}`,
            `KE_VICTIM_${Math.floor(1000 + Math.random() * 8999)}`,
          ];
          return victims.map((v, i) => ({
            tx_id: makeTxId(`RING${i + 1}`),
            tx_type: 'TRANSFER',
            origin_account_id: v,
            vendor_hash: muleWallet,
            amount_kes: 18000.00,
            timestamp: toNaiveIso(new Date(now.getTime() + i * 45000)),
            oldbalance_org: 26000.00,
            newbalance_orig: 8000.00,
            newbalance_dest: 18000.00 * (i + 1),
          }));
        },
        preview: [
          ['Pattern', '3 distinct senders → 1 shared mule wallet in 3 mins'],
          ['Amount per Tx', 'KES 18,000.00 (Static Rule: MISSED)'],
          ['Key Signal', 'Recipient Fan-In (Other Senders 15m ≥ 2)'],
          ['Investigation', 'Click mule wallet ID in audit log to view cluster'],
        ],
      },
      mixed: {
        name: 'Mixed Kenyan Traffic Stream',
        tag: 'Batch (8 Tx)',
        tagClass: 'pat',
        short: '8 transactions mixing legitimate retail & fraud attacks.',
        desc: 'Streams 6 normal Kenyan transactions (Carrefour, KPLC Paybill, Airtel P2P, Java House, Quickmart) alongside a 2:13 AM SIM-swap drain and a 3:16 AM mule transfer.',
        source: 'Simulates realistic multi-account production traffic across a SACCO gateway.',
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
          ['Stream Mix', '6 legitimate retail/P2P + 2 ghost-hour fraud attacks'],
          ['Audit Output', 'Persisted to Parsed_Transactions & ML_Inference_Log'],
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
      const first = SCENARIOS[selectedScenarioKey].buildPayloads()[0];
      fillManualForm(first);
      switchMode('manual');
    }

    async function runSelectedScenario() {
      const btn = document.getElementById('runDemoBtn');
      const payloads = SCENARIOS[selectedScenarioKey].buildPayloads();
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
        btn.textContent = 'Run Scenario Live';
      }
    }

    // ---------------- GUIDED MODE ----------------
    const GUIDED_STEPS = [
      {
        key: 'tx_type',
        title: 'Channel / Transaction Type',
        desc: 'Select how the money moves across the mobile money rail.',
        source: 'Provided automatically by the payment switch (Till payment, P2P Send Money, or Agent Cash-Out).',
        exampleLabel: 'Lipa na M-Pesa / Till (PAYMENT)',
        exampleValue: 'PAYMENT',
        type: 'select',
        options: [
          ['PAYMENT', 'Lipa na M-Pesa / Till (PAYMENT)'],
          ['TRANSFER', 'Send Money P2P (TRANSFER)'],
          ['CASH_OUT', 'Agent Withdrawal (CASH_OUT)'],
        ],
        validate: (v) => v ? '' : 'Choose a transaction type.',
      },
      {
        key: 'amount_kes',
        title: 'Transaction Amount (KES)',
        desc: 'Value of the transfer in Kenya Shillings.',
        source: 'Captured directly from the switch transaction payload before settlement.',
        exampleLabel: 'KES 1,200.00',
        exampleValue: '1200.00',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) > 0) ? '' : 'Enter an amount greater than 0 KES.',
      },
      {
        key: 'origin_account_id',
        title: 'Origin Account ID (Pseudonymised)',
        desc: 'Sender identifier used by Anomaly Guard to compute 15-minute and 24-hour account velocity.',
        source: 'In production, a pseudonymised ledger account token — no raw personal data is processed in this prototype.',
        exampleLabel: 'KE_ACC_254712345678',
        exampleValue: 'KE_ACC_254712345678',
        type: 'text',
        validate: (v) => String(v || '').trim().length >= 3 ? '' : 'Enter at least 3 characters.',
      },
      {
        key: 'vendor_hash',
        title: 'Recipient / Till / Agent ID',
        desc: 'Destination merchant till, agent float, or receiving wallet. Also tracked for multi-sender mule-ring fan-in.',
        source: 'Populated automatically from destination till, paybill, or wallet token.',
        exampleLabel: 'TILL_NAIVAS_4021',
        exampleValue: 'TILL_NAIVAS_4021',
        type: 'text',
        validate: (v) => String(v || '').trim().length >= 3 ? '' : 'Enter at least 3 characters.',
      },
      {
        key: 'oldbalance_org',
        title: 'Sender Old Balance (KES)',
        desc: 'Sender account balance immediately before this transaction.',
        source: 'Read from the institution\'s core ledger prior to debit.',
        exampleLabel: 'KES 15,000.00',
        exampleValue: '15000.00',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) >= 0) ? '' : 'Enter a valid non-negative balance.',
      },
      {
        key: 'newbalance_orig',
        title: 'Sender New Balance (KES)',
        desc: 'Sender balance after debit. Anomaly Guard checks whether Old Balance - Amount equals New Balance and flags account drains or tampering.',
        source: 'Computed by the core ledger post-debit.',
        exampleLabel: 'Consistent: Old - Amount',
        exampleValue: '__CALC_NEW_ORIG__',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) >= 0) ? '' : 'Enter a valid non-negative balance.',
      },
      {
        key: 'newbalance_dest',
        title: 'Receiver New Balance (KES)',
        desc: 'Recipient\'s recorded balance after receiving the transfer.',
        source: 'Recorded from the destination account ledger (0 for unpopulated merchant accounts or mule wallets in PaySim).',
        exampleLabel: 'KES 48,200.00',
        exampleValue: '48200.00',
        type: 'number',
        validate: (v) => (v !== '' && !isNaN(Number(v)) && Number(v) >= 0) ? '' : 'Enter a valid non-negative balance.',
      },
      {
        key: 'timestamp',
        title: 'Transaction Timestamp',
        desc: 'Timestamp used for ghost-hour detection (00:00–04:59) and rolling 15m / 24h velocity windows.',
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
      if (step.exampleValue === '__NOW__') return toLocalInputValue(new Date());
      return step.exampleValue;
    }

    function renderGuidedStep() {
      const total = GUIDED_STEPS.length;
      const isReview = guidedStepIdx >= total;
      const pct = isReview ? 100 : Math.round(((guidedStepIdx + 1) / total) * 100);

      document.getElementById('guidedStepLabel').textContent = isReview ? 'Review & Submit' : `Step ${guidedStepIdx + 1} of ${total}`;
      document.getElementById('guidedPctLabel').textContent = `${pct}% complete`;
      document.getElementById('guidedProgressFill').style.width = `${pct}%`;

      const stepCard = document.getElementById('guidedStepCard');
      const summaryBox = document.getElementById('guidedSummaryBox');
      document.getElementById('guidedPrevBtn').disabled = guidedStepIdx === 0;
      const nextBtn = document.getElementById('guidedNextBtn');

      if (isReview) {
        stepCard.classList.add('hidden');
        summaryBox.classList.remove('hidden');
        nextBtn.textContent = 'Submit & Score Transaction';
        const oldB = parseFloat(guidedState.oldbalance_org);
        const amt = parseFloat(guidedState.amount_kes);
        const newB = parseFloat(guidedState.newbalance_orig);
        const expected = oldB - amt;
        const mathStatus = Math.abs(expected - newB) <= 1.0 ? 'Reconciled cleanly' : `Mismatch (expected KES ${formatKes(expected)})`;
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
        mathEl.textContent = `Ledger math check: KES ${formatKes(oldB)} − KES ${formatKes(amt)} = KES ${formatKes(oldB - amt)}. Entering a different value tests ledger tampering detection.`;
      } else {
        mathEl.textContent = '';
      }
      document.getElementById('guidedError').style.display = 'none';
    }

    function fillGuidedExample() {
      const step = GUIDED_STEPS[guidedStepIdx];
      const ex = getGuidedExampleValue(step);
      guidedState[step.key] = ex;
      const inp = document.getElementById('guidedActiveInput');
      if (inp) inp.value = ex;
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
        note.innerHTML = `<strong>Result breakdown:</strong> Score <span class="mono">${Number(result.score).toFixed(2)}</span> vs cutoff <span class="mono">${Number(result.threshold).toFixed(2)}</span> &rarr; <strong>${isFlag ? 'FLAGGED' : 'CLEARED'}</strong> (Source: <span class="mono">${escapeHtml(result.scoring_source)}</span>). Inspect the comparison and raw API JSON on the right.`;
        note.style.display = 'block';
      } catch (err) {
        showError(`Guided scoring failed: ${err.message}`);
      } finally {
        nextBtn.disabled = false;
        nextBtn.textContent = 'Submit & Score Transaction';
      }
    }

    // ---------------- BENCHMARKS & CONCURRENT LOAD TEST ----------------
    async function loadModelMetrics() {
      const container = document.getElementById('metricsContainer');
      try {
        const res = await fetch('/metrics');
        const data = await res.json();
        if (!data.available || !Array.isArray(data.models)) {
          container.innerHTML = `Active model: <span class="mono">${escapeHtml(data.active_model || 'XGBClassifier')}</span> (cutoff <span class="mono">${Number(data.threshold || activeThreshold).toFixed(2)}</span>). Run <span class="mono">python evaluate_benchmarks.py</span> to populate offline PaySim F1/Precision/Recall comparison.`;
          return;
        }
        const rows = data.models.map((m) => `
          <tr>
            <td><strong>${escapeHtml(m.name)}</strong></td>
            <td class="num">${Number(m.f1).toFixed(4)}</td>
            <td class="num">${Number(m.precision).toFixed(4)}</td>
            <td class="num">${Number(m.recall).toFixed(4)}</td>
            <td class="num">${Number(m.fpr * 100).toFixed(3)}%</td>
          </tr>
        `).join('');
        container.innerHTML = `
          <div style="margin-bottom:6px;font-size:11px;color:var(--muted);">
            Evaluated on <span class="mono">${Number(data.eval_samples || 0).toLocaleString()}</span> PaySim-KES validation records (${Number(data.fraud_samples || 0).toLocaleString()} fraud cases):
          </div>
          <table class="ledger" style="background:#fff;border:1px solid var(--border-soft);">
            <thead>
              <tr><th>Model / Baseline</th><th class="num">F1-Score</th><th class="num">Precision</th><th class="num">Recall</th><th class="num">FPR</th></tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        `;
      } catch (err) {
        container.textContent = `Could not load metrics: ${err.message}`;
      }
    }

    async function runConcurrentLoadTest() {
      const btn = document.getElementById('loadTestBtn');
      const log = document.getElementById('loadTestLog');
      btn.disabled = true;
      btn.textContent = 'Running 20 parallel requests...';
      log.textContent = 'Dispatching 20 concurrent POST /score requests via Promise.all()...\n';
      const now = new Date();
      const tWallStart = performance.now();

      const tasks = Array.from({ length: 20 }, (_, i) => {
        const isAttack = i % 5 === 0;
        const payload = isAttack ? {
          tx_id: makeTxId(`LOADF${i}`),
          tx_type: 'CASH_OUT',
          origin_account_id: `KE_LOAD_F_${i}`,
          vendor_hash: 'AGENT_LOAD_99',
          amount_kes: 190000.00,
          timestamp: toNaiveIso(new Date(now.getFullYear(), now.getMonth(), now.getDate(), 2, 10 + i, 0)),
          oldbalance_org: 190000.00,
          newbalance_orig: 0.00,
          newbalance_dest: 0.00,
        } : {
          tx_id: makeTxId(`LOADN${i}`),
          tx_type: 'PAYMENT',
          origin_account_id: `KE_LOAD_N_${i}`,
          vendor_hash: 'TILL_LOAD_100',
          amount_kes: 450.00 + i * 25,
          timestamp: toNaiveIso(new Date(now.getTime() + i * 1000)),
          oldbalance_org: 15000.00,
          newbalance_orig: 15000.00 - (450.00 + i * 25),
          newbalance_dest: 40000.00,
        };
        const t0 = performance.now();
        return fetch('/score', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }).then(async (r) => {
          const clientMs = performance.now() - t0;
          const body = await r.json();
          return { ok: r.ok, clientMs, serverMs: body.latency_ms || 0, verdict: body.verdict, txId: payload.tx_id };
        });
      });

      try {
        const results = await Promise.all(tasks);
        const wallMs = performance.now() - tWallStart;
        const okCount = results.filter((r) => r.ok).length;
        const flaggedCount = results.filter((r) => r.verdict === 1).length;
        const clientLats = results.map((r) => r.clientMs).sort((a, b) => a - b);
        const serverLats = results.map((r) => r.serverMs).sort((a, b) => a - b);
        const avgClient = clientLats.reduce((a, b) => a + b, 0) / clientLats.length;
        const p95Client = clientLats[Math.floor(clientLats.length * 0.95)];
        const maxClient = clientLats[clientLats.length - 1];
        const avgServer = serverLats.reduce((a, b) => a + b, 0) / serverLats.length;
        const slaPass = maxClient <= 1500.0 ? 'PASS (<= 1,500 ms SLA)' : 'OVER 1,500 ms SLA';

        log.textContent += [
          `Completed: ${okCount}/20 HTTP 200 OK | Flagged: ${flaggedCount}/20`,
          `Total Wall Time (20 parallel): ${wallMs.toFixed(1)} ms (${(20000 / wallMs).toFixed(1)} req/sec)`,
          `Client Round-Trip -> Avg: ${avgClient.toFixed(1)} ms | p95: ${p95Client.toFixed(1)} ms | Max: ${maxClient.toFixed(1)} ms`,
          `Server Inference  -> Avg: ${avgServer.toFixed(2)} ms`,
          `NFR-01 SLA Check  -> ${slaPass}`,
        ].join('\n');
        await refreshAll();
      } catch (err) {
        log.textContent += `\nLoad test error: ${err.message}`;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Run 20-Request Concurrent Load Test';
      }
    }

    // ---------------- CORE API & RENDERING ----------------
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
      document.getElementById('filterStaticMissBtn').className = mode === 'static_miss' ? 'btn btn-active' : 'btn';
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
      const pin = document.getElementById('adminPin').value.trim();
      const msgEl = document.getElementById('adminMsg');
      try {
        const res = await fetch('/settings/threshold', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Token': pin },
          body: JSON.stringify({ threshold: val }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
        activeThreshold = Number(data.threshold);
        document.getElementById('kpiThreshold').textContent = activeThreshold.toFixed(2);
        msgEl.style.color = 'var(--ok-text)';
        msgEl.textContent = `Authenticated — SOC cutoff updated & persisted to ${activeThreshold.toFixed(2)}.`;
      } catch (err) {
        msgEl.style.color = 'var(--bad-text)';
        msgEl.textContent = err.message;
      }
    }

    async function clearAuditLogs() {
      showError('');
      const pin = document.getElementById('adminPin').value.trim();
      const msgEl = document.getElementById('adminMsg');
      if (!confirm('Clear all demo transactions from the SQLite audit log?')) return;
      try {
        const res = await fetch('/admin/logs', {
          method: 'DELETE',
          headers: { 'X-Admin-Token': pin },
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
        closeAccountDrawer();
        await refreshAll();
        msgEl.style.color = 'var(--ok-text)';
        msgEl.textContent = 'SQLite audit log cleared cleanly.';
      } catch (err) {
        msgEl.style.color = 'var(--bad-text)';
        msgEl.textContent = err.message;
      }
    }

    document.getElementById('thresholdSlider').addEventListener('input', (e) => {
      document.getElementById('thresholdReadout').textContent = Number(e.target.value).toFixed(2);
    });

    async function refreshStats() {
      const res = await fetch('/stats');
      const data = await res.json();
      document.getElementById('kpiTotal').textContent = data.total_scored ?? 0;
      document.getElementById('kpiPending').textContent = `${data.pending_review ?? 0} flagged pending review`;
      document.getElementById('kpiFlagged').textContent = data.flagged_fraud ?? 0;
      document.getElementById('kpiStaticGain').textContent =
        `${data.caught_missed_by_static ?? 0} caught that static rules missed`;

      const avg = Number(data.avg_latency_ms || 0);
      const p95 = Number(data.p95_latency_ms || 0);
      const maxL = Number(data.max_latency_ms || 0);
      document.getElementById('kpiLatency').textContent = data.total_scored ? `${avg.toFixed(1)} / ${p95.toFixed(1)} ms` : '--';
      document.getElementById('kpiSla').textContent = `${Number(data.sla_compliance_pct ?? 100).toFixed(1)}% within 1,500 ms SLA`;

      document.getElementById('benchAvgLat').textContent = `${avg.toFixed(2)} ms`;
      document.getElementById('benchP95Lat').textContent = `${p95.toFixed(2)} ms`;
      document.getElementById('benchMaxLat').textContent = `${maxL.toFixed(2)} ms`;
    }

    async function refreshTransactions() {
      const res = await fetch('/transactions?limit=50');
      const data = await res.json();
      cachedTransactions = data.transactions || [];
      renderTable();
    }

    async function setDisposition(txId, status) {
      try {
        const res = await fetch(`/logs/${encodeURIComponent(txId)}/disposition`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ review_status: status }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        await refreshAll();
        const drawerId = document.getElementById('acctDrawerId').textContent;
        if (document.getElementById('accountDrawer').style.display === 'block' && drawerId) {
          await openAccountDrawer(drawerId);
        }
      } catch (err) {
        showError(`Disposition update failed: ${err.message}`);
      }
    }

    async function openAccountDrawer(accountId) {
      try {
        const res = await fetch(`/accounts/${encodeURIComponent(accountId)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        document.getElementById('acctDrawerId').textContent = data.account_id;
        document.getElementById('acctDrawerStats').innerHTML = [
          `<span><strong>Total Tx:</strong> <span class="mono">${data.total_transactions}</span></span>`,
          `<span><strong>Flagged:</strong> <span class="mono" style="color:var(--bad-text);">${data.flagged_count}</span></span>`,
          `<span><strong>Outbound:</strong> <span class="mono">KES ${formatKes(data.total_outbound_kes)}</span></span>`,
          `<span><strong>Inbound:</strong> <span class="mono">KES ${formatKes(data.total_inbound_kes)}</span></span>`,
          `<span><strong>Unique Counterparties:</strong> <span class="mono">${data.unique_counterparties}</span></span>`,
        ].join('');

        document.getElementById('acctDrawerBody').innerHTML = data.transactions.map((t) => `
          <tr>
            <td class="mono">${escapeHtml(t.tx_id)}</td>
            <td class="mono">${escapeHtml(t.role)}</td>
            <td><button type="button" class="acct-link" onclick="openAccountDrawer('${escapeHtml(t.counterparty)}')">${escapeHtml(t.counterparty)}</button></td>
            <td class="mono">${escapeHtml(t.tx_type)}</td>
            <td class="num">${formatKes(t.amount_kes)}</td>
            <td class="num">${Number(t.score || 0).toFixed(2)}</td>
            <td>${t.verdict ? '<span class="tag tag-bad">FLAGGED</span>' : '<span class="tag tag-ok">CLEARED</span>'}</td>
            <td class="mono" style="font-size:11px;">${escapeHtml(t.review_status)}</td>
          </tr>
        `).join('');

        const drawer = document.getElementById('accountDrawer');
        drawer.style.display = 'block';
        drawer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } catch (err) {
        showError(`Could not load account timeline: ${err.message}`);
      }
    }

    function closeAccountDrawer() {
      document.getElementById('accountDrawer').style.display = 'none';
    }

    function renderTable() {
      const tbody = document.getElementById('txTableBody');
      let rows = cachedTransactions;
      if (currentFilter === 'flagged') {
        rows = cachedTransactions.filter((t) => Number(t.verdict) === 1);
      } else if (currentFilter === 'static_miss') {
        rows = cachedTransactions.filter((t) => Number(t.verdict) === 1 && Number(t.static_rule_verdict) === 0);
      }

      if (!rows.length) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:var(--muted);padding:20px;">No matching transactions logged yet.</td></tr>';
        return;
      }

      tbody.innerHTML = rows.map((tx) => {
        const isFraud = Number(tx.verdict) === 1;
        const staticHit = Number(tx.static_rule_verdict) === 1;
        const badge = isFraud
          ? '<span class="tag tag-bad">FLAGGED</span>'
          : '<span class="tag tag-ok">CLEARED</span>';
        let staticTag = '<span class="tag tag-ok">CLEARED</span>';
        if (staticHit) {
          staticTag = '<span class="tag tag-warn">FLAGGED</span>';
        } else if (isFraud && !staticHit) {
          staticTag = '<span class="tag tag-bad">MISSED</span>';
        }

        const status = tx.review_status || 'PENDING';
        let dispCell = '<span style="color:var(--muted);font-size:11px;">—</span>';
        if (status === 'CONFIRMED_FRAUD') {
          dispCell = '<span class="tag tag-bad">CONFIRMED</span>';
        } else if (status === 'FALSE_POSITIVE') {
          dispCell = '<span class="tag tag-ok">FALSE POS</span>';
        } else if (isFraud) {
          const safeId = escapeHtml(tx.tx_id);
          dispCell = `
            <button type="button" class="btn btn-xs" onclick="setDisposition('${safeId}', 'CONFIRMED_FRAUD')">Confirm</button>
            <button type="button" class="btn btn-xs" onclick="setDisposition('${safeId}', 'FALSE_POSITIVE')">Dismiss FP</button>
          `;
        }

        const ts = tx.timestamp ? tx.timestamp.replace('T', ' ').slice(0, 19) : '--';
        return `
          <tr>
            <td class="mono">${escapeHtml(tx.tx_id)}</td>
            <td class="mono" style="color:var(--muted);">${escapeHtml(ts)}</td>
            <td><button type="button" class="acct-link" onclick="openAccountDrawer('${escapeHtml(tx.origin_account_id)}')">${escapeHtml(tx.origin_account_id)}</button></td>
            <td><button type="button" class="acct-link" onclick="openAccountDrawer('${escapeHtml(tx.vendor_hash)}')">${escapeHtml(tx.vendor_hash)}</button></td>
            <td class="num">${formatKes(tx.amount_kes)}</td>
            <td class="num">${Number(tx.score || 0).toFixed(2)} <span style="color:var(--muted);font-size:10px;">(${Number(tx.ml_score || 0).toFixed(2)}/${Number(tx.policy_score || 0).toFixed(2)})</span></td>
            <td>${badge}</td>
            <td>${staticTag}</td>
            <td>${dispCell}</td>
          </tr>
        `;
      }).join('');
    }

    const ACTION_LABELS = {
      ALLOW: 'Allow transaction',
      ALLOW_WITH_MONITORING: 'Allow & monitor account',
      FLAG_FOR_MANUAL_REVIEW: 'Flag for manual review / step-up OTP',
      HOLD_AND_ESCALATE_SOC: 'Hold settlement & escalate to SOC',
    };

    function renderVerdict(payload, result, clientLatencyMs) {
      const isFraud = Number(result.verdict) === 1;
      const staticHit = Number(result.static_rule_verdict) === 1;
      const actionKey = result.recommended_action || (isFraud ? 'FLAG_FOR_MANUAL_REVIEW' : 'ALLOW');

      document.getElementById('verdictTxId').textContent = result.tx_id;
      document.getElementById('scoreValue').textContent =
        `${Number(result.score).toFixed(2)} (cutoff ${Number(result.threshold ?? activeThreshold).toFixed(2)})`;
      document.getElementById('scoreSplit').textContent =
        `ML: ${Number(result.ml_score ?? 0).toFixed(2)} | Policy: ${Number(result.policy_score ?? 0).toFixed(2)} [${result.scoring_source || 'HYBRID'}]`;
      document.getElementById('actionValue').textContent = ACTION_LABELS[actionKey] || actionKey;
      document.getElementById('lastLatencyDetail').textContent =
        `${Number(result.latency_ms ?? 0).toFixed(2)} ms server (${clientLatencyMs.toFixed(1)} ms RTT)`;

      const guardBox = document.getElementById('cmpGuardBox');
      const guardVal = document.getElementById('cmpGuardVal');
      const guardSub = document.getElementById('cmpGuardSub');
      if (actionKey === 'HOLD_AND_ESCALATE_SOC') {
        guardBox.className = 'cmp-card bad';
        guardVal.textContent = 'FLAGGED — HIGH RISK';
        guardSub.textContent = 'Hold settlement & escalate';
      } else if (isFraud) {
        guardBox.className = 'cmp-card warn';
        guardVal.textContent = 'FLAGGED — REVIEW';
        guardSub.textContent = 'Route to analyst / step-up';
      } else {
        guardBox.className = 'cmp-card ok';
        guardVal.textContent = 'CLEARED';
        guardSub.textContent = 'Within behavioral baseline';
      }

      const staticBox = document.getElementById('cmpStaticBox');
      const staticVal = document.getElementById('cmpStaticVal');
      const staticSub = document.getElementById('cmpStaticSub');
      if (staticHit) {
        staticBox.className = 'cmp-card warn';
        staticVal.textContent = 'FLAGGED (> 50k)';
        staticSub.textContent = 'Triggered static KES 50k limit';
      } else if (isFraud && !staticHit) {
        staticBox.className = 'cmp-card bad';
        staticVal.textContent = 'MISSED (CLEARED)';
        staticSub.textContent = 'Bypassed static KES 50k rule!';
      } else {
        staticBox.className = 'cmp-card ok';
        staticVal.textContent = 'CLEARED';
        staticSub.textContent = 'Below static KES 50k limit';
      }

      const f = result.features || {};
      const tsl = f.time_since_last_tx !== undefined ? `${Number(f.time_since_last_tx).toFixed(1)}m gap` : '--';
      document.getElementById('velSummary').textContent = `${f.tx_count_15min ?? 0} / ${f.tx_count_24h ?? 0} / ${tsl}`;
      const fanSenders = f.vendor_unique_senders_15min ?? 0;
      const fanAmt = formatKes(f.vendor_inflow_15min ?? 0);
      document.getElementById('fanInSummary').textContent = `${fanSenders} other senders (KES ${fanAmt})`;

      const signals = Array.isArray(result.signals) && result.signals.length
        ? result.signals
        : ['No anomaly signals triggered.'];
      document.getElementById('signalList').innerHTML = signals.map((s) => `<li>${escapeHtml(s)}</li>`).join('');

      lastRawRequest = payload;
      document.getElementById('rawRequestBlock').textContent = `// Request POST /score\n${JSON.stringify(payload, null, 2)}`;
      const respBlock = document.getElementById('rawResponseBlock');
      respBlock.style.display = 'block';
      respBlock.textContent = `// Response HTTP 200\n${JSON.stringify(result, null, 2)}`;
    }

    function copyCurl() {
      const sample = lastRawRequest || SCENARIOS.normal.buildPayloads()[0];
      const url = `${window.location.origin}/score`;
      const cmd = `curl -X POST "${url}" \\\n  -H "Content-Type: application/json" \\\n  -d '${JSON.stringify(sample)}'`;
      navigator.clipboard.writeText(cmd).then(() => {
        alert('Copied cURL command to clipboard.');
      }).catch(() => {
        prompt('Copy cURL command:', cmd);
      });
    }

    async function scorePayload(payload) {
      showError('');
      const start = performance.now();
      const res = await fetch('/score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const clientMs = performance.now() - start;
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text}`);
      }
      const data = await res.json();
      renderVerdict(payload, data, clientMs);
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
