# Copyright © 2020 Amazon Web Services
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from typing import List

from osdu_api.clients.base_client import BaseClient
from osdu_api.model.http_method import HttpMethod

#from osdu_api.model.storage.schema.schema import Schema
#from osdu_api.model.storage.schema.schema_attribute import SchemaAttribute

class SchemaClient(BaseClient):
    """
    Holds the logic for interfacing with Schema API
    """
    def get_schema_by_id(self, schema_id: str, bearer_token=None):
        return self.make_request(method=HttpMethod.GET, url = '{}/{}/{}'.format(self.schema_url, 'schema', schema_id), 
                data={}, bearer_token=bearer_token)

