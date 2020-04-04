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
        "discord": "651874915498328104",
        "expire": "2022-01-01 00:00 UTC",
        "plan": "Lifetime"
    },
  

}

OTP_STORE = {}

PLANS = ["Lifetime", "$60/6 months", "Plan 3"]

# API Key
#API_KEY = "uBhkCD2CY3ecdVbRLQadXFZ0y0FzaQ"
API_KEY = "uBhkCD2CY3ecdVbRLQadXFZ0y0FzaQ"


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
    if request.headers.get("Authorization") != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    data = request.json
    license = data["license"]
    discord = data["discord"]
    print(license)

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
    if request.headers.get("Authorization") != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    data = request.json
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



@app.route("/unlisted-keys", methods=["POST"])
def unlisted_keys_endpoint():
    """
    Return list of available license plan
     Input in JSON format :
    {
        "discord_id": <USER_DISCORD_ID>,
        "product_type": <PRODUCT_LICENSE_TYPE>,
    }

      
    
    {
        "Keys": [
            {
              "data": {
                "discord": "647663506153275409", 
                "expire": "2022-01-01 00:00 UTC", 
                "plan": "Lifetime", 
                "renewal": false
              }, 
              "key": "PRIVATE_LICENSE_KEY_7"
            }
        ]

    :return: 200 OK
    }
    

    :return 404 Not Found
    :return [401] Unauthorized (Invalid API Key)

    """
 	if request.headers.get("Authorization") != API_KEY:
 		return jsonify({"error": "Invalid API Key"}), 401



 	data = request.json
 	discord_id = data["discord_id"]
 	product_type = data["product_type"]


 	keys = []


 	for x in LICENSE_KEY_STORE:
 		if LICENSE_KEY_STORE[x]['discord'] == discord_id and LICENSE_KEY_STORE[x]['plan'] == product_type:
 			key = dict({'key': x, 'data': LICENSE_KEY_STORE[x]})
 			keys.append(key)


 	return jsonify({"Keys": keys}), 200

if __name__ == "__main__":
    app.run()
