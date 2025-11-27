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
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_policy_recommendations(self, scenario_data, category_data):
        """
        Generate AI-powered policy recommendations (FREE using Google Gemini)
        """
        
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
        Make recommendations specific, actionable, and tied to the data.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
    
    def generate_executive_report(self, scenario_data, results_data, report_type="executive"):
        """
        Generate comprehensive AI reports (FREE using Google Gemini)
        """
        
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
            
            1. SITUATION (2-3 lines) - The current AHP crisis in India
            2. OPPORTUNITY (2-3 lines) - Why this matters for UHC
            3. RECOMMENDED STRATEGY (3 bullet points)
            4. KEY METRICS (3-4 metrics showing impact)
            5. INVESTMENT REQUIRED (Cost breakdown)
            6. EXPECTED OUTCOMES (By year end)
            7. NEXT STEPS (3 immediate actions)
            
            Format with clear sections, bold headers, and professional language suitable 
            for board presentations.
            """
        
        elif report_type == "policy_brief":
            prompt = f"""
            You are a health policy expert. Create a POLICY BRIEF for government health departments 
            and international organizations.
            
            ANALYSIS RESULTS:
            - AHP Gap: {results_data.get('gap', 'N/A'):,} professionals (95% of WHO benchmark)
            - Geographic Focus: 75% gap in rural areas
            - Category Priority: Nurses & Midwives = 44% of gap
            - Timeline to Close: {scenario_data.get('years', 'N/A')} years
            - Total Investment: ₹{results_data.get('total_cost', 'N/A')} crore
            - Population Impacted: 1.4 billion people
            
            Create a policy brief with:
            
            1. EXECUTIVE SUMMARY (1 paragraph)
            2. PROBLEM STATEMENT (2 paragraphs)
               - AHP shortage scale and scope
               - Impact on UHC and health outcomes
            3. POLICY RECOMMENDATIONS (4-5 specific recommendations)
               - Training capacity expansion
               - Rural incentive mechanisms
               - Regulatory framework
               - Funding mechanisms
            4. IMPLEMENTATION FRAMEWORK (Phase-wise approach)
               - Phase 1: Foundation (Year 1-2)
               - Phase 2: Scaling (Year 3-5)
               - Phase 3: Consolidation (Year 6+)
            5. FINANCIAL REQUIREMENTS (Budget breakdown)
            6. SUCCESS INDICATORS (3-4 KPIs)
            7. CONCLUSION (Impact on Universal Health Coverage)
            
            Make it suitable for government circulation and international health agencies.
            """
        
        elif report_type == "implementation":
            prompt = f"""
            You are a healthcare operations consultant. Create an IMPLEMENTATION ROADMAP 
            for healthcare organizations and government agencies.
            
            SCENARIO:
            - Gap: {results_data.get('gap', 'N/A'):,} professionals
            - Timeline: {scenario_data.get('years', 'N/A')} years
            - Annual Budget: ₹{results_data.get('annual_salary', 'N/A')} crore
            - Target Regions: Pan-India with rural focus
            
            Create a detailed implementation roadmap with:
            
            1. PRE-IMPLEMENTATION (Months 1-3)
               - Assessment and planning
               - Stakeholder engagement
               - Infrastructure readiness
            
            2. PHASE 1: FOUNDATION (Months 4-12)
               - Quick wins and pilots
               - Training capacity setup
               - Initial hiring targets
               - Success metrics
            
            3. PHASE 2: SCALING (Year 2-3)
               - Capacity expansion
               - Geographic rollout
               - Retention programs
               - Performance targets
            
            4. PHASE 3: OPTIMIZATION (Year 4+)
               - Efficiency improvements
               - Sustainability measures
               - Impact assessment
               - Course corrections
            
            5. RISKS & MITIGATION
               - Key implementation risks
               - Contingency plans
               - Escalation paths
            
            6. SUCCESS CRITERIA
               - Quantitative metrics
               - Qualitative indicators
               - Monitoring framework
            
            Make it actionable with specific timelines, budgets, and responsible parties.
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating report: {str(e)}"
