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
from osdu_api.model.legal.legal_tag import LegalTag
from osdu_api.model.legal.legal_tag_names import LegalTagNames
from osdu_api.model.legal.update_legal_tag import UpdateLegalTag


class LegalClient(BaseClient):
    """
    Holds the logic for interfacing with Legal's api
    """

    def get_legal_tag(self, legal_tag_name: str, bearer_token=None):
        return self.make_request(method=HttpMethod.GET, url='{}{}/{}'.format(self.legal_url, '/legaltags', legal_tag_name), bearer_token=bearer_token)

    def create_legal_tag(self, legal_tag: LegalTag, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.legal_url, '/legaltags'), 
            data=legal_tag.to_JSON(), bearer_token=bearer_token)
    
    def delete_legal_tag(self, legal_tag_name: str, bearer_token=None):
        return self.make_request(method=HttpMethod.DELETE, url='{}{}/{}'.format(self.legal_url, '/legaltags', legal_tag_name), bearer_token=bearer_token)
    
    def list_legal_tags(self, bearer_token=None):
        return self.make_request(method=HttpMethod.GET, url='{}{}'.format(self.legal_url, '/legaltags'), bearer_token=bearer_token)

    def update_legal_tag(self, update_legal_tag: UpdateLegalTag, bearer_token=None):
        return self.make_request(method=HttpMethod.PUT, url='{}{}'.format(self.legal_url, '/legaltags'), 
            data=update_legal_tag.to_JSON(), bearer_token=bearer_token)

    def get_legal_tags(self, legal_tag_names: LegalTagNames, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.legal_url, '/legaltags:batchRetrieve'), 
            data=legal_tag_names.to_JSON(), bearer_token=bearer_token)
    
    def validate_legal_tags(self, legal_tag_names: LegalTagNames, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.legal_url, '/legaltags:validate'), 
            data=legal_tag_names.to_JSON(), bearer_token=bearer_token)
    
    def get_legal_tag_properties(self, bearer_token=None):
        return self.make_request(method=HttpMethod.GET, url='{}{}'.format(self.legal_url, '/legaltags:properties'), bearer_token=bearer_token)
