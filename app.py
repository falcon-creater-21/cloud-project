import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

  /* Dark sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0f1a 0%, #1a1a2e 100%);
    border-right: 1px solid #2a2a4a;
  }
  [data-testid="stSidebar"] * { color: #c8c8e8 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label { color: #8888bb !important; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; }

  /* Main background */
  .stApp { background: #f5f4f0; }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e8e6e0;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  }
  div[data-testid="metric-container"] label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9090a0 !important;
    font-weight: 500;
  }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-size: 2rem !important;
    font-weight: 800;
    color: #0f0f1a !important;
  }
  div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
  }

  /* Section headers */
  .section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f0f1a;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
  }
  .section-sub {
    font-size: 0.78rem;
    color: #9090a0;
    margin-bottom: 1rem;
  }

  /* Card wrapper */
  .chart-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #e8e6e0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
  }

  /* Page title */
  .page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f0f1a;
    letter-spacing: -0.04em;
    line-height: 1;
  }
  .page-sub {
    color: #9090a0;
    font-size: 0.9rem;
    margin-top: 4px;
  }

  /* Accent pill */
  .accent-pill {
    display: inline-block;
    background: #e8ff5a;
    color: #0f0f1a;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 99px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-left: 10px;
    vertical-align: middle;
  }

  /* Divider */
  hr { border: none; border-top: 1px solid #e8e6e0; margin: 1.5rem 0; }

  /* Hide Streamlit branding */
  #MainMenu, footer { visibility: hidden; }
  .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)


