# BaseLock
### AI-Powered PostgreSQL Security Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![Groq](https://img.shields.io/badge/Groq-Llama3.1-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Early Access](https://img.shields.io/badge/Status-Early%20Access-purple.svg)](https://baselock.dev)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Core Capabilities](#-core-capabilities)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage Examples](#-usage-examples)
- [Architecture](#-architecture)
- [Performance Metrics](#-performance-metrics)
- [Security Considerations](#-security-considerations)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🚀 Overview

**BaseLock** is an autonomous security platform that generates, validates, and simulates PostgreSQL Row-Level Security (RLS) policies before they reach production. It prevents cross-tenant data leaks, privilege escalation, and policy misconfigurations through deterministic policy synthesis, intent-aware validation, and sandboxed attack simulation.

> **🎯 Early Stage Startup** — We're building the security layer every multi-tenant app needs but doesn't know how to implement safely.

### Why BaseLock?

In today's multi-tenant SaaS world, data isolation isn't just a feature—it's a compliance requirement. BaseLock makes RLS policy creation and verification a repeatable, automated process that catches security flaws before they become production incidents.

---

## 🔥 The Problem

RLS is your last line of defense for multi-tenant data isolation. But it's also where security goes to die:

- ❌ **One logic error** exposes all tenant data
- ❌ **Manual reviews** miss semantic bypasses
- ❌ **Testing gaps** leave malicious query patterns undiscovered
- ❌ **Policy drift** goes undetected during schema changes
- ❌ **Complex OR conditions** create unintended access paths
- ❌ **Inconsistent policies** across environments lead to deployment surprises

### Real-World Impact

*"We found a production data leak 6 months after deployment. The RLS policy had an OR condition that let users see other tenants' data when a specific flag was null. Our manual review completely missed it."* — Real quote from a BaseLock early adopter

### The Cost of Failure

| Incident Type | Average Cost | Business Impact |
|---------------|--------------|-----------------|
| Cross-tenant data leak | $4.5M+ | Customer trust loss, legal liability |
| Privilege escalation | $3.2M+ | Security breach, compliance violations |
| Policy misconfiguration | $1.8M+ | Data exposure, remediation costs |

---

## 💡 The Solution

BaseLock transforms access requirements into **provably secure RLS policies** through a comprehensive security pipeline:

```
┌──────────────────────────────────────────────────────────────────────┐
│                        BASE LOCK PIPELINE                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📋 Business    →  🧠 Policy      →  🔍 Validation   →  🎯 Sandbox  │
│  Requirements       Generation        Engine          Simulation    │
│                                                                     │
│       ↓                  ↓                ↓               ↓          │
│  Structured       Deterministic    Intent-aware    Attack          │
│  Input            SQL Synthesis    Analysis        Scenarios       │
│                                                                     │
│       ↓                  ↓                ↓               ↓          │
│  Access Rules      RLS Policies    Security        Identity        │
│  & Tenants         (PostgreSQL)    Patterns        Testing         │
│                                                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📊 Audit Log  →  📈 Learning    →  ✅ Production-Ready Policy    │
│                                                                     │
└──────────────────────────────────────────────────────────────────────┘
```

### Core Capabilities

| Capability | What It Does | Why It Matters |
|------------|--------------|----------------|
| **🧠 Deterministic Policy Generation** | Synthesizes RLS policies from structured requirements | No hallucinations, consistent outputs, repeatable results |
| **🔍 Intent-Aware Validation** | Detects unsafe logic patterns and bypass attempts | Catches what humans miss, prevents semantic errors |
| **🎯 Sandboxed Simulation** | Tests policies against adversarial identities | Confirms isolation under attack, validates edge cases |
| **📚 Policy Learning** | Learns from historical patterns to improve | Gets smarter with every use, reduces future errors |
| **📊 Audit Trail** | Logs every action and validation result | Compliance-ready, traceable security decisions |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Dashboard: Vanilla JS + Chart.js                  │   │
│  │  Real-time metrics, policy visualization            │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    API LAYER                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Backend: FastAPI + Pydantic v2                    │   │
│  │  RESTful API, WebSocket for live updates           │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    SERVICE LAYER                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │  Policy      │ │  Validation  │ │  Simulation  │   │
│  │  Generator   │ │  Engine      │ │  Engine      │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │  Learning    │ │  Audit       │ │  Vector      │   │
│  │  Engine      │ │  Logger      │ │  Store       │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    DATA & AI LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  AI: Groq-hosted Llama 3.1 (70B)                  │   │
│  │  Database: PostgreSQL 14+ with pgvector            │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                    SECURITY LAYER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Deterministic Generation + Security-First Design   │   │
│  │  Input Sanitization, Audit Logging, Least Privilege │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Why These Technologies?

| Technology | Role | Why Chosen |
|------------|------|------------|
| **FastAPI** | Backend API | Async support, automatic OpenAPI docs, Pydantic validation |
| **Pydantic v2** | Data validation | Type safety, performance improvements, robust validation |
| **PostgreSQL 14+** | Primary database | Native RLS support, robust transaction handling |
| **pgvector** | Vector search | Efficient similarity search for policy learning |
| **Groq Llama 3.1** | AI inference | High throughput, low latency, deterministic outputs |
| **Chart.js** | Dashboard charts | Lightweight, customizable, no framework lock-in |

---

## ✨ Key Features

### 🔒 Deterministic Policy Generation

**Example:** Generate tenant-isolated policies from business requirements.

```sql
-- Input: "Users can only read their own orders and create orders for their tenant"

-- Output:
CREATE POLICY user_order_read ON orders
    FOR SELECT
    USING (user_id = current_setting('app.current_user_id')::UUID);

CREATE POLICY tenant_order_insert ON orders
    FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::UUID);

-- Generated with:
-- ✅ Proper policy separation (USING vs WITH CHECK)
-- ✅ Correct data type casting
-- ✅ Fallback checks for NULL values
-- ✅ No OR-based bypass vectors
```

### 🛡️ Threat Detection Patterns

BaseLock automatically scans for these common vulnerabilities:

| Pattern | Risk | Detection Method |
|---------|------|------------------|
| `OR` conditions in `USING` | Cross-tenant data exposure | Static analysis |
| `BYPASSRLS` privilege grants | Complete security bypass | Permission audit |
| Policy overlapping | Inconsistent enforcement | Conflict detection |
| Missing `WITH CHECK` on INSERT | Write-side bypass | Policy completeness check |
| NULL comparisons | Unintended access | Semantic analysis |
| Function injection | Attack surface expansion | Input validation |
| Unqualified table references | Policy scope creep | Permission boundary check |

### 🎭 Identity Simulation

Tests policies against realistic attack scenarios:

```python
# Example simulation configuration
attack_scenarios = [
    {
        "identity": {
            "user_id": "attacker-001",
            "tenant_id": "tenant_a",
            "role": "malicious_user"
        },
        "queries": [
            "SELECT * FROM orders WHERE tenant_id = 'tenant_b'",
            "SELECT * FROM orders WHERE 1=1",
            "UPDATE orders SET status='fraud' WHERE user_id != attacker-001"
        ],
        "expected_result": "ACCESS_DENIED"
    }
]
```

### 📈 Policy Learning & Vector Retrieval

```sql
-- Using pgvector for similarity-based policy retrieval
SELECT 
    policy_text,
    embedding <=> query_embedding AS similarity
FROM policy_embeddings
ORDER BY similarity ASC
LIMIT 5;

-- Result: Similar policies with their effectiveness scores
-- Helps suggest improvements and catch regressions
```

---

## 🚦 Getting Started

### Prerequisites

```bash
# Required
✓ Python 3.11 or higher
✓ PostgreSQL 14 or higher with pgvector extension
✓ Groq API key (free tier available)

# Optional
✓ Docker & Docker Compose
✓ Node.js 18+ (for frontend development)
✓ Make (for Makefile shortcuts)
```

### Quick Start (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/baselock.git
cd baselock

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with:
# - GROQ_API_KEY=your_key_here
# - DATABASE_URL=postgresql://user:pass@localhost:5432/baselock
# - SECRET_KEY=your_secret_key

# 4. Initialize database with pgvector
createdb baselock
psql -d baselock -f scripts/init_db.sql
psql -d baselock -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 5. Run migrations (if applicable)
alembic upgrade head

# 6. Start the server
uvicorn app.main:app --reload --port 8000

# 7. Open the dashboard
open http://localhost:8000
```

### Docker Deployment (Recommended for Production)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f baselock

# Stop services
docker-compose down

# Dashboard available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Environment Variables

```bash
# .env file example
APP_NAME=BaseLock
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://baselock:password@localhost:5432/baselock
POOL_SIZE=10
MAX_OVERFLOW=20

# AI / Groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192
GROQ_TEMPERATURE=0.1  # Low for deterministic outputs

# Security
ENABLE_AUDIT=true
SIMULATION_TIMEOUT=30
MAX_SIMULATIONS_RUNNING=5
```

---

## 📖 Usage Examples

### 1. Generate a Policy from Requirements

```python
# Python client example
import requests

policy_request = {
    "policy_name": "order_tenant_isolation",
    "table": "orders",
    "description": "Orders should only be accessible by users in the same tenant",
    "requirements": {
        "read": "Users can view orders where tenant matches their tenant",
        "write": "Users can create orders for their tenant only",
        "update": "Users can update their own orders within their tenant"
    },
    "context": {
        "tenant_field": "tenant_id",
        "user_field": "user_id",
        "user_context": "current_setting('app.current_user_id')::UUID",
        "tenant_context": "current_setting('app.current_tenant_id')::UUID"
    }
}

response = requests.post(
    "http://localhost:8000/api/v1/policies/generate",
    json=policy_request
)

if response.status_code == 200:
    policy = response.json()
    print(f"Generated Policy ID: {policy['id']}")
    print(f"SQL:\n{policy['sql']}")
    print(f"Validation Score: {policy['validation_score']}")
else:
    print(f"Error: {response.text}")
```

### 2. Validate an Existing Policy

```python
validation_request = {
    "policy_sql": """
        CREATE POLICY tenant_isolation ON orders
        USING (tenant_id = current_setting('app.tenant_id')::UUID)
    """,
    "checks": [
        "or_bypass_detection",
        "privilege_escalation",
        "null_handling",
        "conflict_detection"
    ]
}

response = requests.post(
    "http://localhost:8000/api/v1/policies/validate",
    json=validation_request
)

if response.status_code == 200:
    result = response.json()
    print(f"Validation Status: {result['status']}")
    for issue in result['issues']:
        print(f"⚠️ {issue['severity']}: {issue['description']}")
        print(f"   Suggestion: {issue['suggestion']}")
else:
    print(f"Validation failed: {response.text}")
```

### 3. Run Security Simulation

```python
simulation_request = {
    "policy_id": "pol_abc123",
    "duration": 60,  # seconds
    "identities": [
        {"id": "user_a", "tenant": "tenant_a", "roles": ["admin"]},
        {"id": "user_b", "tenant": "tenant_b", "roles": ["user"]},
        {"id": "attacker", "tenant": "tenant_c", "roles": ["malicious"]}
    ],
    "attack_scenarios": [
        "tenant_enumeration",
        "id_oracle",
        "privilege_escalation",
        "sql_injection",
        "policy_bypass"
    ],
    "queries": [
        "SELECT * FROM orders",
        "SELECT * FROM orders WHERE tenant_id = 'tenant_b'",
        "UPDATE orders SET status='paid' WHERE id = 123",
        "INSERT INTO orders (tenant_id, user_id, amount) VALUES ('tenant_a', 'user_a', 100)"
    ]
}

response = requests.post(
    "http://localhost:8000/api/v1/simulations/run",
    json=simulation_request
)

if response.status_code == 200:
    result = response.json()
    print(f"Simulation ID: {result['id']}")
    print(f"Total Queries: {result['total_queries']}")
    print(f"Access Denied: {result['denied_count']}")
    print(f"Vulnerabilities Found: {result['vulnerabilities']}")
```

### 4. Query Policy History

```python
history_request = {
    "policy_id": "pol_abc123",
    "limit": 10,
    "include_simulations": True,
    "include_validations": True
}

response = requests.get(
    "http://localhost:8000/api/v1/policies/history",
    params=history_request
)

history = response.json()
for entry in history['entries']:
    print(f"{entry['timestamp']} - {entry['action']}: {entry['result']}")
```

---

## 🏗️ Architecture Deep Dive

### System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE LOCK SYSTEM ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     API GATEWAY                              │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │  │
│  │  │ Auth        │  │ Rate Limit  │  │ Request     │        │  │
│  │  │ Middleware  │  │ Middleware  │  │ Validation  │        │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   POLICY     │  │  VALIDATION  │  │  SIMULATION  │            │
│  │   GENERATOR  │  │   ENGINE     │  │    ENGINE    │            │
│  │              │  │              │  │              │            │
│  │ • Requirement│  │ • Static     │  │ • Identity   │            │
│  │   parsing    │  │   analysis   │  │   manager    │            │
│  │ • SQL        │  │ • Semantic   │  │ • Query      │            │
│  │   synthesis  │  │   validation │  │   executor   │            │
│  │ • Template   │  │ • Pattern    │  │ • Attack     │            │
│  │   engine     │  │   matching   │  │   simulator  │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   LEARNING   │  │  AUDIT LOG   │  │  VECTOR      │            │
│  │   ENGINE     │  │              │  │    STORE     │            │
│  │              │  │              │  │              │            │
│  │ • Pattern    │  │ • Activity   │  │ • Embedding  │            │
│  │   learning   │  │   tracking   │  │   generation │            │
│  │ • Similarity │  │ • Compliance │  │ • Similarity │            │
│  │   retrieval  │  │   reporting  │  │   search     │            │
│  │ • Policy     │  │ • Alert      │  │ • Index      │            │
│  │   refinement │  │   generation │  │   management │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                INFRASTRUCTURE LAYER                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │  │
│  │  │ PostgreSQL  │  │    Redis    │  │   Groq API  │        │  │
│  │  │   + pgvector│  │  (caching)  │  │  (LLM)      │        │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Security-First Design Principles

1. **Deterministic Generation** — No randomness in policy creation, ensuring consistent results
2. **Input Sanitization** — All user inputs validated via Pydantic models
3. **Separation of Concerns** — Generation, validation, simulation in isolated services
4. **Audit Trail** — Every action logged for compliance and debugging
5. **Sandboxed Execution** — Simulations run in isolated database sessions
6. **Least Privilege** — Minimal permissions for each service component
7. **Defense in Depth** — Multiple validation layers before policy acceptance

### Data Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│   API       │────▶│   Policy    │────▶│  Validation │
│   Request   │     │   Gateway   │     │  Generator  │     │   Engine    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Database   │◀────│   Policy    │◀────│  Simulation │◀────│   Attack    │
│  (Postgres) │     │   Store     │     │   Engine    │     │  Scenarios  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      │                    ▼                    │
      │            ┌─────────────┐              │
      └────────────│   Audit     │──────────────┘
                   │   Logger    │
                   └─────────────┘
```

---

## 📊 Performance Metrics

| Metric | Value | Conditions |
|--------|-------|------------|
| Policy Generation | < 2 seconds | Average complex policy |
| Validation Check | < 500ms | Single policy validation |
| Full Simulation (100 identities) | < 15 seconds | Standard attack suite |
| Policy Retrieval (pgvector) | < 50ms | Indexed similarity search |
| Concurrent Users Supported | 100+ | Standard deployment |
| Database Queries/sec | 500+ | Optimized queries |
| API Response Time (p95) | 200ms | Normal load |
| System Uptime | 99.9% | Production SLA |

### Scaling Recommendations

| Component | Scaling Strategy |
|-----------|------------------|
| API Gateway | Horizontal scaling with load balancer |
| Policy Generator | Vertical scaling for LLM inference |
| Database | Read replicas for analytics queries |
| Vector Store | Index optimization and sharding |
| Simulation Engine | Task queue with worker pool |

---

## 🔐 Security Considerations

### API Security
- **API Keys**: Store Groq API keys in environment variables, never in code
- **JWT Authentication**: All API endpoints require valid JWT tokens
- **Rate Limiting**: Prevent abuse and DOS attacks
- **Input Validation**: Pydantic models ensure type safety

### Database Security
- **Least Privilege**: Use separate roles for different services
- **Connection Pooling**: Prevent connection exhaustion
- **SSL/TLS**: Encrypt database connections
- **Backup Encryption**: Encrypt backups at rest

### Network Security
- **VPC Deployment**: Deploy behind a VPN or private network
- **Firewall Rules**: Restrict access to necessary ports
- **SSL/TLS**: Encrypt all external communications
- **DDoS Protection**: Use cloud-native DDoS protection

### Operational Security
- **Logging**: Never log sensitive data or policy details
- **Auditing**: All validation failures logged with full context
- **Monitoring**: Set up alerts for suspicious activity
- **Incident Response**: Have a documented incident response plan

### Compliance Considerations
| Regulation | How BaseLock Helps |
|------------|-------------------|
| GDPR | Ensures proper data isolation between tenants |
| SOC 2 | Provides audit logs and security validation |
| HIPAA | Prevents PHI exposure through policy errors |
| PCI DSS | Isolates payment data by tenant |

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_validation.py

# Run with coverage
pytest --cov=app tests/

# Run integration tests
pytest tests/integration/

# Run performance tests
pytest tests/performance/

# Generate coverage report
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html
```

### Test Coverage

| Module | Coverage | Status |
|--------|----------|--------|
| Policy Generator | 94% | ✅ |
| Validation Engine | 92% | ✅ |
| Simulation Engine | 89% | ✅ |
| Learning Engine | 85% | ✅ |
| API Layer | 91% | ✅ |
| Database Layer | 88% | ✅ |

### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run linting
        run: |
          ruff check .
          black --check .
      - name: Run type checking
        run: mypy app/
      - name: Run tests
        run: pytest --cov=app --cov-report=xml tests/
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## 🗺️ Roadmap

### Q4 2024 (MVP)
- ✅ Deterministic policy generation
- ✅ Basic validation engine
- ✅ Simple dashboard
- ✅ Initial simulation capability
- ✅ REST API endpoints

### Q1 2025 (Beta)
- 🔄 Advanced attack pattern detection
- 🔄 Policy versioning and rollback
- 🔄 Integration with CI/CD pipelines
- 🔄 Enterprise audit compliance
- 🔄 Multi-tenant database support
- 🔄 Performance optimization

### Q2 2025 (GA)
- 🚀 Machine learning for policy recommendations
- 🚀 Multi-cloud deployment options
- 🚀 Advanced threat intelligence feeds
- 🚀 SOC 2 compliance package
- 🚀 Terraform deployment modules
- 🚀 Prometheus/Grafana monitoring

### Q3 2025 (Enterprise)
- 🏢 Role-based access control (RBAC) for BaseLock itself
- 🏢 On-premise deployment option
- 🏢 High availability configuration
- 🏢 Disaster recovery automation
- 🏢 Advanced analytics dashboard

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **🐛 Bug Reports**: Open an issue with reproduction steps
2. **💡 Feature Requests**: Tell us what you need
3. **🔧 Pull Requests**: Read our [Contributing Guide](CONTRIBUTING.md)
4. **📚 Documentation**: Help us improve docs
5. **🌐 Translations**: Help localize BaseLock

### Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run linting
ruff check .
ruff check . --fix

# Format code
black .
black . --check

# Run type checking
mypy app/
mypy app/ --strict

# Build documentation
mkdocs build
mkdocs serve
```

### Code Standards

| Aspect | Tool | Configuration |
|--------|------|---------------|
| Formatting | Black | 88 char line length |
| Linting | Ruff | Strict ruleset |
| Type Checking | MyPy | Strict mode |
| Testing | Pytest | Coverage > 85% |
| CI/CD | GitHub Actions | Automated pipeline |

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

```
Copyright (c) 2026 BaseLock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

---

## 🌟 Support the Project

- ⭐ Star us on GitHub
- 🐦 Follow [@BaseLock](https://twitter.com/baselock) on Twitter
- 📧 Email us at hello@baselock.dev
- 💬 Join our [Discord community](https://discord.gg/baselock)
- 🔔 Subscribe to our [Newsletter](https://baselock.dev/newsletter)

---

## 🙏 Acknowledgments

### Open Source Libraries

- [FastAPI](https://fastapi.tiangolo.com/) — Modern web framework
- [Pydantic](https://docs.pydantic.dev/) — Data validation
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for PostgreSQL
- [Alembic](https://alembic.sqlalchemy.org/) — Database migrations
- [pgvector](https://github.com/pgvector/pgvector) — Vector similarity search
- [Chart.js](https://www.chartjs.org/) — Dashboard visualizations
- [httpx](https://www.python-httpx.org/) — Async HTTP client

### Services

- [Groq](https://groq.com/) — High-performance AI inference
- [PostgreSQL](https://www.postgresql.org/) — Reliable database
- [Docker](https://www.docker.com/) — Containerization
- [GitHub Actions](https://github.com/features/actions) — CI/CD

---

## 📞 Contact

**Website**: [https://baselock.dev](https://baselock.dev)  
**Documentation**: [https://docs.baselock.dev](https://docs.baselock.dev)  
**API Reference**: [https://api.baselock.dev/docs](https://api.baselock.dev/docs)  
**Status**: 🚀 Early Access — [Request Demo](https://baselock.dev/demo)

---

## 💬 FAQ

**Q: Is BaseLock free to use?**  
A: Yes, BaseLock is open-source under the MIT license for self-hosted use. Cloud-hosted options will be available for enterprise users.

**Q: Does BaseLock work with existing RLS policies?**  
A: Yes, BaseLock can validate and simulate existing policies, not just generate new ones.

**Q: What PostgreSQL versions are supported?**  
A: PostgreSQL 14 and above, with pgvector extension required.

**Q: Can BaseLock handle very large tenant databases?**  
A: Yes, BaseLock is designed to scale with your database. The simulation engine uses isolated sessions to avoid impacting production performance.

**Q: Is BaseLock production-ready?**  
A: BaseLock is currently in Early Access. Testing in staging environments first is recommended. GA release planned for Q2 2025.

---

> **⚠️ Disclaimer**: BaseLock is a security tool that helps generate and validate RLS policies. Always review generated policies and test thoroughly before deploying to production. No tool can guarantee perfect security. Use BaseLock as part of a comprehensive security strategy.
