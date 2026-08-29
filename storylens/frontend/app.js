let currentPersona = 'executive';
let currentScenario = 'supply_chain';

// Chart registry — prevents double-init
const _charts = {};

document.addEventListener('DOMContentLoaded', () => {
  initSidebarNavigation();
  initPersonaDropdown();
  initScenarioTabs();
  initSimSlider();
  initWaterfallChart(); // legacy v_drivers chart
  renderState();
});

// ── Sidebar Navigation ─────────────────────────────────────────
function initSidebarNavigation() {
  const links = document.querySelectorAll('.nav-link[data-view]');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      const target = e.currentTarget.getAttribute('data-view');
      navigateTo(target);
    });
  });
}

function navigateTo(viewId) {
  document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active-panel'));
  const panel = document.getElementById(viewId);
  if (panel) panel.classList.add('active-panel');
  document.querySelectorAll('.nav-link[data-view]').forEach(l => {
    l.classList.toggle('active', l.getAttribute('data-view') === viewId);
  });
  // Lazy init analytics charts when Analytics Lab is opened
  if (viewId === 'v_analytics') {
    requestAnimationFrame(() => initAllAnalyticsCharts());
  }
}
window.navigateTo = navigateTo;

// ── Persona & Scenario Controls ────────────────────────────────
function initPersonaDropdown() {
  const sel = document.getElementById('personaDropdown');
  if (sel) sel.addEventListener('change', e => { currentPersona = e.target.value; renderState(); });
}

function initScenarioTabs() {
  document.querySelectorAll('.scenario-tab').forEach(tab => {
    tab.addEventListener('click', e => {
      document.querySelectorAll('.scenario-tab').forEach(t => {
        t.classList.remove('btn-primary'); t.classList.add('btn-secondary');
      });
      e.currentTarget.classList.add('btn-primary'); e.currentTarget.classList.remove('btn-secondary');
      currentScenario = e.currentTarget.getAttribute('data-scenario');
      renderState();
    });
  });
}

function renderState() {
  const headline = document.getElementById('incidentHeadline');
  const primary  = document.getElementById('incidentPrimaryDriver');
  const dataAlert = document.getElementById('dataIncidentAlert');
  if (!headline) return;

  if (currentScenario === 'data_pipeline_fault') {
    dataAlert.style.display = 'flex';
    headline.innerText = 'Data Pipeline Ingestion Anomaly Detected (Investigation Paused)';
    primary.innerHTML = '<strong style="color:var(--accent-rose);">Reason: SAP Sales Ingest connector dropped 19.4% records at 03:00 UTC.</strong> Refusing to explain unhealthy data.';
    return;
  } else { dataAlert.style.display = 'none'; }

  if (currentScenario === 'abstain_scenario') {
    headline.innerText = 'System Abstention: Discrepancy between Ad Spend & Product Return Logs';
    primary.innerHTML = '<strong style="color:var(--accent-amber);">Reason: Confidence (41.0%) < 60% Safety Threshold.</strong> Input Batch Quality Audit to resolve.';
    return;
  }

  headline.innerText = 'Net Revenue is ₹8.1M below expected performance (-8.1%)';
  if (currentPersona === 'operations') {
    primary.innerHTML = 'Primary driver: <strong>Supplier A fulfillment deterioration</strong> (Floor Backlog: 4,200 units). <span style="color:var(--accent-amber);font-weight:700;">🔒 PBR Financial Masking Active</span>';
  } else {
    primary.innerHTML = 'Primary driver: <strong>Supplier A fulfillment deterioration</strong> — Model-explained gap: <strong>₹7.2M / 88.9%</strong> | Supplier A attributable: <strong>₹4.9M / 60.5%</strong> | Residual: <strong>₹0.9M / 11.1%</strong>';
  }
}

