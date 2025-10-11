"""
Reports service for BusinessThis
Handles PDF reports, Excel exports, and email summaries
"""
import os
import io
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import plotly.graph_objects as go
import plotly.express as px
import base64
from io import BytesIO

class ReportsService:
    """Reports service for generating PDF reports and Excel exports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for reports"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6
        ))
    
    def generate_financial_report_pdf(self, user_profile: Dict[str, Any], 
                                     savings_goals: List[Dict[str, Any]], 
                                     financial_health: Dict[str, Any]) -> bytes:
        """Generate comprehensive financial report PDF"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph("BusinessThis Financial Report", self.styles['CustomTitle'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Report date
            report_date = Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", self.styles['CustomBody'])
            story.append(report_date)
            story.append(Spacer(1, 20))
            
            # Financial Overview
            story.append(Paragraph("Financial Overview", self.styles['CustomHeading']))
            
            overview_data = [
                ['Monthly Income', f"${user_profile.get('monthly_income', 0):,.2f}"],
                ['Fixed Expenses', f"${user_profile.get('fixed_expenses', 0):,.2f}"],
                ['Variable Expenses', f"${user_profile.get('variable_expenses', 0):,.2f}"],
                ['Emergency Fund', f"${user_profile.get('emergency_fund_current', 0):,.2f}"],
                ['Total Debt', f"${user_profile.get('total_debt', 0):,.2f}"]
            ]
            
            overview_table = Table(overview_data, colWidths=[2*inch, 1.5*inch])
            overview_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 20))
            
            # Financial Health Score
            if financial_health:
                story.append(Paragraph("Financial Health Score", self.styles['CustomHeading']))
                
                health_score = financial_health.get('overall_score', 0)
                health_level = financial_health.get('health_level', 'Unknown')
                
                health_text = f"Your financial health score is {health_score}/100 ({health_level})"
                story.append(Paragraph(health_text, self.styles['CustomBody']))
                
                if financial_health.get('recommendations'):
                    story.append(Paragraph("Recommendations:", self.styles['CustomBody']))
                    for rec in financial_health['recommendations']:
                        story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 20))
            
            # Savings Goals
            if savings_goals:
                story.append(Paragraph("Savings Goals", self.styles['CustomHeading']))
                
                goals_data = [['Goal Name', 'Target Amount', 'Current Amount', 'Progress']]
                for goal in savings_goals:
                    progress = (goal.get('current_amount', 0) / goal.get('target_amount', 1)) * 100
                    goals_data.append([
                        goal.get('name', 'Unnamed Goal'),
                        f"${goal.get('target_amount', 0):,.2f}",
                        f"${goal.get('current_amount', 0):,.2f}",
                        f"{progress:.1f}%"
                    ])
                
                goals_table = Table(goals_data, colWidths=[1.5*inch, 1*inch, 1*inch, 0.8*inch])
                goals_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(goals_table)
                story.append(Spacer(1, 20))
            
            # Recommendations
            story.append(Paragraph("Key Recommendations", self.styles['CustomHeading']))
            
            recommendations = self._generate_recommendations(user_profile, financial_health)
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
            
            story.append(Spacer(1, 20))
            
            # Footer
            footer = Paragraph("This report was generated by BusinessThis - Your Personal Financial Planning Assistant", 
                             self.styles['CustomBody'])
            story.append(footer)
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Error generating PDF report: {str(e)}")
    
    def generate_excel_export(self, user_profile: Dict[str, Any], 
                             savings_goals: List[Dict[str, Any]], 
                             transactions: List[Dict[str, Any]]) -> bytes:
        """Generate Excel export of financial data"""
        try:
            # Create Excel writer
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Financial Profile Sheet
                profile_data = {
                    'Metric': [
                        'Monthly Income',
                        'Fixed Expenses',
                        'Variable Expenses',
                        'Emergency Fund Current',
                        'Emergency Fund Target',
                        'Total Debt',
                        'Credit Score',
                        'Age',
                        'Risk Tolerance'
                    ],
                    'Value': [
                        user_profile.get('monthly_income', 0),
                        user_profile.get('fixed_expenses', 0),
                        user_profile.get('variable_expenses', 0),
                        user_profile.get('emergency_fund_current', 0),
                        user_profile.get('emergency_fund_target', 0),
                        user_profile.get('total_debt', 0),
                        user_profile.get('credit_score', 'N/A'),
                        user_profile.get('age', 'N/A'),
                        user_profile.get('risk_tolerance', 'N/A')
                    ]
                }
                
                profile_df = pd.DataFrame(profile_data)
                profile_df.to_excel(writer, sheet_name='Financial Profile', index=False)
                
                # Savings Goals Sheet
                if savings_goals:
                    goals_data = []
                    for goal in savings_goals:
                        progress = (goal.get('current_amount', 0) / goal.get('target_amount', 1)) * 100
                        goals_data.append({
                            'Goal Name': goal.get('name', 'Unnamed Goal'),
                            'Target Amount': goal.get('target_amount', 0),
                            'Current Amount': goal.get('current_amount', 0),
                            'Progress %': progress,
                            'Target Date': goal.get('target_date', 'N/A'),
                            'Monthly Contribution': goal.get('monthly_contribution', 0),
                            'Priority': goal.get('priority', 1),
                            'Is Achieved': goal.get('is_achieved', False)
                        })
                    
                    goals_df = pd.DataFrame(goals_data)
                    goals_df.to_excel(writer, sheet_name='Savings Goals', index=False)
                
                # Transactions Sheet
                if transactions:
                    transactions_df = pd.DataFrame(transactions)
                    transactions_df.to_excel(writer, sheet_name='Transactions', index=False)
                
                # Summary Sheet
                summary_data = {
                    'Metric': [
                        'Total Monthly Income',
                        'Total Monthly Expenses',
                        'Monthly Savings',
                        'Savings Rate %',
                        'Emergency Fund Progress %',
                        'Debt-to-Income Ratio %'
                    ],
                    'Value': [
                        user_profile.get('monthly_income', 0),
                        user_profile.get('fixed_expenses', 0) + user_profile.get('variable_expenses', 0),
                        user_profile.get('monthly_income', 0) - user_profile.get('fixed_expenses', 0) - user_profile.get('variable_expenses', 0),
                        self._calculate_savings_rate(user_profile),
                        self._calculate_emergency_fund_progress(user_profile),
                        self._calculate_debt_to_income_ratio(user_profile)
                    ]
                }
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Error generating Excel export: {str(e)}")
    
    def generate_email_summary(self, user_profile: Dict[str, Any], 
                              savings_goals: List[Dict[str, Any]], 
                              recent_transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate email summary for user"""
        try:
            # Calculate key metrics
            monthly_income = user_profile.get('monthly_income', 0)
            monthly_expenses = user_profile.get('fixed_expenses', 0) + user_profile.get('variable_expenses', 0)
            monthly_savings = monthly_income - monthly_expenses
            savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
            
            # Emergency fund progress
            emergency_fund_current = user_profile.get('emergency_fund_current', 0)
            emergency_fund_target = user_profile.get('emergency_fund_target', 0)
            emergency_fund_progress = (emergency_fund_current / emergency_fund_target * 100) if emergency_fund_target > 0 else 0
            
            # Goals progress
            total_goals = len(savings_goals)
            achieved_goals = sum(1 for goal in savings_goals if goal.get('is_achieved', False))
            goals_progress = (achieved_goals / total_goals * 100) if total_goals > 0 else 0
            
            # Recent spending analysis
            spending_by_category = {}
            for transaction in recent_transactions:
                if transaction.get('transaction_type') == 'expense':
                    category = transaction.get('category', 'Other')
                    amount = transaction.get('amount', 0)
                    spending_by_category[category] = spending_by_category.get(category, 0) + amount
            
            # Generate insights
            insights = []
            if savings_rate < 10:
                insights.append("Consider increasing your savings rate to build wealth faster")
            if emergency_fund_progress < 50:
                insights.append("Focus on building your emergency fund for financial security")
            if goals_progress > 50:
                insights.append("Great job on your savings goals! Keep up the momentum")
            
            return {
                'monthly_income': monthly_income,
                'monthly_expenses': monthly_expenses,
                'monthly_savings': monthly_savings,
                'savings_rate': savings_rate,
                'emergency_fund_progress': emergency_fund_progress,
                'goals_progress': goals_progress,
                'total_goals': total_goals,
                'achieved_goals': achieved_goals,
                'spending_by_category': spending_by_category,
                'insights': insights,
                'report_date': datetime.now().strftime('%B %d, %Y')
            }
            
        except Exception as e:
            return {'error': f'Error generating email summary: {str(e)}'}
    
    def create_financial_chart(self, chart_type: str, data: Dict[str, Any]) -> str:
        """Create financial chart and return as base64 string"""
        try:
            if chart_type == 'spending_breakdown':
                return self._create_spending_breakdown_chart(data)
            elif chart_type == 'savings_progress':
                return self._create_savings_progress_chart(data)
            elif chart_type == 'financial_health':
                return self._create_financial_health_chart(data)
            elif chart_type == 'income_vs_expenses':
                return self._create_income_vs_expenses_chart(data)
            else:
                raise ValueError(f"Unknown chart type: {chart_type}")
                
        except Exception as e:
            raise Exception(f"Error creating chart: {str(e)}")
    
    def _create_spending_breakdown_chart(self, data: Dict[str, Any]) -> str:
        """Create spending breakdown pie chart"""
        categories = data.get('categories', {})
        
        fig = go.Figure(data=[go.Pie(
            labels=list(categories.keys()),
            values=list(categories.values()),
            hole=0.3
        )])
        
        fig.update_layout(
            title="Spending Breakdown",
            font_size=12,
            showlegend=True
        )
        
        return self._fig_to_base64(fig)
    
    def _create_savings_progress_chart(self, data: Dict[str, Any]) -> str:
        """Create savings progress bar chart"""
        goals = data.get('goals', [])
        
        goal_names = [goal.get('name', 'Goal') for goal in goals]
        progress_values = [(goal.get('current_amount', 0) / goal.get('target_amount', 1)) * 100 
                          for goal in goals]
        
        fig = go.Figure(data=[go.Bar(
            x=goal_names,
            y=progress_values,
            marker_color='lightblue'
        )])
        
        fig.update_layout(
            title="Savings Goals Progress",
            xaxis_title="Goals",
            yaxis_title="Progress (%)",
            yaxis=dict(range=[0, 100])
        )
        
        return self._fig_to_base64(fig)
    
    def _create_financial_health_chart(self, data: Dict[str, Any]) -> str:
        """Create financial health gauge chart"""
        score = data.get('score', 0)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Financial Health Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        return self._fig_to_base64(fig)
    
    def _create_income_vs_expenses_chart(self, data: Dict[str, Any]) -> str:
        """Create income vs expenses bar chart"""
        months = data.get('months', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
        income = data.get('income', [5000, 5000, 5000, 5000, 5000, 5000])
        expenses = data.get('expenses', [3000, 3200, 2800, 3500, 3100, 3300])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Income', x=months, y=income, marker_color='green'))
        fig.add_trace(go.Bar(name='Expenses', x=months, y=expenses, marker_color='red'))
        
        fig.update_layout(
            title="Monthly Income vs Expenses",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            barmode='group'
        )
        
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """Convert plotly figure to base64 string"""
        img_bytes = fig.to_image(format="png", width=800, height=600)
        return base64.b64encode(img_bytes).decode()
    
    def _generate_recommendations(self, user_profile: Dict[str, Any], 
                                 financial_health: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Emergency fund recommendations
        emergency_fund_current = user_profile.get('emergency_fund_current', 0)
        emergency_fund_target = user_profile.get('emergency_fund_target', 0)
        if emergency_fund_current < emergency_fund_target * 0.5:
            recommendations.append("Focus on building your emergency fund to 3-6 months of expenses")
        
        # Debt recommendations
        total_debt = user_profile.get('total_debt', 0)
        monthly_income = user_profile.get('monthly_income', 0)
        if total_debt > monthly_income * 6:
            recommendations.append("Consider debt consolidation or aggressive debt payoff strategies")
        
        # Savings rate recommendations
        monthly_expenses = user_profile.get('fixed_expenses', 0) + user_profile.get('variable_expenses', 0)
        savings_rate = (monthly_income - monthly_expenses) / monthly_income * 100 if monthly_income > 0 else 0
        if savings_rate < 20:
            recommendations.append("Aim to save at least 20% of your income for long-term financial security")
        
        # Investment recommendations
        if emergency_fund_current >= emergency_fund_target and total_debt < monthly_income * 2:
            recommendations.append("Consider starting an investment portfolio for long-term wealth building")
        
        return recommendations
    
    def _calculate_savings_rate(self, user_profile: Dict[str, Any]) -> float:
        """Calculate savings rate percentage"""
        monthly_income = user_profile.get('monthly_income', 0)
        monthly_expenses = user_profile.get('fixed_expenses', 0) + user_profile.get('variable_expenses', 0)
        if monthly_income > 0:
            return ((monthly_income - monthly_expenses) / monthly_income) * 100
        return 0
    
    def _calculate_emergency_fund_progress(self, user_profile: Dict[str, Any]) -> float:
        """Calculate emergency fund progress percentage"""
        current = user_profile.get('emergency_fund_current', 0)
        target = user_profile.get('emergency_fund_target', 0)
        if target > 0:
            return (current / target) * 100
        return 0
    
    def _calculate_debt_to_income_ratio(self, user_profile: Dict[str, Any]) -> float:
        """Calculate debt-to-income ratio percentage"""
        total_debt = user_profile.get('total_debt', 0)
        monthly_income = user_profile.get('monthly_income', 0)
        if monthly_income > 0:
            return (total_debt / monthly_income) * 100
        return 0