# ── Data generation ───────────────────────────────────────────────────────────
@st.cache_data
def generate_data(seed=42):
    np.random.seed(seed)
    random.seed(seed)

    months = pd.date_range("2024-01-01", periods=12, freq="MS")
    categories = ["Electronics", "Apparel", "Home & Garden", "Sports", "Beauty"]
    regions = ["North", "South", "East", "West", "Central"]

    # Monthly sales by category
    sales_data = []
    for month in months:
        for cat in categories:
            base = {"Electronics": 85000, "Apparel": 55000, "Home & Garden": 42000,
                    "Sports": 38000, "Beauty": 30000}[cat]
            growth = 1 + (months.get_loc(month) * 0.015)
            noise = np.random.normal(1, 0.08)
            sales_data.append({
                "month": month, "category": cat,
                "revenue": int(base * growth * noise),
                "units": int((base * growth * noise) / random.uniform(22, 28)),
                "profit": int(base * growth * noise * random.uniform(0.18, 0.32)),
            })
    df_sales = pd.DataFrame(sales_data)

    # Daily transactions (last 90 days)
    days = pd.date_range(end=datetime(2024, 12, 31), periods=90, freq="D")
    daily = pd.DataFrame({
        "date": days,
        "transactions": np.random.poisson(340, 90) + np.sin(np.arange(90) * 0.22) * 40,
        "avg_order": np.random.normal(87, 12, 90),
        "returns": np.random.poisson(18, 90),
    })

    # Regional performance
    regional = pd.DataFrame({
        "region": regions,
        "revenue": [np.random.randint(420000, 680000) for _ in regions],
        "customers": [np.random.randint(3200, 7800) for _ in regions],
        "satisfaction": [round(np.random.uniform(3.8, 4.9), 1) for _ in regions],
    })

    # Top products
    products = [
        "Wireless Earbuds Pro", "Yoga Mat Elite", "Smart Watch X3",
        "Running Shoes V2", "Coffee Maker Deluxe", "Skincare Bundle",
        "Laptop Stand", "Resistance Bands Set", "Moisturizer SPF50", "Backpack Ultra",
    ]
    top_products = pd.DataFrame({
        "product": products,
        "revenue": sorted(np.random.randint(28000, 140000, 10), reverse=True),
        "units": sorted(np.random.randint(400, 3200, 10), reverse=True),
        "rating": [round(np.random.uniform(3.9, 4.95), 2) for _ in products],
        "category": [random.choice(categories) for _ in products],
    })

    return df_sales, daily, regional, top_products


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Dashboard Controls")
    st.markdown("---")

    selected_categories = st.multiselect(
        "Categories",
        ["Electronics", "Apparel", "Home & Garden", "Sports", "Beauty"],
        default=["Electronics", "Apparel", "Home & Garden", "Sports", "Beauty"],
    )

    selected_metric = st.selectbox(
        "Primary Metric",
        ["Revenue", "Units Sold", "Profit"],
        index=0,
    )

    chart_style = st.selectbox(
        "Chart Style",
        ["Area", "Bar", "Line"],
        index=0,
    )

    st.markdown("---")
    st.markdown("**Date Range**")
    month_start = st.slider("From month", 1, 12, 1)
    month_end = st.slider("To month", 1, 12, 12)

    st.markdown("---")
    st.markdown('<p style="font-size:0.7rem;color:#5555aa;text-align:center">Sales Intelligence v1.0<br>Data: FY 2024</p>', unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df_sales, daily, regional, top_products = generate_data()

# Filter
df_filtered = df_sales[
    (df_sales["category"].isin(selected_categories)) &
    (df_sales["month"].dt.month >= month_start) &
    (df_sales["month"].dt.month <= month_end)
]

metric_col = {"Revenue": "revenue", "Units Sold": "units", "Profit": "profit"}[selected_metric]

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_date = st.columns([3, 1])
with col_title:
    st.markdown('<div class="page-title">Sales Intelligence <span class="accent-pill">LIVE</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Fiscal Year 2024 · All markets · Updated Dec 31</div>', unsafe_allow_html=True)
with col_date:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:right;font-size:0.8rem;color:#9090a0">{datetime.now().strftime("%B %d, %Y")}</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_rev = df_filtered["revenue"].sum()
total_units = df_filtered["units"].sum()
total_profit = df_filtered["profit"].sum()
margin = (total_profit / total_rev * 100) if total_rev else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${total_rev:,.0f}", "+12.4%")
k2.metric("Units Sold", f"{total_units:,}", "+8.7%")
k3.metric("Net Profit", f"${total_profit:,.0f}", "+15.2%")
k4.metric("Profit Margin", f"{margin:.1f}%", "+1.8pp")

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Trend + Donut ──────────────────────────────────────────────────────
col_trend, col_donut = st.columns([3, 2])

with col_trend:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">{selected_metric} Trend by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Monthly performance across selected categories</div>', unsafe_allow_html=True)

    pivot = df_filtered.pivot_table(index="month", columns="category", values=metric_col, aggfunc="sum").fillna(0)

    palette = ["#0f0f1a", "#e8ff5a", "#6c63ff", "#ff6584", "#43e97b"]
    fig_trend = go.Figure()
    for i, cat in enumerate(pivot.columns):
        color = palette[i % len(palette)]
        if chart_style == "Area":
            fig_trend.add_trace(go.Scatter(
                x=pivot.index, y=pivot[cat], name=cat, mode="lines",
                line=dict(color=color, width=2.5),
                fill="tozeroy", fillcolor=color.replace(")", ",0.08)").replace("rgb", "rgba") if color.startswith("rgb") else color + "14",
                stackgroup=None,
            ))
        elif chart_style == "Bar":
            fig_trend.add_trace(go.Bar(x=pivot.index, y=pivot[cat], name=cat, marker_color=color))
        else:
            fig_trend.add_trace(go.Scatter(x=pivot.index, y=pivot[cat], name=cat, mode="lines+markers",
                                           line=dict(color=color, width=2.5), marker=dict(size=6)))

    fig_trend.update_layout(
        height=280, margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=11, family="DM Sans")),
        xaxis=dict(showgrid=False, tickfont=dict(size=11), tickformat="%b"),
        yaxis=dict(showgrid=True, gridcolor="#f0eee8", tickfont=dict(size=11),
                   tickprefix="$" if selected_metric != "Units Sold" else ""),
        barmode="stack" if chart_style == "Bar" else None,
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_donut:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">Category Mix</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">Share of {selected_metric.lower()} by category</div>', unsafe_allow_html=True)

    cat_totals = df_filtered.groupby("category")[metric_col].sum().reset_index()
    fig_donut = go.Figure(go.Pie(
        labels=cat_totals["category"], values=cat_totals[metric_col],
        hole=0.62,
        marker=dict(colors=["#0f0f1a", "#e8ff5a", "#6c63ff", "#ff6584", "#43e97b"],
                    line=dict(color="white", width=3)),
        textfont=dict(family="DM Sans", size=11),
    ))
    fig_donut.update_layout(
        height=280, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="white",
        legend=dict(font=dict(size=10, family="DM Sans"), orientation="h",
                    yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text=f"<b>{len(selected_categories)}</b><br>cats", x=0.5, y=0.5,
                          font=dict(size=14, family="Syne"), showarrow=False)],
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 2: Daily volume + Regional ───────────────────────────────────────────
col_daily, col_region = st.columns([2, 3])