// ── Decision Simulator ─────────────────────────────────────────
function initSimSlider() {
  const slider = document.getElementById('volSlider');
  if (!slider) return;
  slider.addEventListener('input', e => {
    const val = parseFloat(e.target.value);
    document.getElementById('sliderValLabel').innerText = val + '%';
    const alert = document.getElementById('simConstraintAlert');
    alert.style.display = val > 32 ? 'flex' : 'none';
    const eff = Math.min(32, val);
    document.getElementById('projDelay').innerText    = Math.max(3.0, (18.2 - eff * 0.45)).toFixed(1) + '%';
    document.getElementById('projCancel').innerText   = Math.max(2.5, (14.1 - eff * 0.32)).toFixed(1) + '%';
    document.getElementById('projRecovery').innerText = '₹' + (3.0 * (eff / 22.0)).toFixed(1) + 'M';
  });
}

// ── Legacy v_drivers Waterfall ─────────────────────────────────
function initWaterfallChart() {
  const canvas = document.getElementById('waterfallChart');
  if (!canvas || _charts.waterfall) return;
  _charts.waterfall = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: ['Expected', 'Cancellations', 'Volume Drop', 'Repeat Purchase', 'Product Mix', 'Pricing', 'Actual'],
      datasets: [{ label: 'Revenue Bridge (₹M)', data: [100.0, -2.4, -2.2, -1.8, -1.1, -0.3, 91.9],
        backgroundColor: ['#2563eb','#ef4444','#ef4444','#ef4444','#f59e0b','#f59e0b','#10b981'] }]
    },
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { color: '#e2e8f0' }, ticks: { color: '#0f172a', font: { weight: '600' } } },
                y: { grid: { color: '#e2e8f0' }, ticks: { color: '#0f172a', font: { weight: '600' }, callback: v => '₹' + v + 'M' } } }
    }
  });
}

// ══════════════════════════════════════════════════════════════
//  ANALYTICS LAB — 6 HERO CHART INITIALISERS
// ══════════════════════════════════════════════════════════════

function initAllAnalyticsCharts() {
  initActualVsExpected();
  initRevenueBridge();
  initImpactMatrix();
  initDiDChart();
  initCohortChart();
}

