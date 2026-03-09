#!/bin/bash

echo "📦 Backing up existing frontend..."
cp -r app/templates app/templates_backup_$(date +%Y%m%d_%H%M%S)
cp -r app/static app/static_backup_$(date +%Y%m%d_%H%M%S)
echo "✅ Backup complete"

mkdir -p app/static/css
mkdir -p app/static/js

cat > app/static/css/dark-glass-terminal.css << 'ENDCSS'
:root {
  --bg-void:#05071a;--bg-base:#0a0e27;--bg-panel:#0f1535;--bg-elevated:#151932;
  --bg-glass:rgba(255,255,255,0.04);--bg-glass-hover:rgba(255,255,255,0.07);
  --cyan:#00f0ff;--green:#00ff41;--magenta:#ff00ff;--amber:#ffb700;--red:#ff3355;
  --accent:var(--cyan);--accent-dim:rgba(0,240,255,0.15);
  --accent-glow:0 0 20px rgba(0,240,255,0.3);
  --text-primary:#e8eaf6;--text-secondary:#8892b0;--text-dim:#4a5280;
  --border:rgba(255,255,255,0.08);--border-accent:rgba(0,240,255,0.3);
  --font-ui:'Space Grotesk',sans-serif;--font-mono:'Fira Code',monospace;
  --t-fast:0.12s ease;--t-smooth:0.25s cubic-bezier(0.4,0,0.2,1);
  --t-spring:0.4s cubic-bezier(0.34,1.56,0.64,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{height:100%;scroll-behavior:smooth}
body{font-family:var(--font-ui);background:var(--bg-void);color:var(--text-primary);min-height:100vh;overflow-x:hidden;font-size:14px;line-height:1.5}
body::before{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.03) 2px,rgba(0,0,0,0.03) 4px);pointer-events:none;z-index:1000}
.ambient{position:fixed;border-radius:50%;filter:blur(120px);opacity:.12;pointer-events:none;z-index:0}
.ambient-1{width:600px;height:600px;background:var(--cyan);top:-200px;right:-100px}
.ambient-2{width:400px;height:400px;background:var(--magenta);bottom:-100px;left:-100px}
.ambient-3{width:300px;height:300px;background:var(--green);top:50%;left:40%;opacity:.06}
.app-shell{position:relative;z-index:1;display:grid;grid-template-rows:52px 1fr;grid-template-columns:220px 1fr;min-height:100vh}
.topbar{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;padding:0 24px;background:rgba(10,14,39,.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.logo{display:flex;align-items:center;gap:12px;font-family:var(--font-mono);font-weight:600;font-size:15px;letter-spacing:.08em}
.logo-mark{width:28px;height:28px;background:linear-gradient(135deg,var(--cyan),var(--magenta));border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--bg-void);box-shadow:var(--accent-glow)}
.logo-tag{color:var(--cyan);font-size:10px;letter-spacing:.15em;text-transform:uppercase;padding:2px 6px;border:1px solid var(--border-accent);border-radius:4px}
.topbar-center{flex:1;display:flex;justify-content:center}
.cmd-trigger{display:flex;align-items:center;gap:8px;background:var(--bg-glass);border:1px solid var(--border);border-radius:8px;padding:8px 16px;color:var(--text-secondary);font-family:var(--font-mono);font-size:12px;cursor:pointer;transition:all var(--t-smooth);width:280px}
.cmd-trigger:hover{border-color:var(--border-accent);background:var(--bg-glass-hover);color:var(--text-primary);box-shadow:var(--accent-glow)}
.cmd-trigger .kbd{margin-left:auto;display:flex;gap:3px}
.cmd-trigger .kbd span{background:rgba(255,255,255,.08);padding:1px 5px;border-radius:3px;font-size:10px;color:var(--text-dim)}
.topbar-right{display:flex;align-items:center;gap:16px}
.status-bar{display:flex;align-items:center;gap:12px;font-family:var(--font-mono);font-size:11px;color:var(--text-dim)}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.topbar-time{font-family:var(--font-mono);font-size:12px;color:var(--text-secondary)}
.icon-btn{width:32px;height:32px;display:flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--border);border-radius:4px;color:var(--text-secondary);cursor:pointer;transition:all var(--t-fast);font-size:14px}
.icon-btn:hover{border-color:var(--border-accent);color:var(--cyan);background:var(--accent-dim)}
.sidebar{background:rgba(10,14,39,.6);border-right:1px solid var(--border);padding:24px 0;display:flex;flex-direction:column;gap:8px;overflow-y:auto}
.nav-section-label{font-family:var(--font-mono);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--text-dim);padding:0 20px 8px;margin-top:16px}
.nav-item{display:flex;align-items:center;gap:12px;padding:8px 20px;color:var(--text-secondary);cursor:pointer;transition:all var(--t-fast);border-left:2px solid transparent;font-size:13px;text-decoration:none}
.nav-item:hover{color:var(--text-primary);background:var(--bg-glass)}
.nav-item.active{color:var(--cyan);border-left-color:var(--cyan);background:var(--accent-dim)}
.nav-icon{width:16px;font-size:13px;text-align:center;flex-shrink:0}
.nav-badge{margin-left:auto;font-family:var(--font-mono);font-size:9px;padding:1px 5px;border-radius:99px;background:var(--accent-dim);color:var(--cyan);border:1px solid var(--border-accent)}
.sidebar-footer{margin-top:auto;padding:16px 20px;border-top:1px solid var(--border)}
.sys-status{font-family:var(--font-mono);font-size:10px;color:var(--text-dim);line-height:1.8}
.sys-status .ok{color:var(--green)}.sys-status .warn{color:var(--amber)}.sys-status .err{color:var(--red)}
.main-content{overflow-y:auto;padding:24px;display:flex;flex-direction:column;gap:24px;padding-bottom:48px}
.content-header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
.panel-breadcrumb{font-family:var(--font-mono);font-size:10px;color:var(--text-dim);letter-spacing:.1em;margin-bottom:4px}
.panel-breadcrumb span{color:var(--cyan)}
.panel-heading{font-size:22px;font-weight:600;letter-spacing:-.02em;color:var(--text-primary)}
.header-actions{display:flex;align-items:center;gap:8px}
.glass-card{background:var(--bg-glass);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:12px;transition:all var(--t-smooth);position:relative;overflow:hidden}
.glass-card::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.03) 0%,transparent 60%);pointer-events:none}
.glass-card:hover{border-color:rgba(0,240,255,.2);box-shadow:0 8px 32px rgba(0,0,0,.4);transform:translateY(-1px)}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.metric-card{padding:20px;cursor:default}
.metric-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.metric-label{font-family:var(--font-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-dim)}
.metric-icon{width:28px;height:28px;display:flex;align-items:center;justify-content:center;border-radius:4px;font-size:13px}
.metric-icon.cyan{background:rgba(0,240,255,.12);color:var(--cyan)}
.metric-icon.green{background:rgba(0,255,65,.12);color:var(--green)}
.metric-icon.magenta{background:rgba(255,0,255,.12);color:var(--magenta)}
.metric-icon.amber{background:rgba(255,183,0,.12);color:var(--amber)}
.metric-value{font-family:var(--font-mono);font-size:26px;font-weight:600;line-height:1;color:var(--text-primary);margin-bottom:8px;transition:all .3s ease}
.metric-sub{display:flex;align-items:center;gap:8px;font-size:11px}
.metric-delta{font-family:var(--font-mono);font-weight:500}
.metric-delta.pos{color:var(--green)}.metric-delta.neg{color:var(--red)}
.metric-desc{color:var(--text-dim)}
.metric-sparkline{margin-top:12px;height:32px}
.metric-sparkline svg{width:100%;height:100%;overflow:visible}
.dashboard-grid{display:grid;grid-template-columns:1fr 1fr 360px;gap:20px}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border)}
.panel-title-row{display:flex;align-items:center;gap:8px}
.panel-title{font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-secondary)}
.panel-dot{width:6px;height:6px;border-radius:50%}
.panel-actions{display:flex;gap:8px}
.panel-body{padding:16px 20px}
.pill-btn{font-family:var(--font-mono);font-size:10px;padding:3px 8px;border-radius:99px;border:1px solid var(--border);background:transparent;color:var(--text-dim);cursor:pointer;transition:all var(--t-fast)}
.pill-btn:hover,.pill-btn.active{border-color:var(--border-accent);color:var(--cyan);background:var(--accent-dim)}
.crypto-table{width:100%;border-collapse:collapse}
.crypto-table th{font-family:var(--font-mono);font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--text-dim);text-align:left;padding:8px;border-bottom:1px solid var(--border)}
.crypto-table th.right{text-align:right}
.crypto-table td{padding:12px 8px;border-bottom:1px solid rgba(255,255,255,.03);transition:background var(--t-fast);vertical-align:middle}
.crypto-table tr:hover td{background:var(--bg-glass)}
.crypto-table tr:last-child td{border-bottom:none}
.coin-cell{display:flex;align-items:center;gap:8px}
.coin-icon{width:28px;height:28px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}
.coin-name{font-size:13px;font-weight:500;color:var(--text-primary);line-height:1}
.coin-symbol{font-family:var(--font-mono);font-size:10px;color:var(--text-dim)}
.coin-price{font-family:var(--font-mono);font-size:13px;color:var(--text-primary);text-align:right}
.coin-change{font-family:var(--font-mono);font-size:11px;text-align:right;font-weight:500}
.coin-change.pos{color:var(--green)}.coin-change.pos::before{content:'▲ ';font-size:8px}
.coin-change.neg{color:var(--red)}.coin-change.neg::before{content:'▼ ';font-size:8px}
.sparkline-cell{width:80px}
.weather-main{padding:20px;display:flex;gap:20px;align-items:flex-start}
.weather-temp-display{font-family:var(--font-mono);font-size:56px;font-weight:300;line-height:1;color:var(--text-primary);letter-spacing:-.03em}
.weather-temp-display sup{font-size:24px;color:var(--cyan);vertical-align:super}
.weather-condition{font-size:14px;color:var(--text-secondary);margin-top:8px}
.weather-location{display:flex;align-items:center;gap:4px;font-family:var(--font-mono);font-size:11px;color:var(--cyan);margin-top:4px}
.weather-stats{margin-left:auto;display:flex;flex-direction:column;gap:8px}
.weather-stat{display:flex;align-items:center;gap:8px;font-family:var(--font-mono);font-size:11px;color:var(--text-secondary)}
.weather-stat .stat-val{color:var(--text-primary)}
.weather-icon-large{font-size:48px;line-height:1;filter:drop-shadow(0 0 20px rgba(0,240,255,.3))}
.forecast-row{display:grid;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--border)}
.forecast-item{padding:12px;text-align:center;border-right:1px solid var(--border);transition:background var(--t-fast);cursor:default}
.forecast-item:last-child{border-right:none}
.forecast-item:hover{background:var(--bg-glass)}
.fc-day{font-family:var(--font-mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-dim);margin-bottom:4px}
.fc-icon{font-size:18px;margin-bottom:4px}
.fc-temp{font-family:var(--font-mono);font-size:13px;color:var(--text-primary)}
.fc-temp span{color:var(--text-dim);font-size:11px}
.temp-chart-wrap{padding:16px 20px;border-top:1px solid var(--border)}
.chart-label{font-family:var(--font-mono);font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--text-dim);margin-bottom:12px}
.news-panel{grid-column:3;grid-row:1/3;max-height:780px;display:flex;flex-direction:column}
.news-filter{display:flex;gap:8px;padding:0 20px 16px;flex-wrap:wrap}
.news-scroll{flex:1;overflow-y:auto;padding:0 20px}
.news-scroll::-webkit-scrollbar{width:3px}
.news-scroll::-webkit-scrollbar-thumb{background:var(--border-accent);border-radius:99px}
.news-item{padding:16px 0;border-bottom:1px solid rgba(255,255,255,.04);cursor:pointer;transition:all var(--t-fast)}
.news-item:last-child{border-bottom:none}
.news-item:hover .news-headline{color:var(--cyan)}
.news-meta{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.news-source{font-family:var(--font-mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--cyan)}
.news-time{font-family:var(--font-mono);font-size:9px;color:var(--text-dim);margin-left:auto}
.news-tag{font-family:var(--font-mono);font-size:8px;padding:1px 5px;border-radius:3px;background:rgba(255,183,0,.1);color:var(--amber);border:1px solid rgba(255,183,0,.2)}
.news-headline{font-size:13px;font-weight:500;line-height:1.4;color:var(--text-primary);transition:color var(--t-fast);margin-bottom:8px}
.news-snippet{font-size:11px;color:var(--text-secondary);line-height:1.5;display:none}
.news-item.expanded .news-snippet{display:block}
.news-read-btn{font-family:var(--font-mono);font-size:9px;color:var(--cyan);background:none;border:none;cursor:pointer;padding:0}
.news-read-btn:hover{text-decoration:underline}
.github-panel{grid-column:1/3;grid-row:2}
.repo-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:20px}
.repo-card{background:var(--bg-elevated);border:1px solid var(--border);border-radius:8px;padding:16px;cursor:pointer;transition:all var(--t-smooth);position:relative;overflow:hidden}
.repo-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--cyan),var(--magenta));transform:scaleX(0);transition:transform var(--t-smooth);transform-origin:left}
.repo-card:hover{border-color:rgba(0,240,255,.2);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}
.repo-card:hover::after{transform:scaleX(1)}
.repo-name{font-family:var(--font-mono);font-size:12px;font-weight:500;color:var(--cyan);margin-bottom:4px}
.repo-desc{font-size:11px;color:var(--text-secondary);line-height:1.4;margin-bottom:12px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.repo-stats{display:flex;gap:12px;flex-wrap:wrap}
.repo-stat{display:flex;align-items:center;gap:4px;font-family:var(--font-mono);font-size:10px;color:var(--text-dim)}
.repo-lang-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.chip{display:inline-flex;align-items:center;gap:4px;font-family:var(--font-mono);font-size:9px;padding:3px 8px;border-radius:3px;cursor:pointer;border:1px solid transparent;transition:all var(--t-fast);white-space:nowrap}
.chip.cyan{background:rgba(0,240,255,.1);color:var(--cyan);border-color:rgba(0,240,255,.2)}
.chip.neutral{background:var(--bg-glass);color:var(--text-secondary);border-color:var(--border)}
.chip:hover{filter:brightness(1.2);transform:translateY(-1px)}
.refresh-btn{display:flex;align-items:center;gap:8px;font-family:var(--font-mono);font-size:10px;padding:8px 12px;background:var(--bg-glass);border:1px solid var(--border);border-radius:4px;color:var(--text-secondary);cursor:pointer;transition:all var(--t-fast)}
.refresh-btn:hover{border-color:var(--border-accent);color:var(--cyan);background:var(--accent-dim)}
.refresh-btn.spinning svg{animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.cmd-overlay{position:fixed;inset:0;background:rgba(5,7,26,.85);backdrop-filter:blur(8px);z-index:9000;display:flex;align-items:flex-start;justify-content:center;padding-top:15vh;opacity:0;pointer-events:none;transition:opacity var(--t-smooth)}
.cmd-overlay.open{opacity:1;pointer-events:all}
.cmd-palette{width:600px;max-width:calc(100vw - 40px);background:var(--bg-panel);border:1px solid var(--border-accent);border-radius:16px;box-shadow:0 24px 80px rgba(0,0,0,.8),0 0 60px rgba(0,240,255,.08);overflow:hidden;transform:scale(.96) translateY(-8px);transition:transform var(--t-spring)}
.cmd-overlay.open .cmd-palette{transform:scale(1) translateY(0)}
.cmd-input-wrap{display:flex;align-items:center;gap:12px;padding:16px 20px;border-bottom:1px solid var(--border)}
.cmd-prompt{font-family:var(--font-mono);font-size:14px;color:var(--cyan);flex-shrink:0}
.cmd-input{flex:1;background:none;border:none;outline:none;font-family:var(--font-mono);font-size:14px;color:var(--text-primary)}
.cmd-input::placeholder{color:var(--text-dim)}
.cmd-results{max-height:360px;overflow-y:auto;padding:8px 0}
.cmd-section-label{font-family:var(--font-mono);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--text-dim);padding:8px 20px}
.cmd-result-item{display:flex;align-items:center;gap:12px;padding:12px 20px;cursor:pointer;transition:background var(--t-fast)}
.cmd-result-item:hover,.cmd-result-item.focused{background:var(--accent-dim)}
.cmd-result-icon{width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:var(--bg-glass);border:1px solid var(--border);border-radius:4px;font-size:12px;flex-shrink:0}
.cmd-result-name{font-size:13px;color:var(--text-primary)}
.cmd-result-desc{font-size:11px;color:var(--text-dim);font-family:var(--font-mono)}
.cmd-result-kbd{margin-left:auto;font-family:var(--font-mono);font-size:9px;padding:2px 6px;background:rgba(255,255,255,.06);border:1px solid var(--border);border-radius:3px;color:var(--text-dim)}
.cmd-footer{display:flex;align-items:center;gap:20px;padding:12px 20px;border-top:1px solid var(--border);font-family:var(--font-mono);font-size:9px;color:var(--text-dim)}
.cmd-footer kbd{padding:1px 4px;background:rgba(255,255,255,.06);border:1px solid var(--border);border-radius:3px}
.toast-container{position:fixed;top:64px;right:20px;display:flex;flex-direction:column;gap:8px;z-index:9999}
.toast{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--bg-panel);border:1px solid var(--border-accent);border-radius:8px;font-family:var(--font-mono);font-size:11px;color:var(--text-primary);box-shadow:0 8px 24px rgba(0,0,0,.5);transform:translateX(120%);transition:transform var(--t-spring);min-width:260px}
.toast.show{transform:translateX(0)}
.toast-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.toast.info .toast-dot{background:var(--cyan);box-shadow:0 0 8px var(--cyan)}
.toast.success .toast-dot{background:var(--green);box-shadow:0 0 8px var(--green)}
.toast.warn .toast-dot{background:var(--amber);box-shadow:0 0 8px var(--amber)}
.terminal-log{position:fixed;bottom:0;left:220px;right:0;height:28px;background:rgba(5,7,26,.95);border-top:1px solid var(--border);display:flex;align-items:center;padding:0 16px;gap:16px;font-family:var(--font-mono);font-size:10px;overflow:hidden;z-index:50}
.log-prefix{color:var(--green);flex-shrink:0}
.log-ticker{flex:1;overflow:hidden;white-space:nowrap}
.log-ticker-inner{display:inline-block;animation:ticker 30s linear infinite}
@keyframes ticker{0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}
.log-item{color:var(--text-secondary);margin-right:32px}
.log-item .val{color:var(--cyan)}.log-item .pos{color:var(--green)}.log-item .neg{color:var(--red)}
.glass-card,.metric-card{animation:fadeUp .4s ease both}
.metric-card:nth-child(1){animation-delay:.05s}.metric-card:nth-child(2){animation-delay:.1s}
.metric-card:nth-child(3){animation-delay:.15s}.metric-card:nth-child(4){animation-delay:.2s}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:99px}
::-webkit-scrollbar-thumb:hover{background:rgba(0,240,255,.2)}
@media(max-width:1200px){.dashboard-grid{grid-template-columns:1fr 1fr}.news-panel{grid-column:1/-1;grid-row:3;max-height:500px}.github-panel{grid-column:1/-1}}
@media(max-width:900px){.app-shell{grid-template-columns:1fr}.sidebar{display:none}.metrics-row{grid-template-columns:repeat(2,1fr)}.dashboard-grid{grid-template-columns:1fr}.terminal-log{left:0}}
ENDCSS
echo "✅ CSS written"

