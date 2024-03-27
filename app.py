# **********************************************************
# * CATEGORY  SOFTWARE
# * GROUP     FINANCE
# * AUTHOR    LANCE HAYNIE <LHAYNIE@SCCITY.ORG>
# **********************************************************
# Pelorus Past Due Balance API
# Copyright Santa Clara City
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os, sys
from dotenv import load_dotenv

load_dotenv()

from flask import jsonify
from flask_restful import Api
import api as a
from api.settings import env, version_data
from flask_swagger_ui import get_swaggerui_blueprint

app = a.api()
api = Api(app)

SWAGGER_URL = "/docs"
API_URL = "/static/swagger.yaml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": version_data["program"]}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.errorhandler(404)
def PageNotFound(e):
    return jsonify(error=str(e)), 404


@app.route("/", methods=["GET"])
def HttpRoot():
    return jsonify(
        application=version_data["program"],
        version=version_data["version"],
        environment=env,
        copyright=version_data["copyright"],
        author=version_data["author"],
    )


api.add_resource(a.Accounts, "/accounts")

if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000, threads=100)