// ── 1. Actual vs Expected KPI Monitor ─────────────────────────
function initActualVsExpected() {
  const canvas = document.getElementById('actualVsExpectedChart');
  if (!canvas || _charts.actualVsExpected) return;

  const labels = [], actual = [], expected = [], upper = [], lower = [];
  for (let i = 0; i < 45; i++) {
    const d = new Date('2026-07-15');
    d.setDate(d.getDate() + i);
    labels.push(d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    // Seeded pseudo-random for reproducibility
    const seed = Math.sin(i * 7.3) * 0.5 + Math.sin(i * 2.1) * 0.3;
    const exp = 100.2 + Math.sin(i / 8) * 1.4 + i * 0.04;
    expected.push(+exp.toFixed(2));
    upper.push(+(exp + 2.4).toFixed(2));
    lower.push(+(exp - 2.6).toFixed(2));
    if (i < 28) {
      actual.push(+(exp + seed * 0.9).toFixed(2));
    } else {
      const drop = (i - 28) * 0.6;
      actual.push(+(exp - drop + seed * 0.4).toFixed(2));
    }
  }
  actual[44] = 91.9;

  const eventLinePlugin = {
    id: 'eventLine',
    afterDraw(chart) {
      const { ctx, scales: { x, y } } = chart;
      const xPos = x.getPixelForValue(28);
      ctx.save();
      ctx.setLineDash([5, 4]);
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(xPos, y.top); ctx.lineTo(xPos, y.bottom); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#ef4444';
      ctx.font = '600 11px Plus Jakarta Sans';
      ctx.fillText('⚡ Supplier A SLA', xPos + 5, y.top + 13);
      ctx.fillText('degradation', xPos + 5, y.top + 26);
      ctx.restore();
    }
  };

  _charts.actualVsExpected = new Chart(canvas.getContext('2d'), {
    data: {
      labels,
      datasets: [
        { type: 'line', label: 'Upper 95% Band', data: upper, borderColor: 'transparent',
          backgroundColor: 'rgba(37,99,235,0.07)', fill: '+1', pointRadius: 0, tension: 0.4 },
        { type: 'line', label: 'Lower 95% Band', data: lower, borderColor: 'transparent',
          backgroundColor: 'rgba(37,99,235,0.07)', fill: false, pointRadius: 0, tension: 0.4 },
        { type: 'line', label: 'Expected Baseline', data: expected, borderColor: '#94a3b8',
          borderDash: [6, 4], borderWidth: 2, backgroundColor: 'transparent',
          pointRadius: 0, tension: 0.4 },
        { type: 'line', label: 'Actual Revenue', data: actual, borderColor: '#2563eb',
          borderWidth: 2.5, backgroundColor: 'transparent',
          pointRadius: 0, pointHoverRadius: 5, tension: 0.4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { boxWidth: 14, font: { size: 12, weight: '700' } } },
        tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ₹' + ctx.parsed.y.toFixed(1) + 'M' } }
      },
      scales: {
        x: { grid: { color: '#f1f5f9' }, ticks: { maxTicksLimit: 9, color: '#64748b', font: { size: 11 } } },
        y: { min: 88, max: 106, grid: { color: '#f1f5f9' },
          ticks: { color: '#64748b', font: { size: 11 }, callback: v => '₹' + v + 'M' } }
      }
    },
    plugins: [eventLinePlugin]
  });
}

// ── 2. Revenue Bridge — True Floating Waterfall ────────────────
function initRevenueBridge() {
  const canvas = document.getElementById('revenueBridgeChart');
  if (!canvas || _charts.revenueBridge) return;

  // Cumulative running totals for floating bar [base, top]
  // Each negative bar shows the DROP from the previous level
  const items = [
    { label: 'Expected\n₹100.0M', base: 0,    top: 100.0, color: '#2563eb', isEndpoint: true },
    { label: 'Cancellations\n−₹2.4M',   base: 97.6,  top: 100.0, color: '#ef4444' },
    { label: 'Volume Drop\n−₹2.2M',     base: 95.4,  top: 97.6,  color: '#ef4444' },
    { label: 'Repeat Purchase\n−₹1.8M', base: 93.6,  top: 95.4,  color: '#ef4444' },
    { label: 'Product Mix\n−₹1.1M',     base: 92.5,  top: 93.6,  color: '#f59e0b' },
    { label: 'Pricing\n−₹0.3M',         base: 92.2,  top: 92.5,  color: '#f59e0b' },
    { label: 'Residual\n−₹0.3M',        base: 91.9,  top: 92.2,  color: '#f59e0b' },
    { label: 'Actual\n₹91.9M',          base: 0,     top: 91.9,  color: '#10b981', isEndpoint: true }
  ];

  const connectorPlugin = {
    id: 'connectorLines',
    afterDatasetsDraw(chart) {
      const { ctx, data, scales: { x, y } } = chart;
      ctx.save();
      ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
      // Draw connector from top of each bar to base of next bar
      for (let i = 0; i < items.length - 2; i++) {
        const prevTop = items[i].isEndpoint ? items[i].top : items[i].base;
        const thisBase = items[i + 1].base;
        const x1 = x.getPixelForValue(i) + x.width / (items.length * 2);
        const x2 = x.getPixelForValue(i + 1) - x.width / (items.length * 2);
        const yVal = y.getPixelForValue(items[i].isEndpoint ? items[i].top : items[i].base);
        ctx.beginPath(); ctx.moveTo(x1, yVal); ctx.lineTo(x2, yVal); ctx.stroke();
      }
      ctx.restore();
    }
  };

  _charts.revenueBridge = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: items.map(it => it.label),
      datasets: [{
        data: items.map(it => [it.base, it.top]),
        backgroundColor: items.map(it => it.color),
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false },
        tooltip: { callbacks: {
          label: (ctx) => {
            const item = items[ctx.dataIndex];
            const diff = (item.top - item.base).toFixed(1);
            return item.isEndpoint ? '₹' + item.top + 'M' : '−₹' + diff + 'M';
          }
        }}
      },
      scales: {
        x: { grid: { display: false },
          ticks: { color: '#0f172a', font: { size: 11, weight: '700' }, maxRotation: 0, autoSkip: false } },
        y: { min: 88, max: 103,
          grid: { color: '#f1f5f9' },
          ticks: { color: '#64748b', font: { size: 11 }, callback: v => '₹' + v + 'M' } }
      }
    },
    plugins: [connectorPlugin]
  });
}

