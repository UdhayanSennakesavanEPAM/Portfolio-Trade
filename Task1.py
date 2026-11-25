portfolios = {

    "POR001": {
        "cash_balance": 50000,
        "restricted_securities": ["XYZCORP"],
        "max_position_pct": 0.30,

        "current_holdings": [
            {"security_id": "AAPL", "quantity": 100, "market_price": 150},
            {"security_id": "TCS", "quantity": 100, "market_price": 310},
            {"security_id": "INFY", "quantity": 50, "market_price": 1500}
        ]
    }

}

trades = [

    {"portfolio_id": "POR001", "security_id": "AAPL", "action": "Buy", "quantity": 20, "price": 150, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "AAPL", "action": "Buy", "quantity": 60, "price": 150, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "TCS", "action": "Sell", "quantity": 50, "price": 310, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "TCS", "action": "Sell", "quantity": 60, "price": 310, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "XYZCORP", "action": "Buy", "quantity": 10, "price": 50, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "AAPL", "action": "Buy", "quantity": 400, "price": 150, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "AAPL", "action": "Buy", "quantity": -10, "price": 150, "security_type": "Equity"},
    {"portfolio_id": "POR001", "security_id": "INFY", "action": "Buy", "quantity": 10, "price": 1500, "security_type": "Equity"},

    {"portfolio_id": "POR002", "security_id": "GOOGL", "action": "Buy", "quantity": 5, "price": 2000, "security_type": "Equity"},

    {"portfolio_id": "POR003", "security_id": "BADCO", "action": "Buy", "quantity": 10, "price": 100, "security_type": "Equity"},
    {"portfolio_id": "POR003", "security_id": "TCS", "action": "Buy", "quantity": 5, "price": 300, "security_type": "Equity"},
    {"portfolio_id": "POR003", "security_id": "INFY", "action": "Buy", "quantity": 50, "price": 1500, "security_type": "Equity"},
    {"portfolio_id": "POR003", "security_id": "RELIANCE", "action": "Sell", "quantity": 30, "price": 2400, "security_type": "Equity"},
    {"portfolio_id": "POR003", "security_id": "RELIANCE", "action": "Sell", "quantity": 31, "price": 2400, "security_type": "Equity"},

    {"portfolio_id": "POR004", "security_id": "GOOGL", "action": "Buy", "quantity": 10, "price": 2000, "security_type": "Equity"},
    {"portfolio_id": "POR004", "security_id": "AAPL", "action": "Buy", "quantity": 300, "price": 150, "security_type": "Equity"},

    {"portfolio_id": "POR005", "security_id": "PENNY1", "action": "Buy", "quantity": 5, "price": 10, "security_type": "Equity"},
    {"portfolio_id": "POR005", "security_id": "AAPL", "action": "Buy", "quantity": 33, "price": 150, "security_type": "Equity"},
    {"portfolio_id": "POR005", "security_id": "AAPL", "action": "Buy", "quantity": 34, "price": 150, "security_type": "Equity"},
    {"portfolio_id": "POR005", "security_id": "TCS", "action": "Buy", "quantity": 20, "price": 250, "security_type": "Equity"}

]



def check_trade(trade, portfolio):

    security_id = trade["security_id"]
    action = trade["action"]
    quantity = trade["quantity"]
    price = trade["price"]

    #step 1
    if quantity <= 0 or price <= 0:
        return "Rejected", "Invalid trade data."

    if action != "Buy" and action != "Sell":
        return "Rejected", "Invalid trade data."

    #step 2
    if security_id in portfolio["restricted_securities"]:
        return "Rejected", "Security is restricted for this portfolio."

    #step 3
    existing_quantity = 0
    holdings = portfolio["current_holdings"]
    for holding in holdings:
        if holding["security_id"] == security_id:
            existing_quantity = holding["quantity"]
            break

    if action == "Sell":
        if existing_quantity < quantity:
            return "Rejected", "Insufficient holdings to sell."
        
    #step 4
    if action == "Buy":
        cash_balance = portfolio["cash_balance"]
        trade_cost = quantity * price
        if trade_cost > cash_balance:
            return "Rejected", "Insufficient cash for this buy order."

    #step 5
        post_trade_cash = cash_balance - trade_cost
        post_trade_quantity = existing_quantity + quantity
        post_trade_value = post_trade_quantity * price
        value_of_other_holdings = 0

        for holding in holdings:
            if holding["security_id"] != security_id:
                holding_value = (
                    holding["quantity"] * holding["market_price"]
                )
                value_of_other_holdings = (
                    value_of_other_holdings + holding_value
                )
                
        total_portfolio_value = (
            post_trade_cash
            + post_trade_value
            + value_of_other_holdings
        )

        position_pct = post_trade_value / total_portfolio_value
        max_position_pct = portfolio["max_position_pct"]
        if position_pct > max_position_pct:
            return (
                "Needs Manual Sign-off",
                "Exceeds maximum position concentration — requires approval."
            )
    return "Approved", "Trade passed all compliance checks."

results = []

for trade in trades:
    portfolio_id = trade["portfolio_id"]
    if portfolio_id not in portfolios:
        decision = "Rejected"
        reason = "Portfolio not found."
    else:
        portfolio = portfolios[portfolio_id]
        decision, reason = check_trade(trade, portfolio)

    result = {
        "portfolio_id": portfolio_id,
        "security_id": trade["security_id"],
        "action": trade["action"],
        "quantity": trade["quantity"],
        "decision": decision,
        "reason": reason
    }
    results.append(result)

print("\nCOMPLIANCE RESULTS \n")

for result in results:

    print("Portfolio:", result["portfolio_id"])
    print("Security:", result["security_id"])
    print("Action:", result["action"])
    print("Quantity:", result["quantity"])
    print("Decision:", result["decision"])
    print("Reason:", result["reason"])
    print()

