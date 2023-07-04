from flask import Flask, jsonify, render_template, request
import redis
import json

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_events", methods=["GET"])
def get_events():
    events = r.lrange("off_limit_hours", 0, -1)
    events = [json.loads(event) for event in events]
    return jsonify(events)


@app.route("/add_off_limit_hours", methods=["POST"])
def add_off_limit_hours():
    data = request.get_json()
    time_range = json.dumps({"start": data["start"], "end": data["end"]})
    r.rpush("off_limit_hours", time_range)
    return jsonify(start=data["start"], end=data["end"])


@app.route("/delete_off_limit_hours", methods=["POST"])
def delete_off_limit_hours():
    data = request.get_json()
    time_range_to_delete = json.dumps({"start": data["start"], "end": data["end"]})

    time_ranges = r.lrange("off_limit_hours", 0, -1)
    for time_range in time_ranges:
        if time_range == time_range_to_delete:
            r.lrem("off_limit_hours", 1, time_range)
            break
    return jsonify(start=data["start"], end=data["end"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