// ── 3. Impact × Evidence Confidence Matrix ─────────────────────
function initImpactMatrix() {
  const canvas = document.getElementById('impactMatrixChart');
  if (!canvas || _charts.impactMatrix) return;

  const quadrantPlugin = {
    id: 'quadrants',
    beforeDraw(chart) {
      const { ctx, scales: { x, y } } = chart;
      const xMid = x.getPixelForValue(35);
      const yMid = y.getPixelForValue(60);
      ctx.save();
      // Quadrant fills
      const regions = [
        { x: xMid, y: y.top,  w: x.right - xMid,    h: yMid - y.top,  color: 'rgba(220,252,231,0.4)',  label: '⚡ ACT',         lx: (xMid + x.right)/2,   ly: y.top + 16 },
        { x: x.left, y: y.top,  w: xMid - x.left, h: yMid - y.top,  color: 'rgba(219,234,254,0.4)',  label: '🔍 INVESTIGATE', lx: (x.left + xMid)/2,   ly: y.top + 16 },
        { x: xMid, y: yMid, w: x.right - xMid,    h: y.bottom - yMid, color: 'rgba(254,249,195,0.4)',  label: '👁 WATCH',        lx: (xMid + x.right)/2,   ly: yMid + 18 },
        { x: x.left, y: yMid, w: xMid - x.left, h: y.bottom - yMid, color: 'rgba(241,245,249,0.4)',  label: '↓ DEPRIORITIZE', lx: (x.left + xMid)/2,   ly: yMid + 18 },
      ];
      regions.forEach(r => {
        ctx.fillStyle = r.color;
        ctx.fillRect(r.x, r.y, r.w, r.h);
        ctx.fillStyle = '#94a3b8'; ctx.font = '700 10px Plus Jakarta Sans'; ctx.textAlign = 'center';
        ctx.fillText(r.label, r.lx, r.ly);
      });
      // Crosshair lines
      ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(xMid, y.top); ctx.lineTo(xMid, y.bottom); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x.left, yMid); ctx.lineTo(x.right, yMid); ctx.stroke();
      ctx.restore();
    }
  };

  _charts.impactMatrix = new Chart(canvas.getContext('2d'), {
    type: 'bubble',
    data: {
      datasets: [
        { label: 'Supplier A Fulfilment', data: [{ x: 60.5, y: 84, r: 22 }],
          backgroundColor: 'rgba(239,68,68,0.75)', borderColor: '#ef4444', borderWidth: 2 },
        { label: 'Product Mix Shift', data: [{ x: 27.2, y: 62, r: 14 }],
          backgroundColor: 'rgba(245,158,11,0.75)', borderColor: '#f59e0b', borderWidth: 2 },
        { label: 'Regional Demand Softness', data: [{ x: 18.5, y: 41, r: 10 }],
          backgroundColor: 'rgba(148,163,184,0.65)', borderColor: '#94a3b8', borderWidth: 2 },
        { label: 'Pricing Pressure', data: [{ x: 8.1, y: 31, r: 8 }],
          backgroundColor: 'rgba(148,163,184,0.4)', borderColor: '#94a3b8', borderWidth: 1.5 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11, weight: '700' } } },
        tooltip: { callbacks: {
          label: ctx => `${ctx.dataset.label}: Impact ${ctx.raw.x}% · Confidence ${ctx.raw.y}%`
        }}
      },
      scales: {
        x: { min: 0, max: 80, grid: { color: '#f1f5f9' },
          title: { display: true, text: 'Business Contribution (% of ₹8.1M Gap)', font: { size: 11, weight: '700' }, color: '#64748b' },
          ticks: { callback: v => v + '%', color: '#64748b', font: { size: 11 } } },
        y: { min: 0, max: 100, grid: { color: '#f1f5f9' },
          title: { display: true, text: 'Evidence Confidence (%)', font: { size: 11, weight: '700' }, color: '#64748b' },
          ticks: { callback: v => v + '%', color: '#64748b', font: { size: 11 } } }
      }
    },
    plugins: [quadrantPlugin]
  });
}