with col_daily:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Daily Transactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Last 90 days · orders processed</div>', unsafe_allow_html=True)

    fig_daily = go.Figure(go.Bar(
        x=daily["date"], y=daily["transactions"],
        marker_color="#6c63ff", marker_line_width=0,
        hovertemplate="<b>%{x|%b %d}</b><br>%{y:.0f} orders<extra></extra>",
    ))
    fig_daily.update_layout(
        height=240, margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, tickformat="%b %d", tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#f0eee8", tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_daily, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_region:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Regional Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Revenue, customers & satisfaction by region</div>', unsafe_allow_html=True)

    fig_bubble = go.Figure(go.Scatter(
        x=regional["customers"], y=regional["revenue"],
        mode="markers+text",
        text=regional["region"],
        textposition="top center",
        marker=dict(
            size=regional["satisfaction"] * 12,
            color=["#0f0f1a", "#e8ff5a", "#6c63ff", "#ff6584", "#43e97b"],
            line=dict(color="white", width=2),
            opacity=0.9,
        ),
        hovertemplate="<b>%{text}</b><br>Customers: %{x:,}<br>Revenue: $%{y:,}<extra></extra>",
    ))
    fig_bubble.update_layout(
        height=240, margin=dict(l=0, r=0, t=10, b=30),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(title="Customers", showgrid=True, gridcolor="#f0eee8", tickfont=dict(size=10)),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#f0eee8", tickfont=dict(size=10),
                   tickprefix="$"),
        showlegend=False,
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 3: Top Products ───────────────────────────────────────────────────────
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">Top Products by Revenue</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Ranked by total revenue · bubble size = customer rating</div>', unsafe_allow_html=True)

col_bar, col_table = st.columns([3, 2])

with col_bar:
    fig_prod = go.Figure(go.Bar(
        x=top_products["revenue"][:8],
        y=top_products["product"][:8],
        orientation="h",
        marker=dict(
            color=top_products["revenue"][:8],
            colorscale=[[0, "#e8e6e0"], [1, "#6c63ff"]],
            line=dict(width=0),
        ),
        text=[f"${r:,.0f}" for r in top_products["revenue"][:8]],
        textposition="outside",
        textfont=dict(size=11, family="DM Sans"),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,}<extra></extra>",
    ))
    fig_prod.update_layout(
        height=300, margin=dict(l=0, r=60, t=0, b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f0eee8", tickprefix="$", tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, tickfont=dict(size=11)),
    )
    st.plotly_chart(fig_prod, use_container_width=True)

with col_table:
    display_df = top_products[["product", "units", "rating", "category"]].head(8).copy()
    display_df.columns = ["Product", "Units", "⭐ Rating", "Category"]
    display_df["Units"] = display_df["Units"].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True, height=295, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;font-size:0.75rem;color:#b0b0c0;font-family:DM Sans">'
    '📊 Sales Intelligence Dashboard · Built with Streamlit & Plotly · FY 2024 Data'
    '</div>',
    unsafe_allow_html=True
)
