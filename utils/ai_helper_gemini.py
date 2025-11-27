import os
import google.generativeai as genai
import streamlit as st

class AIHealthcareAnalyst:
    """AI-powered healthcare policy analyst using Google Gemini (FREE)"""
    
    def __init__(self):
        """Initialize Gemini client"""
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def get_policy_recommendations(self, scenario_data, category_data):
        """Generate AI-powered policy recommendations"""
        
        category_summary = "\n".join([
            f"- {cat}: {info['gap']:,} gap, {info['gap_percentage']}% of total, "
            f"₹{info['avg_salary_inr']:,} avg salary"
            for cat, info in category_data.items()
        ])
        
        prompt = f"""
        You are an expert healthcare policy consultant specializing in workforce development 
        and UHC implementation in India.
        
        Analyze this healthcare workforce scenario and provide strategic policy recommendations:
        
        SCENARIO DETAILS:
        - Total AHP Gap: {scenario_data.get('total_gap', 'Not specified'):,} professionals
        - Target Timeline: {scenario_data.get('years', 'Not specified')} years
        - Strategy Type: {scenario_data.get('strategy_type', 'Not specified')}
        - Budget Required: ₹{scenario_data.get('budget', 'Not specified')} crore
        - Gap Closure Target: {scenario_data.get('gap_closure_pct', 'Not specified')}%
        
        CATEGORY PRIORITIES:
        {category_summary}
        
        GEOGRAPHIC CONTEXT:
        - 75% of gap in rural areas
        - 65% of India's population in rural regions
        - Only 42% of current AHPs serve rural areas
        
        Based on this analysis, provide:
        
        1. IMMEDIATE ACTIONS (0-6 months)
           - 3-4 specific, actionable steps
           - Focus on quick wins
           - Low-cost interventions
        
        2. MEDIUM-TERM STRATEGIES (6-18 months)
           - Capacity building initiatives
           - Infrastructure requirements
           - Funding mechanisms
        
        3. LONG-TERM VISION (18+ months)
           - Sustainable systems
           - Retention strategies
           - Equity considerations (rural focus)
        
        4. IMPLEMENTATION RISKS & MITIGATION
           - 3-4 key risks
           - Mitigation strategies
        
        5. SUCCESS METRICS
           - 3-4 KPIs to track
           - Monitoring framework
        
        Format your response clearly with bold headers and bullet points.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
    
    def generate_executive_report(self, scenario_data, results_data, report_type="executive"):
        """Generate comprehensive AI reports"""
        
        if report_type == "executive":
            prompt = f"""
            You are a healthcare management consultant. Create a professional EXECUTIVE SUMMARY 
            for healthcare leaders and policymakers.
            
            SCENARIO ANALYSIS RESULTS:
            - Current AHP Supply: {results_data.get('current_supply', 'N/A'):,}
            - Required AHP Supply: {results_data.get('required_supply', 'N/A'):,}
            - Total Gap: {results_data.get('gap', 'N/A'):,}
            - Gap Percentage: {results_data.get('gap_pct', 'N/A')}%
            - Target Timeline: {scenario_data.get('years', 'N/A')} years
            - Annual Salary Budget: ₹{results_data.get('annual_salary', 'N/A')} crore
            - Training Investment: ₹{results_data.get('training_cost', 'N/A')} crore
            - Total First Year Cost: ₹{results_data.get('total_cost', 'N/A')} crore
            - Professionals to Add: {results_data.get('professionals_added', 'N/A'):,}
            
            Create a 1-page executive summary with these sections:
            
            1. SITUATION (2-3 lines)
            2. OPPORTUNITY (2-3 lines)
            3. RECOMMENDED STRATEGY (3 bullets)
            4. KEY METRICS (3-4 metrics)
            5. INVESTMENT REQUIRED
            6. EXPECTED OUTCOMES
            7. NEXT STEPS (3 actions)
            
            Use professional language suitable for board presentations.
            """
        
        elif report_type == "policy_brief":
            prompt = f"""
            You are a health policy expert. Create a POLICY BRIEF for government agencies.
            
            ANALYSIS RESULTS:
            - AHP Gap: {results_data.get('gap', 'N/A'):,} (95% of WHO benchmark)
            - Geographic Focus: 75% gap in rural areas
            - Category Priority: Nurses & Midwives = 44% of gap
            - Timeline: {scenario_data.get('years', 'N/A')} years
            - Total Investment: ₹{results_data.get('total_cost', 'N/A')} crore
            
            Create policy brief with:
            1. EXECUTIVE SUMMARY
            2. PROBLEM STATEMENT
            3. POLICY RECOMMENDATIONS (4-5 specific)
            4. IMPLEMENTATION FRAMEWORK (Phase-wise)
            5. FINANCIAL REQUIREMENTS
            6. SUCCESS INDICATORS
            7. CONCLUSION
            """
        
        elif report_type == "implementation":
            prompt = f"""
            Create an IMPLEMENTATION ROADMAP for healthcare organizations.
            
            Gap: {results_data.get('gap', 'N/A'):,} professionals
            Timeline: {scenario_data.get('years', 'N/A')} years
            Budget: ₹{results_data.get('annual_salary', 'N/A')} crore
            
            Include:
            1. PRE-IMPLEMENTATION (Months 1-3)
            2. PHASE 1: FOUNDATION (Months 4-12)
            3. PHASE 2: SCALING (Year 2-3)
            4. PHASE 3: OPTIMIZATION (Year 4+)
            5. RISKS & MITIGATION
            6. SUCCESS CRITERIA
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating report: {str(e)}"