// ── 4. DiD Causal Validation Chart ────────────────────────────
function initDiDChart() {
  const canvas = document.getElementById('didChart');
  if (!canvas || _charts.did) return;

  const days = [], treatment = [], control = [];
  for (let i = -14; i <= 14; i++) {
    days.push(i === 0 ? 'Day 0 ⚡' : 'D' + (i > 0 ? '+' : '') + i);
    const noise = Math.sin(i * 3.7) * 0.25;
    control.push(+(30.5 + noise).toFixed(2));
    if (i < 0) {
      treatment.push(+(31.5 + noise * 0.8).toFixed(2));
    } else {
      treatment.push(+(31.5 - i * 0.54 + noise * 0.3).toFixed(2));
    }
  }

  const eventPlugin = {
    id: 'didEvent',
    afterDraw(chart) {
      const { ctx, scales: { x, y } } = chart;
      const idx = 14; // Day 0
      const xPos = x.getPixelForValue(idx);
      ctx.save();
      ctx.setLineDash([5, 4]);
      ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(xPos, y.top); ctx.lineTo(xPos, y.bottom); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#0f172a'; ctx.font = '700 11px Plus Jakarta Sans'; ctx.textAlign = 'center';
      ctx.fillText('Disruption Event', xPos, y.top - 4);
      ctx.restore();
    }
  };

  _charts.did = new Chart(canvas.getContext('2d'), {
    type: 'line',
    data: {
      labels: days,
      datasets: [
        { label: 'Control SKUs (Supplier B/C)', data: control, borderColor: '#10b981',
          borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: '#10b981', tension: 0.3 },
        { label: 'Treatment SKUs (Supplier A)', data: treatment, borderColor: '#ef4444',
          borderWidth: 2.5, pointRadius: 3, pointBackgroundColor: '#ef4444', tension: 0.3,
          borderDash: undefined }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 14, font: { size: 11, weight: '700' } } },
        tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + '%' } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { maxTicksLimit: 8, color: '#64748b', font: { size: 10 } } },
        y: { min: 18, max: 36, grid: { color: '#f1f5f9' },
          title: { display: true, text: 'Repeat Purchase Rate (%)', font: { size: 11, weight: '700' }, color: '#64748b' },
          ticks: { callback: v => v + '%', color: '#64748b', font: { size: 11 } } }
      }
    },
    plugins: [eventPlugin]
  });
}

