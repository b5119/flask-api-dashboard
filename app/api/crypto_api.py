#!/usr/bin/env python3
"""
CryptoTracker Flask API
API wrapper for cryptocurrency tracking and portfolio management
"""

from flask import Flask, jsonify, request
from tracker import CryptoTracker  # Assuming your class is in tracker.py

app = Flask(__name__)
tracker = CryptoTracker()


@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to CryptoTracker API",
        "routes": {
            "/coins": "List all available cryptocurrencies",
            "/price?ids=bitcoin,ethereum": "Get current prices",
            "/details/<coin_id>": "Get detailed info for a coin",
            "/top?limit=20": "Get top coins by market cap",
            "/trending": "Get trending coins",
            "/portfolio": "View portfolio value",
            "/portfolio/add": "Add coin to portfolio (POST)"
        }
    })


@app.route('/coins', methods=['GET'])
def get_coins():
    data = tracker.get_coin_list()
    return jsonify(data)


@app.route('/price', methods=['GET'])
def get_price():
    coin_ids = request.args.get('ids')
    vs_currency = request.args.get('currency', 'usd')
    if not coin_ids:
        return jsonify({"error": "Missing 'ids' parameter"}), 400
    coin_list = coin_ids.split(',')
    data = tracker.get_price(coin_list, vs_currency)
    return jsonify(data)


@app.route('/details/<coin_id>', methods=['GET'])
def get_details(coin_id):
    data = tracker.get_coin_details(coin_id)
    if not data:
        return jsonify({"error": f"Coin '{coin_id}' not found"}), 404
    return jsonify(data)


@app.route('/chart/<coin_id>', methods=['GET'])
def get_chart(coin_id):
    vs_currency = request.args.get('currency', 'usd')
    days = request.args.get('days', 7)
    data = tracker.get_market_chart(coin_id, vs_currency, days)
    if not data:
        return jsonify({"error": "Unable to fetch chart data"}), 500
    return jsonify(data)


@app.route('/trending', methods=['GET'])
def get_trending():
    data = tracker.get_trending()
    return jsonify(data)


@app.route('/top', methods=['GET'])
def get_top():
    vs_currency = request.args.get('currency', 'usd')
    limit = int(request.args.get('limit', 100))
    page = int(request.args.get('page', 1))
    data = tracker.get_top_coins(vs_currency, limit, page)
    return jsonify(data)


@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    """View total portfolio value"""
    vs_currency = request.args.get('currency', 'usd')
    portfolio_value = tracker.calculate_portfolio_value(vs_currency)
    return jsonify(portfolio_value if portfolio_value else {"message": "Portfolio empty"})


@app.route('/portfolio/add', methods=['POST'])
def add_to_portfolio():
    """Add coin to portfolio"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    coin_id = data.get('coin_id')
    amount = data.get('amount')
    purchase_price = data.get('purchase_price', None)
    
    if not coin_id or not amount:
        return jsonify({"error": "Missing 'coin_id' or 'amount'"}), 400
    
    tracker.add_to_portfolio(coin_id, amount, purchase_price)
    return jsonify({"message": f"Added {amount} {coin_id} to portfolio"}), 201


if __name__ == '__main__':
    app.run(debug=True)
