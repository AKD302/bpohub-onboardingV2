import streamlit as st
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BPO Hub | Client Onboarding",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background: #f8fafc; }

  /* Header */
  .bpo-header {
    background: linear-gradient(135deg, #0a2463 0%, #1e4db7 50%, #0d7377 100%);
    padding: 2.5rem 2rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
  }
  .bpo-header h1 { color: white; font-size: 2rem; font-weight: 700; margin: 0; }
  .bpo-header p { color: rgba(255,255,255,0.85); margin: 0.5rem 0 0; font-size: 1.05rem; }

  /* Progress bar */
  .progress-container {
    background: #e2e8f0;
    border-radius: 100px;
    height: 8px;
    margin: 1.5rem 0;
  }
  .progress-fill {
    background: linear-gradient(90deg, #1e4db7, #0d7377);
    height: 8px;
    border-radius: 100px;
    transition: width 0.4s ease;
  }
  .step-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 0.3rem;
  }

  /* Step card */
  .step-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
  }
  .step-number {
    display: inline-block;
    background: #1e4db7;
    color: white;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    line-height: 32px;
    text-align: center;
    font-weight: 700;
    font-size: 0.9rem;
    margin-right: 0.6rem;
  }
  .step-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0a2463;
    display: inline;
  }

  /* Product card */
  .product-card {
    background: #f0f7ff;
    border-left: 4px solid #1e4db7;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
  }
  .product-name { font-weight: 700; color: #0a2463; font-size: 1rem; }
  .product-tag {
    display: inline-block;
    background: #1e4db7;
    color: white;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 4px;
  }
  .match-score {
    float: right;
    background: #0d7377;
    color: white;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 700;
  }

  /* Case study card */
  .case-card {
    background: #f0fdf4;
    border-left: 4px solid #0d7377;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
  }
  .case-industry { font-weight: 700; color: #0a2463; font-size: 0.92rem; }
  .case-headline { color: #374151; font-size: 0.85rem; margin-top: 2px; }
  .case-metric {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-right: 4px;
    margin-top: 6px;
  }

  /* Nav buttons */
  .stButton > button {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.5rem 1.5rem;
  }
  div[data-testid="stHorizontalBlock"] .stButton:first-child > button {
    background: white;
    border: 2px solid #1e4db7;
    color: #1e4db7;
  }
  div[data-testid="stHorizontalBlock"] .stButton:last-child > button {
    background: linear-gradient(135deg, #1e4db7, #0d7377);
    border: none;
    color: white;
  }

  .summary-box {
    background: linear-gradient(135deg, #0a2463, #1e4db7);
    color: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .summary-box h3 { margin: 0 0 0.5rem; font-size: 1rem; opacity: 0.8; }
  .summary-box p { margin: 0; font-size: 1.1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA: PRODUCTS
# ─────────────────────────────────────────────
PRODUCTS = [
    {
        "name": "Variance Analysis & Analytical Data Review",
        "category": "Reporting & Analytics",
        "description": "Compares actual performance against prior periods, budgets, forecasts, and benchmarks. Isolates material variances, identifies root causes, and converts complex data into clear, actionable insights.",
        "who_for": "Founders, finance leaders, and management teams needing clarity behind performance changes.",
        "tags": ["reporting", "analytics", "variance", "management", "finance leaders", "budgeting", "performance"],
        "pain_keywords": ["manual reporting", "slow reporting", "no insights", "performance unclear", "budget variance"],
        "stats": "50–70% reduction in manual variance analysis time | 60% fewer management questions"
    },
    {
        "name": "Financial Reporting Efficiency Review",
        "category": "Reporting & Analytics",
        "description": "Evaluates the entire financial reporting lifecycle to identify bottlenecks, manual dependencies, duplication, and control gaps that slow reporting and reduce accuracy.",
        "who_for": "Organizations experiencing delayed closes, inconsistent reports, or increasing reporting complexity.",
        "tags": ["reporting", "efficiency", "close", "controls", "scalability", "finance ops"],
        "pain_keywords": ["slow close", "delayed reporting", "manual processes", "reporting errors", "inconsistent reports"],
        "stats": "20–40% reduction in reporting cycle time | 30–50% reduction in post-close corrections"
    },
    {
        "name": "Monthly Financial Reporting Pack",
        "category": "Reporting & Analytics",
        "description": "Delivers standardized financial statements and supporting schedules on a fixed monthly cadence, providing clarity on performance, cash flow, and trends.",
        "who_for": "Small and mid-market organizations needing reliable management-ready monthly financial insight.",
        "tags": ["reporting", "monthly", "SMB", "mid-market", "statements", "management reporting"],
        "pain_keywords": ["no monthly reports", "inconsistent financials", "need regular reporting", "management visibility"],
        "stats": "On-time delivery across 12 reporting cycles | 25–40% reduction in management follow-up queries"
    },
    {
        "name": "Annual Financial Statements & Management Reporting",
        "category": "Reporting & Analytics",
        "description": "Delivers year-end financial statements aligned with regulatory standards and management expectations. Ensures reconciled balances, accurate cut-offs, and structured schedules ready for audit.",
        "who_for": "Organizations preparing for audits, investor reviews, or regulatory submissions.",
        "tags": ["annual", "audit", "year-end", "compliance", "investor", "regulatory"],
        "pain_keywords": ["audit stress", "year-end chaos", "audit delays", "investor reporting", "year-end adjustments"],
        "stats": "30–50% faster audit turnaround | Up to 40% fewer audit adjustments"
    },
    {
        "name": "Management KPI Dashboard",
        "category": "Reporting & Analytics",
        "description": "Consolidates key financial and operational metrics into a single, intuitive view aligned with business goals for real-time performance monitoring.",
        "who_for": "Leadership and management teams requiring continuous real-time performance visibility.",
        "tags": ["dashboard", "KPI", "real-time", "leadership", "analytics", "performance", "BI"],
        "pain_keywords": ["no dashboards", "fragmented data", "no real-time visibility", "spreadsheet dependency", "manual reporting"],
        "stats": "15–30 KPIs with real-time access | 40–60% reduction in manual reporting prep time"
    },
    {
        "name": "Executive & Board Reporting Pack Design",
        "category": "Reporting & Analytics",
        "description": "Designs executive and board-level reporting packs that translate financial and operational data into clear narratives for stakeholders.",
        "who_for": "Mid-market companies, investor-backed businesses, and leadership teams preparing board or investor updates.",
        "tags": ["board", "executive", "investor", "PE", "reporting", "leadership", "stakeholders"],
        "pain_keywords": ["board reporting", "investor reporting", "PE reporting", "board meetings", "stakeholder confidence"],
        "stats": "30–50% reduction in board-level clarification questions | 25–40% improved board meeting efficiency"
    },
    {
        "name": "Fast Close Transformation",
        "category": "Close & Compliance",
        "description": "Redesigns month-end and year-end close processes to eliminate delays, bottlenecks, and rework. Standardizes workflows, responsibilities, controls, and timelines.",
        "who_for": "Mid-market companies and investor-backed businesses struggling with slow or unpredictable closes.",
        "tags": ["close", "month-end", "fast close", "transformation", "controls", "PE"],
        "pain_keywords": ["slow close", "15 day close", "late close", "manual close", "post-close adjustments", "close delays"],
        "stats": "Close cycle reduced from 10–15 days to 3–5 days | 30–50% fewer post-close adjustments"
    },
    {
        "name": "Pre-Close Readiness & Close Calendar Design",
        "category": "Close & Compliance",
        "description": "Prepares your organization for a smooth close by defining tasks, timelines, dependencies, and responsibilities in advance.",
        "who_for": "Organizations experiencing frequent close delays, rework, or dependency issues.",
        "tags": ["close", "calendar", "preparation", "month-end", "controls"],
        "pain_keywords": ["close surprises", "missed dependencies", "close delays", "close preparation"],
        "stats": "20–30% reduction in close preparation time | Fewer missed dependencies and handoffs"
    },
    {
        "name": "Compliance Documentation & Audit Trail Setup",
        "category": "Close & Compliance",
        "description": "Creates standardized compliance documentation and audit trails aligned with regulatory and audit expectations.",
        "who_for": "Regulated organizations and growing businesses preparing for audits or compliance reviews.",
        "tags": ["compliance", "audit", "documentation", "controls", "governance", "regulatory"],
        "pain_keywords": ["compliance gaps", "audit trail missing", "documentation issues", "governance", "regulatory risk"],
        "stats": "30–50% reduction in audit preparation effort | Clear traceability for key controls"
    },
    {
        "name": "Regulated Reporting Support",
        "category": "Close & Compliance",
        "description": "Supports the preparation, validation, and submission of regulated financial and operational reports with accuracy and compliance.",
        "who_for": "Healthcare, financial services, and regulated organizations with recurring reporting obligations.",
        "tags": ["regulatory", "compliance", "healthcare", "financial services", "reporting", "government"],
        "pain_keywords": ["regulatory deadlines", "compliance reporting", "regulatory penalties", "regulated industry"],
        "stats": "30–50% reduction in reporting errors | Improved on-time regulatory submissions"
    },
    {
        "name": "Audit & Tax Queries Support",
        "category": "Close & Compliance",
        "description": "Provides end-to-end support for audit and tax queries raised by auditors, tax advisors, and regulators. Coordinates data extraction, documentation, explanations, and follow-ups.",
        "who_for": "Small and mid-market organizations, accounting firms, and regulated businesses facing recurring audit or tax queries.",
        "tags": ["audit", "tax", "CPA", "accounting firms", "compliance", "multi-jurisdiction"],
        "pain_keywords": ["audit queries", "tax questions", "auditor requests", "tax compliance", "audit disruption"],
        "stats": "30–50% faster query turnaround | Up to 40% reduction in repeat auditor questions"
    },
    {
        "name": "Revenue Recognition Framework",
        "category": "Close & Compliance",
        "description": "Designs and documents a revenue recognition framework tailored to your industry and contracts, aligned with applicable accounting standards.",
        "who_for": "Healthcare, software, services, and regulated organizations with complex revenue models.",
        "tags": ["revenue", "recognition", "ASC 606", "healthcare", "software", "compliance", "audit"],
        "pain_keywords": ["revenue recognition issues", "complex contracts", "revenue errors", "ASC 606", "revenue audit"],
        "stats": "Up to 50% reduction in revenue-related audit findings"
    },
    {
        "name": "Cash Flow Visibility & Forecasting Framework",
        "category": "Cash & Payments",
        "description": "Builds a cash flow visibility and forecasting framework tailored to your business model, integrating historical data, near-term obligations, and expected inflows.",
        "who_for": "Founders and finance teams managing growth, seasonality, or tight cash cycles.",
        "tags": ["cash flow", "forecasting", "working capital", "growth", "startups", "founders"],
        "pain_keywords": ["cash flow problems", "cash surprises", "funding gaps", "cash visibility", "cash planning"],
        "stats": "8–13 week forward cash visibility | 30–50% improvement in cash planning accuracy"
    },
    {
        "name": "Invoice-to-Cash Acceleration Program",
        "category": "Cash & Payments",
        "description": "Analyzes and optimizes the entire invoice-to-cash lifecycle, removing process delays and improving follow-ups to align billing, AR, and cash application.",
        "who_for": "Organizations experiencing slow collections, inconsistent follow-ups, or cash flow pressure.",
        "tags": ["AR", "collections", "DSO", "invoice", "cash flow", "receivables"],
        "pain_keywords": ["slow collections", "high DSO", "unpaid invoices", "AR aging", "cash flow pressure"],
        "stats": "10–25% DSO reduction | 70–90% on-time collections | 30–50% faster dispute resolution"
    },
    {
        "name": "Cash Leak Diagnostic & Recovery Program",
        "category": "Cash & Payments",
        "description": "Examines revenue, costs, billing, payments, and reconciliations to identify cash leakage, quantifies the financial impact, and provides a recovery plan.",
        "who_for": "Organizations with margin pressure, unexplained cash gaps, or rapid operational growth.",
        "tags": ["cash leakage", "margin", "recovery", "reconciliation", "billing", "growth"],
        "pain_keywords": ["unexplained cash gaps", "margin pressure", "cash leakage", "billing errors", "reconciliation issues"],
        "stats": "2–7% of annual revenue leakage identified | Cash recovered within 30–90 days"
    },
    {
        "name": "Working Capital Optimization Program",
        "category": "Cash & Payments",
        "description": "Analyzes receivables, payables, and inventory to optimize working capital and identifies practical actions to release cash tied up in operations.",
        "who_for": "Organizations facing cash pressure or funding constraints.",
        "tags": ["working capital", "AR", "AP", "inventory", "cash flow", "liquidity"],
        "pain_keywords": ["cash pressure", "funding constraints", "working capital", "liquidity issues", "slow AR"],
        "stats": "5–15% of net working capital released | 10–25% DSO reduction | Results within 60–90 days"
    },
    {
        "name": "Subscription & Spend Leakage Diagnostic",
        "category": "Cash & Payments",
        "description": "Analyzes subscription, software, and recurring spend to identify leakage and inefficiencies. Highlights unused services, duplicate tools, and cost optimization opportunities.",
        "who_for": "Technology, startup, and growth-stage organizations with recurring subscription spend.",
        "tags": ["SaaS", "subscriptions", "spend", "cost optimization", "startups", "tech"],
        "pain_keywords": ["SaaS sprawl", "subscription costs", "software spend", "duplicate tools", "spend visibility"],
        "stats": "5–15% savings in recurring spend | Within 30 days unused tools flagged"
    },
    {
        "name": "Cross-Border Payments & Foreign Exchange Control Framework",
        "category": "Cash & Payments",
        "description": "Designs a controlled approach to cross-border payments and foreign exchange management, improving visibility into currency exposure, fees, and settlement timing.",
        "who_for": "Global organizations managing international vendors, customers, or entities.",
        "tags": ["international", "FX", "cross-border", "global", "multi-currency", "payments"],
        "pain_keywords": ["FX losses", "international payments", "cross-border issues", "currency exposure", "global operations"],
        "stats": "3–8% cost reduction in FX | 100% visibility across cross-border transactions"
    },
    {
        "name": "Payment System Implementation",
        "category": "Cash & Payments",
        "description": "Implements and configures payment platforms tailored to your business workflows with secure setup, approval controls, system integrations, and clean handover.",
        "who_for": "Growing organizations modernizing vendor, payroll, or customer payment processes.",
        "tags": ["payments", "automation", "AP", "fintech", "modernization", "controls"],
        "pain_keywords": ["manual payments", "payment errors", "no payment system", "payment automation", "AP modernization"],
        "stats": "40–60% reduction in manual payment processing | 100% visibility across all transactions"
    },
    {
        "name": "Invoicing System Implementation",
        "category": "Cash & Payments",
        "description": "Implements and configures invoicing systems aligned with your revenue model for accurate invoice generation, tax handling, and integration with accounting.",
        "who_for": "Organizations experiencing billing delays, invoice errors, or slow collections.",
        "tags": ["invoicing", "billing", "AR", "automation", "DSO", "collections"],
        "pain_keywords": ["invoice errors", "billing delays", "manual invoicing", "slow collections", "billing disputes"],
        "stats": "30–50% accelerated invoice issuance | 40–60% reduction in billing errors | 10–20% DSO reduction"
    },
    {
        "name": "1099 Data Gathering, Validation & Filing",
        "category": "Cash & Payments",
        "description": "Manages the full 1099 lifecycle from vendor data collection and validation to filing and corrections. Ensures compliance with IRS deadlines.",
        "who_for": "United States businesses and accounting firms issuing multiple 1099s annually.",
        "tags": ["1099", "tax", "IRS", "compliance", "US tax", "vendors", "CPA firms"],
        "pain_keywords": ["1099 filing", "IRS deadline", "contractor forms", "1099 errors", "tax compliance"],
        "stats": "100–10,000+ 1099s handled per season | 40–60% reduction in filing errors"
    },
    {
        "name": "Platform-Level Profitability & Margin Analysis",
        "category": "Cash & Payments",
        "description": "Analyzes revenue, costs, and margins at a platform, product, or channel level. Identifies true profitability by allocating direct and indirect costs accurately.",
        "who_for": "E-commerce, technology, and multi-channel businesses seeking profitability clarity.",
        "tags": ["ecommerce", "profitability", "margin", "multi-channel", "platform", "analytics"],
        "pain_keywords": ["blended reporting", "no channel profitability", "margin analysis", "ecommerce reporting", "platform P&L"],
        "stats": "5–15% margin leakage identified | Improved transparency in contribution margins"
    },
    {
        "name": "System Data Migration",
        "category": "Systems & Technology",
        "description": "Manages the end-to-end migration of financial data from legacy systems to new platforms with completeness, accuracy, reconciliation, and audit readiness.",
        "who_for": "Organizations upgrading, consolidating, or replacing financial systems.",
        "tags": ["migration", "data", "ERP", "legacy", "systems", "audit"],
        "pain_keywords": ["system migration", "data migration", "legacy system", "moving to new system", "data integrity"],
        "stats": "100% reconciliation before go-live | Zero-loss migration | 50–70% reduction in post-migration fixes"
    },
    {
        "name": "System Implementation & Set-Up",
        "category": "Systems & Technology",
        "description": "Implements financial systems configured to your chart of accounts, processes, and controls. Ensures systems are usable, compliant, and integrated.",
        "who_for": "Organizations implementing new accounting, invoicing, or payment platforms.",
        "tags": ["implementation", "ERP", "QuickBooks", "Xero", "accounting software", "setup"],
        "pain_keywords": ["new system setup", "system implementation", "accounting system", "QuickBooks setup", "Xero setup"],
        "stats": "40–60% reduction in post-implementation changes | Faster month-end close post go-live"
    },
    {
        "name": "ERP Migration (Legacy to Cloud)",
        "category": "Systems & Technology",
        "description": "Manages the migration from on-premise or legacy ERPs to cloud-based systems, ensuring process continuity, data accuracy, and stakeholder confidence.",
        "who_for": "Mid-market and enterprise organizations transitioning to cloud-based ERP platforms.",
        "tags": ["ERP", "cloud", "migration", "NetSuite", "Dynamics", "enterprise"],
        "pain_keywords": ["ERP migration", "legacy ERP", "moving to cloud", "NetSuite migration", "Dynamics implementation"],
        "stats": "3–10+ years of historical data supported | Minimizes downtime during cutover"
    },
    {
        "name": "ERP Consolidation",
        "category": "Systems & Technology",
        "description": "Merges multiple accounting or ERP systems into one standardized platform, aligning data models, charts of accounts, and reporting.",
        "who_for": "Mid-market and enterprise organizations operating multiple legal entities or legacy systems.",
        "tags": ["ERP", "consolidation", "multi-entity", "enterprise", "group reporting", "systems"],
        "pain_keywords": ["multiple ERPs", "fragmented systems", "consolidation issues", "group reporting", "multi-entity"],
        "stats": "2–6 systems consolidated to 1 | 40–60% reduction in intercompany reconciliation effort"
    },
    {
        "name": "Legacy System Retirement & Data Archival",
        "category": "Systems & Technology",
        "description": "Manages the controlled shutdown of legacy systems while preserving historical data in an audit-ready, accessible format.",
        "who_for": "Organizations transitioning from legacy platforms or post-ERP migration.",
        "tags": ["legacy", "retirement", "archival", "data", "compliance", "cost reduction"],
        "pain_keywords": ["legacy system costs", "old system", "system retirement", "historical data access", "archival"],
        "stats": "5–15+ years of historical data retained | 80–100% cost reduction in legacy system expenses"
    },
    {
        "name": "Multi-Entity Chart of Accounts Standardization",
        "category": "Systems & Technology",
        "description": "Redesigns and standardizes the chart of accounts across multiple entities to support consolidated reporting, controls, and scalability.",
        "who_for": "Groups with multiple subsidiaries, business units, or geographic entities.",
        "tags": ["COA", "multi-entity", "consolidation", "group", "standardization", "subsidiaries"],
        "pain_keywords": ["inconsistent COA", "multi-entity reporting", "group reporting", "chart of accounts", "consolidation issues"],
        "stats": "2–50+ entities standardized | 30–50% reduction in consolidation adjustments"
    },
    {
        "name": "Transaction-to-Ledger Mapping Framework",
        "category": "Systems & Technology",
        "description": "Designs and documents how operational transactions flow into accounting systems, ensuring accuracy, traceability, and reconciliation.",
        "who_for": "Organizations with multiple transaction sources feeding accounting systems.",
        "tags": ["mapping", "ledger", "transactions", "reconciliation", "automation", "ecommerce"],
        "pain_keywords": ["posting errors", "unreconciled transactions", "suspense accounts", "mapping issues", "transaction errors"],
        "stats": "100% mapped transaction sources | 40–60% reduction in reconciliation effort"
    },
    {
        "name": "Budgeting, Forecasting & Scenario Modeling",
        "category": "Strategy & Advisory",
        "description": "Designs integrated budgets, rolling forecasts, and scenario models aligned with business drivers and financial outcomes.",
        "who_for": "Growing organizations needing disciplined, forward-looking financial planning.",
        "tags": ["budgeting", "forecasting", "scenario", "planning", "growth", "FP&A"],
        "pain_keywords": ["no budget", "poor forecasting", "planning issues", "scenario planning", "FP&A", "forecast accuracy"],
        "stats": "20–40% improvement in forecast accuracy | 3–5 scenarios modeled simultaneously"
    },
    {
        "name": "Investment Due Diligence Support",
        "category": "Strategy & Advisory",
        "description": "Supports financial due diligence for acquisitions, divestments, and investments. Analyzes historical performance, quality of earnings, working capital, and key risks.",
        "who_for": "Investors, founders, and management teams involved in transactions or capital raises.",
        "tags": ["M&A", "due diligence", "PE", "investment", "transactions", "QoE", "capital raise"],
        "pain_keywords": ["acquisition", "due diligence", "M&A", "QoE", "quality of earnings", "transaction support"],
        "stats": "$1M–$100M+ transactions supported | 5–20% EBITDA adjustments identified"
    },
    {
        "name": "Finance Function Maturity Assessment",
        "category": "Strategy & Advisory",
        "description": "Evaluates finance processes, systems, controls, and talent against maturity benchmarks to identify gaps and prioritize improvements.",
        "who_for": "Organizations preparing for scale, audits, investment, or transformation.",
        "tags": ["assessment", "maturity", "transformation", "benchmarking", "controls", "readiness"],
        "pain_keywords": ["finance gaps", "finance maturity", "transformation planning", "investor readiness", "finance assessment"],
        "stats": "20–40 capability areas assessed | Quick wins identified alongside long-term gaps"
    },
    {
        "name": "Finance Transformation Roadmap",
        "category": "Strategy & Advisory",
        "description": "Converts assessment findings into a structured finance transformation roadmap with defined initiatives, sequencing, timelines, and outcomes.",
        "who_for": "Organizations committed to modernizing finance capabilities.",
        "tags": ["transformation", "roadmap", "strategy", "modernization", "PE", "growth"],
        "pain_keywords": ["finance transformation", "modernization", "strategic planning", "transformation roadmap"],
        "stats": "12–36 month transformation horizons | Initiatives prioritized by ROI"
    },
    {
        "name": "Management Reporting Automation",
        "category": "Strategy & Advisory",
        "description": "Automates recurring management reporting by integrating data sources, defining logic, and standardizing outputs while preserving accuracy and governance.",
        "who_for": "Organizations producing recurring monthly or weekly management reports.",
        "tags": ["automation", "reporting", "management", "BI", "recurring", "efficiency"],
        "pain_keywords": ["manual reporting", "reporting automation", "spreadsheet reporting", "recurring reports", "reporting burden"],
        "stats": "50–70% reduction in reporting preparation time | 10–30 recurring reports automated"
    },
    {
        "name": "Finance Dashboarding & Business Intelligence",
        "category": "Strategy & Advisory",
        "description": "Designs and deploys interactive dashboards using finance and operational data aligned with decision-making needs.",
        "who_for": "Leadership teams and finance functions needing live performance visibility.",
        "tags": ["BI", "dashboard", "analytics", "real-time", "Power BI", "Tableau", "leadership"],
        "pain_keywords": ["no dashboards", "static reports", "real-time visibility", "BI tools", "performance visibility"],
        "stats": "20–50 KPIs tracked | 40–60% reduction in ad-hoc reporting requests"
    },
    {
        "name": "AI-Enabled Financial Analysis & Insights",
        "category": "Strategy & Advisory",
        "description": "Applies AI-driven analysis to financial data to identify patterns, anomalies, and insights, combined with professional expert review.",
        "who_for": "Organizations seeking deeper insights from growing financial datasets.",
        "tags": ["AI", "analytics", "anomaly detection", "automation", "insights", "data", "technology"],
        "pain_keywords": ["AI", "automated analysis", "data insights", "anomaly detection", "advanced analytics"],
        "stats": "2–3x faster anomaly detection | 30–50% improvement in variance detection accuracy"
    },
    {
        "name": "Fractional CFO Advisory Support",
        "category": "Strategy & Advisory",
        "description": "Provides access to senior finance leadership on a fractional basis, supporting strategy, planning, investor readiness, and financial decision-making.",
        "who_for": "Founders and leadership teams needing senior finance guidance.",
        "tags": ["CFO", "advisory", "fractional", "strategy", "founders", "startups", "investor readiness"],
        "pain_keywords": ["need CFO", "senior finance", "strategic finance", "investor readiness", "fundraising support"],
        "stats": "60–75% less than a full-time CFO | 15–25+ years of finance leadership experience"
    },
    {
        "name": "Finance Function Build-Out & Scaling Support",
        "category": "Strategy & Advisory",
        "description": "Supports the design and scaling of finance functions as organizations grow, aligning people, processes, and systems to current and future needs.",
        "who_for": "Growing organizations building or scaling finance teams.",
        "tags": ["scaling", "build-out", "finance team", "growth", "operating model", "hiring"],
        "pain_keywords": ["scaling finance", "finance team growth", "operating model", "finance build-out", "hiring finance"],
        "stats": "Designs finance functions for 2x–5x growth | 25–40% finance team productivity improvement"
    },
    {
        "name": "Revenue & Cost Matching Framework (Healthcare)",
        "category": "Strategy & Advisory",
        "description": "Aligns healthcare revenue streams with direct and indirect costs, ensuring accurate margin analysis, regulatory alignment, and meaningful financial insights.",
        "who_for": "Healthcare providers, clinics, and healthcare-focused organizations.",
        "tags": ["healthcare", "revenue", "cost", "margin", "RCM", "clinic", "provider"],
        "pain_keywords": ["healthcare revenue", "RCM", "margin analysis", "healthcare finance", "reimbursement"],
        "stats": "30–50% improvement in service-level margin accuracy"
    },
    {
        "name": "Qualified Audit Professionals",
        "category": "Talent",
        "description": "Provides access to ACCA/CA-qualified audit professionals who support audit execution, reviews, documentation, and regulatory requirements.",
        "who_for": "Accounting & Audit / CPA firms, internal audit teams, and regulated organizations requiring qualified audit expertise.",
        "tags": ["audit", "CPA firms", "ACCA", "CA", "talent", "staffing", "audit execution"],
        "pain_keywords": ["audit staffing", "need auditors", "peak season", "audit capacity", "CPA firm staffing"],
        "stats": "5–12+ years of audit experience | Scales up or down based on engagement needs"
    },
    {
        "name": "Competent Audit Support Staff",
        "category": "Talent",
        "description": "Provides audit support staff who assist with testing, documentation, reconciliations, and audit schedules with consistency and supervision.",
        "who_for": "Audit firms and finance teams needing dependable audit execution support.",
        "tags": ["audit support", "staffing", "documentation", "testing", "audit firms", "cost effective"],
        "pain_keywords": ["audit support", "reduce audit cost", "peak season staffing", "audit documentation", "testing support"],
        "stats": "50–1,000+ testing items supported | 30–50% reduction in senior auditor workload"
    },
    {
        "name": "Qualified Accounting Professionals",
        "category": "Talent",
        "description": "Provides qualified accounting professionals to manage complex accounting, reporting, and compliance activities aligned with accounting standards.",
        "who_for": "Growing organizations and finance teams requiring experienced accounting expertise.",
        "tags": ["accounting", "talent", "staffing", "ACCA", "CPA", "qualified", "reporting"],
        "pain_keywords": ["accounting staffing", "need accountants", "qualified accounting", "accounting talent", "hiring accountants"],
        "stats": "5–15+ years of accounting experience | Scales with business complexity"
    },
    {
        "name": "Competent Accounting Support Staff",
        "category": "Talent",
        "description": "Provides accounting support staff to handle routine accounting, reconciliations, and transaction processing with consistent execution and supervision.",
        "who_for": "Finance teams seeking reliable execution support without increasing fixed headcount.",
        "tags": ["accounting support", "staffing", "transaction processing", "reconciliation", "cost effective", "flexible"],
        "pain_keywords": ["accounting backlog", "transaction volume", "need accounting help", "routine accounting", "flexible staffing"],
        "stats": "1,000–50k+ monthly transactions supported | 30–60% reduction in accounting backlogs"
    }
]

# ─────────────────────────────────────────────
# DATA: CASE STUDIES
# ─────────────────────────────────────────────
CASE_STUDIES = [
    {
        "id": 1, "industry": "CPA / Accounting Firms", "title": "From Talent Bottlenecks to Predictable Close Cycles",
        "context": "A U.S.-based CPA firm faced persistent shortages of CPA-ready talent, rising onshore hiring costs, and lengthening recruiting cycles causing slow close cycles and peak-season bottlenecks.",
        "metrics": ["45% faster close cycles", "2× peak-season capacity", "Up to 55% reduction in operating costs"],
        "tags": ["CPA", "accounting", "staffing", "close", "tax", "audit", "talent"],
        "product_matches": ["Qualified Audit Professionals", "Qualified Accounting Professionals", "Fast Close Transformation"]
    },
    {
        "id": 2, "industry": "US Tax Services", "title": "From Tax-Season Bottlenecks to Peak-Ready Precision",
        "context": "A U.S.-based tax services firm faced extreme workload spikes during tax season with multi-state filing complexity and internal preparer and reviewer shortages.",
        "metrics": ["60% reduction in error rates", "100% on-time filings", "Up to 50% cost savings"],
        "tags": ["tax", "1099", "IRS", "CPA", "staffing", "peak season", "US tax"],
        "product_matches": ["1099 Data Gathering, Validation & Filing", "Qualified Audit Professionals", "Competent Audit Support Staff"]
    },
    {
        "id": 3, "industry": "Staffing & Recruitment", "title": "From Subscription Chaos to Cost Discipline",
        "context": "A U.S.-based staffing firm experienced uncontrolled SaaS subscription growth following leadership changes, with auto-billed tools accumulating without ownership or usage tracking.",
        "metrics": ["30–35% reduction in software/tool expenses", "Full license visibility achieved", "Sustained cost discipline"],
        "tags": ["SaaS", "subscriptions", "spend", "cost", "staffing", "software"],
        "product_matches": ["Subscription & Spend Leakage Diagnostic", "Cash Leak Diagnostic & Recovery Program"]
    },
    {
        "id": 4, "industry": "Private Equity", "title": "From Hidden Overhead to Recoverable Portfolio Revenue",
        "context": "A U.S.-based PE firm lacked a structured mechanism to allocate and recover shared corporate expenses across portfolio companies, obscuring true portfolio performance.",
        "metrics": ["25–30% increase in recoverable corporate revenue", "Improved portfolio-level cost visibility", "Stronger governance across entities"],
        "tags": ["private equity", "PE", "portfolio", "management fees", "governance", "overhead"],
        "product_matches": ["Finance Function Maturity Assessment", "Executive & Board Reporting Pack Design", "Finance Transformation Roadmap"]
    },
    {
        "id": 5, "industry": "Startups (Solar Installation)", "title": "From Referral-Driven Growth to a Predictable Lead Engine",
        "context": "A U.S.-based solar startup had strong technical execution but lacked internal capacity for consistent digital marketing and structured lead generation.",
        "metrics": ["3× increase in inbound and outbound leads", "Up to 50% reduction in hiring costs", "Predictable growth pipeline"],
        "tags": ["startup", "solar", "marketing", "lead generation", "growth", "CRM"],
        "product_matches": ["Finance Function Build-Out & Scaling Support", "Cash Flow Visibility & Forecasting Framework", "Fractional CFO Advisory Support"]
    },
    {
        "id": 6, "industry": "Fresh Produce Distribution", "title": "Plug Cash Leaks — AP Governance Meets Liquidity Mastery",
        "context": "A fast-growing fresh produce distributor experienced cash leakage due to fragmented vendor payment processes, limited visibility into outstanding balances, and high-frequency purchasing cycles.",
        "metrics": [">20% increase in available cash", ">75% reduction in exception-based payments", ">30% improvement in on-time payment accuracy"],
        "tags": ["AP", "accounts payable", "cash", "vendor", "distribution", "manufacturing", "payments"],
        "product_matches": ["Payment System Implementation", "Cash Leak Diagnostic & Recovery Program", "Working Capital Optimization Program"]
    },
    {
        "id": 7, "industry": "Health & Medical (Urgent Care)", "title": "From Denials and Delays to Predictable Cash Realization",
        "context": "A network of urgent care clinics in Northeast Ohio faced persistent revenue-cycle challenges including high claim denial rates, delayed reimbursements, and fragmented billing workflows.",
        "metrics": ["35–40% reduction in claim denials", "Up to 50% cost savings vs U.S. billing", "Improved reimbursement predictability"],
        "tags": ["healthcare", "urgent care", "RCM", "billing", "claims", "denials", "reimbursement"],
        "product_matches": ["Revenue & Cost Matching Framework (Healthcare)", "Revenue Recognition Framework", "Regulated Reporting Support"]
    },
    {
        "id": 8, "industry": "Health & Medical (Home Healthcare)", "title": "From Revenue Uncertainty to Financial Control",
        "context": "A Houston-based home healthcare provider experienced delayed revenue recognition, inconsistent CRM data interpretation, and aging receivables extending beyond 180 days.",
        "metrics": ["35% reduction in revenue adjustments", "Improved revenue recognition accuracy", "Greater cash-flow predictability"],
        "tags": ["healthcare", "home health", "revenue", "receivables", "RCM", "cash flow"],
        "product_matches": ["Revenue & Cost Matching Framework (Healthcare)", "Invoice-to-Cash Acceleration Program", "Cash Flow Visibility & Forecasting Framework"]
    },
    {
        "id": 9, "industry": "Signage Manufacturing", "title": "From Production Errors to On-Time, Accurate Fulfillment",
        "context": "A Denver-based wholesale manufacturer of custom channel letter signage faced frequent production delays caused by non-production-ready design files, order-detail errors, and slow quote turnaround.",
        "metrics": ["80% reduction in production file errors", "75% improvement in order accuracy", "Quote turnaround from 48 hrs to 12 hrs"],
        "tags": ["manufacturing", "signage", "production", "operations", "order management", "wholesale"],
        "product_matches": ["Finance Function Build-Out & Scaling Support", "Management Reporting Automation", "Competent Accounting Support Staff"]
    },
    {
        "id": 10, "industry": "Construction", "title": "From Missed Bids to Coordinated Project Execution",
        "context": "A Cleveland-based real estate and construction firm faced capacity gaps across B2B sales, estimating, and project coordination with fragmented handoffs slowing proposal turnaround.",
        "metrics": ["50% increase in bid submissions", "~50% lower operating costs vs U.S. hiring", "Improved execution reliability"],
        "tags": ["construction", "real estate", "bidding", "project management", "operations", "sales"],
        "product_matches": ["Finance Function Build-Out & Scaling Support", "Competent Accounting Support Staff", "Cash Flow Visibility & Forecasting Framework"]
    },
    {
        "id": 11, "industry": "E-Commerce (Multi-Channel)", "title": "From Blended Numbers to Platform-Level Profitability",
        "context": "A multi-channel home-goods e-commerce brand lacked visibility into platform-level performance with revenues and costs captured in aggregate.",
        "metrics": ["5–7% increase in overall profitability", "Full platform-level P&L visibility", "Improved cost control through accurate expense allocation"],
        "tags": ["ecommerce", "multi-channel", "profitability", "margin", "Amazon", "Shopify", "platform"],
        "product_matches": ["Platform-Level Profitability & Margin Analysis", "Finance Dashboarding & Business Intelligence", "Management KPI Dashboard"]
    },
    {
        "id": 12, "industry": "Home Inspection Services", "title": "From Disorganized Scheduling to Operational Control",
        "context": "A U.S.-based home inspection technology provider struggled with disorganized scheduling, slow onboarding of inspectors, and inconsistent report quality creating documentation backlogs.",
        "metrics": ["70% reduction in scheduling errors", "~50% lower staffing costs", "Reduced documentation backlogs"],
        "tags": ["services", "operations", "scheduling", "real estate", "operations support", "staffing"],
        "product_matches": ["Competent Accounting Support Staff", "Finance Function Build-Out & Scaling Support", "Management Reporting Automation"]
    },
    {
        "id": 13, "industry": "Private Equity / Investment Firm", "title": "From Year-End Risk to Portfolio Continuity",
        "context": "A U.S.-based PE and strategic investment firm faced an unexpected year-end staffing shortage within its centralized accounting function with multiple portfolio companies dependent on timely close.",
        "metrics": ["50% cost savings vs local accounting firms", "Zero disruption to portfolio companies", "100% on-time close and reporting"],
        "tags": ["private equity", "PE", "portfolio", "year-end", "accounting", "continuity", "close"],
        "product_matches": ["Qualified Accounting Professionals", "Annual Financial Statements & Management Reporting", "Fast Close Transformation"]
    },
    {
        "id": 14, "industry": "AI / Technology", "title": "From Financial Fragmentation to Cash & Revenue Control",
        "context": "A provider of high-performance AI compute infrastructure faced fragmented invoicing, inconsistent AP workflows, and complex multi-stream revenue recognition.",
        "metrics": ["Fully automated AP with zero duplicate payments", "Improved short-term cash visibility", "High-confidence multi-stream revenue reporting"],
        "tags": ["AI", "technology", "startup", "revenue recognition", "AP", "cash flow", "GPU"],
        "product_matches": ["Revenue Recognition Framework", "Payment System Implementation", "Cash Flow Visibility & Forecasting Framework"]
    },
    {
        "id": 15, "industry": "High-Growth Company", "title": "From Capacity Constraints to 300% Revenue Growth Without Adding Headcount",
        "context": "A high-growth company experienced rapid revenue expansion placing increasing pressure on its finance function with transaction volumes multiplying across billing, collections, and vendor payments.",
        "metrics": ["300% revenue growth supported", "Zero incremental internal finance headcount", "Stable close timelines maintained throughout"],
        "tags": ["high-growth", "scaling", "startup", "finance ops", "AP", "AR", "close"],
        "product_matches": ["Finance Function Build-Out & Scaling Support", "Competent Accounting Support Staff", "Invoice-to-Cash Acceleration Program"]
    },
    {
        "id": 16, "industry": "Multi-Entity / ERP Consolidation", "title": "From Platform Sprawl to One Unified Finance System",
        "context": "A growing organization had accumulated multiple accounting platforms with inconsistent COAs, duplicated processes, and fragmented reporting making consolidations slow and error-prone.",
        "metrics": ["3+ accounting platforms consolidated into one", "30% reduction in system and license costs", "Single source of truth for financial reporting"],
        "tags": ["ERP", "consolidation", "multi-entity", "systems", "COA", "group reporting"],
        "product_matches": ["ERP Consolidation", "Multi-Entity Chart of Accounts Standardization", "System Data Migration"]
    },
    {
        "id": 17, "industry": "Financial Close Transformation", "title": "From a 15-Day Close to a 3-Day Close",
        "context": "A mid-sized organization was operating with a prolonged 15-day monthly close driven by manual reconciliations, late adjustments, and fragmented ownership.",
        "metrics": ["Close cycle reduced from 15 days to 3 days", "Financial results available 12 days earlier", "80% reduction in post-close adjustments"],
        "tags": ["close", "fast close", "month-end", "reconciliation", "transformation"],
        "product_matches": ["Fast Close Transformation", "Pre-Close Readiness & Close Calendar Design", "Financial Reporting Efficiency Review"]
    },
    {
        "id": 18, "industry": "Tech Startup (Payments & Vendor Management)", "title": "From Payment Chaos to Scalable Vendor Control",
        "context": "A rapidly expanding tech startup experienced explosive vendor growth with fragmented AP processes, inconsistent approvals, and unpredictable payment timing.",
        "metrics": ["50% reduction in late vendor payments", "100% vendor master data visibility", "Improved short-term cash forecast accuracy"],
        "tags": ["startup", "tech", "AP", "vendor management", "payments", "cash flow"],
        "product_matches": ["Payment System Implementation", "Cash Leak Diagnostic & Recovery Program", "Invoice-to-Cash Acceleration Program"]
    },
    {
        "id": 19, "industry": "Legacy System Retirement", "title": "From Legacy Lock-In to Clean, Audit-Ready Financial History",
        "context": "A mature organization relied on a costly, increasingly unstable legacy accounting system containing more than a decade of historical financial data needed for audits and tax reviews.",
        "metrics": ["10+ years of financial data migrated", "100% balance and transaction fidelity", "Legacy system fully decommissioned"],
        "tags": ["legacy", "migration", "archival", "data", "audit", "ERP", "system retirement"],
        "product_matches": ["Legacy System Retirement & Data Archival", "System Data Migration", "ERP Migration (Legacy to Cloud)"]
    },
    {
        "id": 20, "industry": "Executive Reporting & Analytics", "title": "From Static Reports to Real-Time Decision Support",
        "context": "A growing organization relied on backward-looking static financial reports produced days or weeks after period close, limiting timely executive decision-making.",
        "metrics": ["60% reduction in decision cycle-time", "Real-time KPI visibility", "Near-elimination of manual report preparation"],
        "tags": ["reporting", "analytics", "BI", "dashboards", "KPI", "leadership", "real-time"],
        "product_matches": ["Finance Dashboarding & Business Intelligence", "Management KPI Dashboard", "Management Reporting Automation"]
    },
    {
        "id": 21, "industry": "Finance Operating Model Strategy", "title": "From In-House Expansion to a Lower Total Cost of Ownership",
        "context": "A growing organization faced a decision between expanding internal finance teams or redesigning their operating model, with rising fixed costs and longer onboarding cycles.",
        "metrics": ["45–60% lower total cost of ownership", "Zero incremental internal headcount", "Faster time-to-capacity vs hiring"],
        "tags": ["operating model", "outsourcing", "cost", "scaling", "finance ops", "efficiency"],
        "product_matches": ["Finance Function Build-Out & Scaling Support", "Competent Accounting Support Staff", "Finance Function Maturity Assessment"]
    },
    {
        "id": 22, "industry": "QuickBooks (SMB / Mid-Market)", "title": "From Messy Books to Month-End Confidence",
        "context": "SMB and mid-market QuickBooks clients had high transaction volumes but inconsistent categorization, unreconciled balances, and delayed closes making financials unreliable.",
        "metrics": ["50–70% faster close cycles", "60%+ reduction in clean-up adjustments", "95%+ reconciliation accuracy"],
        "tags": ["QuickBooks", "SMB", "mid-market", "bookkeeping", "close", "reconciliation"],
        "product_matches": ["System Implementation & Set-Up", "Monthly Financial Reporting Pack", "Fast Close Transformation"]
    },
    {
        "id": 23, "industry": "Xero / MYOB / Sage / Zoho Books", "title": "From Basic Accounting to Standardized Multi-Entity Reporting",
        "context": "Cloud accounting platform clients had transactional capture but lacked standardized structures across entities with reporting varying month to month.",
        "metrics": ["50–65% faster close timelines", "70% reduction in manual corrections", "3× improvement in reporting consistency"],
        "tags": ["Xero", "MYOB", "Sage", "Zoho", "cloud accounting", "multi-entity", "reporting"],
        "product_matches": ["System Implementation & Set-Up", "Multi-Entity Chart of Accounts Standardization", "Monthly Financial Reporting Pack"]
    },
    {
        "id": 24, "industry": "Wave / FreshBooks (Small Business)", "title": "From Bookkeeping Tools to Finance-Grade Visibility",
        "context": "Small businesses using lightweight accounting tools struggled with AR discipline, cash accuracy, and month-end structure with books existing but not decision-ready.",
        "metrics": ["40–55% improvement in reporting timeliness", "50–65% reduction in cash and AR discrepancies", "2× faster invoice-to-cash tracking"],
        "tags": ["Wave", "FreshBooks", "small business", "bookkeeping", "AR", "cash"],
        "product_matches": ["Invoice-to-Cash Acceleration Program", "Monthly Financial Reporting Pack", "System Implementation & Set-Up"]
    },
    {
        "id": 25, "industry": "Ramp (Corporate Card & Spend Management)", "title": "From Spend Leakage to Policy-Driven Financial Control",
        "context": "Fast-scaling organizations using corporate cards faced rising leakage, weak approval discipline, and delayed expense reconciliation with transactions moving faster than finance review.",
        "metrics": ["50–75% reduction in spend exceptions", "40% faster expense reconciliation", "30–45% improvement in month-end close readiness"],
        "tags": ["Ramp", "spend management", "corporate cards", "expenses", "controls", "fintech"],
        "product_matches": ["Subscription & Spend Leakage Diagnostic", "Payment System Implementation", "Cash Leak Diagnostic & Recovery Program"]
    },
    {
        "id": 26, "industry": "Bill.com / Zoho Invoice", "title": "From Fragmented AP & Billing to Predictable Cash Discipline",
        "context": "Organizations managing both payables and customer invoicing across disconnected tools struggled with approval bottlenecks, inconsistent documentation, and delayed billing cycles.",
        "metrics": ["30–50% faster billing cycles", "50% reduction in late vendor payments", "40% reduction in invoice exceptions"],
        "tags": ["Bill.com", "AP", "invoicing", "billing", "cash", "payables", "AR"],
        "product_matches": ["Invoicing System Implementation", "Invoice-to-Cash Acceleration Program", "Payment System Implementation"]
    },
    {
        "id": 27, "industry": "Stripe / PayPal / Square", "title": "From Payment Complexity to Accurate Revenue & Cash Tracking",
        "context": "Businesses collecting payments across multiple gateways faced mismatches between gross sales, net settlements, fees, refunds, disputes, and chargebacks.",
        "metrics": ["2–4× faster settlement reconciliation", "60–80% reduction in reconciliation effort", "Near-zero revenue-to-cash variance"],
        "tags": ["Stripe", "PayPal", "Square", "payment gateway", "reconciliation", "ecommerce", "revenue"],
        "product_matches": ["Transaction-to-Ledger Mapping Framework", "Revenue Recognition Framework", "Invoice-to-Cash Acceleration Program"]
    },
    {
        "id": 28, "industry": "Wise / Payoneer (Cross-Border Payments)", "title": "From Cross-Border Payment Friction to Predictable Global Payouts",
        "context": "Organizations paying global vendors and contractors struggled with FX leakage, unclear payout timing, inconsistent reconciliation, and budget variance from currency volatility.",
        "metrics": ["15–30% reduction in FX leakage", "2× faster cross-border reconciliation", "Consistent on-time global payouts"],
        "tags": ["Wise", "Payoneer", "cross-border", "FX", "international", "global", "payments"],
        "product_matches": ["Cross-Border Payments & Foreign Exchange Control Framework", "Payment System Implementation", "Transaction-to-Ledger Mapping Framework"]
    },
    {
        "id": 29, "industry": "Oracle NetSuite / Microsoft Dynamics 365", "title": "From ERP Complexity to Controlled, Consolidated Reporting",
        "context": "Clients running NetSuite and Dynamics experienced long close cycles, intercompany mismatches, and consolidation delays driven by over-customization and manual reconciliations.",
        "metrics": ["30–50% reduction in close timelines", "60% reduction in manual consolidation effort", "40% reduction in intercompany mismatches"],
        "tags": ["NetSuite", "Dynamics", "ERP", "consolidation", "close", "multi-entity", "intercompany"],
        "product_matches": ["ERP Consolidation", "Fast Close Transformation", "Multi-Entity Chart of Accounts Standardization"]
    },
    {
        "id": 30, "industry": "US Tax Compliance (1099 Emergency)", "title": "When Deadlines Are Non-Negotiable: Rapid 1099 Filing at Scale",
        "context": "A U.S.-based company approached BPO Hub 48 hours before the IRS 1099 filing deadline requesting urgent support to file several hundred 1099 forms with fragmented, incomplete data.",
        "metrics": ["100% on-time IRS submission", "Hundreds of 1099s filed within 48 hours", "Zero filing penalties or rejections"],
        "tags": ["1099", "IRS", "tax", "deadline", "compliance", "emergency", "US tax"],
        "product_matches": ["1099 Data Gathering, Validation & Filing", "Audit & Tax Queries Support"]
    },
    {
        "id": 31, "industry": "Manufacturing (Onshore Assembly)", "title": "From Fixed Overhead to a 40% Leaner Finance Function",
        "context": "A mid-market manufacturing firm operated with a fully in-house finance team sized for peak workloads with fixed costs rising despite fluctuating transaction volumes.",
        "metrics": ["40% reduction in total accounting costs", "Zero disruption during transition", "Scalable finance capacity without incremental hiring"],
        "tags": ["manufacturing", "operations", "cost reduction", "outsourcing", "finance ops", "AP"],
        "product_matches": ["Competent Accounting Support Staff", "Finance Function Build-Out & Scaling Support", "Financial Reporting Efficiency Review"]
    },
    {
        "id": 32, "industry": "ERP Migration (Multi-State Corporation)", "title": "From Fragmented Legacy Systems to a Unified Cloud ERP in 90 Days",
        "context": "A multi-state corporation operated on a patchwork of legacy accounting systems across entities resulting in delayed consolidations, inconsistent financial data, and limited group visibility.",
        "metrics": ["90-day end-to-end ERP migration", "100% balance reconciliation at cutover", "Zero reporting downtime during transition"],
        "tags": ["ERP", "migration", "cloud", "multi-state", "legacy", "enterprise", "consolidation"],
        "product_matches": ["ERP Migration (Legacy to Cloud)", "System Data Migration", "ERP Consolidation"]
    },
    {
        "id": 33, "industry": "Healthcare Finance Automation", "title": "From Manual Reporting to Automated Financial Intelligence",
        "context": "A multi-location healthcare provider relied on spreadsheet-driven financial reporting with slow cycles, frequent manual reconciliations, and inconsistencies reducing confidence in outputs.",
        "metrics": ["70% reduction in manual reporting effort", "Financial reports delivered in hours instead of days", "Higher executive confidence in financials"],
        "tags": ["healthcare", "automation", "reporting", "reconciliation", "BI", "multi-location"],
        "product_matches": ["Management Reporting Automation", "Finance Dashboarding & Business Intelligence", "Revenue & Cost Matching Framework (Healthcare)"]
    },
    {
        "id": 34, "industry": "Financial Services (FIS / Banking)", "title": "From Transaction Processing to Finance-Grade Banking Reporting",
        "context": "Financial services clients using FIS platforms generated massive transaction volumes but struggled to translate operational data into finance-grade reporting with manual, error-prone reconciliations.",
        "metrics": ["60–80% reduction in reconciliation effort", "Near-zero unreconciled transaction balances", "Faster close cycles with improved audit readiness"],
        "tags": ["financial services", "banking", "FIS", "reconciliation", "transactions", "audit"],
        "product_matches": ["Transaction-to-Ledger Mapping Framework", "Compliance Documentation & Audit Trail Setup", "Fast Close Transformation"]
    },
    {
        "id": 35, "industry": "Healthcare (WellSky)", "title": "From Clinical Operations to Revenue-Ready Healthcare Finance",
        "context": "Healthcare providers using WellSky managed complex clinical workflows but faced challenges converting service delivery data into accurate billing, receivables, and revenue reporting.",
        "metrics": ["30–45% improvement in billing timeliness", "Reduction in revenue leakage and delayed claims", "Audit-ready revenue reporting"],
        "tags": ["healthcare", "WellSky", "billing", "revenue", "RCM", "claims", "receivables"],
        "product_matches": ["Revenue & Cost Matching Framework (Healthcare)", "Revenue Recognition Framework", "Invoice-to-Cash Acceleration Program"]
    },
    {
        "id": 36, "industry": "Real Estate & Property Management", "title": "From Property Operations to Controlled, Multi-Entity Financial Visibility",
        "context": "Real estate and property management firms using Buildium/AppFolio/Yardi/RealPage managed thousands of tenant transactions with reconciliation, owner reporting, and close challenges at scale.",
        "metrics": ["Controlled multi-entity financial visibility", "Reduced reconciliation exceptions at property level", "Stronger trust account governance"],
        "tags": ["real estate", "property management", "Buildium", "AppFolio", "Yardi", "multi-entity", "reconciliation"],
        "product_matches": ["Multi-Entity Chart of Accounts Standardization", "Monthly Financial Reporting Pack", "System Implementation & Set-Up"]
    }
]


# ─────────────────────────────────────────────
# MATCHING ENGINE
# ─────────────────────────────────────────────
def compute_matches(answers):
    industry = answers.get("industry", "").lower()
    pain_points = [p.lower() for p in answers.get("pain_points", [])]
    challenges = answers.get("challenges", "").lower()
    systems = answers.get("systems", "").lower()
    goals = [g.lower() for g in answers.get("goals", [])]
    size = answers.get("company_size", "")
    sector = answers.get("sector", "").lower()

    all_text = f"{industry} {' '.join(pain_points)} {challenges} {systems} {' '.join(goals)} {sector}"

    # Score products
    product_scores = []
    for p in PRODUCTS:
        score = 0
        tag_text = " ".join(p["tags"]).lower()
        desc_text = (p["description"] + " " + p["who_for"]).lower()

        # Tag overlap
        for token in all_text.split():
            if len(token) > 3 and token in tag_text:
                score += 2

        # Pain keyword overlap
        for kw in p.get("pain_keywords", []):
            if any(kw in pp for pp in pain_points) or kw in challenges:
                score += 3

        # Goal alignment
        goal_map = {
            "faster close": ["Fast Close Transformation", "Pre-Close Readiness & Close Calendar Design", "Financial Reporting Efficiency Review"],
            "reduce costs": ["Subscription & Spend Leakage Diagnostic", "Cash Leak Diagnostic & Recovery Program", "Working Capital Optimization Program"],
            "better reporting": ["Monthly Financial Reporting Pack", "Management KPI Dashboard", "Finance Dashboarding & Business Intelligence", "Management Reporting Automation"],
            "cash flow": ["Cash Flow Visibility & Forecasting Framework", "Invoice-to-Cash Acceleration Program", "Working Capital Optimization Program"],
            "scale": ["Finance Function Build-Out & Scaling Support", "Competent Accounting Support Staff", "Qualified Accounting Professionals"],
            "audit ready": ["Compliance Documentation & Audit Trail Setup", "Annual Financial Statements & Management Reporting", "Audit & Tax Queries Support"],
            "systems": ["System Implementation & Set-Up", "ERP Migration (Legacy to Cloud)", "ERP Consolidation"],
        }
        for g in goals:
            for key, names in goal_map.items():
                if key in g and p["name"] in names:
                    score += 4

        # Sector boosts
        if "healthcare" in sector and "healthcare" in tag_text:
            score += 3
        if "ecommerce" in sector and "ecommerce" in tag_text:
            score += 3
        if "cpa" in sector or "accounting firm" in sector:
            if any(t in tag_text for t in ["cpa", "audit", "tax", "accounting firms"]):
                score += 3
        if "private equity" in sector and "pe" in tag_text:
            score += 3

        if score > 0:
            product_scores.append((p, score))

    product_scores.sort(key=lambda x: -x[1])
    top_products = product_scores[:5]

    # Match case studies
    case_scores = []
    for cs in CASE_STUDIES:
        score = 0
        tag_text = " ".join(cs["tags"]).lower()

        for token in all_text.split():
            if len(token) > 3 and token in tag_text:
                score += 2

        if any(p[0]["name"] in cs["product_matches"] for p in top_products[:3]):
            score += 3

        if score > 0:
            case_scores.append((cs, score))

    case_scores.sort(key=lambda x: -x[1])
    top_cases = case_scores[:4]

    return top_products, top_cases


# ─────────────────────────────────────────────
# PDF REPORT GENERATOR
# ─────────────────────────────────────────────
def generate_pdf(answers, top_products, top_cases):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch
    )

    BPO_BLUE = colors.HexColor("#0a2463")
    BPO_MID  = colors.HexColor("#1e4db7")
    BPO_TEAL = colors.HexColor("#0d7377")
    BPO_LIGHT= colors.HexColor("#f0f7ff")
    GRAY     = colors.HexColor("#64748b")
    LGRAY    = colors.HexColor("#e2e8f0")

    styles = getSampleStyleSheet()

    s_title   = ParagraphStyle("Title",   fontName="Helvetica-Bold",  fontSize=22, textColor=BPO_BLUE,  spaceAfter=6,  leading=26)
    s_sub     = ParagraphStyle("Sub",     fontName="Helvetica",       fontSize=11, textColor=GRAY,      spaceAfter=16, leading=14)
    s_h1      = ParagraphStyle("H1",      fontName="Helvetica-Bold",  fontSize=14, textColor=BPO_BLUE,  spaceBefore=18, spaceAfter=6, leading=18)
    s_h2      = ParagraphStyle("H2",      fontName="Helvetica-Bold",  fontSize=11, textColor=BPO_MID,   spaceBefore=10, spaceAfter=4, leading=14)
    s_h3      = ParagraphStyle("H3",      fontName="Helvetica-Bold",  fontSize=10, textColor=BPO_TEAL,  spaceBefore=8,  spaceAfter=3, leading=13)
    s_body    = ParagraphStyle("Body",    fontName="Helvetica",       fontSize=9,  textColor=colors.HexColor("#374151"), spaceAfter=4, leading=13)
    s_small   = ParagraphStyle("Small",   fontName="Helvetica",       fontSize=8,  textColor=GRAY,      spaceAfter=3,  leading=11)
    s_metric  = ParagraphStyle("Metric",  fontName="Helvetica-Bold",  fontSize=9,  textColor=BPO_TEAL,  spaceAfter=2,  leading=12)
    s_footer  = ParagraphStyle("Footer",  fontName="Helvetica",       fontSize=7.5,textColor=GRAY,      alignment=TA_CENTER)
    s_label   = ParagraphStyle("Label",   fontName="Helvetica-Bold",  fontSize=8,  textColor=GRAY,      spaceAfter=2)
    s_value   = ParagraphStyle("Value",   fontName="Helvetica",       fontSize=9,  textColor=BPO_BLUE,  spaceAfter=6, leading=12)

    story = []
    now = datetime.now().strftime("%B %d, %Y")

    # ── COVER HEADER ──
    header_data = [[
        Paragraph("BPO Hub", ParagraphStyle("logo", fontName="Helvetica-Bold", fontSize=18, textColor=colors.white)),
        Paragraph(f"Discovery Call Brief<br/><font size='9' color='#a0b4d0'>Prepared {now}</font>",
                  ParagraphStyle("rh", fontName="Helvetica", fontSize=11, textColor=colors.white, alignment=TA_RIGHT))
    ]]
    header_tbl = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BPO_BLUE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING", (0,0), (0,-1), 16),
        ("RIGHTPADDING", (-1,0), (-1,-1), 16),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 16))

    # ── PROSPECT OVERVIEW ──
    story.append(Paragraph("Prospect Overview", s_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=LGRAY, spaceAfter=10))

    def info_row(label, value):
        row_data = [[
            Paragraph(label, s_label),
            Paragraph(str(value) if value else "—", s_value)
        ]]
        t = Table(row_data, colWidths=[1.8*inch, 5.2*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,0), BPO_LIGHT),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("BOX", (0,0), (-1,-1), 0.5, LGRAY),
            ("LINEBELOW", (0,0), (-1,-1), 0.5, LGRAY),
        ]))
        return t

    story.append(info_row("Company Name", answers.get("company_name", "")))
    story.append(info_row("Contact Name", answers.get("contact_name", "")))
    story.append(info_row("Email", answers.get("email", "")))
    story.append(info_row("Industry / Sector", answers.get("sector", "")))
    story.append(info_row("Company Size", answers.get("company_size", "")))
    story.append(info_row("Current Systems", answers.get("systems", "")))
    story.append(info_row("Annual Revenue Range", answers.get("revenue", "")))
    story.append(Spacer(1, 14))

    # Pain points + goals
    pain_pts = answers.get("pain_points", [])
    goals_list = answers.get("goals", [])

    two_col = [[
        [Paragraph("Key Pain Points", s_h2)] + [Paragraph(f"• {p}", s_body) for p in pain_pts],
        [Paragraph("Strategic Goals", s_h2)] + [Paragraph(f"• {g}", s_body) for g in goals_list],
    ]]
    tc = Table(two_col, colWidths=[3.5*inch, 3.5*inch])
    tc.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (0,0), colors.HexColor("#f0f7ff")),
        ("BACKGROUND", (1,0), (1,0), colors.HexColor("#f0fdf4")),
        ("BOX", (0,0), (0,0), 0.5, BPO_MID),
        ("BOX", (1,0), (1,0), 0.5, BPO_TEAL),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(tc)
    story.append(Spacer(1, 4))

    if answers.get("challenges"):
        story.append(Paragraph("Additional Context", s_h2))
        story.append(Paragraph(answers["challenges"], s_body))

    story.append(PageBreak())

    # ── RECOMMENDED SOLUTIONS ──
    story.append(Paragraph("Recommended Solutions", s_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=LGRAY, spaceAfter=10))
    story.append(Paragraph(
        "Based on your responses, the following BPO Hub solutions are most aligned with your priorities and challenges.",
        s_body
    ))
    story.append(Spacer(1, 8))

    for i, (prod, score) in enumerate(top_products, 1):
        rank_label = ["Top Match", "Strong Match", "Recommended", "Consider", "Explore"][min(i-1, 4)]
        rank_color = [BPO_TEAL, BPO_MID, BPO_BLUE, GRAY, GRAY][min(i-1, 4)]

        prod_header = [[
            Paragraph(f"{i}. {prod['name']}", ParagraphStyle("ph", fontName="Helvetica-Bold", fontSize=11, textColor=colors.white)),
            Paragraph(rank_label, ParagraphStyle("rl", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=TA_RIGHT))
        ]]
        ph_tbl = Table(prod_header, colWidths=[5*inch, 2*inch])
        ph_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), rank_color),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (0,0), 12),
            ("RIGHTPADDING", (-1,0), (-1,0), 12),
        ]))
        story.append(ph_tbl)

        prod_body = [
            [Paragraph("Category", s_label), Paragraph(prod["category"], s_value)],
            [Paragraph("What It Does", s_label), Paragraph(prod["description"], s_body)],
            [Paragraph("Who It's For", s_label), Paragraph(prod["who_for"], s_body)],
            [Paragraph("Key Stats", s_label), Paragraph(prod["stats"], s_metric)],
        ]
        pb_tbl = Table(prod_body, colWidths=[1.5*inch, 5.5*inch])
        pb_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f8fafc")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LINEBELOW", (0,0), (-1,-2), 0.3, LGRAY),
            ("BOX", (0,0), (-1,-1), 0.5, LGRAY),
        ]))
        story.append(pb_tbl)
        story.append(Spacer(1, 12))

    story.append(PageBreak())

    # ── MATCHED CASE STUDIES ──
    story.append(Paragraph("Relevant Client Impact Stories", s_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=LGRAY, spaceAfter=10))
    story.append(Paragraph(
        "These BPO Hub engagements reflect challenges and outcomes most aligned with your situation.",
        s_body
    ))
    story.append(Spacer(1, 8))

    for cs, _ in top_cases:
        cs_header = [[Paragraph(cs["industry"], ParagraphStyle("csh", fontName="Helvetica-Bold", fontSize=10, textColor=colors.white))]]
        csh_tbl = Table(cs_header, colWidths=[7*inch])
        csh_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), BPO_TEAL),
            ("LEFTPADDING", (0,0), (-1,-1), 12),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ]))
        story.append(csh_tbl)

        story.append(Paragraph(cs["title"], ParagraphStyle("cst", fontName="Helvetica-Bold", fontSize=10, textColor=BPO_BLUE,
                                                             spaceBefore=6, spaceAfter=4, leftIndent=8)))
        story.append(Paragraph(cs["context"], ParagraphStyle("csc", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#374151"),
                                                               spaceAfter=6, leftIndent=8, leading=12)))

        metric_data = [[Paragraph(f"✓  {m}", s_metric) for m in cs["metrics"]]]
        if len(metric_data[0]) < 3:
            metric_data[0] += [Paragraph("", s_metric)] * (3 - len(metric_data[0]))
        mt = Table(metric_data, colWidths=[2.33*inch]*3)
        mt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
            ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#bbf7d0")),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(mt)
        story.append(Spacer(1, 14))

    # ── DISCOVERY CALL AGENDA ──
    story.append(PageBreak())
    story.append(Paragraph("Suggested Discovery Call Agenda", s_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=LGRAY, spaceAfter=10))

    agenda = [
        ("00–05 min", "Introductions & Context", "Brief background on BPO Hub and the prospect's business."),
        ("05–15 min", "Business Challenge Deep-Dive", f"Explore pain points: {', '.join(pain_pts[:3]) if pain_pts else 'as identified'}."),
        ("15–25 min", "Solution Walkthrough", f"Present: {', '.join([p[0]['name'] for p in top_products[:2]]) if top_products else 'matched solutions'}."),
        ("25–35 min", "Relevant Case Studies", "Walk through 1–2 client examples most relevant to prospect's situation."),
        ("35–45 min", "Current Systems & Integration", f"Review current tech stack ({answers.get('systems', 'as noted')}) and integration approach."),
        ("45–55 min", "Commercials & Engagement Model", "Discuss engagement options, pricing structure, and next steps."),
        ("55–60 min", "Q&A & Close", "Address questions and agree on follow-up actions."),
    ]
    for time, topic, detail in agenda:
        ag_row = [[
            Paragraph(time, ParagraphStyle("at", fontName="Helvetica-Bold", fontSize=8, textColor=BPO_TEAL)),
            Paragraph(f"<b>{topic}</b><br/>{detail}", ParagraphStyle("ad", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#374151"), leading=12))
        ]]
        at = Table(ag_row, colWidths=[1.1*inch, 5.9*inch])
        at.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,0), colors.HexColor("#f0fdf4")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LINEBELOW", (0,0), (-1,-1), 0.3, LGRAY),
        ]))
        story.append(at)

    story.append(Spacer(1, 20))

    # ── KEY QUESTIONS ──
    story.append(Paragraph("Key Discovery Questions", s_h2))
    questions = [
        "What does your current close process look like, and where do the biggest delays occur?",
        "How are you currently tracking cash flow and managing working capital?",
        "What level of finance reporting do leadership/board expect, and how often?",
        "Have you previously worked with an outsourced finance or accounting partner?",
        "What's your timeline for addressing these challenges?",
        "Are there any upcoming events (audit, investment round, ERP migration) driving urgency?",
    ]
    for q in questions:
        story.append(Paragraph(f"▸  {q}", ParagraphStyle("kq", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#374151"),
                                                           spaceAfter=5, leftIndent=8, leading=12)))

    story.append(Spacer(1, 20))

    # ── FOOTER ──
    story.append(HRFlowable(width="100%", thickness=0.5, color=LGRAY, spaceAfter=6))
    story.append(Paragraph(
        f"BPO Hub  ·  info@bpohub.com  ·  +1-888-229-5790  ·  www.bpohub.com  ·  Prepared {now}",
        s_footer
    ))
    story.append(Paragraph(
        "This document is confidential and prepared exclusively for internal BPO Hub discovery call use.",
        ParagraphStyle("conf", fontName="Helvetica-Oblique", fontSize=7, textColor=GRAY, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "results_ready" not in st.session_state:
    st.session_state.results_ready = False

TOTAL_STEPS = 5

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="bpo-header">
  <h1>🏢 BPO Hub Client Onboarding</h1>
  <p>Answer a few questions to receive your personalised solution recommendations and discovery call brief</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PROGRESS BAR
# ─────────────────────────────────────────────
if not st.session_state.results_ready:
    pct = int((st.session_state.step / TOTAL_STEPS) * 100)
    step_labels = ["Contact", "Business", "Challenges", "Goals", "Systems", "Results"]
    labels_html = "".join([f"<span>{l}</span>" for l in step_labels])
    st.markdown(f"""
    <div class="progress-container">
      <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    <div class="step-label">{labels_html}</div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STEP 0: CONTACT INFO
# ─────────────────────────────────────────────
if st.session_state.step == 0 and not st.session_state.results_ready:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-number">1</span><span class="step-title">Contact Information</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company Name *", value=st.session_state.answers.get("company_name", ""), placeholder="e.g. Acme Corp")
        email = st.text_input("Email Address *", value=st.session_state.answers.get("email", ""), placeholder="name@company.com")
    with col2:
        contact = st.text_input("Your Name *", value=st.session_state.answers.get("contact_name", ""), placeholder="First and Last Name")
        phone = st.text_input("Phone Number", value=st.session_state.answers.get("phone", ""), placeholder="+1 (555) 000-0000")

    st.markdown('</div>', unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav2:
        if st.button("Next →", key="next0", use_container_width=True):
            if company and contact and email:
                st.session_state.answers.update({"company_name": company, "contact_name": contact, "email": email, "phone": phone})
                st.session_state.step = 1
                st.rerun()
            else:
                st.error("Please fill in the required fields.")

# ─────────────────────────────────────────────
# STEP 1: BUSINESS PROFILE
# ─────────────────────────────────────────────
elif st.session_state.step == 1 and not st.session_state.results_ready:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-number">2</span><span class="step-title">Business Profile</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    sector_options = [
        "Select...",
        "Accounting / CPA Firm",
        "Artificial Intelligence / Technology",
        "Banking / Financial Services",
        "Construction / Real Estate",
        "E-Commerce / Retail",
        "Healthcare / Medical",
        "Manufacturing / Distribution",
        "Private Equity / Investment",
        "Professional Services",
        "Property Management",
        "SaaS / Software",
        "Staffing / Recruitment",
        "Startup / Early-Stage",
        "Other"
    ]
    size_options = ["Select...", "1–10 employees", "11–50 employees", "51–200 employees", "201–500 employees", "500+ employees"]
    revenue_options = ["Select...", "Under $1M", "$1M–$5M", "$5M–$20M", "$20M–$100M", "$100M+"]

    col1, col2 = st.columns(2)
    with col1:
        sector = st.selectbox("Industry / Sector *", sector_options,
                              index=sector_options.index(st.session_state.answers.get("sector", "Select...")) if st.session_state.answers.get("sector", "Select...") in sector_options else 0)
        size = st.selectbox("Company Size *", size_options,
                            index=size_options.index(st.session_state.answers.get("company_size", "Select...")) if st.session_state.answers.get("company_size", "Select...") in size_options else 0)
    with col2:
        revenue = st.selectbox("Annual Revenue Range", revenue_options,
                               index=revenue_options.index(st.session_state.answers.get("revenue", "Select...")) if st.session_state.answers.get("revenue", "Select...") in revenue_options else 0)
        country = st.text_input("Primary Country of Operations", value=st.session_state.answers.get("country", ""), placeholder="e.g. United States")

    st.markdown('</div>', unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("← Back", key="back1", use_container_width=True):
            st.session_state.step = 0
            st.rerun()
    with col_nav2:
        if st.button("Next →", key="next1", use_container_width=True):
            if sector != "Select..." and size != "Select...":
                st.session_state.answers.update({"sector": sector, "company_size": size, "revenue": revenue, "country": country})
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please select your industry and company size.")

# ─────────────────────────────────────────────
# STEP 2: PAIN POINTS
# ─────────────────────────────────────────────
elif st.session_state.step == 2 and not st.session_state.results_ready:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-number">3</span><span class="step-title">Current Challenges</span>', unsafe_allow_html=True)
    st.markdown("Select all that apply to your organization:", unsafe_allow_html=False)
    st.markdown("<br>", unsafe_allow_html=True)

    pain_options = [
        "Slow or unpredictable month-end / year-end close",
        "Manual reporting — too much time in spreadsheets",
        "Poor cash flow visibility or forecasting",
        "High cost of in-house finance team",
        "Audit delays or compliance risk",
        "Billing errors or slow collections (high DSO)",
        "Fragmented or inconsistent financial reporting",
        "No real-time KPI or performance dashboards",
        "ERP system issues or migration needed",
        "Revenue recognition complexity",
        "Subscription / SaaS spend out of control",
        "Scaling finance operations without adding headcount",
        "Talent shortages during peak periods (tax, audit)",
        "Multi-entity / group consolidation issues",
        "Cash leakage or unexplained margin erosion",
        "Cross-border payment or FX management issues",
    ]

    prev_pain = st.session_state.answers.get("pain_points", [])
    selected_pain = []
    cols = st.columns(2)
    for i, opt in enumerate(pain_options):
        with cols[i % 2]:
            if st.checkbox(opt, value=(opt in prev_pain), key=f"pain_{i}"):
                selected_pain.append(opt)

    st.markdown("<br>", unsafe_allow_html=True)
    challenges = st.text_area(
        "Anything else you'd like us to know about your situation?",
        value=st.session_state.answers.get("challenges", ""),
        placeholder="Describe any specific challenges, upcoming events, or context that would help us understand your needs...",
        height=100
    )

    st.markdown('</div>', unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("← Back", key="back2", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col_nav2:
        if st.button("Next →", key="next2", use_container_width=True):
            if selected_pain:
                st.session_state.answers.update({"pain_points": selected_pain, "challenges": challenges})
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please select at least one challenge.")

# ─────────────────────────────────────────────
# STEP 3: GOALS
# ─────────────────────────────────────────────
elif st.session_state.step == 3 and not st.session_state.results_ready:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-number">4</span><span class="step-title">Strategic Goals</span>', unsafe_allow_html=True)
    st.markdown("What are you trying to achieve in the next 12 months?", unsafe_allow_html=False)
    st.markdown("<br>", unsafe_allow_html=True)

    goal_options = [
        "Achieve a faster close (under 5 days)",
        "Build real-time reporting and dashboards",
        "Improve cash flow management and visibility",
        "Reduce operating costs / improve margins",
        "Scale finance operations without hiring",
        "Prepare for an audit or regulatory review",
        "Migrate or consolidate ERP/accounting systems",
        "Implement or improve budgeting and forecasting",
        "Support fundraising or investor due diligence",
        "Improve accounts receivable and reduce DSO",
        "Strengthen internal controls and governance",
        "Automate manual finance and accounting processes",
    ]

    prev_goals = st.session_state.answers.get("goals", [])
    selected_goals = []
    cols = st.columns(2)
    for i, opt in enumerate(goal_options):
        with cols[i % 2]:
            if st.checkbox(opt, value=(opt in prev_goals), key=f"goal_{i}"):
                selected_goals.append(opt)

    timeline_opts = ["Select...", "Immediately (within 30 days)", "1–3 months", "3–6 months", "6–12 months", "Exploring options"]
    timeline = st.selectbox("When are you looking to get started?",
                            timeline_opts,
                            index=timeline_opts.index(st.session_state.answers.get("timeline", "Select...")) if st.session_state.answers.get("timeline", "Select...") in timeline_opts else 0)

    st.markdown('</div>', unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("← Back", key="back3", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with col_nav2:
        if st.button("Next →", key="next3", use_container_width=True):
            if selected_goals:
                st.session_state.answers.update({"goals": selected_goals, "timeline": timeline})
                st.session_state.step = 4
                st.rerun()
            else:
                st.error("Please select at least one goal.")

# ─────────────────────────────────────────────
# STEP 4: SYSTEMS
# ─────────────────────────────────────────────
elif st.session_state.step == 4 and not st.session_state.results_ready:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<span class="step-number">5</span><span class="step-title">Current Systems & Setup</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    system_options = [
        "QuickBooks (Online or Desktop)",
        "Xero",
        "Sage",
        "MYOB",
        "Zoho Books",
        "Wave / FreshBooks",
        "Oracle NetSuite",
        "Microsoft Dynamics 365",
        "SAP",
        "Ramp",
        "Bill.com",
        "Stripe / Square / PayPal",
        "Wise / Payoneer",
        "WellSky",
        "Buildium / AppFolio / Yardi",
        "No formal system (spreadsheets)",
        "Other / In-house built",
    ]

    prev_systems = st.session_state.answers.get("system_list", [])
    selected_systems = []
    cols = st.columns(3)
    for i, sys in enumerate(system_options):
        with cols[i % 3]:
            if st.checkbox(sys, value=(sys in prev_systems), key=f"sys_{i}"):
                selected_systems.append(sys)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        prev_bpo = st.session_state.answers.get("prev_bpo", "")
        prev_bpo_opts = ["Select...", "Yes — currently outsourcing some finance/accounting", "Yes — tried it before", "No — fully in-house", "No — but open to it"]
        prev_bpo = st.selectbox("Have you previously outsourced finance or accounting?",
                                prev_bpo_opts,
                                index=prev_bpo_opts.index(prev_bpo) if prev_bpo in prev_bpo_opts else 0)
    with col2:
        budget_opts = ["Select...", "Under $2,000/month", "$2,000–$5,000/month", "$5,000–$10,000/month", "$10,000–$25,000/month", "$25,000+/month", "Not yet defined"]
        budget = st.selectbox("Estimated monthly budget for services",
                              budget_opts,
                              index=budget_opts.index(st.session_state.answers.get("budget", "Select...")) if st.session_state.answers.get("budget", "Select...") in budget_opts else 0)

    st.markdown('</div>', unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("← Back", key="back4", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    with col_nav2:
        if st.button("🔍 Generate My Recommendations", key="next4", use_container_width=True):
            systems_str = ", ".join(selected_systems) if selected_systems else "Not specified"
            st.session_state.answers.update({
                "system_list": selected_systems,
                "systems": systems_str,
                "prev_bpo": prev_bpo,
                "budget": budget
            })
            st.session_state.results_ready = True
            st.rerun()

# ─────────────────────────────────────────────
# RESULTS PAGE
# ─────────────────────────────────────────────
elif st.session_state.results_ready:
    answers = st.session_state.answers
    top_products, top_cases = compute_matches(answers)

    # Summary boxes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="summary-box">
          <h3>Company</h3>
          <p>{answers.get("company_name", "—")}</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="summary-box">
          <h3>Industry</h3>
          <p>{answers.get("sector", "—")}</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="summary-box">
          <h3>Key Priority</h3>
          <p>{answers.get("goals", ["—"])[0] if answers.get("goals") else "—"}</p>
        </div>""", unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📦 Recommended Solutions", "📊 Matched Case Studies", "📋 Discovery Call Brief"])

    with tab1:
        st.markdown("### Your Personalised Solution Matches")
        st.markdown(f"Based on **{len(answers.get('pain_points',[]))} pain points** and **{len(answers.get('goals',[]))} strategic goals** identified.", unsafe_allow_html=False)
        st.markdown("<br>", unsafe_allow_html=True)

        rank_labels = ["🥇 Top Match", "🥈 Strong Match", "🥉 Recommended", "4️⃣ Consider", "5️⃣ Explore"]
        for i, (prod, score) in enumerate(top_products):
            label = rank_labels[min(i, 4)]
            st.markdown(f"""
            <div class="product-card">
              <span class="match-score">{label}</span>
              <div class="product-name">{prod['name']}</div>
              <div style="margin:4px 0 8px; font-size:0.8rem; color:#64748b; font-weight:600;">{prod['category']}</div>
              <div style="font-size:0.88rem; color:#374151; margin-bottom:8px;">{prod['description']}</div>
              <div style="font-size:0.82rem; color:#64748b; margin-bottom:6px;"><em>{prod['who_for']}</em></div>
              <div style="font-size:0.82rem; color:#0d7377; font-weight:600;">📈 {prod['stats']}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Matched Client Impact Stories")
        st.markdown("These real BPO Hub engagements mirror your current challenges.", unsafe_allow_html=False)
        st.markdown("<br>", unsafe_allow_html=True)

        for cs, _ in top_cases:
            metrics_html = "".join([f'<span class="case-metric">✓ {m}</span>' for m in cs["metrics"]])
            st.markdown(f"""
            <div class="case-card">
              <div class="case-industry">📁 {cs['industry']}</div>
              <div class="case-headline" style="font-weight:600; color:#1e4db7; margin:4px 0;">{cs['title']}</div>
              <div style="font-size:0.85rem; color:#374151; margin-bottom:8px;">{cs['context']}</div>
              {metrics_html}
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### Discovery Call Brief")
        st.markdown("Generate a professional PDF brief for your sales team's discovery call with this prospect.")
        st.markdown("<br>", unsafe_allow_html=True)

        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown("**The PDF brief includes:**")
            st.markdown("""
- ✅ Full prospect overview and contact info
- ✅ Pain points, strategic goals, and context
- ✅ Top 5 recommended solutions with descriptions and stats
- ✅ Matched client case studies with quantified impact
- ✅ Suggested discovery call agenda (60-min structure)
- ✅ Key discovery questions to guide the conversation
            """)
        with col_right:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📄 Generate PDF Brief", key="gen_pdf", use_container_width=True):
                with st.spinner("Building your discovery call brief..."):
                    pdf_buffer = generate_pdf(answers, top_products, top_cases)
                    company_slug = answers.get("company_name", "prospect").replace(" ", "_").lower()
                    filename = f"BPO_Hub_Discovery_Brief_{company_slug}_{datetime.now().strftime('%Y%m%d')}.pdf"
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_buffer,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("Your discovery call brief is ready!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    col_reset1, col_reset2, col_reset3 = st.columns([1, 1, 1])
    with col_reset2:
        if st.button("🔄 Start New Assessment", use_container_width=True):
            st.session_state.step = 0
            st.session_state.answers = {}
            st.session_state.results_ready = False
            st.rerun()
