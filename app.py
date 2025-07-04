from flask import Flask, render_template, request, jsonify
from model import (
    load_data,
    content_based_recommendation,
    collaborative_based_recommendation,
    hybrid_recommendation,
    get_recommendations
)

app = Flask(__name__)

# Load data globally so it can be used in imported functions
data, user_item_matrix = load_data()

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    if request.method == "POST":
        item_name = request.form.get("item_name")
        user_id = request.form.get("user_id")
        try:
            user_id = float(user_id)
        except:
            user_id = None

        if item_name and user_id:
            recommendations = hybrid_recommendation(data, user_item_matrix, user_id, item_name)
        elif item_name:
            recommendations = content_based_recommendation(data, item_name)
        elif user_id:
            recommendations = collaborative_based_recommendation(data, user_item_matrix, user_id)

    return render_template("index.html", recommendations=recommendations)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("q", "")
    matches = get_recommendations(data, query)
    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True)