// ── 6. Customer Delay × Retention Cohort ─────────────────────
function initCohortChart() {
  const canvas = document.getElementById('cohortChart');
  if (!canvas || _charts.cohort) return;

  _charts.cohort = new Chart(canvas.getContext('2d'), {
    type: 'line',
    data: {
      labels: ['No Delay\n(n=4,200)', '1–2 Days\n(n=2,840)', '3–5 Days\n(n=1,960)', '>5 Days\n(n=820)'],
      datasets: [{
        label: 'Repeat Purchase Rate',
        data: [31.4, 28.9, 23.1, 16.8],
        borderColor: '#2563eb', borderWidth: 3,
        backgroundColor: 'rgba(37,99,235,0.08)', fill: true,
        pointRadius: 8, pointBackgroundColor: '#2563eb',
        pointHoverRadius: 10, tension: 0.3
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: {
          label: ctx => 'Repeat Purchase: ' + ctx.parsed.y + '%',
          afterLabel: ctx => {
            const drops = [null, '−2.5pp vs no delay', '−8.3pp vs no delay', '−14.6pp vs no delay'];
            return drops[ctx.dataIndex] || '';
          }
        }}
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#0f172a', font: { size: 11, weight: '700' } } },
        y: { min: 10, max: 40, grid: { color: '#f1f5f9' },
          title: { display: true, text: 'Repeat Purchase Rate (%)', font: { size: 11, weight: '700' }, color: '#64748b' },
          ticks: { callback: v => v + '%', color: '#64748b', font: { size: 11 } } }
      }
    }
  });
}

// ── Heatmap Click Handler ──────────────────────────────────────
window.heatmapClick = function(region, category, value, suppData) {
  // Close any open expansions first
  document.querySelectorAll('.heatmap-expansion').forEach(el => el.classList.remove('open'));
  const el = document.getElementById(`hm-exp-${region}-${category}`);
  if (el) el.classList.toggle('open');
};

// ── Modal / Drawer Controls ────────────────────────────────────
window.openBriefModal = function() {
  const overlay = document.getElementById('briefOverlay');
  const panel   = document.getElementById('briefPanel');
  overlay.classList.add('active');
  panel.classList.add('active');
  panel.style.right = '0px';
};

window.closeBriefModal = function() {
  const overlay = document.getElementById('briefOverlay');
  const panel   = document.getElementById('briefPanel');
  overlay.classList.remove('active');
  panel.classList.remove('active');
  panel.style.right = '-620px';
};

window.openDrawer = function(id) {
  const overlay = document.getElementById('drawerOverlay');
  const panel   = document.getElementById('drawerPanel');
  overlay.classList.add('active');
  panel.classList.add('active');
  panel.style.right = '0px';

  const claims = {
    'EV-3941': { claim: 'Net Revenue declined 8.1% QoQ (₹8.1M gap)', src: 'sales_orders (SAP ERP)',
      sql: "SELECT SUM(net_revenue) FROM sales_orders WHERE order_date >= '2026-08-01'",
      fresh: '7 min', rows: '12,570', quality: '99.8%' },
    'EV-3942': { claim: 'Supplier A fill rate fell 21.4% and outbound delivery delays increased 18.2%',
      src: 'shipments (Manhattan WMS)',
      sql: 'SELECT supplier_id, AVG(delay_days) FROM shipments GROUP BY supplier_id',
      fresh: '53 min', rows: '12,570', quality: '97.1%' },
    'EV-3943': { claim: 'Customer complaint tickets for SLA breach increased 24.0%',
      src: 'support_tickets (Zendesk CRM)',
      sql: "SELECT COUNT(*) FROM support_tickets WHERE issue_type = 'Delivery SLA Breach'",
      fresh: '2 min', rows: '542', quality: '94.6%' }
  };
  const item = claims[id] || claims['EV-3942'];
  document.getElementById('dTitle').innerText   = id;
  document.getElementById('dClaim').innerText   = item.claim;
  document.getElementById('dSource').innerText  = item.src;
  document.getElementById('dFresh').innerText   = item.fresh;
  document.getElementById('dRows').innerText    = item.rows;
  document.getElementById('dQuality').innerText = item.quality;
  document.getElementById('dSql').innerText     = item.sql;
};

window.closeDrawer = function() {
  const overlay = document.getElementById('drawerOverlay');
  const panel   = document.getElementById('drawerPanel');
  overlay.classList.remove('active');
  panel.classList.remove('active');
  panel.style.right = '-620px';
};