cat > app/templates/base.html << 'ENDHTML'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}NEXUS Intelligence{% endblock %}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static', filename='css/dark-glass-terminal.css') }}">
{% block extra_css %}{% endblock %}
</head>
<body>
<div class="ambient ambient-1"></div>
<div class="ambient ambient-2"></div>
<div class="ambient ambient-3"></div>
<div class="toast-container" id="toastContainer"></div>

<div class="cmd-overlay" id="cmdOverlay">
  <div class="cmd-palette">
    <div class="cmd-input-wrap">
      <span class="cmd-prompt">❯</span>
      <input class="cmd-input" id="cmdInput" placeholder="Search assets, navigate, run commands..." autocomplete="off">
    </div>
    <div class="cmd-results">
      <div class="cmd-section-label">// NAVIGATE</div>
      <div class="cmd-result-item" data-href="{{ url_for('main.index') }}">
        <div class="cmd-result-icon">⬛</div>
        <div><div class="cmd-result-name">Overview</div><div class="cmd-result-desc">main dashboard</div></div>
        <span class="cmd-result-kbd">⌘0</span>
      </div>
      <div class="cmd-result-item" data-href="{{ url_for('crypto.index') }}">
        <div class="cmd-result-icon">₿</div>
        <div><div class="cmd-result-name">Crypto Intelligence</div><div class="cmd-result-desc">live prices · portfolio · alerts</div></div>
        <span class="cmd-result-kbd">⌘1</span>
      </div>
      <div class="cmd-result-item" data-href="{{ url_for('weather.index') }}">
        <div class="cmd-result-icon">⛅</div>
        <div><div class="cmd-result-name">Weather Intelligence</div><div class="cmd-result-desc">forecasts · temperature graph</div></div>
        <span class="cmd-result-kbd">⌘2</span>
      </div>
      <div class="cmd-result-item" data-href="{{ url_for('news.index') }}">
        <div class="cmd-result-icon">◈</div>
        <div><div class="cmd-result-name">News Feed</div><div class="cmd-result-desc">headlines · categories · filters</div></div>
        <span class="cmd-result-kbd">⌘3</span>
      </div>
      <div class="cmd-result-item" data-href="{{ url_for('github.index') }}">
        <div class="cmd-result-icon">◉</div>
        <div><div class="cmd-result-name">GitHub Explorer</div><div class="cmd-result-desc">trending repos · analytics</div></div>
        <span class="cmd-result-kbd">⌘4</span>
      </div>
      <div class="cmd-section-label">// ACTIONS</div>
      <div class="cmd-result-item" data-action="refresh">
        <div class="cmd-result-icon">↻</div>
        <div><div class="cmd-result-name">Refresh All Feeds</div><div class="cmd-result-desc">force sync all API modules</div></div>
        <span class="cmd-result-kbd">⌘R</span>
      </div>
    </div>
    <div class="cmd-footer">
      <span><kbd>↑↓</kbd> navigate</span>
      <span><kbd>↵</kbd> select</span>
      <span><kbd>esc</kbd> close</span>
      <span style="margin-left:auto">NEXUS CMD v1.0</span>
    </div>
  </div>
