def project_investment(amount, forecast_period, ai_prediction):
    """
    Calculates the projected value of an investment based on AI prediction.

    Parameters:
    - amount (float): Initial investment in EUR.
    - forecast_period (str): "6 Months" or "1 Year"
    - ai_prediction (int): 1 for Up, 0 for Down

    Returns:
    - future_value (float)
    - diff (float)
    """
    if ai_prediction == 1:
        growth_rate = 0.15 if forecast_period == "1 Year" else 0.07
    else:
        growth_rate = -0.05 if forecast_period == "1 Year" else -0.025

    future_value = amount * (1 + growth_rate)
    diff = future_value - amount
    return future_value, diff
