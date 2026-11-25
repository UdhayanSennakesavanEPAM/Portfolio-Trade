
import csv

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

trades = []

with open("trades_test.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        trade = {
            "portfolio_id": row["portfolio_id"],
            "security_id": row["security_id"],
            "action": row["action"],
            "quantity": float(row["quantity"]),
            "price": float(row["price"]),
            "security_type": row["security_type"]
        }
        trades.append(trade)

def check_trade(trade, portfolio):
    security_id = trade["security_id"]
    action = trade["action"]
    quantity = trade["quantity"]
    price = trade["price"]
    # Step 1: Validate trade data
    if quantity <= 0 or price <= 0:
        return "Rejected", "Invalid trade data."
    if action != "Buy" and action != "Sell":
        return "Rejected", "Invalid trade data."
    # Step 2: Restricted security check
    if security_id in portfolio["restricted_securities"]:
        return "Rejected", "Security is restricted for this portfolio."
    # Step 3: Find existing holdings
    existing_quantity = 0
    holdings = portfolio["current_holdings"]
    for holding in holdings:
        if holding["security_id"] == security_id:
            existing_quantity = holding["quantity"]
            break
    # Step 4: Sell check
    if action == "Sell":
        if existing_quantity < quantity:
            return "Rejected", "Insufficient holdings to sell."
    # Step 5: Buy affordability check
    if action == "Buy":
        cash_balance = portfolio["cash_balance"]
        trade_cost = quantity * price
        if trade_cost > cash_balance:
            return "Rejected", "Insufficient cash for this buy order."
        # Step 6: Position concentration check
        post_trade_cash = cash_balance - trade_cost
        post_trade_quantity = existing_quantity + quantity
        post_trade_value = post_trade_quantity * price
        value_of_other_holdings = 0
        for holding in holdings:
            if holding["security_id"] != security_id:
                holding_value = holding["quantity"] * holding["market_price"]
                value_of_other_holdings = value_of_other_holdings + holding_value
        total_portfolio_value = post_trade_cash + post_trade_value + value_of_other_holdings
        position_pct = post_trade_value / total_portfolio_value
        max_position_pct = portfolio["max_position_pct"]
        if position_pct > max_position_pct:
            return "Needs Manual Sign-off", "Exceeds maximum position concentration — requires approval."
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

print("\nCOMPLIANCE RESULTS\n")
for result in results:
    print("Portfolio:", result["portfolio_id"])
    print("Security:", result["security_id"])
    print("Action:", result["action"])
    print("Quantity:", result["quantity"])
    print("Decision:", result["decision"])
    print("Reason:", result["reason"])
    print()

approved = 0
rejected = 0
manual = 0

for result in results:
    if result["decision"] == "Approved":
        approved += 1
    elif result["decision"] == "Rejected":
        rejected += 1
    else:
        manual += 1

print("COMPLIANCE SUMMARY")
print("Total Trades:", len(trades))
print("Approved:", approved)
print("Rejected:", rejected)
print("Needs Manual Sign-off:", manual)
