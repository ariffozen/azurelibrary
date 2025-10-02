from flask import Flask, request, jsonify, render_template
import requests
import base64
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def build_auth_header(personal_access_token: str) -> dict:
    """Generate the Azure DevOps basic auth header from the PAT."""
    encoded_token = base64.b64encode(f":{personal_access_token}".encode()).decode()
    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }


def flatten_json(json_obj, prefix=""):
    """Flatten nested JSON into key/value pairs compatible with Azure variable groups."""
    flattened = {}
    for key, value in json_obj.items():
        full_key = f"{prefix}{key}" if prefix else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, full_key + "."))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened.update(flatten_json(item, f"{full_key}.{i}."))
                else:
                    flattened[f"{full_key}.{i}"] = {"value": str(item), "isSecret": False}
        else:
            flattened[full_key] = {"value": str(value), "isSecret": False}
    return flattened


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/update-variable-group", methods=["POST"])
def update_variable_group():
    try:
        data = request.json or {}
        project_name = data.get("projectName")
        variable_group_name = data.get("variableGroupName")
        json_data = data.get("jsonData")
        azure_host = data.get("azureHost")
        azure_org = data.get("azureOrg")
        azure_pat = data.get("azurePat")

        if not project_name or not variable_group_name or not json_data:
            return jsonify({"error": "Azure Project, Variable Group adı veya JSON verisi eksik!"}), 400

        if not azure_host or not azure_org or not azure_pat:
            return jsonify({"error": "Azure host, organizasyonu veya PAT eksik!"}), 400

        variables = flatten_json(json_data)

        if not variables:
            return jsonify({"error": "JSON içeriği boş!"}), 400

        normalized_host = azure_host.rstrip("/")

        azure_url = (
            f"{normalized_host}/{azure_org}/"
            f"{project_name}/_apis/distributedtask/variablegroups?api-version=7.0-preview.1"
        )

        payload = {
            "name": variable_group_name,
            "type": "Vsts",
            "description": "Generated from appsettings.json",
            "variables": variables
        }

        print("Gönderilen JSON:", json.dumps(payload, indent=4))

        response = requests.post(azure_url, headers=build_auth_header(azure_pat), json=payload)

        if response.status_code in [200, 201]:
            return jsonify({"message": "Variable Group başarıyla oluşturuldu!", "response": response.json()}), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
