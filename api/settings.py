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
import os, sys, yaml

env = os.environ["ENV"]
loglevel = os.environ["LOGLEVEL"]
jira_log_api = os.environ["JIRA_LOG_API"]

db_host = os.environ["DB_HOST"]
db_instance = os.environ["DB_INSTANCE"]
db_database = os.environ["DB_DATABASE"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]

version_file = "./api/version.yaml"
if not os.path.exists(version_file):
    print("version.yaml not found!")
    sys.exit()

with open(version_file, "r") as f:
    version_data = yaml.load(f, Loader=yaml.FullLoader)
