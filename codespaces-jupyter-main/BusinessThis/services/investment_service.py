"""
Investment service for BusinessThis
Handles investment calculations, portfolio management, and retirement planning
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from decimal import Decimal
import math
import logging

class InvestmentService:
    """Investment service for portfolio management and calculations"""
    
    def __init__(self):
        pass
    
    def calculate_asset_allocation(self, age: int, risk_tolerance: str, investment_amount: float) -> Dict[str, Any]:
        """Calculate recommended asset allocation based on age and risk tolerance"""
        try:
            # Base allocation rules
            if risk_tolerance == "conservative":
                stock_percentage = max(20, 100 - age)
                bond_percentage = min(80, age + 20)
                cash_percentage = 10
            elif risk_tolerance == "aggressive":
                stock_percentage = max(80, 100 - age + 10)
                bond_percentage = min(20, age - 10)
                cash_percentage = 5
            else:  # moderate
                stock_percentage = max(60, 100 - age)
                bond_percentage = min(40, age)
                cash_percentage = 5
            
            # Ensure percentages add up to 100
            total = stock_percentage + bond_percentage + cash_percentage
            if total != 100:
                stock_percentage = int(stock_percentage * 100 / total)
                bond_percentage = int(bond_percentage * 100 / total)
                cash_percentage = 100 - stock_percentage - bond_percentage
            
            # Calculate dollar amounts
            stock_amount = investment_amount * stock_percentage / 100
            bond_amount = investment_amount * bond_percentage / 100
            cash_amount = investment_amount * cash_percentage / 100
            
            return {
                'stock_percentage': stock_percentage,
                'bond_percentage': bond_percentage,
                'cash_percentage': cash_percentage,
                'stock_amount': stock_amount,
                'bond_amount': bond_amount,
                'cash_amount': cash_amount,
                'recommendations': self.get_allocation_recommendations(stock_percentage, bond_percentage, cash_percentage)
            }
            
        except Exception as e:
            return {'error': f'Error calculating asset allocation: {str(e)}'}
    
    def get_allocation_recommendations(self, stock_pct: int, bond_pct: int, cash_pct: int) -> List[str]:
        """Get recommendations based on asset allocation"""
        recommendations = []
        
        if stock_pct > 80:
            recommendations.append("Consider reducing stock allocation for better diversification")
        elif stock_pct < 40:
            recommendations.append("Consider increasing stock allocation for long-term growth")
        
        if bond_pct > 60:
            recommendations.append("High bond allocation may limit growth potential")
        elif bond_pct < 20:
            recommendations.append("Consider adding bonds for stability")
        
        if cash_pct > 20:
            recommendations.append("High cash allocation may lose value to inflation")
        elif cash_pct < 5:
            recommendations.append("Consider maintaining emergency cash reserves")
        
        if not recommendations:
            recommendations.append("Your asset allocation looks well-balanced!")
        
        return recommendations
    
    def calculate_retirement_needs(self, current_age: int, retirement_age: int, current_savings: float, 
                                 monthly_income: float, desired_retirement_income: float) -> Dict[str, Any]:
        """Calculate retirement savings needs and recommendations"""
        try:
            years_to_retirement = retirement_age - current_age
            if years_to_retirement <= 0:
                return {'error': 'Retirement age must be greater than current age'}
            
            # Calculate retirement income needs (80% of current income as default)
            if desired_retirement_income <= 0:
                desired_retirement_income = monthly_income * 12 * 0.8
            
            # Calculate total needed (25x annual expenses rule)
            total_needed = desired_retirement_income * 25
            
            # Calculate monthly contribution needed
            # Using future value of annuity formula
            annual_return = 0.07  # 7% annual return assumption
            monthly_return = annual_return / 12
            
            if monthly_return > 0:
                future_value_factor = (1 + monthly_return) ** (years_to_retirement * 12)
                monthly_contribution = (total_needed - current_savings * future_value_factor) / \
                                    ((future_value_factor - 1) / monthly_return)
            else:
                monthly_contribution = (total_needed - current_savings) / (years_to_retirement * 12)
            
            # Calculate 401k and IRA contributions
            max_401k_contribution = 23000  # 2024 limit
            max_ira_contribution = 7000    # 2024 limit
            
            # Recommendations
            recommendations = []
            if monthly_contribution > max_401k_contribution / 12:
                recommendations.append("Max out 401k contributions first")
                remaining = monthly_contribution - max_401k_contribution / 12
                if remaining > max_ira_contribution / 12:
                    recommendations.append("Also max out IRA contributions")
                    recommendations.append("Consider additional taxable investments")
                else:
                    recommendations.append("Use IRA for remaining contributions")
            else:
                recommendations.append("401k contributions should cover your needs")
            
            return {
                'years_to_retirement': years_to_retirement,
                'total_needed': total_needed,
                'monthly_contribution_needed': max(0, monthly_contribution),
                'current_savings': current_savings,
                'gap': max(0, total_needed - current_savings),
                'recommendations': recommendations,
                'max_401k_contribution': max_401k_contribution,
                'max_ira_contribution': max_ira_contribution
            }
            
        except Exception as e:
            return {'error': f'Error calculating retirement needs: {str(e)}'}
    
    def calculate_compound_interest(self, principal: float, monthly_contribution: float, 
                                  annual_rate: float, years: int) -> Dict[str, Any]:
        """Calculate compound interest growth"""
        try:
            monthly_rate = annual_rate / 12
            total_months = years * 12
            
            # Future value of principal
            principal_future = principal * (1 + monthly_rate) ** total_months
            
            # Future value of monthly contributions (annuity)
            if monthly_rate > 0:
                annuity_future = monthly_contribution * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
            else:
                annuity_future = monthly_contribution * total_months
            
            total_future_value = principal_future + annuity_future
            total_contributions = principal + (monthly_contribution * total_months)
            total_interest = total_future_value - total_contributions
            
            return {
                'principal_future': principal_future,
                'annuity_future': annuity_future,
                'total_future_value': total_future_value,
                'total_contributions': total_contributions,
                'total_interest': total_interest,
                'growth_multiple': total_future_value / total_contributions if total_contributions > 0 else 0
            }
            
        except Exception as e:
            return {'error': f'Error calculating compound interest: {str(e)}'}
    
    def calculate_tax_optimization(self, income: float, filing_status: str, 
                                 deductions: float = 0, credits: float = 0) -> Dict[str, Any]:
        """Calculate tax optimization strategies"""
        try:
            # 2024 tax brackets (single filer)
            tax_brackets = [
                (0, 11000, 0.10),
                (11000, 44725, 0.12),
                (44725, 95375, 0.22),
                (95375, 182050, 0.24),
                (182050, 231250, 0.32),
                (231250, 578125, 0.35),
                (578125, float('inf'), 0.37)
            ]
            
            # Adjust brackets for different filing status
            if filing_status == "married_joint":
                # Rough adjustment - in practice, use exact brackets
                tax_brackets = [(bracket[0] * 2, bracket[1] * 2, bracket[2]) for bracket in tax_brackets]
            
            # Calculate taxable income
            standard_deduction = 13850  # 2024 single filer
            if filing_status == "married_joint":
                standard_deduction = 27700
            
            taxable_income = max(0, income - max(standard_deduction, deductions))
            
            # Calculate tax
            total_tax = 0
            tax_breakdown = []
            
            for bracket in tax_brackets:
                if taxable_income <= bracket[0]:
                    break
                
                bracket_income = min(taxable_income, bracket[1]) - bracket[0]
                if bracket_income > 0:
                    bracket_tax = bracket_income * bracket[2]
                    total_tax += bracket_tax
                    tax_breakdown.append({
                        'bracket': f"{bracket[0]:,.0f} - {bracket[1]:,.0f}",
                        'rate': f"{bracket[2]*100:.0f}%",
                        'income': bracket_income,
                        'tax': bracket_tax
                    })
            
            # Apply credits
            final_tax = max(0, total_tax - credits)
            effective_rate = final_tax / income if income > 0 else 0
            marginal_rate = tax_brackets[-1][2]  # Highest bracket rate
            
            # Optimization recommendations
            recommendations = []
            if effective_rate > 0.20:
                recommendations.append("Consider maxing out 401k contributions to reduce taxable income")
            if income > 100000:
                recommendations.append("Consider Roth IRA conversions in lower income years")
            if deductions < standard_deduction:
                recommendations.append("Consider itemizing deductions if they exceed standard deduction")
            
            return {
                'taxable_income': taxable_income,
                'total_tax': total_tax,
                'credits': credits,
                'final_tax': final_tax,
                'effective_rate': effective_rate,
                'marginal_rate': marginal_rate,
                'tax_breakdown': tax_breakdown,
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {'error': f'Error calculating tax optimization: {str(e)}'}
    
    def calculate_what_if_scenarios(self, base_income: float, base_expenses: float, 
                                  scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate what-if scenarios for financial planning"""
        try:
            results = {}
            
            for i, scenario in enumerate(scenarios):
                scenario_name = scenario.get('name', f'Scenario {i+1}')
                
                # Apply scenario changes
                income = base_income * scenario.get('income_multiplier', 1.0)
                expenses = base_expenses * scenario.get('expense_multiplier', 1.0)
                
                # Calculate new financial position
                monthly_savings = income - expenses
                annual_savings = monthly_savings * 12
                
                # Calculate emergency fund timeline
                emergency_fund_target = expenses * 6  # 6 months expenses
                if monthly_savings > 0:
                    months_to_emergency_fund = emergency_fund_target / monthly_savings
                else:
                    months_to_emergency_fund = float('inf')
                
                results[scenario_name] = {
                    'income': income,
                    'expenses': expenses,
                    'monthly_savings': monthly_savings,
                    'annual_savings': annual_savings,
                    'emergency_fund_target': emergency_fund_target,
                    'months_to_emergency_fund': months_to_emergency_fund,
                    'savings_rate': (monthly_savings / income) * 100 if income > 0 else 0
                }
            
            return {
                'base_scenario': {
                    'income': base_income,
                    'expenses': base_expenses,
                    'monthly_savings': base_income - base_expenses
                },
                'scenarios': results
            }
            
        except Exception as e:
            return {'error': f'Error calculating what-if scenarios: {str(e)}'}
    
    def get_investment_recommendations(self, age: int, income: float, risk_tolerance: str, 
                                     current_investments: float = 0) -> Dict[str, Any]:
        """Get personalized investment recommendations"""
        try:
            recommendations = []
            
            # 401k recommendations
            max_401k = 23000  # 2024 limit
            recommended_401k = min(max_401k, income * 0.15)  # 15% of income
            if recommended_401k > 0:
                recommendations.append({
                    'type': '401k',
                    'amount': recommended_401k,
                    'priority': 'high',
                    'reason': 'Tax-advantaged retirement savings'
                })
            
            # IRA recommendations
            max_ira = 7000  # 2024 limit
            if income < 138000:  # Roth IRA income limit
                recommendations.append({
                    'type': 'Roth IRA',
                    'amount': max_ira,
                    'priority': 'high',
                    'reason': 'Tax-free growth for retirement'
                })
            else:
                recommendations.append({
                    'type': 'Traditional IRA',
                    'amount': max_ira,
                    'priority': 'medium',
                    'reason': 'Tax-deferred growth'
                })
            
            # Emergency fund
            emergency_fund_target = income * 0.5  # 6 months of income
            if current_investments < emergency_fund_target:
                recommendations.append({
                    'type': 'Emergency Fund',
                    'amount': emergency_fund_target - current_investments,
                    'priority': 'high',
                    'reason': 'Financial safety net'
                })
            
            # Taxable investments
            if income > 100000:
                recommendations.append({
                    'type': 'Taxable Brokerage',
                    'amount': income * 0.10,
                    'priority': 'medium',
                    'reason': 'Additional growth opportunities'
                })
            
            return {
                'recommendations': recommendations,
                'total_recommended': sum(rec['amount'] for rec in recommendations),
                'risk_tolerance': risk_tolerance,
                'age_based_advice': self.get_age_based_advice(age)
            }
            
        except Exception as e:
            return {'error': f'Error getting investment recommendations: {str(e)}'}
    
    def get_age_based_advice(self, age: int) -> List[str]:
        """Get age-specific investment advice"""
        advice = []
        
        if age < 30:
            advice.append("Focus on growth investments - you have time to recover from market downturns")
            advice.append("Consider starting with target-date funds for simplicity")
        elif age < 50:
            advice.append("Balance growth with stability - consider 60/40 stock/bond allocation")
            advice.append("Maximize employer 401k matching if available")
        elif age < 65:
            advice.append("Shift toward more conservative investments as retirement approaches")
            advice.append("Consider catch-up contributions to retirement accounts")
        else:
            advice.append("Focus on income generation and capital preservation")
            advice.append("Consider dividend-paying stocks and bonds")
        
        return advice