</div>

<div class="app-shell">
  <header class="topbar">
    <div class="logo">
      <div class="logo-mark">N</div>
      <span>NEXUS</span>
      <span class="logo-tag">v1.0</span>
    </div>
    <div class="topbar-center">
      <button class="cmd-trigger" id="cmdTriggerBtn">
        <span>❯ search or run command</span>
        <div class="kbd"><span>⌘</span><span>K</span></div>
      </button>
    </div>
    <div class="topbar-right">
      <div class="status-bar">
        <div class="status-dot"></div>
        <span>FEEDS LIVE</span>
      </div>
      <div class="topbar-time" id="topbarTime">--:--:--</div>
      <button class="icon-btn">⚙</button>
    </div>
  </header>

  <aside class="sidebar">
    <div class="nav-section-label">// INTELLIGENCE</div>
    <a class="nav-item {% if request.endpoint == 'main.index' %}active{% endif %}" href="{{ url_for('main.index') }}">
      <span class="nav-icon">⬛</span> Overview
    </a>
    <a class="nav-item {% if request.endpoint and 'crypto' in request.endpoint %}active{% endif %}" href="{{ url_for('crypto.index') }}">
      <span class="nav-icon">₿</span> Crypto
      <span class="nav-badge">LIVE</span>
    </a>
    <a class="nav-item {% if request.endpoint and 'weather' in request.endpoint %}active{% endif %}" href="{{ url_for('weather.index') }}">
      <span class="nav-icon">⛅</span> Weather
    </a>
    <a class="nav-item {% if request.endpoint and 'news' in request.endpoint %}active{% endif %}" href="{{ url_for('news.index') }}">
      <span class="nav-icon">◈</span> News Feed
    </a>
    <a class="nav-item {% if request.endpoint and 'github' in request.endpoint %}active{% endif %}" href="{{ url_for('github.index') }}">
      <span class="nav-icon">◉</span> GitHub
    </a>
    <div class="nav-section-label" style="margin-top:auto">// COMING SOON</div>
    <div class="nav-item" style="opacity:.4;cursor:not-allowed">
      <span class="nav-icon">📈</span> Stocks
      <span class="nav-badge" style="background:rgba(255,183,0,.1);color:var(--amber);border-color:rgba(255,183,0,.2)">SOON</span>
    </div>
    <div class="sidebar-footer">
      <div class="sys-status">
        <div>> NEWSAPI &nbsp;&nbsp;&nbsp;<span class="ok">■ OK</span></div>
        <div>> WEATHER &nbsp;&nbsp;<span class="ok">■ OK</span></div>
        <div>> COINGECKO <span class="ok">■ OK</span></div>
        <div>> GITHUB &nbsp;&nbsp;&nbsp;<span class="ok">■ OK</span></div>
      </div>
    </div>
  </aside>

  <main class="main-content">
    {% block content %}{% endblock %}
  </main>
