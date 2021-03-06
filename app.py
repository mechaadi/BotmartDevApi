from flask import Flask, request, jsonify
from string import ascii_uppercase
from random import choice
from datetime import datetime
import json



# Mock Data Store
LICENSE_KEY_STORE = {
    "PRIVATE_LICENSE_KEY": {
        "renewal": True,
        "discord": "XXXXXXXXXXXXXXXXXXXXX",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "$60/6 months"
    },

    "PRIVATE_LICENSE_KEY2": {
        "renewal": False,
        "discord": "647663506153275409",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "Lifetime"
    },

     "PRIVATE_LICENSE_KEY3": {
        "renewal": False,
        "discord": "575104533936603176",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "Lifetime"
    },

     "PRIVATE_LICENSE_KEY21": {
        "renewal": False,
        "discord": "575104533936603176",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "Lifetime"
    },

     "PRIVATE_LICENSE_KEY22": {
        "renewal": False,
        "discord": "575104533936603176",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "Lifetime"
    },

     "PRIVATE_LICENSE_KEY23": {
        "renewal": False,
        "discord": "575104533936603176",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "Lifetime"
    }

}


OTP_STORE = {}

PLANS = ["Lifetime", "$60/6 months", "Plan 3"]


API_KEY = "PE35NdyLjDPaCgjuHRbM6VuvCRvHg2"
API_SECRET = "secretly_secret"


app = Flask(__name__)


@app.route('/verify', methods=['POST'])
def verify_endpoint():
    #print(license, request.headers.get("Authorization"))

    """
    Verify a given license, whether it's valid or not
    Input in JSON format :
    {
        "license": <LICENSE_STR>,
        "discord": <DISCORD_ID_STR>
    }
    :return: 200 OK
    {
        "require_renewal": <RENEWAL_BOOL>,
        "expire_datetime": <EXPIRE_yyyy-mm-dd hh:mm UTC>
    }
    :return 401 Unauthorized
    :return 404 Not Found
    """
    data = request.json
    if request.headers.get("Authorization") != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    if data["secret_key"] != API_SECRET:
        return jsonify({"error": "Invalid API SECRET KEY"}), 401

    license = data["license"]
    discord = data["discord"]

    # Check if the license exists or not, return 404 if not found
    if license not in LICENSE_KEY_STORE:
        return jsonify({
            "error": "Key not found"
        }), 404

    # License exists
    # Check if the specified discord is the same, return 404 if not
    if LICENSE_KEY_STORE[license]["discord"] != discord:
        return jsonify({
            "error": "Discord not found"
        }), 404

    # License exists & valid discord
    # Return json with 200 status code
    license_data = LICENSE_KEY_STORE[license]

    # if LICENSE_KEY_STORE[license]["renewal"] and LICENSE_KEY_STORE[license]["expire"]:
    return jsonify({
        "require_renewal": license_data["renewal"],
        "expire_datetime": license_data["expire"],
        "plan": license_data["plan"]
    }), 200


@app.route("/transfer", methods=["POST"])
def transfer_endpoint():
    """
    Transfer ownership of a given license by
    deactivating the old one and create a new one
    with the same expiry

    Input in JSON format :
    {
        "from_license": <FROM_LICENSE_STR>,
        "from_discord": <FROM_DISCORD_ID_STR>,
        "to_discord": <TO_DISCORD_ID_STR>
    }

    :return: 200 OK
    {
        "license": <NEW_LICENSE_STR>,
        "discord": <TO_DISCORD_ID_STR>
    }

    :return 404 Not Found
    """

    data = request.json

    if request.headers.get("Authorization") != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    if data["secret_key"] != API_SECRET:
        return jsonify({"error": "Invalid API SECRET KEY"}), 401

    
    license = data["from_license"]
    discord = data["from_discord"]
    to_discord = data["to_discord"]

    # Check if the license exists or not, return 404 if not found
    if license not in LICENSE_KEY_STORE:
        return jsonify({
            "error": "Key not found"
        }), 404

    # License exists
    # Check if the specified discord is the same, return 404 if not
    if LICENSE_KEY_STORE[license]["discord"] != discord:
        return jsonify({
            "error": "Discord not found"
        }), 404

    # Generate new license made up from random chars
    new_license = [choice(ascii_uppercase) for _ in range(10)]
    new_license = ''.join(new_license)

    # Copy the old license to new license
    LICENSE_KEY_STORE[new_license] = LICENSE_KEY_STORE[license]

    # Change to new discord
    LICENSE_KEY_STORE[new_license]["discord"] = to_discord

    # Delete the old license
    del LICENSE_KEY_STORE[license]

    return jsonify({
        "discord": LICENSE_KEY_STORE[new_license]["discord"],
        "license": new_license,
        "plan": LICENSE_KEY_STORE[new_license]["plan"]
    }), 200


@app.route("/plan", methods=["GET"])
def plan_endpoint():
    """
    Return list of available license plan

    Input: None

    :return: 200 OK
    {
        "plans" : ["plan1", "plan2", ...]
    }
    """
    return jsonify({"plans": PLANS})



if __name__ == "__main__":
    app.run(debug=True)
   #app.run(debug=True)
