import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import os
import sys
import google.generativeai as genai

from utils.ai_helper import AIHealthcareAnalyst

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from data.india_healthcare_data import (
    TOTAL_GAP, AHP_CATEGORIES, STATE_DATA, DEMOGRAPHIC_DATA, WHO_BENCHMARKS,
    REGION_DATA, TRAINING_INFRASTRUCTURE, CURRENT_FUNDING, INDIA_BUDGET_TREND,
    GLOBAL_HEALTH_SPENDING_COMPARISON, FUNDING_SOURCES, STRATEGY_PORTFOLIO, DATA_SOURCES,
    get_category_dataframe, get_state_dataframe, get_region_summary,
    calculate_cost_projection, get_scenario_comparison,
    project_baseline_scenario, project_no_intervention_scenario, 
    project_proposed_strategy_scenario, format_indian_number, format_large_number,
    get_budget_trend_dataframe, get_funding_sources_dataframe, 
    get_global_comparison_dataframe, get_strategy_summary
)

st.set_page_config(
    page_title="India AHP Gap Analysis & Strategy Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #5a6c7d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .section-header {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1e3a5f;
        border-bottom: 3px solid #3182ce;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .crisis-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    }
    .success-metric {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
    }
    .info-box {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8eef5 100%);
        border-left: 5px solid #3182ce;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .warning-box {
        background: linear-gradient(135deg, #fffaf0 0%, #fff5e6 100%);
        border-left: 5px solid #ed8936;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .critical-box {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
        border-left: 5px solid #e53e3e;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .strategy-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .strategy-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    .phase-immediate { border-left: 4px solid #e53e3e; }
    .phase-intermediate { border-left: 4px solid #ed8936; }
    .phase-long-term { border-left: 4px solid #38a169; }
    .source-badge {
        display: inline-block;
        background: #edf2f7;
        color: #4a5568;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.25rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: #f0f4f8;
        border-radius: 10px 10px 0 0;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3182ce;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/255px-Flag_of_India.svg.png", width=80)
    st.title("Navigation")
    
    page = st.radio(
        "Select Module",
        [
            "🏠 Executive Summary",
            "📊 Current Situation",
            "🗺️ Geographic Analysis",
            "📈 Scenario Comparison",
            "💰 Cost Calculator",
            "💵 Budget & Funding",
            "🎯 Strategy Formulation",
            "📋 Investment Planning",
            "👥 Demographics Analysis",
            "🤖 AI Policy Recommendations",     
            "📊 AI Report Generator" 
            "📚 Data Sources"
        ],
        index=0
    )
    
    st.divider()
    st.markdown("### Quick Stats")
    st.metric("Total Gap", f"{TOTAL_GAP/1e6:.1f}M", delta=None)
    st.metric("States Analyzed", len(STATE_DATA))
    st.metric("AHP Categories", len(AHP_CATEGORIES))
    
    st.divider()
    st.markdown("### WHO UHC Target")
    st.progress(WHO_BENCHMARKS["uhc_service_coverage_index"]["india_current"] / 100)
    st.caption(f"India: {WHO_BENCHMARKS['uhc_service_coverage_index']['india_current']}% | Target: {WHO_BENCHMARKS['uhc_service_coverage_index']['who_target']}%")


def create_3d_crisis_gauge():
    fig = go.Figure()
    
    categories = list(AHP_CATEGORIES.keys())
    gaps = [AHP_CATEGORIES[cat]["gap"] for cat in categories]
    currents = [AHP_CATEGORIES[cat]["current"] for cat in categories]
    
    max_gap = max(gaps)
    normalized_gaps = [g / max_gap for g in gaps]
    
    theta = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
    x = np.cos(theta) * 2
    y = np.sin(theta) * 2
    z = [g / 1e5 for g in gaps]
    
    colors = ['#e53e3e' if g > 500000 else '#ecc94b' if g > 200000 else '#48bb78' for g in gaps]
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        marker=dict(
            size=[max(10, ng * 30) for ng in normalized_gaps],
            color=colors,
            opacity=0.8,
            line=dict(color='white', width=2)
        ),
        text=[f"{cat[:15]}..." if len(cat) > 15 else cat for cat in categories],
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Gap: %{z:.0f}K<extra></extra>',
        name='AHP Categories'
    ))
    
    fig.add_trace(go.Mesh3d(
        x=[0, 0, 0, 0],
        y=[0, 0, 0, 0],
        z=[0, 0, 0, 0],
        opacity=0,
        showlegend=False
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(showgrid=False, showticklabels=False, title=''),
            yaxis=dict(showgrid=False, showticklabels=False, title=''),
            zaxis=dict(title='Gap (Lakhs)', tickformat='.0f'),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        title=dict(text='3D Gap Visualization by Category', font=dict(size=18)),
        height=500,
        margin=dict(l=0, r=0, t=40, b=0),
        hoverlabel=dict(bgcolor="white", font_size=14)
    )
    
    return fig


def create_interactive_category_chart():
    df = get_category_dataframe()
    df = df.sort_values('Gap', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['Category'],
        x=df['Current'],
        name='Current Workforce',
        orientation='h',
        marker=dict(
            color='#4299e1',
            line=dict(color='#2b6cb0', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Current: %{x:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        y=df['Category'],
        x=df['Gap'],
        name='Gap (Shortage)',
        orientation='h',
        marker=dict(
            color='#fc8181',
            line=dict(color='#c53030', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Gap: %{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='stack',
        title=dict(text='Allied Health Professionals: Current Workforce vs Gap', font=dict(size=18)),
        xaxis_title='Number of Professionals',
        yaxis_title='',
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="white", font_size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig


def create_3d_scenario_comparison(scenario_df):
    scenarios = scenario_df['Scenario'].unique()
    years = scenario_df['Year'].unique()
    
    fig = go.Figure()
    
    colors = {
        'Baseline (Current Trend)': '#3182ce',
        'No Intervention': '#e53e3e',
        'Proposed Strategy': '#38a169'
    }
    
    for scenario in scenarios:
        df_scenario = scenario_df[scenario_df['Scenario'] == scenario]
        
        fig.add_trace(go.Scatter3d(
            x=[scenarios.tolist().index(scenario)] * len(df_scenario),
            y=df_scenario['Year'],
            z=df_scenario['Gap'] / 1e6,
            mode='lines+markers',
            name=scenario,
            line=dict(color=colors.get(scenario, '#888'), width=6),
            marker=dict(size=6, color=colors.get(scenario, '#888')),
            hovertemplate=f'<b>{scenario}</b><br>Year: %{{y}}<br>Gap: %{{z:.2f}}M<extra></extra>'
        ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                ticktext=list(scenarios),
                tickvals=list(range(len(scenarios))),
                title='Scenario'
            ),
            yaxis=dict(title='Year'),
            zaxis=dict(title='Gap (Millions)'),
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2))
        ),
        title=dict(text='3D Scenario Projection Comparison', font=dict(size=18)),
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0.95, xanchor="center", x=0.5)
    )
    
    return fig


def create_state_gap_map():
    state_df = get_state_dataframe()
    
    m = folium.Map(location=[22.5, 82.5], zoom_start=5, tiles='CartoDB positron')
    
    max_gap = state_df['Gap'].max()
    
    for _, row in state_df.iterrows():
        if row['Gap'] > 0:
            color = '#e53e3e' if row['Gap'] > 200000 else ('#ecc94b' if row['Gap'] > 50000 else '#48bb78')
            radius = max(5, min(30, (row['Gap'] / max_gap) * 30))
        else:
            color = '#38a169'
            radius = 8
        
        popup_html = f"""
        <div style="font-family: Arial; min-width: 220px; padding: 10px;">
            <h4 style="margin-bottom: 10px; color: #1a365d; border-bottom: 2px solid #3182ce; padding-bottom: 5px;">{row['State']}</h4>
            <table style="width: 100%; font-size: 13px;">
                <tr><td><b>Population:</b></td><td style="text-align: right;">{row['Population']:,}</td></tr>
                <tr><td><b>Current AHP:</b></td><td style="text-align: right;">{row['Current AHP']:,}</td></tr>
                <tr><td><b>Required AHP:</b></td><td style="text-align: right;">{row['Required AHP']:,}</td></tr>
                <tr><td><b>Gap:</b></td><td style="text-align: right; color: {'#e53e3e' if row['Gap'] > 0 else '#38a169'}; font-weight: bold;">{row['Gap']:,}</td></tr>
                <tr><td><b>AHP per 10K:</b></td><td style="text-align: right;">{row['AHP per 10K']}</td></tr>
                <tr><td><b>Training Institutions:</b></td><td style="text-align: right;">{row['Training Institutions']}</td></tr>
            </table>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=2
        ).add_to(m)
    
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                background-color: white; padding: 15px; border-radius: 10px;
                border: 2px solid #ccc; font-size: 13px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
        <p style="margin: 0 0 8px 0; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px;">Gap Severity</p>
        <p style="margin: 4px 0;"><span style="color: #e53e3e; font-size: 16px;">●</span> Critical (>200K)</p>
        <p style="margin: 4px 0;"><span style="color: #ecc94b; font-size: 16px;">●</span> Moderate (50K-200K)</p>
        <p style="margin: 4px 0;"><span style="color: #48bb78; font-size: 16px;">●</span> Low (<50K)</p>
        <p style="margin: 4px 0;"><span style="color: #38a169; font-size: 16px;">●</span> Surplus</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m


def create_budget_trend_chart():
    df = get_budget_trend_dataframe()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=df['Financial Year'],
            y=df['Health Budget (₹ Cr)'],
            name='Health Budget (₹ Cr)',
            marker_color='#4299e1',
            hovertemplate='FY %{x}<br>Budget: ₹%{y:,.0f} Cr<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['Financial Year'],
            y=df['Health % of Budget'],
            mode='lines+markers',
            name='% of Total Budget',
            line=dict(color='#e53e3e', width=3),
            marker=dict(size=8),
            hovertemplate='FY %{x}<br>%{y:.2f}% of Budget<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['Financial Year'],
            y=df['Health % of GDP'],
            mode='lines+markers',
            name='% of GDP',
            line=dict(color='#38a169', width=3, dash='dot'),
            marker=dict(size=8),
            hovertemplate='FY %{x}<br>%{y:.2f}% of GDP<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.add_hline(y=2.5, line_dash="dash", line_color="orange", 
                  annotation_text="NHP Target: 2.5% of GDP", secondary_y=True)
    
    fig.update_layout(
        title=dict(text='India Health Budget Trend (10-Year Analysis)', font=dict(size=18)),
        xaxis_title='Financial Year',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="white", font_size=14)
    )
    fig.update_yaxes(title_text="Health Budget (₹ Crores)", secondary_y=False)
    fig.update_yaxes(title_text="Percentage (%)", secondary_y=True)
    
    return fig


def create_funding_waterfall():
    df = get_funding_sources_dataframe()
    df = df.sort_values('Potential (₹ Cr/Year)', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Source'],
        y=df['Current (₹ Cr/Year)'],
        name='Current Funding',
        marker_color='#4299e1',
        hovertemplate='<b>%{x}</b><br>Current: ₹%{y:,.0f} Cr<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=df['Source'],
        y=df['Additional Mobilizable'],
        name='Additional Potential',
        marker_color='#48bb78',
        hovertemplate='<b>%{x}</b><br>Additional Potential: ₹%{y:,.0f} Cr<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='stack',
        title=dict(text='Funding Sources: Current vs Potential', font=dict(size=18)),
        xaxis_title='',
        yaxis_title='Amount (₹ Crores/Year)',
        height=450,
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_global_comparison_chart():
    df = get_global_comparison_dataframe()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Country'],
        y=df['Total Health % GDP'],
        name='Total Health Spending % GDP',
        marker_color='#4299e1'
    ))
    
    fig.add_trace(go.Bar(
        x=df['Country'],
        y=df['Govt Health % GDP'],
        name='Government Health % GDP',
        marker_color='#38a169'
    ))
    
    fig.update_layout(
        barmode='group',
        title=dict(text='Global Health Spending Comparison (% of GDP)', font=dict(size=18)),
        xaxis_title='',
        yaxis_title='Percentage of GDP',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_scenario_comparison_chart(scenario_df):
    fig = px.line(
        scenario_df,
        x='Year',
        y='Gap',
        color='Scenario',
        title='Workforce Gap Projection: Scenario Comparison',
        color_discrete_map={
            'Baseline (Current Trend)': '#3182ce',
            'No Intervention': '#e53e3e',
            'Proposed Strategy': '#38a169'
        }
    )
    
    fig.update_traces(line=dict(width=3))
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Workforce Gap',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="white", font_size=14)
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="green", 
                  annotation_text="Zero Gap (UHC Target)")
    
    return fig


def create_cost_breakdown_chart(cost_df):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=cost_df['Calendar Year'],
        y=cost_df['Training Cost (₹ Cr)'],
        name='Training',
        marker_color='#4299e1',
        hovertemplate='Year %{x}<br>Training: ₹%{y:,.0f} Cr<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=cost_df['Calendar Year'],
        y=cost_df['Salary Cost (₹ Cr)'],
        name='Salaries',
        marker_color='#48bb78',
        hovertemplate='Year %{x}<br>Salaries: ₹%{y:,.0f} Cr<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=cost_df['Calendar Year'],
        y=cost_df['Infrastructure Cost (₹ Cr)'],
        name='Infrastructure',
        marker_color='#ecc94b',
        hovertemplate='Year %{x}<br>Infrastructure: ₹%{y:,.0f} Cr<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=cost_df['Calendar Year'],
        y=cost_df['Retention Cost (₹ Cr)'],
        name='Retention',
        marker_color='#9f7aea',
        hovertemplate='Year %{x}<br>Retention: ₹%{y:,.0f} Cr<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='stack',
        title=dict(text='Annual Cost Breakdown by Category (Inflation Adjusted)', font=dict(size=18)),
        xaxis_title='Year',
        yaxis_title='Cost (₹ Crores)',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_cumulative_cost_chart(cost_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=cost_df['Calendar Year'],
            y=cost_df['Cumulative Cost (₹ Cr)'],
            mode='lines+markers',
            name='Cumulative Cost',
            line=dict(color='#3182ce', width=3),
            fill='tozeroy',
            fillcolor='rgba(49, 130, 206, 0.1)',
            hovertemplate='Year %{x}<br>Cumulative: ₹%{y:,.0f} Cr<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=cost_df['Calendar Year'],
            y=cost_df['Gap Closure %'],
            mode='lines+markers',
            name='Gap Closure %',
            line=dict(color='#38a169', width=3, dash='dot'),
            hovertemplate='Year %{x}<br>Gap Closure: %{y:.1f}%<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title=dict(text='Cumulative Investment vs Gap Closure Progress', font=dict(size=18)),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Cumulative Cost (₹ Crores)", secondary_y=False)
    fig.update_yaxes(title_text="Gap Closure (%)", secondary_y=True)
    
    return fig


def generate_ai_strategy(gap_analysis, budget_constraints, priority_areas, timeline, phase_focus):
    if not OPENAI_API_KEY:
        return None
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""You are a senior healthcare policy expert specializing in India's healthcare workforce development and Universal Health Coverage planning.

Based on the following analysis, provide a comprehensive strategy to address the Allied Health Professional gap:

GAP ANALYSIS:
- Total workforce gap: 6.5 million professionals (verified by Ministry of Health 2012)
- Key shortage areas: {gap_analysis}
- Timeline for closure: {timeline} years
- Budget constraints: {budget_constraints}
- Priority focus areas: {priority_areas}
- Phase emphasis: {phase_focus}

Please provide a detailed, actionable strategy document with the following sections:

## 1. EXECUTIVE SUMMARY (3-4 paragraphs)
- Current crisis assessment
- Strategic vision
- Key success factors

## 2. PHASED IMPLEMENTATION STRATEGY

### IMMEDIATE PRIORITIES (Years 1-2)
For each strategy, provide:
- Strategy Name and Description
- Specific Locations for Implementation
- Expected Impact (quantified)
- Cost Estimate (₹ Crores)
- Gap Reduction Potential
- Key Actions (5-7 steps)
- Success Metrics

### INTERMEDIATE PHASE (Years 3-5)
[Same structure as above]

### LONG-TERM SUSTAINABILITY (Years 6-{timeline})
[Same structure as above]

## 3. FUNDING MECHANISM
- Government budget allocation recommendations
- Public-Private Partnership models
- International aid opportunities
- Innovative financing (health cess, CSR, etc.)

## 4. POLICY RECOMMENDATIONS
- Legislative changes needed
- Regulatory framework updates
- Institutional reforms

## 5. RISK MITIGATION
- Key risks and contingencies
- Monitoring and evaluation framework

## 6. SUCCESS METRICS & MILESTONES
- Year-wise targets
- Key Performance Indicators

Format with clear headers, bullet points, and quantified targets where possible."""

        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a senior healthcare policy advisor with 20+ years of experience in workforce planning for developing nations, particularly India. Provide evidence-based, practical, and detailed recommendations with specific implementation steps, cost estimates, and measurable outcomes."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=8192
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        st.error(f"Error generating strategy: {str(e)}")
        return None


if "🏠 Executive Summary" in page:
    st.markdown('<h1 class="main-header">India Allied Health Professionals Gap Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Strategic Planning Platform for WHO Universal Health Coverage Achievement</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="critical-box">
        <h3 style="margin-top: 0; color: #c53030;">NATIONAL HEALTH EMERGENCY</h3>
        <p style="font-size: 1.1rem; margin-bottom: 0;">
            India faces a critical shortage of <b>6.5 million</b> Allied Health Professionals to achieve WHO's Universal Health Coverage goals. 
            Without immediate, comprehensive intervention, this gap will persist for decades, leaving <b>hundreds of millions</b> without adequate healthcare access.
        </p>
        <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
            Source: Ministry of Health and Family Welfare Assessment, 2012 | WHO India Health Workforce Report
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="crisis-metric">
            <h2 style="margin:0; font-size: 2.5rem;">6.5M</h2>
            <p style="margin:0; font-size: 1.1rem;">Professional Shortage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        deficit_states = len([s for s, d in STATE_DATA.items() if d['gap'] > 0])
        st.markdown(f"""
        <div class="metric-card">
            <h2 style="margin:0; font-size: 2.5rem;">{deficit_states}</h2>
            <p style="margin:0; font-size: 1.1rem;">States in Deficit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="warning-box" style="background: linear-gradient(135deg, #f6ad55 0%, #ed8936 100%); color: white; border: none; border-radius: 16px;">
            <h2 style="margin:0; font-size: 2.5rem;">₹90K Cr</h2>
            <p style="margin:0; font-size: 1.1rem;">Annual Health Budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="success-metric">
            <h2 style="margin:0; font-size: 2.5rem;">55%</h2>
            <p style="margin:0; font-size: 1.1rem;">UHC Coverage Index</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h3 class="section-header">3D Gap Visualization</h3>', unsafe_allow_html=True)
        st.plotly_chart(create_3d_crisis_gauge(), use_container_width=True)
        st.caption("Interactive 3D view - Drag to rotate, scroll to zoom. Height represents gap magnitude.")
    
    with col2:
        st.markdown('<h3 class="section-header">WHO Benchmark Comparison</h3>', unsafe_allow_html=True)
        benchmarks = []
        for metric, data in WHO_BENCHMARKS.items():
            benchmarks.append({
                'Metric': metric.replace('_', ' ').title(),
                'WHO Target': data['who_target'],
                'India Current': data['india_current'],
                'Gap %': data['gap_pct']
            })
        
        bench_df = pd.DataFrame(benchmarks)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=bench_df['Metric'],
            y=bench_df['WHO Target'],
            name='WHO Target',
            marker_color='#38a169'
        ))
        fig.add_trace(go.Bar(
            x=bench_df['Metric'],
            y=bench_df['India Current'],
            name='India Current',
            marker_color='#e53e3e'
        ))
        fig.update_layout(
            barmode='group',
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-15
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<h3 class="section-header">Workforce Gap by Category</h3>', unsafe_allow_html=True)
    st.plotly_chart(create_interactive_category_chart(), use_container_width=True)
    
    st.markdown("---")
    st.markdown('<h3 class="section-header">Critical Insights</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #2b6cb0; margin-top: 0;">Highest Shortage Category</h4>
            <p style="font-size: 1.1rem;"><b>Nurses & Midwives</b> account for <b>44%</b> of the total gap with a shortage of <b>2.86 million</b> professionals.</p>
            <p style="font-size: 0.9rem; color: #666;">This single category requires focused intervention.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4 style="color: #c05621; margin-top: 0;">Rural Healthcare Crisis</h4>
            <p style="font-size: 1.1rem;"><b>75%</b> of the gap is concentrated in rural areas where <b>65%</b> of India's population resides.</p>
            <p style="font-size: 0.9rem; color: #666;">Urban-rural disparity is the primary equity challenge.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="critical-box">
            <h4 style="color: #c53030; margin-top: 0;">Training Capacity Deficit</h4>
            <p style="font-size: 1.1rem;">Current annual graduate output of <b>485K</b> is insufficient to close the gap within <b>20 years</b>.</p>
            <p style="font-size: 0.9rem; color: #666;">Training capacity must be doubled for UHC by 2030.</p>
        </div>
        """, unsafe_allow_html=True)


elif "📊 Current Situation" in page:
    st.markdown('<h1 class="main-header">Current Situation Dashboard</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Overview", "Category Analysis", "Training Infrastructure", "Current Funding"])
    
    with tabs[0]:
        st.markdown('<h3 class="section-header">National Overview</h3>', unsafe_allow_html=True)
        
        category_df = get_category_dataframe()
        total_current = category_df['Current'].sum()
        total_required = category_df['Required'].sum()
        total_gap = category_df['Gap'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Workforce", f"{total_current/1e6:.2f}M")
        col2.metric("Required Workforce", f"{total_required/1e6:.2f}M")
        col3.metric("Absolute Gap", f"{total_gap/1e6:.2f}M", delta=f"-{(total_gap/total_required)*100:.1f}%")
        col4.metric("Gap as % of Target", f"{(total_gap/total_required)*100:.1f}%")
        
        st.plotly_chart(create_interactive_category_chart(), use_container_width=True)
        
        st.markdown('<h3 class="section-header">Gap Distribution</h3>', unsafe_allow_html=True)
        
        fig = px.pie(
            category_df,
            values='Gap',
            names='Category',
            title='Share of Total Gap by Professional Category',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown('<h3 class="section-header">Detailed Category Analysis</h3>', unsafe_allow_html=True)
        
        category_df = get_category_dataframe()
        
        selected_category = st.selectbox(
            "Select Category for Detailed View",
            category_df['Category'].tolist()
        )
        
        cat_data = AHP_CATEGORIES[selected_category]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Workforce", f"{cat_data['current']:,}")
        col2.metric("Required Workforce", f"{cat_data['required']:,}")
        col3.metric("Gap", f"{cat_data['gap']:,}", delta=f"-{cat_data['gap_percentage']:.1f}%")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Annual Salary", format_indian_number(cat_data['avg_salary_inr']))
        col2.metric("Training Cost/Person", format_indian_number(cat_data['training_cost_inr']))
        col3.metric("Training Duration", f"{cat_data['training_duration_years']} years")
        
        st.info(f"**Description:** {cat_data['description']}")
        
        total_training_cost = cat_data['gap'] * cat_data['training_cost_inr']
        annual_salary_cost = cat_data['gap'] * cat_data['avg_salary_inr']
        
        st.markdown("### Cost to Close This Category's Gap")
        col1, col2 = st.columns(2)
        col1.metric("Total Training Investment", f"₹{total_training_cost/1e11:.2f} Lakh Cr")
        col2.metric("Annual Salary Requirement", f"₹{annual_salary_cost/1e11:.2f} Lakh Cr/year")
        
        st.markdown("### Category Comparison")
        
        comparison_fig = go.Figure()
        comparison_fig.add_trace(go.Bar(
            x=category_df['Category'],
            y=category_df['Training Cost (₹)']/1e5,
            name='Training Cost (₹ Lakhs)',
            marker_color='#4299e1'
        ))
        comparison_fig.add_trace(go.Bar(
            x=category_df['Category'],
            y=category_df['Avg Salary (₹)']/1e5,
            name='Annual Salary (₹ Lakhs)',
            marker_color='#48bb78'
        ))
        comparison_fig.update_layout(
            barmode='group',
            xaxis_tickangle=-45,
            height=400,
            title='Training Cost vs Salary Comparison Across Categories'
        )
        st.plotly_chart(comparison_fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown('<h3 class="section-header">Training Infrastructure Status</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Institutions", f"{TRAINING_INFRASTRUCTURE['total_institutions']:,}")
        col2.metric("Nursing Colleges", f"{TRAINING_INFRASTRUCTURE['nursing_colleges']:,}")
        col3.metric("Annual Seats", f"{TRAINING_INFRASTRUCTURE['annual_seats']/1e3:.0f}K")
        col4.metric("Seat Utilization", f"{TRAINING_INFRASTRUCTURE['utilization_rate']*100:.0f}%")
        
        st.markdown("### Infrastructure Challenges")
        
        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                          subplot_titles=['Accreditation', 'Faculty', 'Infrastructure'])
        
        fig.add_trace(go.Pie(
            labels=['Accredited', 'Non-Accredited'],
            values=[TRAINING_INFRASTRUCTURE['quality_accredited_pct'], 100 - TRAINING_INFRASTRUCTURE['quality_accredited_pct']],
            marker_colors=['#48bb78', '#fc8181'],
            hole=0.4
        ), row=1, col=1)
        
        fig.add_trace(go.Pie(
            labels=['Available', 'Shortage'],
            values=[100 - TRAINING_INFRASTRUCTURE['faculty_shortage_pct'], TRAINING_INFRASTRUCTURE['faculty_shortage_pct']],
            marker_colors=['#4299e1', '#fc8181'],
            hole=0.4
        ), row=1, col=2)
        
        fig.add_trace(go.Pie(
            labels=['Adequate', 'Gap'],
            values=[100 - TRAINING_INFRASTRUCTURE['infrastructure_gap_pct'], TRAINING_INFRASTRUCTURE['infrastructure_gap_pct']],
            marker_colors=['#9f7aea', '#fc8181'],
            hole=0.4
        ), row=1, col=3)
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.markdown('<h3 class="section-header">Current Funding Landscape</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Central Health Budget (2024-25)", f"₹{CURRENT_FUNDING['central_budget_health_cr']:,} Cr")
            st.metric("State Health Budgets (Combined)", f"₹{CURRENT_FUNDING['state_budgets_total_cr']:,} Cr")
            st.metric("Total Public Health Spending", f"₹{(CURRENT_FUNDING['central_budget_health_cr'] + CURRENT_FUNDING['state_budgets_total_cr']):,} Cr")
        
        with col2:
            funding_data = {
                'Category': ['NHM Allocation', 'Ayushman Bharat', 'HR Development', 'Training Infrastructure'],
                'Amount (₹ Cr)': [
                    CURRENT_FUNDING['nhm_allocation_cr'],
                    CURRENT_FUNDING['ayushman_bharat_cr'],
                    CURRENT_FUNDING['human_resource_development_cr'],
                    CURRENT_FUNDING['training_infrastructure_cr']
                ]
            }
            funding_df = pd.DataFrame(funding_data)
            
            fig = px.pie(funding_df, values='Amount (₹ Cr)', names='Category',
                        title='Key Program Allocations', hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)


elif "🗺️ Geographic Analysis" in page:
    st.markdown('<h1 class="main-header">Geographic Analysis</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Interactive Map", "State-wise Data", "Regional Analysis"])
    
    with tabs[0]:
        st.markdown('<h3 class="section-header">State-wise Gap Distribution</h3>', unsafe_allow_html=True)
        st.markdown("*Click on markers to view detailed state information*")
        
        map_obj = create_state_gap_map()
        st_folium(map_obj, width=1200, height=600)
    
    with tabs[1]:
        st.markdown('<h3 class="section-header">State-wise Detailed Data</h3>', unsafe_allow_html=True)
        
        state_df = get_state_dataframe()
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            region_filter = st.multiselect(
                "Filter by Region",
                options=list(REGION_DATA.keys()),
                default=[]
            )
            
            sort_by = st.selectbox(
                "Sort by",
                ['Gap', 'Population', 'Current AHP', 'AHP per 10K']
            )
            
            sort_order = st.radio("Order", ['Descending', 'Ascending'])
        
        with col2:
            filtered_df = state_df.copy()
            
            if region_filter:
                filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]
            
            ascending = sort_order == 'Ascending'
            filtered_df = filtered_df.sort_values(sort_by, ascending=ascending)
            
            st.dataframe(
                filtered_df[['State', 'Region', 'Population', 'Current AHP', 'Required AHP', 
                            'Gap', 'AHP per 10K', 'Training Institutions', 'Annual Graduates']],
                use_container_width=True,
                height=400
            )
        
        top_n = st.slider("Number of states to display", 5, 30, 15)
        
        top_gap_states = state_df.nlargest(top_n, 'Gap')
        
        fig = px.bar(
            top_gap_states,
            x='State',
            y='Gap',
            color='Region',
            title=f'Top {top_n} States by Workforce Gap',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(xaxis_tickangle=-45, height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown('<h3 class="section-header">Regional Summary</h3>', unsafe_allow_html=True)
        
        region_df = get_region_summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                region_df.sort_values('Gap', ascending=True),
                y='Region',
                x='Gap',
                orientation='h',
                title='Workforce Gap by Region',
                color='Gap',
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                region_df.sort_values('AHP per 10K', ascending=True),
                y='Region',
                x='AHP per 10K',
                orientation='h',
                title='AHP Density per 10,000 Population',
                color='AHP per 10K',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(region_df, use_container_width=True)


elif "📈 Scenario Comparison" in page:
    st.markdown('<h1 class="main-header">Multi-Scenario Comparison Engine</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">Compare Three Strategic Scenarios</h4>
        <ul style="margin-bottom: 0;">
            <li><b>Baseline:</b> Current trend continues with existing growth rates</li>
            <li><b>No Intervention:</b> Training capacity declines, leading to worsening gap</li>
            <li><b>Proposed Strategy:</b> Enhanced training, improved retention, infrastructure boost</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">Configure Proposed Strategy Parameters</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        training_increase = st.slider(
            "Training Capacity Increase",
            min_value=1.0,
            max_value=4.0,
            value=2.0,
            step=0.1,
            help="Multiplier for current training output"
        )
    
    with col2:
        infrastructure_boost = st.slider(
            "Infrastructure Investment",
            min_value=1.0,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help="Multiplier for infrastructure development"
        )
    
    with col3:
        retention_improvement = st.slider(
            "Retention Improvement",
            min_value=0.0,
            max_value=0.50,
            value=0.30,
            step=0.05,
            help="Reduction in attrition rate"
        )
    
    projection_years = st.slider("Projection Timeline (Years)", 10, 25, 15)
    
    scenario_df = get_scenario_comparison(
        years=projection_years,
        training_capacity_increase=training_increase,
        infrastructure_boost=infrastructure_boost,
        retention_improvement=retention_improvement
    )
    
    tab1, tab2 = st.tabs(["2D Comparison", "3D Visualization"])
    
    with tab1:
        st.plotly_chart(create_scenario_comparison_chart(scenario_df), use_container_width=True)
    
    with tab2:
        st.plotly_chart(create_3d_scenario_comparison(scenario_df), use_container_width=True)
        st.caption("Interactive 3D view - Drag to rotate, scroll to zoom")
    
    st.markdown('<h3 class="section-header">Scenario Outcomes Summary</h3>', unsafe_allow_html=True)
    
    final_year = 2024 + projection_years
    final_data = scenario_df[scenario_df['Year'] == final_year]
    
    col1, col2, col3 = st.columns(3)
    
    baseline_final = final_data[final_data['Scenario'] == 'Baseline (Current Trend)'].iloc[0]
    no_int_final = final_data[final_data['Scenario'] == 'No Intervention'].iloc[0]
    proposed_final = final_data[final_data['Scenario'] == 'Proposed Strategy'].iloc[0]
    
    with col1:
        st.markdown(f"""
        <div class="info-box">
            <h4 style="margin-top: 0;">Baseline Scenario ({final_year})</h4>
            <p>Remaining Gap: <b>{baseline_final['Gap']/1e6:.2f}M</b></p>
            <p>Gap Closure: <b>{baseline_final['Gap Closure %']:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="critical-box">
            <h4 style="margin-top: 0;">No Intervention ({final_year})</h4>
            <p>Remaining Gap: <b>{no_int_final['Gap']/1e6:.2f}M</b></p>
            <p>Gap Closure: <b>{no_int_final['Gap Closure %']:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); padding: 1.2rem; border-radius: 12px; color: white;">
            <h4 style="margin-top: 0;">Proposed Strategy ({final_year})</h4>
            <p>Remaining Gap: <b>{proposed_final['Gap']/1e6:.2f}M</b></p>
            <p>Gap Closure: <b>{proposed_final['Gap Closure %']:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)


elif "💰 Cost Calculator" in page:
    st.markdown('<h1 class="main-header">Advanced Cost Projection Calculator</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">Inflation-Adjusted Cost Projections</h4>
        <p>Configure parameters below to calculate the total investment required. 
        Training costs are automatically adjusted for inflation year-over-year.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Target Parameters")
        
        gap_closure_target = st.slider(
            "Target Gap Closure (%)",
            min_value=10,
            max_value=100,
            value=80,
            step=5,
            help="What percentage of the 6.5M gap do you want to close?"
        )
        
        timeline_years = st.slider(
            "Timeline (Years)",
            min_value=5,
            max_value=25,
            value=15,
            help="Number of years to achieve the target"
        )
        
        training_cost_multiplier = st.slider(
            "Training Cost Adjustment",
            min_value=0.8,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Multiplier for base training costs"
        )
    
    with col2:
        st.markdown("### Economic Parameters")
        
        inflation_rate = st.slider(
            "Annual Inflation Rate (%)",
            min_value=3.0,
            max_value=10.0,
            value=5.0,
            step=0.5,
            help="Inflation rate applied to training costs"
        ) / 100
        
        salary_growth_rate = st.slider(
            "Annual Salary Growth Rate (%)",
            min_value=3.0,
            max_value=10.0,
            value=5.0,
            step=0.5
        ) / 100
        
        infrastructure_pct = st.slider(
            "Infrastructure Investment (%)",
            min_value=10,
            max_value=40,
            value=20,
            help="Percentage of budget allocated to infrastructure"
        ) / 100
        
        include_retention = st.checkbox("Include Retention Incentives", value=True)
    
    cost_df = calculate_cost_projection(
        target_gap_closure_pct=gap_closure_target,
        years=timeline_years,
        training_cost_multiplier=training_cost_multiplier,
        salary_growth_rate=salary_growth_rate,
        infrastructure_investment_pct=infrastructure_pct,
        include_retention=include_retention,
        inflation_rate=inflation_rate
    )
    
    st.markdown("---")
    st.markdown('<h3 class="section-header">Cost Projection Results</h3>', unsafe_allow_html=True)
    
    total_cost = cost_df['Cumulative Cost (₹ Cr)'].iloc[-1]
    avg_annual_cost = total_cost / timeline_years
    professionals_added = cost_df['Cumulative Professionals'].iloc[-1]
    cost_per_professional = (total_cost * 1e7) / professionals_added if professionals_added > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Investment Required", f"₹{total_cost:,.0f} Cr")
    col2.metric("Average Annual Investment", f"₹{avg_annual_cost:,.0f} Cr")
    col3.metric("Professionals to be Added", f"{professionals_added/1e6:.2f}M")
    col4.metric("Cost per Professional", f"₹{cost_per_professional/1e5:.2f} L")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_cost_breakdown_chart(cost_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_cumulative_cost_chart(cost_df), use_container_width=True)
    
    st.markdown('<h3 class="section-header">Year-wise Detailed Projection</h3>', unsafe_allow_html=True)
    
    display_df = cost_df.copy()
    display_df['Gap Remaining'] = display_df['Gap Remaining'].apply(lambda x: f"{x/1e6:.2f}M")
    display_df['Cumulative Professionals'] = display_df['Cumulative Professionals'].apply(lambda x: f"{x/1e6:.2f}M")
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">Note on Inflation Adjustment</h4>
        <p>Training costs are compounded annually at the specified inflation rate. 
        Year 1 costs are at base rates, with each subsequent year adjusted for inflation 
        (shown in the 'Inflation Factor' column).</p>
    </div>
    """, unsafe_allow_html=True)


elif "💵 Budget & Funding" in page:
    st.markdown('<h1 class="main-header">Budget Analysis & Funding Strategy</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Budget Trend", "Global Comparison", "Funding Sources", "Funding Gap Analysis"])
    
    with tabs[0]:
        st.markdown('<h3 class="section-header">India Health Budget: 10-Year Trend Analysis</h3>', unsafe_allow_html=True)
        
        st.plotly_chart(create_budget_trend_chart(), use_container_width=True)
        
        budget_df = get_budget_trend_dataframe()
        
        col1, col2, col3 = st.columns(3)
        
        latest = budget_df.iloc[-1]
        earliest = budget_df.iloc[0]
        
        growth = ((latest['Health Budget (₹ Cr)'] - earliest['Health Budget (₹ Cr)']) / earliest['Health Budget (₹ Cr)']) * 100
        
        col1.metric("10-Year Budget Growth", f"{growth:.0f}%", f"₹{earliest['Health Budget (₹ Cr)']:,.0f} → ₹{latest['Health Budget (₹ Cr)']:,.0f} Cr")
        col2.metric("Current % of GDP", f"{latest['Health % of GDP']:.2f}%", delta=f"Target: 2.5%")
        col3.metric("Current % of Budget", f"{latest['Health % of Budget']:.2f}%")
        
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin-top: 0;">Key Observation</h4>
            <p>Despite absolute growth in health budget, India's health spending as percentage of GDP 
            remains well below the National Health Policy 2017 target of <b>2.5% of GDP</b>. 
            Current spending is approximately <b>0.28% of GDP</b> from central government.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(budget_df, use_container_width=True)
    
    with tabs[1]:
        st.markdown('<h3 class="section-header">Global Health Spending Comparison</h3>', unsafe_allow_html=True)
        
        st.plotly_chart(create_global_comparison_chart(), use_container_width=True)
        
        global_df = get_global_comparison_dataframe()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                global_df.sort_values('Out-of-Pocket %', ascending=True),
                y='Country',
                x='Out-of-Pocket %',
                orientation='h',
                title='Out-of-Pocket Health Expenditure',
                color='Out-of-Pocket %',
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="critical-box">
                <h4 style="margin-top: 0;">India's Challenge</h4>
                <ul>
                    <li>Total health spending: <b>2.1% of GDP</b> (vs. WHO target 5%)</li>
                    <li>Government contribution: <b>1.35% of GDP</b></li>
                    <li>Out-of-pocket: <b>48%</b> (vs. WHO target <15%)</li>
                    <li>High OOPE leads to 55 million pushed to poverty annually</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.dataframe(global_df, use_container_width=True)
    
    with tabs[2]:
        st.markdown('<h3 class="section-header">Potential Funding Sources</h3>', unsafe_allow_html=True)
        
        st.plotly_chart(create_funding_waterfall(), use_container_width=True)
        
        funding_df = get_funding_sources_dataframe()
        
        total_potential = funding_df['Potential (₹ Cr/Year)'].sum()
        total_current = funding_df['Current (₹ Cr/Year)'].sum()
        total_additional = funding_df['Additional Mobilizable'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Potential Annual Funding", f"₹{total_potential:,} Cr")
        col2.metric("Currently Mobilized", f"₹{total_current:,} Cr")
        col3.metric("Additional Mobilizable", f"₹{total_additional:,} Cr", delta=f"+{(total_additional/total_current)*100:.0f}%")
        
        st.markdown("### Detailed Funding Sources")
        st.dataframe(funding_df, use_container_width=True)
        
        st.markdown("### Funding by Feasibility")
        
        feasibility_groups = funding_df.groupby('Feasibility').agg({
            'Potential (₹ Cr/Year)': 'sum',
            'Additional Mobilizable': 'sum'
        }).reset_index()
        
        fig = px.bar(
            feasibility_groups,
            x='Feasibility',
            y='Additional Mobilizable',
            title='Additional Funding Potential by Feasibility Level',
            color='Feasibility',
            color_discrete_map={'High': '#48bb78', 'Medium': '#ecc94b', 'Low': '#fc8181'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:
        st.markdown('<h3 class="section-header">Funding Gap Analysis</h3>', unsafe_allow_html=True)
        
        required_annual = 50000
        available_annual = 35900
        gap_annual = required_annual - available_annual
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Required Annual Investment", f"₹{required_annual:,} Cr")
        col2.metric("Available/Mobilizable", f"₹{available_annual:,} Cr")
        col3.metric("Annual Funding Gap", f"₹{gap_annual:,} Cr", delta=f"-{(gap_annual/required_annual)*100:.0f}%")
        
        st.markdown("""
        <div class="info-box">
            <h4 style="margin-top: 0;">Strategies to Bridge the Funding Gap</h4>
            <ol>
                <li><b>Health Cess:</b> 2% additional cess on income tax could generate ₹25,000 Cr annually</li>
                <li><b>PPP Expansion:</b> Private sector training partnerships can reduce government burden by 30%</li>
                <li><b>NHM Reallocation:</b> Redirecting 15% of NHM budget to workforce development</li>
                <li><b>International Aid:</b> WHO/World Bank health systems strengthening loans</li>
                <li><b>State Matching:</b> 60:40 cost-sharing with states increases pooled resources</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


elif "🎯 Strategy Formulation" in page:
    st.markdown('<h1 class="main-header">Strategy Formulation</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Phased Strategy Portfolio", "AI Strategy Generator", "Implementation Roadmap"])
    
    with tabs[0]:
        st.markdown('<h3 class="section-header">Comprehensive Phased Strategy</h3>', unsafe_allow_html=True)
        
        for phase_key in ['immediate', 'intermediate', 'long_term']:
            phase_data = STRATEGY_PORTFOLIO[phase_key]
            
            phase_class = f"phase-{phase_key.replace('_', '-')}"
            
            st.markdown(f"""
            <div class="strategy-card {phase_class}">
                <h3 style="color: #1e3a5f; margin-top: 0;">{phase_data['phase']}</h3>
                <p style="color: #666;">{phase_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            for strategy in phase_data['strategies']:
                with st.expander(f"📋 {strategy['name']} | Cost: ₹{strategy['cost_cr_annual']:,} Cr/year | Gap Reduction: {strategy['gap_reduction_pct']}%"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {strategy['description']}")
                        st.markdown(f"**Expected Impact:** {strategy['expected_impact']}")
                        st.markdown(f"**Implementation Locations:** {', '.join(strategy['implementation_locations'])}")
                        
                        st.markdown("**Key Actions:**")
                        for action in strategy['key_actions']:
                            st.markdown(f"- {action}")
                    
                    with col2:
                        st.metric("Annual Cost", f"₹{strategy['cost_cr_annual']:,} Cr")
                        st.metric("Target Professionals", f"{strategy['target_professionals']:,}" if strategy['target_professionals'] > 0 else "Infrastructure")
                        st.metric("Gap Reduction", f"{strategy['gap_reduction_pct']}%")
                        
                        st.markdown("**Success Metrics:**")
                        for metric in strategy['success_metrics']:
                            st.markdown(f"- {metric}")
            
            st.markdown("---")
        
        summary_df = get_strategy_summary()
        
        total_annual_cost = summary_df['Annual Cost (₹ Cr)'].sum()
        total_gap_reduction = summary_df['Gap Reduction %'].sum()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Annual Investment (All Phases)", f"₹{total_annual_cost:,} Cr")
        col2.metric("Total Potential Gap Reduction", f"{total_gap_reduction:.1f}%")
    
    with tabs[1]:
        st.markdown('<h3 class="section-header">AI-Powered Strategy Generator</h3>', unsafe_allow_html=True)
        
        if not OPENAI_API_KEY:
            st.warning("OpenAI API key is required for AI-powered strategy generation. Please configure the OPENAI_API_KEY environment variable.")
        else:
            st.markdown("""
            <div class="info-box">
                Configure parameters below to generate a customized, comprehensive strategy document.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                category_df = get_category_dataframe()
                top_categories = category_df.nlargest(5, 'Gap')['Category'].tolist()
                
                priority_categories = st.multiselect(
                    "Priority Professional Categories",
                    options=category_df['Category'].tolist(),
                    default=top_categories[:3]
                )
                
                region_focus = st.multiselect(
                    "Priority Regions",
                    options=list(REGION_DATA.keys()),
                    default=['North', 'East']
                )
                
                phase_focus = st.selectbox(
                    "Phase Emphasis",
                    options=['Balanced', 'Immediate Actions', 'Long-term Sustainability', 'Training Focus', 'Retention Focus']
                )
            
            with col2:
                budget_level = st.select_slider(
                    "Budget Availability",
                    options=['Very Limited', 'Limited', 'Moderate', 'Substantial', 'Unlimited'],
                    value='Moderate'
                )
                
                timeline = st.slider(
                    "Target Timeline (Years)",
                    min_value=5,
                    max_value=20,
                    value=15
                )
                
                focus_areas = st.multiselect(
                    "Priority Focus Areas",
                    options=[
                        'Training Capacity Expansion',
                        'Rural Deployment',
                        'Retention & Incentives',
                        'Quality Improvement',
                        'Public-Private Partnership',
                        'Digital Health Integration',
                        'International Collaboration'
                    ],
                    default=['Training Capacity Expansion', 'Rural Deployment', 'Retention & Incentives']
                )
            
            if st.button("Generate Comprehensive Strategy", type="primary", use_container_width=True):
                with st.spinner("Generating detailed strategy document... This may take 1-2 minutes."):
                    gap_analysis = f"Priority categories: {', '.join(priority_categories)}. Focus regions: {', '.join(region_focus)}"
                    
                    strategy = generate_ai_strategy(
                        gap_analysis=gap_analysis,
                        budget_constraints=budget_level,
                        priority_areas=', '.join(focus_areas),
                        timeline=timeline,
                        phase_focus=phase_focus
                    )
                    
                    if strategy:
                        st.success("Strategy generated successfully!")
                        st.markdown("---")
                        st.markdown(strategy)
                        
                        st.download_button(
                            label="Download Strategy Document",
                            data=strategy,
                            file_name="ahp_strategy_document.md",
                            mime="text/markdown"
                        )
    
    with tabs[2]:
        st.markdown('<h3 class="section-header">Implementation Roadmap</h3>', unsafe_allow_html=True)
        
        milestones = [
            {"Phase": "Phase 1", "Years": "2025-2026", "Focus": "Emergency Training & Retention", "Gap Target": "10%", "Investment": "₹27,500 Cr/year"},
            {"Phase": "Phase 2", "Years": "2027-2029", "Focus": "Institution Building & Rural Deployment", "Gap Target": "30%", "Investment": "₹42,000 Cr/year"},
            {"Phase": "Phase 3", "Years": "2030-2034", "Focus": "Scaling & Quality Enhancement", "Gap Target": "65%", "Investment": "₹55,000 Cr/year"},
            {"Phase": "Phase 4", "Years": "2035-2040", "Focus": "Sustainability & UHC Achievement", "Gap Target": "95%", "Investment": "₹40,000 Cr/year"}
        ]
        
        milestone_df = pd.DataFrame(milestones)
        
        fig = go.Figure()
        
        phases = milestone_df['Phase'].tolist()
        gap_targets = [10, 30, 65, 95]
        
        fig.add_trace(go.Scatter(
            x=phases,
            y=gap_targets,
            mode='lines+markers+text',
            text=[f"{g}%" for g in gap_targets],
            textposition='top center',
            line=dict(color='#38a169', width=4),
            marker=dict(size=20, color='#38a169'),
            name='Gap Closure Progress'
        ))
        
        fig.update_layout(
            title=dict(text='Gap Closure Progress Across Implementation Phases', font=dict(size=18)),
            xaxis_title='Implementation Phase',
            yaxis_title='Cumulative Gap Closure (%)',
            height=400,
            yaxis=dict(range=[0, 105])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(milestone_df, use_container_width=True)


elif "📋 Investment Planning" in page:
    st.markdown('<h1 class="main-header">Investment Strategy & Planning</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Budget Allocation", "Timeline Milestones", "ROI Analysis"])
    
    with tabs[0]:
        st.markdown('<h3 class="section-header">Recommended Budget Allocation</h3>', unsafe_allow_html=True)
        
        allocation_data = {
            'Category': [
                'Training Infrastructure Expansion',
                'Salary & Compensation',
                'Scholarship & Student Support',
                'Faculty Development',
                'Equipment & Technology',
                'Rural Incentive Programs',
                'Retention & Welfare',
                'Administration & Monitoring'
            ],
            'Allocation %': [25, 30, 10, 8, 7, 10, 7, 3],
            'Amount (₹ Cr/Year)': [12500, 15000, 5000, 4000, 3500, 5000, 3500, 1500]
        }
        
        alloc_df = pd.DataFrame(allocation_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.pie(
                alloc_df,
                values='Allocation %',
                names='Category',
                title='Recommended Annual Budget Allocation',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='outside', textinfo='percent+label')
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Allocation Details")
            st.dataframe(alloc_df, use_container_width=True, hide_index=True)
            st.metric("Total Annual Budget", f"₹{alloc_df['Amount (₹ Cr/Year)'].sum():,} Cr")
    
    with tabs[1]:
        st.markdown('<h3 class="section-header">Implementation Timeline & Milestones</h3>', unsafe_allow_html=True)
        
        milestones = [
            {"Phase": "Phase 1: Foundation", "Years": "2025-2027", "Target": "Infrastructure & Policy Setup", 
             "Gap Closure": "15%", "Investment": "₹1,50,000 Cr"},
            {"Phase": "Phase 2: Scale-Up", "Years": "2028-2032", "Target": "Training Capacity Doubling", 
             "Gap Closure": "45%", "Investment": "₹3,50,000 Cr"},
            {"Phase": "Phase 3: Acceleration", "Years": "2033-2037", "Target": "Full Deployment & Retention", 
             "Gap Closure": "80%", "Investment": "₹4,00,000 Cr"},
            {"Phase": "Phase 4: Sustainability", "Years": "2038-2040", "Target": "UHC Achievement", 
             "Gap Closure": "95%", "Investment": "₹2,00,000 Cr"}
        ]
        
        st.dataframe(pd.DataFrame(milestones), use_container_width=True, hide_index=True)
    
    with tabs[2]:
        st.markdown('<h3 class="section-header">Return on Investment Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            economic_benefits = {
                'Benefit Category': [
                    'Healthcare Productivity Gains',
                    'Reduced Out-of-Pocket Expenses',
                    'Employment Generation',
                    'Rural Economy Boost',
                    'Medical Tourism Growth',
                    'Reduced Disease Burden'
                ],
                'Estimated Annual Value (₹ Cr)': [45000, 35000, 28000, 15000, 12000, 55000]
            }
            
            econ_df = pd.DataFrame(economic_benefits)
            
            fig = px.bar(
                econ_df,
                y='Benefit Category',
                x='Estimated Annual Value (₹ Cr)',
                orientation='h',
                title='Estimated Annual Economic Benefits',
                color='Estimated Annual Value (₹ Cr)',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            total_investment = 50000
            total_benefits = sum(economic_benefits['Estimated Annual Value (₹ Cr)'])
            roi = ((total_benefits - total_investment) / total_investment) * 100
            
            st.metric("Total Annual Investment", f"₹{total_investment:,} Cr")
            st.metric("Total Annual Benefits", f"₹{total_benefits:,} Cr")
            st.metric("Return on Investment", f"{roi:.0f}%", delta=f"+{roi:.0f}%")
            
            st.markdown("""
            <div class="success-metric" style="text-align: left; padding: 1.5rem;">
                <h4 style="margin-top: 0;">Social Impact Indicators</h4>
                <ul>
                    <li>6.5M jobs created over 15 years</li>
                    <li>80% UHC coverage achieved</li>
                    <li>50% reduction in preventable deaths</li>
                    <li>Rural healthcare access doubled</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


elif "👥 Demographics Analysis" in page:
    st.markdown('<h1 class="main-header">Demographics & Equity Analysis</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Urban-Rural Divide", "Age Group Analysis", "Socioeconomic Impact"])
    
    with tabs[0]:
        st.markdown('<h3 class="section-header">Urban-Rural Healthcare Divide</h3>', unsafe_allow_html=True)
        
        urban_rural = DEMOGRAPHIC_DATA['urban_rural']
        
        col1, col2 = st.columns(2)
        
        with col1:
            categories = ['Population', 'AHP Share', 'Gap Share']
            urban_vals = [urban_rural['Urban']['population_pct'], 
                         urban_rural['Urban']['ahp_share'], 
                         urban_rural['Urban']['gap_share']]
            rural_vals = [urban_rural['Rural']['population_pct'], 
                         urban_rural['Rural']['ahp_share'], 
                         urban_rural['Rural']['gap_share']]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Urban', x=categories, y=urban_vals, marker_color='#4299e1'))
            fig.add_trace(go.Bar(name='Rural', x=categories, y=rural_vals, marker_color='#48bb78'))
            
            fig.update_layout(
                barmode='group',
                title='Urban vs Rural Distribution',
                yaxis_title='Percentage (%)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="critical-box">
                <h4 style="margin-top: 0;">The Rural Crisis</h4>
                <p><b>65%</b> of India's population lives in rural areas, but they have access to only <b>42%</b> of Allied Health Professionals.</p>
                <p>This creates a disproportionate <b>75%</b> share of the total gap concentrated in rural India.</p>
            </div>
            """, unsafe_allow_html=True)
            
            density_data = {
                'Area': ['Urban', 'Rural'],
                'AHP per 10,000': [urban_rural['Urban']['density_per_10k'], urban_rural['Rural']['density_per_10k']]
            }
            
            fig = px.bar(
                pd.DataFrame(density_data),
                x='Area',
                y='AHP per 10,000',
                color='Area',
                title='Healthcare Professional Density',
                color_discrete_sequence=['#4299e1', '#48bb78']
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown('<h3 class="section-header">Age Group Healthcare Needs</h3>', unsafe_allow_html=True)
        
        age_data = DEMOGRAPHIC_DATA['age_groups']
        
        age_df = pd.DataFrame([
            {'Age Group': group, **data}
            for group, data in age_data.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                age_df,
                values='population_pct',
                names='Age Group',
                title='Population Distribution by Age',
                color_discrete_sequence=px.colors.sequential.Viridis,
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                age_df,
                x='Age Group',
                y='healthcare_need_index',
                title='Healthcare Need Index by Age Group',
                color='healthcare_need_index',
                color_continuous_scale='Reds'
            )
            fig.add_hline(y=1.0, line_dash="dash", annotation_text="Baseline Need")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown('<h3 class="section-header">Socioeconomic Impact Analysis</h3>', unsafe_allow_html=True)
        
        socio_data = DEMOGRAPHIC_DATA['socioeconomic']
        
        socio_df = pd.DataFrame([
            {'Category': cat, **data}
            for cat, data in socio_data.items()
        ])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=socio_df['Category'],
            y=socio_df['population_pct'],
            name='Population Share (%)',
            marker_color='#4299e1'
        ))
        
        fig.add_trace(go.Bar(
            x=socio_df['Category'],
            y=socio_df['ahp_access_pct'],
            name='AHP Access (%)',
            marker_color='#48bb78'
        ))
        
        fig.add_trace(go.Bar(
            x=socio_df['Category'],
            y=socio_df['out_of_pocket_pct'],
            name='Out-of-Pocket Expenses (%)',
            marker_color='#fc8181'
        ))
        
        fig.update_layout(
            barmode='group',
            title='Healthcare Access & Financial Burden by Socioeconomic Class',
            xaxis_tickangle=-15,
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)


elif "📚 Data Sources" in page:
    st.markdown('<h1 class="main-header">Data Sources & Citations</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0;">About This Data</h4>
        <p>This platform aggregates data from multiple authoritative sources including government reports, 
        WHO statistics, and peer-reviewed research. All figures are verified and cross-referenced 
        for accuracy and credibility.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">Primary Data Sources</h3>', unsafe_allow_html=True)
    
    for source in DATA_SOURCES:
        st.markdown(f"""
        <div class="strategy-card">
            <h4 style="margin-top: 0; color: #1e3a5f;">{source['title']}</h4>
            <p><b>Publisher:</b> {source['publisher']}</p>
            <p><b>Year:</b> {source['year']}</p>
            <p><b>Data Used:</b> {source['data_used']}</p>
            <p><a href="{source['url']}" target="_blank">🔗 Access Source</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="section-header">Key Statistics Verification</h3>', unsafe_allow_html=True)
    
    verification_data = [
        {"Statistic": "6.5 Million AHP Gap", "Source": "MoHFW 2012 Assessment", "Status": "Verified"},
        {"Statistic": "WHO 44.5/10,000 Benchmark", "Source": "WHO Global Strategy on HRH", "Status": "Verified"},
        {"Statistic": "Health Budget ₹90,959 Cr", "Source": "Union Budget 2024-25", "Status": "Verified"},
        {"Statistic": "48% Out-of-Pocket Expenditure", "Source": "National Health Accounts 2022", "Status": "Verified"},
        {"Statistic": "55% UHC Service Coverage Index", "Source": "WHO UHC Monitoring Report", "Status": "Verified"}
    ]
    
    st.dataframe(pd.DataFrame(verification_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div class="warning-box">
        <h4 style="margin-top: 0;">Data Limitations</h4>
        <ul>
            <li>Baseline gap assessment is from 2012; actual current gap may be higher due to population growth</li>
            <li>State-wise data uses Census 2011 populations; updated census data pending</li>
            <li>Cost projections are estimates based on current salary and training cost structures</li>
            <li>Scenario projections involve assumptions about policy implementation effectiveness</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem;">
    <p style="margin-bottom: 0.5rem;"><b>India AHP Gap Analysis & Strategy Platform</b></p>
    <p style="margin-bottom: 0.5rem;">Data Sources: WHO, Ministry of Health & Family Welfare, Census 2011, PRS Legislative Research</p>
    <p style="margin: 0;">Built to support India's journey towards Universal Health Coverage by 2030</p>
</div>
""", unsafe_allow_html=True)
elif page == "🤖 AI Policy Recommendations":
    from utils.ai_helper_gemini import AIHealthcareAnalyst
    
    st.header("🤖 AI-Powered Policy Recommendations")
    st.markdown("Get AI-generated strategic policy recommendations based on your scenario analysis.")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario_type = st.selectbox(
            "Select Strategy Type",
            [
                "Conservative (50% by 2035)",
                "Moderate (75% by 2035)",
                "Aggressive (100% by 2035)",
                "Quick Win (50% by 2030)"
            ]
        )
    
    with col2:
        custom_timeline = st.number_input(
            "Timeline (years)",
            min_value=5,
            max_value=20,
            value=10
        )
    
    st.divider()
    
    if st.button("🚀 Generate AI Policy Recommendations", key="policy_btn"):
        with st.spinner("🤖 AI consultant analyzing scenario..."):
            try:
                analyst = AIHealthcareAnalyst()
                
                scenario_data = {
                    "total_gap": 6_500_000,
                    "years": custom_timeline,
                    "strategy_type": scenario_type,
                    "budget": 150_000,
                    "gap_closure_pct": 50 if "50%" in scenario_type else 75 if "75%" in scenario_type else 100
                }
                
                category_summary = {
                    "Nurses & Midwives": {
                        "gap": 2_860_000,
                        "gap_percentage": 44.0,
                        "avg_salary_inr": 420_000
                    },
                    "Lab Technicians": {
                        "gap": 750_000,
                        "gap_percentage": 11.5,
                        "avg_salary_inr": 360_000
                    },
                    "Community Health Workers": {
                        "gap": 880_000,
                        "gap_percentage": 13.5,
                        "avg_salary_inr": 240_000
                    }
                }
                
                recommendations = analyst.get_policy_recommendations(scenario_data, category_summary)
                
                st.success("✅ AI Analysis Complete!")
                st.markdown(recommendations)
                
                st.download_button(
                    label="📥 Download Recommendations",
                    data=recommendations,
                    file_name=f"AI_Recommendations_{scenario_type}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure GOOGLE_API_KEY is set in Streamlit Cloud secrets.")


elif page == "📊 AI Report Generator":
    from utils.ai_helper_gemini import AIHealthcareAnalyst
    
    st.header("📊 AI Report Generator")
    st.markdown("Generate professional reports for different audiences.")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Select Report Type",
            [
                "executive - Executive Summary",
                "policy_brief - Policy Brief",
                "implementation - Implementation Roadmap"
            ],
            format_func=lambda x: x.split(" - ")[1]
        )
        report_type = report_type.split(" - ")[0]
    
    with col2:
        scenario_for_report = st.selectbox(
            "Select Scenario",
            [
                "Conservative (50% by 2035)",
                "Moderate (75% by 2035)",
                "Aggressive (100% by 2035)",
                "Quick Win (50% by 2030)"
            ]
        )
    
    st.divider()
    
    if st.button("📄 Generate Report", key="report_btn"):
        with st.spinner("📝 AI generating report..."):
            try:
                analyst = AIHealthcareAnalyst()
                
                scenario_data = {
                    "years": 10,
                    "strategy_type": scenario_for_report,
                    "budget": 150_000
                }
                
                results_data = {
                    "current_supply": 2_120_000,
                    "required_supply": 8_600_000,
                    "gap": 6_500_000,
                    "gap_pct": 95,
                    "annual_salary": 450_000,
                    "training_cost": 125_000,
                    "total_cost": 575_000,
                    "professionals_added": 325_000
                }
                
                report = analyst.generate_executive_report(
                    scenario_data,
                    results_data,
                    report_type
                )
                
                st.success("✅ Report Generated!")
                st.markdown(report)
                
                report_name = {
                    "executive": "Executive_Summary",
                    "policy_brief": "Policy_Brief",
                    "implementation": "Implementation_Roadmap"
                }.get(report_type, "Report")
                
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"AHP_{report_name}_{scenario_for_report}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure GOOGLE_API_KEY is set in Streamlit Cloud secrets.")