</div>

<div class="terminal-log">
  <div class="log-prefix">❯ LIVE</div>
  <div class="log-ticker">
    <div class="log-ticker-inner">
      {% block ticker %}<span class="log-item">NEXUS INTELLIGENCE DASHBOARD · ALL SYSTEMS OPERATIONAL</span>{% endblock %}
    </div>
  </div>
</div>

<script>
(function(){
  function tick(){
    var n=new Date(),h=String(n.getHours()).padStart(2,'0'),m=String(n.getMinutes()).padStart(2,'0'),s=String(n.getSeconds()).padStart(2,'0');
    var el=document.getElementById('topbarTime');
    if(el)el.textContent=h+':'+m+':'+s;
  }
  setInterval(tick,1000);tick();
})();
window.showToast=function(msg,type){
  type=type||'info';
  var c=document.getElementById('toastContainer');
  var t=document.createElement('div');
  t.className='toast '+type;
  t.innerHTML='<div class="toast-dot"></div><span>'+msg+'</span>';
  c.appendChild(t);
  requestAnimationFrame(function(){requestAnimationFrame(function(){t.classList.add('show')})});
  setTimeout(function(){t.classList.remove('show');setTimeout(function(){t.remove()},400)},3000);
};
var overlay=document.getElementById('cmdOverlay');
var cmdInput=document.getElementById('cmdInput');
document.getElementById('cmdTriggerBtn').addEventListener('click',function(){openCmd()});
function openCmd(){overlay.classList.add('open');setTimeout(function(){cmdInput.focus()},50)}
function closeCmd(){overlay.classList.remove('open');cmdInput.value=''}
overlay.addEventListener('click',function(e){if(e.target===overlay)closeCmd()});
document.addEventListener('keydown',function(e){
  if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault();overlay.classList.contains('open')?closeCmd():openCmd()}
  if(e.key==='Escape')closeCmd();
});
document.querySelectorAll('.cmd-result-item').forEach(function(item){
  item.addEventListener('click',function(){
    var href=item.dataset.href,action=item.dataset.action;
    closeCmd();
    if(href)window.location.href=href;
    else if(action==='refresh')window.location.reload();
  });
});
document.querySelectorAll('.panel-actions').forEach(function(g){
  g.querySelectorAll('.pill-btn').forEach(function(b){
    b.addEventListener('click',function(){
      g.querySelectorAll('.pill-btn').forEach(function(x){x.classList.remove('active')});
      b.classList.add('active');
    });
  });
});
</script>
{% block extra_js %}{% endblock %}
</body>
</html>
ENDHTML
echo "✅ base.html written"

pip show flask-limiter > /dev/null 2>&1 || pip install flask-limiter --break-system-packages 2>/dev/null

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅  NEXUS DARK GLASS TERMINAL DEPLOYED  ║"
echo "║                                          ║"
echo "║  Run:  python run.py                     ║"
echo "║  Open: http://localhost:5000             ║"
echo "╚══════════════════════════════════════════╝"
