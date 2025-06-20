from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(
    "mongodb+srv://testsiddheshkanawade:Q41c1fALOVs3nLaU@cluster0.pf6vbum.mongodb.net/"
)
db = client["josaa"]  # database name
josaa_collection = db["college_data"]  # collection name for JOSAA data
csab_collection = db["csab_college_data"]  # collection name for CSAB data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/csab")
def csab():
    return render_template("csab.html")


@app.route("/get-institutes", methods=["GET"])
def get_institutes():
    category = request.args.get("category", "josaa")
    collection = csab_collection if category == "csab" else josaa_collection
    # Get unique institutes sorted alphabetically
    institutes = sorted(collection.distinct("Institute"))
    return jsonify(institutes)


@app.route("/get-branches", methods=["GET"])
def get_branches():
    category = request.args.get("category", "josaa")
    collection = csab_collection if category == "csab" else josaa_collection
    # Get unique academic programs (branches) sorted alphabetically
    branches = sorted(collection.distinct("Academic Program Name"))
    return jsonify(branches)


@app.route("/get-quotas", methods=["GET"])
def get_quotas():
    category = request.args.get("category", "josaa")
    collection = csab_collection if category == "csab" else josaa_collection
    # Get unique quotas sorted alphabetically
    quotas = sorted(collection.distinct("Quota"))
    return jsonify(quotas)


@app.route("/search", methods=["POST"])
def search():
    search_params = request.json
    category = search_params.get("category", "josaa")
    collection = csab_collection if category == "csab" else josaa_collection
    
    query = {}

    # Handle Round filter (multiple selection)
    if search_params.get("rounds"):
        query["Round"] = {"$in": search_params["rounds"]}

    # Handle Seat Type filter (multiple selection)
    if search_params.get("seatType"):
        query["Seat Type"] = {"$in": search_params["seatType"]}

    # Handle Gender filter
    if search_params.get("gender"):
        query["Gender"] = search_params["gender"]

    # Handle Institute filter (multiple selection)
    if search_params.get("institutes"):
        query["Institute"] = {"$in": search_params["institutes"]}

    # Handle Branch filter (multiple selection)
    if search_params.get("branches"):
        query["Academic Program Name"] = {"$in": search_params["branches"]}
        
    # Handle Quota filter (multiple selection)
    if search_params.get("quotas"):
        query["Quota"] = {"$in": search_params["quotas"]}

    # Handle Rank Range filter
    if search_params.get("rankType"):
        rank_field = (
            "Opening Rank" if search_params["rankType"] == "opening" else "Closing Rank"
        )
        rank_query = {}

        if search_params.get("minRank"):
            rank_query["$gte"] = int(search_params["minRank"])
        if search_params.get("maxRank"):
            rank_query["$lte"] = int(search_params["maxRank"])

        if rank_query:
            query[rank_field] = rank_query

    # Add category filter for CSAB data
    if category == "csab":
        query["Category"] = "csab"

    # Perform the search
    results = list(collection.find(query, {"_id": 0}))

    # Sort results by Closing Rank
    results.sort(key=lambda x: x.get("Opening Rank", float("inf")))

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=10000, host="0.0.0.0")
