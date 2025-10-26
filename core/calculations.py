def safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate the safe daily spending amount based on financial inputs.

    Args:
        monthly_income (float): Monthly income.
        fixed_expenses (float): Monthly fixed expenses (e.g., rent, bills).
        variable_expenses_estimate (float): Estimated monthly variable expenses (e.g., food, entertainment).
        savings_goal (float): Total savings goal amount.
        months_for_goal (int): Number of months to achieve the savings goal.

    Returns:
        float: Safe daily spending amount.
        
    Raises:
        ValueError: If any input is negative or months_for_goal is not positive.
    """
    # Input validation
    if monthly_income < 0:
        raise ValueError("Monthly income must be non-negative.")
    if fixed_expenses < 0:
        raise ValueError("Fixed expenses must be non-negative.")
    if variable_expenses_estimate < 0:
        raise ValueError("Variable expenses estimate must be non-negative.")
    if savings_goal < 0:
        raise ValueError("Savings goal must be non-negative.")
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

    Args:
        monthly_income (float): Monthly income.
        fixed_expenses (float): Monthly fixed expenses (e.g., rent, bills).
        variable_expenses_estimate (float): Estimated monthly variable expenses (e.g., food, entertainment).
        savings_goal (float): Total savings goal amount.
        months_for_goal (int): Number of months to achieve the savings goal.

    Returns:
        float: Safe weekly spending amount.
        
    Raises:
        ValueError: If any input is negative or months_for_goal is not positive.
    """
    daily_spend = safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    return daily_spend * 7  # 7 days in a week


def safe_monthly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate the safe monthly spending amount based on financial inputs.

    Args:
        monthly_income (float): Monthly income.
        fixed_expenses (float): Monthly fixed expenses (e.g., rent, bills).
        variable_expenses_estimate (float): Estimated monthly variable expenses (e.g., food, entertainment).
        savings_goal (float): Total savings goal amount.
        months_for_goal (int): Number of months to achieve the savings goal.

    Returns:
        float: Safe monthly spending amount.
        
    Raises:
        ValueError: If any input is negative or months_for_goal is not positive.
    """
    daily_spend = safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    return daily_spend * 30  # 30 days in a month


def get_all_safe_spends(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal):
    """
    Calculate all safe spending amounts (daily, weekly, monthly) based on financial inputs.

    Args:
        monthly_income (float): Monthly income.
        fixed_expenses (float): Monthly fixed expenses (e.g., rent, bills).
        variable_expenses_estimate (float): Estimated monthly variable expenses (e.g., food, entertainment).
        savings_goal (float): Total savings goal amount.
        months_for_goal (int): Number of months to achieve the savings goal.

    Returns:
        dict: Dictionary containing daily, weekly, and monthly safe spending amounts.
        
    Raises:
        ValueError: If any input is negative or months_for_goal is not positive.
    """
    daily = safe_daily_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    weekly = safe_weekly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    monthly = safe_monthly_spend(monthly_income, fixed_expenses, variable_expenses_estimate, savings_goal, months_for_goal)
    
    return {
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly
    }
