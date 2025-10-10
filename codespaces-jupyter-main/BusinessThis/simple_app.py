#!/usr/bin/env python3
"""
Simple BusinessThis calculator - no dependencies required
Run with: python simple_app.py
"""

def safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate the safe daily spending amount based on financial inputs.
    """
    if months_for_goal <= 0:
        raise ValueError("Months for goal must be positive.")

    monthly_savings_contribution = savings_goal / months_for_goal
    monthly_disposable = monthly_income - fixed_expenses - monthly_savings_contribution
    monthly_safe_spend = monthly_disposable - variable_expenses_estimate

    # Assume 30 days in a month for simplicity
    daily_safe_spend = monthly_safe_spend / 30

    return max(0, daily_safe_spend)  # Ensure non-negative


def safe_weekly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate the safe weekly spending amount based on financial inputs.
    """
    daily_spend = safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    return daily_spend * 7  # 7 days in a week


def safe_monthly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate the safe monthly spending amount based on financial inputs.
    """
    daily_spend = safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    return daily_spend * 30  # 30 days in a month


def get_all_safe_spends(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate all safe spending amounts (daily, weekly, monthly) based on financial inputs.
    """
    daily = safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    weekly = safe_weekly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    monthly = safe_monthly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    
    return {
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly
    }

def main():
    print("=" * 60)
    print("🏦 BusinessThis - Financial Calculator")
    print("=" * 60)
    print()
    
    try:
        # Get user inputs with validation
        while True:
            try:
                monthly_income = float(input("Monthly Income ($): "))
                if monthly_income < 0:
                    print("❌ Income cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number for income.")
        
        while True:
            try:
                fixed_expenses = float(input("Fixed Expenses ($): "))
                if fixed_expenses < 0:
                    print("❌ Fixed expenses cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number for fixed expenses.")
        
        while True:
            try:
                variable_expenses = float(input("Variable Expenses Estimate ($): "))
                if variable_expenses < 0:
                    print("❌ Variable expenses cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number for variable expenses.")
        
        while True:
            try:
                savings_goal = float(input("Savings Goal ($): "))
                if savings_goal < 0:
                    print("❌ Savings goal cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid number for savings goal.")
        
        while True:
            try:
                months_for_goal = int(input("Months for Goal: "))
                if months_for_goal <= 0:
                    print("❌ Months for goal must be positive. Please try again.")
                    continue
                break
            except ValueError:
                print("❌ Please enter a valid integer for months for goal.")
        
        print()
        print("Calculating...")
        
        # Calculate all safe spends
        safe_spends = get_all_safe_spends(
            monthly_income, fixed_expenses, variable_expenses, 
            savings_goal, months_for_goal
        )
        
        # Display results
        print("=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print(f"Your safe daily spend:   ${safe_spends['daily']:.2f}")
        print(f"Your safe weekly spend:  ${safe_spends['weekly']:.2f}")
        print(f"Your safe monthly spend: ${safe_spends['monthly']:.2f}")
        print()
        
        # Breakdown
        monthly_savings = savings_goal / months_for_goal
        
        print("Monthly Budget Breakdown:")
        print(f"  💰 Monthly Income:     ${monthly_income:,.2f}")
        print(f"  🏠 Fixed Expenses:     ${fixed_expenses:,.2f}")
        print(f"  💎 Savings Goal:       ${monthly_savings:,.2f}")
        print(f"  🛒 Variable Expenses:  ${variable_expenses:,.2f}")
        print(f"  ✅ Safe Monthly Spend: ${safe_spends['monthly']:,.2f}")
        print()
        
        # Validation
        total_allocated = fixed_expenses + monthly_savings + variable_expenses + safe_spends['monthly']
        remaining = monthly_income - total_allocated
        
        if abs(remaining) < 0.01:  # Account for floating point precision
            print("✅ Budget is perfectly balanced!")
        elif remaining > 0:
            print(f"⚠️  You have ${remaining:.2f} unallocated each month")
        else:
            print(f"❌ You're overspending by ${abs(remaining):.2f} each month")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
