import os
from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

center_products = {
    "C1": {"A", "B", "C"},
    "C2": {"D", "E", "F"},
    "C3": {"G", "H", "I"},
}

distances = {
    ("C1", "L1"): 10,
    ("C2", "L1"): 20,
    ("C3", "L1"): 30,
    ("C1", "C2"): 15,
    ("C1", "C3"): 25,
    ("C2", "C3"): 10,
}

def get_distance(a, b):
    return distances.get((a, b), distances.get((b, a), float('inf')))

@app.route('/')
def index():
    return "Backend is live and working!"

@app.route('/calculate-delivery-cost', methods=['POST'])
def calculate_cost():
    order = request.get_json()
    required_products = {k: v for k, v in order.items() if v > 0}
    centers_needed = set()

    for product in required_products:
        for center, items in center_products.items():
            if product in items:
                centers_needed.add(center)
                break

    min_cost = float('inf')
    for start in centers_needed:
        for path in permutations(centers_needed):
            if path[0] != start:
                continue

            cost = 0
            current = path[0]
            for center in path:
                if current != center:
                    cost += get_distance(current, center)
                    current = center

                cost += get_distance(current, "L1") * sum(
                    required_products[p]
                    for p in required_products
                    if p in center_products[center]
                )

            min_cost = min(min_cost, cost)

    return jsonify({"min_cost": min_cost})

if __name__ == '__main__':
    # Get the port from the environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
