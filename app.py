from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.info['regularMarketPrice']
        return price
    except Exception as e:
        print("Error fetching price:", e)
        return None

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    print("Received data:", data)
    message = data.get('message', '').upper()

    # Very simple symbol extractor (assumes last word is symbol)
    words = message.split()
    symbol = words[-1] if words else ""

    price = get_stock_price(symbol)
    if price is None:
        return jsonify({"reply": f"Sorry, I couldn't find price for symbol '{symbol}'."})

    reply = f"📈 The current price of {symbol} is ${price:.2f}."
    print("Reply:", reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

