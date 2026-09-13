import os

from flask import Flask, request, jsonify, send_from_directory


app = Flask(__name__)


# ============================================================
# ROBOT IDS
# ============================================================
#
# The actual IDs are stored in Render Environment Variables.
#
# Example:
#
# ROBOT_IDS=#230714
#
# Multiple IDs:
#
# ROBOT_IDS=#230714,#123456,#987654
#
# ============================================================

VALID_ROBOT_IDS = {
    robot_id.strip().upper()
    for robot_id in os.getenv("ROBOT_IDS", "").split(",")
    if robot_id.strip()
}


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return send_from_directory(".", "index.html")


# ============================================================
# ROBOT PAGE
# ============================================================

@app.route("/web.html")
def robot_page():

    return send_from_directory(".", "web.html")


# ============================================================
# ROBOT ID VERIFICATION
# ============================================================

@app.route("/check-robot", methods=["POST"])
def check_robot():

    data = request.get_json(silent=True) or {}

    robot_id = str(
        data.get("robot_id", "")
    ).strip().upper()


    # No ID supplied
    if not robot_id:

        return jsonify({
            "valid": False,
            "message": "Robot ID is required."
        }), 400


    # Add # automatically
    if not robot_id.startswith("#"):

        robot_id = "#" + robot_id


    # Check against private server-side IDs
    if robot_id in VALID_ROBOT_IDS:

        return jsonify({
            "valid": True
        })


    # Invalid ID
    return jsonify({
        "valid": False,
        "message": "Robot ID not found."
    }), 401


# ============================================================
# STATIC FILES
# ============================================================

@app.route("/<path:path>")
def static_files(path):

    return send_from_directory(".", path)


# ============================================================
# LOCAL SERVER
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
