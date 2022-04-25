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
from osdu_api.model.entitlements.group import Group
from osdu_api.model.entitlements.group_member import GroupMember
from osdu_api.model.http_method import HttpMethod


class EntitlementsClient(BaseClient):
    """
    Holds the logic for interfacing with Entitlement's api
    """

    def get_groups_for_user(self, bearer_token=None):
        return self.make_request(method=HttpMethod.GET, url='{}{}'.format(self.entitlements_url, '/groups'), bearer_token=bearer_token)
    
    def get_group_members(self, group_email: str, limit: int, role: str, bearer_token=None):
        params = {}
        params['limit'] = limit
        params['role'] = role
        return self.make_request(method=HttpMethod.GET, url='{}{}{}{}'.format(self.entitlements_url, '/groups/', group_email, '/members'), params=params, bearer_token=bearer_token)

    def delete_group_member(self, group_email: str, member_email: str, bearer_token=None):
        return self.make_request(method=HttpMethod.DELETE, url='{}{}{}{}{}'.format(self.entitlements_url, '/groups/', group_email, '/members/', member_email), bearer_token=bearer_token)

    def create_group(self, group: Group, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.entitlements_url, '/groups'), 
            data=group.to_JSON(), bearer_token=bearer_token)
    
    def create_group_member(self, group_email:str, group_member: GroupMember, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}{}{}'.format(self.entitlements_url, '/groups/', group_email, '/members'), 
            data=group_member.to_JSON(), bearer_token=bearer_token)
