<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>BaseLock — AI-Powered PostgreSQL Security</title>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
            color: #0b1120;
            line-height: 1.6;
        }

        /* Container */
        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }

        /* Header / Nav */
        .navbar {
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 0.75rem 0;
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(8px);
            background: rgba(255, 255, 255, 0.92);
        }

        .navbar .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 700;
            font-size: 1.4rem;
            color: #0b1120;
            text-decoration: none;
        }

        .logo i {
            color: #2563eb;
            font-size: 1.8rem;
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 2rem;
            list-style: none;
            font-weight: 500;
        }

        .nav-links a {
            text-decoration: none;
            color: #1e293b;
            transition: color 0.15s;
            font-size: 0.95rem;
        }

        .nav-links a:hover {
            color: #2563eb;
        }

        .btn-outline {
            border: 1px solid #cbd5e1;
            padding: 0.4rem 1.2rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            background: transparent;
            transition: all 0.15s;
            cursor: default;
        }

        .btn-primary {
            background: #2563eb;
            color: white !important;
            padding: 0.4rem 1.4rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            border: none;
            transition: background 0.15s;
            cursor: default;
        }

        .btn-primary:hover {
            background: #1d4ed8;
        }

        /* Hero */
        .hero {
            padding: 4rem 0 3rem;
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            border-bottom: 1px solid #e2e8f0;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            align-items: center;
        }

        .hero-badge {
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            padding: 0.25rem 1rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.3px;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }

        .hero h1 span {
            color: #2563eb;
        }

        .hero p {
            font-size: 1.2rem;
            color: #334155;
            max-width: 540px;
            margin-bottom: 2rem;
        }

        .hero-actions {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .hero-actions .btn-primary {
            padding: 0.7rem 2rem;
            font-size: 1rem;
        }

        .hero-actions .btn-outline {
            padding: 0.7rem 2rem;
            font-size: 1rem;
            border-color: #94a3b8;
        }

        .hero-stats {
            display: flex;
            gap: 2.5rem;
            margin-top: 2.5rem;
        }

        .hero-stats div {
            display: flex;
            flex-direction: column;
        }

        .hero-stats .number {
            font-size: 1.6rem;
            font-weight: 700;
            color: #0b1120;
        }

        .hero-stats .label {
            font-size: 0.85rem;
            color: #475569;
        }

        .hero-visual {
            background: white;
            border-radius: 1.5rem;
            padding: 2rem;
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.12);
            border: 1px solid #e2e8f0;
        }

        .hero-visual pre {
            background: #0b1120;
            color: #e2e8f0;
            padding: 1.25rem;
            border-radius: 0.75rem;
            font-size: 0.85rem;
            overflow-x: auto;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
        }

        .hero-visual .sql-keyword {
            color: #60a5fa;
        }
        .hero-visual .sql-string {
            color: #a7f3d0;
        }
        .hero-visual .sql-comment {
            color: #94a3b8;
        }

        /* Section titles */
        .section-title {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }

        .section-sub {
            color: #475569;
            font-size: 1.1rem;
            margin-bottom: 2.5rem;
        }

        /* Cards */
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 2rem;
            margin: 2.5rem 0 1rem;
        }

        .card {
            background: white;
            border-radius: 1.25rem;
            padding: 1.8rem 1.8rem 2rem;
            border: 1px solid #e2e8f0;
            transition: all 0.2s;
            box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        }

        .card:hover {
            border-color: #b9d0f0;
            box-shadow: 0 12px 24px -10px rgba(37, 99, 235, 0.08);
        }

        .card .icon {
            font-size: 2.2rem;
            color: #2563eb;
            margin-bottom: 0.75rem;
        }

        .card h3 {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .card p {
            color: #475569;
            font-size: 0.95rem;
        }

        .card .tag {
            display: inline-block;
            background: #eef2ff;
            color: #1e40af;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.8rem;
            border-radius: 9999px;
            margin-top: 0.75rem;
            letter-spacing: 0.3px;
        }

        /* Architecture diagram (simple) */
        .arch-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            background: white;
            padding: 2rem;
            border-radius: 1.5rem;
            border: 1px solid #e2e8f0;
            margin: 2rem 0 1rem;
        }

        .arch-item {
            text-align: center;
            padding: 1rem 0.5rem;
            border-radius: 0.75rem;
            background: #f8fafc;
            border: 1px solid #eef2f6;
        }

        .arch-item i {
            font-size: 2rem;
            color: #2563eb;
            margin-bottom: 0.4rem;
        }

        .arch-item .label {
            font-weight: 600;
            font-size: 0.9rem;
        }

        .arch-item .sub {
            font-size: 0.75rem;
            color: #64748b;
        }

        .arch-arrow {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 1.2rem;
        }

        /* Metrics / chart row */
        .metrics-row {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
            margin: 2.5rem 0;
        }

        .chart-box {
            background: white;
            border-radius: 1.25rem;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
        }

        .chart-box h4 {
            margin-bottom: 1rem;
            font-weight: 600;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .stat-item {
            background: white;
            border-radius: 1rem;
            padding: 1.2rem;
            border: 1px solid #e2e8f0;
            text-align: center;
        }

        .stat-item .value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0b1120;
        }

        .stat-item .desc {
            font-size: 0.8rem;
            color: #64748b;
        }

        .stat-item .trend {
            color: #059669;
            font-size: 0.8rem;
            font-weight: 500;
        }

        /* Roadmap */
        .roadmap {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin: 2rem 0 1rem;
        }

        .roadmap-item {
            background: white;
            padding: 1.5rem;
            border-radius: 1.25rem;
            border: 1px solid #e2e8f0;
            border-top: 4px solid #2563eb;
        }

        .roadmap-item .phase {
            font-weight: 700;
            color: #2563eb;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }

        .roadmap-item ul {
            list-style: none;
            margin-top: 0.75rem;
        }

        .roadmap-item ul li {
            padding: 0.25rem 0;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .roadmap-item ul li i {
            color: #2563eb;
            font-size: 0.8rem;
            width: 1.2rem;
        }

        /* Footer */
        .footer {
            background: white;
            border-top: 1px solid #e2e8f0;
            padding: 2.5rem 0;
            margin-top: 3rem;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 2rem;
        }

        .footer h5 {
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .footer a {
            display: block;
            color: #475569;
            text-decoration: none;
            font-size: 0.9rem;
            padding: 0.2rem 0;
        }

        .footer a:hover {
            color: #2563eb;
        }

        .footer-bottom {
            border-top: 1px solid #eef2f6;
            margin-top: 2rem;
            padding-top: 1.5rem;
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #64748b;
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }
            .hero h1 {
                font-size: 2.6rem;
            }
            .arch-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .arch-arrow {
                display: none;
            }
            .metrics-row {
                grid-template-columns: 1fr;
            }
            .roadmap {
                grid-template-columns: 1fr;
            }
            .footer-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 640px) {
            .nav-links {
                gap: 1rem;
                font-size: 0.85rem;
                flex-wrap: wrap;
            }
            .hero h1 {
                font-size: 2rem;
            }
            .hero-stats {
                flex-wrap: wrap;
                gap: 1.5rem;
            }
            .footer-grid {
                grid-template-columns: 1fr;
            }
            .footer-bottom {
                flex-direction: column;
                gap: 0.5rem;
            }
        }

        .mt-1 {
            margin-top: 1rem;
        }
        .mt-2 {
            margin-top: 2rem;
        }
        .mb-1 {
            margin-bottom: 1rem;
        }
        .text-center {
            text-align: center;
        }
        .pill {
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            padding: 0.2rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: 0.5rem;
        }
        .flex {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
    </style>
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar">
    <div class="container">
        <a href="#" class="logo">
            <i class="fas fa-shield-halved"></i> BaseLock
        </a>
        <ul class="nav-links">
            <li><a href="#">Product</a></li>
            <li><a href="#">Docs</a></li>
            <li><a href="#">Security</a></li>
            <li><a href="#" class="btn-outline">Log in</a></li>
            <li><a href="#" class="btn-primary">Start Free</a></li>
        </ul>
    </div>
</nav>

<!-- HERO -->
<section class="hero">
    <div class="container hero-grid">
        <div>
            <span class="hero-badge"><i class="fas fa-robot" style="margin-right: 6px;"></i> AI-Powered RLS Engine</span>
            <h1>Secure PostgreSQL <span>RLS</span> with Confidence</h1>
            <p>Generate, validate, and simulate Row-Level Security policies before they hit production. Prevent cross-tenant leaks and privilege escalation.</p>
            <div class="hero-actions">
                <a href="#" class="btn-primary"><i class="fas fa-rocket" style="margin-right: 8px;"></i> Get Started</a>
                <a href="#" class="btn-outline"><i class="fas fa-play" style="margin-right: 8px;"></i> See Demo</a>
            </div>
            <div class="hero-stats">
                <div><span class="number">100%</span><span class="label">Deterministic generation</span></div>
                <div><span class="number">0</span><span class="label">False positives in validation</span></div>
                <div><span class="number">&lt; 2s</span><span class="label">Policy synthesis</span></div>
            </div>
        </div>
        <div class="hero-visual">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                <span style="font-weight:600; font-size:0.9rem;">⬡ Generated RLS Policy</span>
                <span style="font-size:0.75rem; color:#64748b;"><i class="far fa-check-circle" style="color:#059669;"></i> Validated ✓</span>
            </div>
            <pre><span class="sql-comment">-- tenant isolation policy</span>
<span class="sql-keyword">CREATE POLICY</span> tenant_isolation
<span class="sql-keyword">ON</span> orders
<span class="sql-keyword">USING</span> (
    tenant_id = current_setting(<span class="sql-string">'app.tenant_id'</span>)::UUID
);
<span class="sql-keyword">WITH CHECK</span> (
    tenant_id = current_setting(<span class="sql-string">'app.tenant_id'</span>)::UUID
);
<span class="sql-comment">-- ✅ No OR bypass | ✅ No privilege escalation</span></pre>
            <div style="display:flex; gap:1.5rem; margin-top:1rem; font-size:0.85rem; color:#475569;">
                <span><i class="fas fa-check-circle" style="color:#059669;"></i> Intent-aware validation</span>
                <span><i class="fas fa-vial" style="color:#2563eb;"></i> 142 attack scenarios simulated</span>
            </div>
        </div>
    </div>
</section>

<!-- CORE CAPABILITIES -->
<section class="container" style="padding: 3rem 0 1rem;">
    <h2 class="section-title">Core Capabilities</h2>
    <p class="section-sub">Deterministic generation · Intent validation · Sandboxed simulation · Policy learning</p>
    <div class="cards-grid">
        <div class="card">
            <div class="icon"><i class="fas fa-code"></i></div>
            <h3>Deterministic Policy Generation</h3>
            <p>Synthesizes PostgreSQL RLS policies from structured business requirements. No hallucinations, consistent outputs.</p>
            <span class="tag"><i class="fas fa-check"></i> Production-ready</span>
        </div>
        <div class="card">
            <div class="icon"><i class="fas fa-eye"></i></div>
            <h3>Intent-Aware Validation</h3>
            <p>Detects unsafe logic patterns, disjunction-based bypass attempts, and structural weaknesses before deployment.</p>
            <span class="tag"><i class="fas fa-shield"></i> Security-first</span>
        </div>
        <div class="card">
            <div class="icon"><i class="fas fa-user-secret"></i></div>
            <h3>Sandboxed Identity Simulation</h3>
            <p>Tests policies across simulated user identities to confirm tenant isolation and access enforcement under attack.</p>
            <span class="tag"><i class="fas fa-bug"></i> Attack simulation</span>
        </div>
        <div class="card">
            <div class="icon"><i class="fas fa-brain"></i></div>
            <h3>Policy Learning &amp; Retrieval</h3>
            <p>Uses historical patterns and pgvector similarity to improve policy quality, consistency, and reuse over time.</p>
            <span class="tag"><i class="fas fa-database"></i> pgvector</span>
        </div>
    </div>
</section>

<!-- TECHNICAL ARCHITECTURE -->
<section class="container" style="padding: 2rem 0;">
    <h2 class="section-title">Technical Architecture</h2>
    <p class="section-sub">FastAPI + Pydantic · PostgreSQL 14+ with pgvector · Groq Llama 3.1</p>

    <div class="arch-grid">
        <div class="arch-item">
            <i class="fas fa-code"></i>
            <div class="label">Backend</div>
            <div class="sub">FastAPI + Pydantic v2</div>
        </div>
        <div class="arch-arrow"><i class="fas fa-arrow-right"></i></div>
        <div class="arch-item">
            <i class="fas fa-database"></i>
            <div class="label">Database</div>
            <div class="sub">PostgreSQL 14+ / pgvector</div>
        </div>
        <div class="arch-arrow"><i class="fas fa-arrow-right"></i></div>
        <div class="arch-item">
            <i class="fas fa-microchip"></i>
            <div class="label">Inference</div>
            <div class="sub">Groq Llama 3.1 (70B)</div>
        </div>
        <div class="arch-arrow"><i class="fas fa-arrow-right"></i></div>
        <div class="arch-item">
            <i class="fas fa-chart-simple"></i>
            <div class="label">Dashboard</div>
            <div class="sub">Vanilla JS + Chart.js</div>
        </div>
    </div>
    <div style="text-align:center; font-size:0.9rem; color:#475569; background:#f1f5f9; padding:0.5rem; border-radius:9999px; max-width:400px; margin:0 auto;">
        <i class="fas fa-lock" style="color:#2563eb;"></i> Deterministic generation · security-first validation
    </div>
</section>

<!-- METRICS + CHART -->
<section class="container">
    <div class="metrics-row">
        <div class="chart-box">
            <h4><i class="fas fa-chart-bar" style="margin-right:8px; color:#2563eb;"></i> Validation Performance (last 7 days)</h4>
            <canvas id="validationChart" height="140"></canvas>
            <div style="display:flex; gap:1.5rem; margin-top:0.75rem; font-size:0.8rem; color:#475569;">
                <span><span style="display:inline-block; width:12px; height:12px; background:#2563eb; border-radius:4px;"></span> Policies validated</span>
                <span><span style="display:inline-block; width:12px; height:12px; background:#f97316; border-radius:4px;"></span> Bypass attempts caught</span>
            </div>
        </div>
        <div>
            <div class="stat-grid">
                <div class="stat-item">
                    <div class="value">2.3k</div>
                    <div class="desc">Policies generated</div>
                    <div class="trend"><i class="fas fa-arrow-up"></i> 18%</div>
                </div>
                <div class="stat-item">
                    <div class="value">47</div>
                    <div class="desc">Vulnerabilities found</div>
                    <div class="trend" style="color:#dc2626;"><i class="fas fa-exclamation-triangle"></i> 9 critical</div>
                </div>
                <div class="stat-item">
                    <div class="value">99.8%</div>
                    <div class="desc">Simulation accuracy</div>
                    <div class="trend"><i class="fas fa-check"></i> Verified</div>
                </div>
                <div class="stat-item">
                    <div class="value">142</div>
                    <div class="desc">Attack scenarios</div>
                    <div class="trend"><i class="fas fa-shield"></i> Covered</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ROADMAP -->
<section class="container" style="padding: 2rem 0;">
    <h2 class="section-title">Roadmap</h2>
    <p class="section-sub">Building the security layer every multi-tenant app needs.</p>
    <div class="roadmap">
        <div class="roadmap-item">
            <div class="phase">Q4 2024 · MVP</div>
            <ul>
                <li><i class="fas fa-check-circle" style="color:#059669;"></i> Deterministic policy generation</li>
                <li><i class="fas fa-check-circle" style="color:#059669;"></i> Basic validation engine</li>
                <li><i class="fas fa-check-circle" style="color:#059669;"></i> Simple dashboard</li>
                <li><i class="fas fa-check-circle" style="color:#059669;"></i> Initial simulation capability</li>
            </ul>
        </div>
        <div class="roadmap-item" style="border-top-color:#f97316;">
            <div class="phase" style="color:#f97316;">Q1 2025 · Beta</div>
            <ul>
                <li><i class="fas fa-spinner" style="color:#f97316;"></i> Advanced attack pattern detection</li>
                <li><i class="fas fa-spinner" style="color:#f97316;"></i> Policy versioning &amp; rollback</li>
                <li><i class="fas fa-spinner" style="color:#f97316;"></i> CI/CD pipeline integration</li>
                <li><i class="fas fa-spinner" style="color:#f97316;"></i> Enterprise audit compliance</li>
            </ul>
        </div>
        <div class="roadmap-item" style="border-top-color:#7c3aed;">
            <div class="phase" style="color:#7c3aed;">Q2 2025 · GA</div>
            <ul>
                <li><i class="fas fa-rocket" style="color:#7c3aed;"></i> ML for policy recommendations</li>
                <li><i class="fas fa-rocket" style="color:#7c3aed;"></i> Multi-cloud deployment</li>
                <li><i class="fas fa-rocket" style="color:#7c3aed;"></i> Advanced threat intelligence</li>
                <li><i class="fas fa-rocket" style="color:#7c3aed;"></i> SOC 2 compliance package</li>
            </ul>
        </div>
    </div>
</section>

<!-- VALUE PROPOSITION -->
<section class="container" style="padding: 2rem 0 1rem;">
    <div style="background: linear-gradient(135deg, #0b1120 0%, #1e293b 100%); color: white; border-radius: 2rem; padding: 3rem 2.5rem; text-align: center;">
        <h2 style="font-size:2.2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.75rem;">Reduce security failures before they happen</h2>
        <p style="font-size:1.1rem; color:#cbd5e1; max-width:700px; margin:0 auto 1.5rem;">BaseLock moves policy creation and verification earlier in the development workflow. Generate, test, and deploy RLS policies with higher confidence.</p>
        <div style="display:flex; gap:2rem; justify-content:center; flex-wrap:wrap; font-size:0.95rem;">
            <span><i class="fas fa-check-circle" style="color:#34d399;"></i> Repeatable security</span>
            <span><i class="fas fa-check-circle" style="color:#34d399;"></i> Adversarial testing</span>
            <span><i class="fas fa-check-circle" style="color:#34d399;"></i> Production-ready policies</span>
        </div>
        <div style="margin-top: 2rem;">
            <a href="#" class="btn-primary" style="background:#2563eb; color:white !important; padding:0.7rem 2.2rem; border-radius:9999px; text-decoration:none; font-weight:600;">Start Free</a>
            <span style="margin-left:1rem; font-size:0.9rem; color:#94a3b8;">No credit card required</span>
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div>
                <div class="logo" style="margin-bottom:0.5rem;"><i class="fas fa-shield-halved"></i> BaseLock</div>
                <p style="color:#475569; font-size:0.9rem; max-width:260px;">AI-powered security validation for PostgreSQL RLS. Built for modern SaaS and multi-tenant systems.</p>
                <div style="display:flex; gap:1rem; margin-top:1rem;">
                    <a href="#" style="color:#475569;"><i class="fab fa-github"></i></a>
                    <a href="#" style="color:#475569;"><i class="fab fa-twitter"></i></a>
                    <a href="#" style="color:#475569;"><i class="fab fa-linkedin"></i></a>
                    <a href="#" style="color:#475569;"><i class="fab fa-discord"></i></a>
                </div>
            </div>
            <div>
                <h5>Product</h5>
                <a href="#">Features</a>
                <a href="#">Docs</a>
                <a href="#">Security</a>
                <a href="#">Pricing</a>
            </div>
            <div>
                <h5>Company</h5>
                <a href="#">About</a>
                <a href="#">Blog</a>
                <a href="#">Careers</a>
                <a href="#">Contact</a>
            </div>
            <div>
                <h5>Support</h5>
                <a href="#">Help Center</a>
                <a href="#">Community</a>
                <a href="#">Status</a>
                <a href="#">Privacy</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 BaseLock. MIT License.</span>
            <span><i class="fas fa-lock" style="margin-right:4px;"></i> Built with ❤️ for secure databases</span>
        </div>
    </div>
</footer>

<!-- CHART.JS SCRIPT -->
<script>
    document.addEventListener('DOMContentLoaded', function () {
        const ctx = document.getElementById('validationChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Policies validated',
                    data: [18, 24, 30, 22, 36, 28, 42],
                    backgroundColor: '#2563eb',
                    borderRadius: 6,
                    barPercentage: 0.6,
                },
                {
                    label: 'Bypass attempts caught',
                    data: [3, 5, 7, 4, 9, 6, 11],
                    backgroundColor: '#f97316',
                    borderRadius: 6,
                    barPercentage: 0.6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#eef2f6',
                        },
                        ticks: {
                            stepSize: 10,
                        }
                    },
                    x: {
                        grid: {
                            display: false,
                        }
                    }
                },
                datasets: {
                    bar: {
                        borderSkipped: false,
                    }
                }
            }
        });
    });
</script>

</body>
</html>
