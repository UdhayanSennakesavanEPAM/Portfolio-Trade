
# Portfolio Trade Order Compliance & Execution Checker

A Python application that validates proposed portfolio trades before execution based on predefined compliance rules.

## Features
- Validates trade quantity, price and action.
- Checks restricted securities.
- Verifies sufficient holdings for Sell orders.
- Checks available cash for Buy orders.
- Calculates position concentration for Buy orders.
- Returns Approved, Rejected, or Needs Manual Sign-off with a reason.

## Input
- Proposed trades from `trades_test.csv`.
- Portfolio reference data containing cash balance, restricted securities, maximum position percentage and current holdings.

## Output
A compliance decision and reason for each proposed trade.

## How to Run
Run the Python file:

```bash
python main.py
```
