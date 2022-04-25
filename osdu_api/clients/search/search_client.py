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
from osdu_api.model.search.query_request import QueryRequest
from osdu_api.model.search.query_response import QueryResponse


class SearchClient(BaseClient):
    """
    Holds the logic for interfacing with Search's query api
    """

    def query_records(self, query_request: QueryRequest, bearer_token = None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.search_url, '/query'), 
            data=query_request.to_JSON(), bearer_token=bearer_token)

    def query_with_cursor(self, query_request: QueryRequest, bearer_token = None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.search_url, '/query_with_cursor'), 
            data=query_request.to_JSON(), bearer_token=bearer_token)
