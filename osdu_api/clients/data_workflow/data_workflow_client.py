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
from osdu_api.model.data_workflow.start_workflow import StartWorkflow
from osdu_api.model.data_workflow.update_status_request import UpdateStatusRequest
from osdu_api.model.http_method import HttpMethod


class DataWorkflowClient(BaseClient):
    """
    Holds the logic for interfacing with Data Workflow's api
    """

    def start_workflow(self, start_workflow: StartWorkflow, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.data_workflow_url, '/startWorkflow'), 
            data=start_workflow.to_JSON(), bearer_token=bearer_token)
    
    def update_status(self, update_status_request: UpdateStatusRequest, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.data_workflow_url, '/updateStatus'), 
            data=update_status_request.to_JSON(), bearer_token=bearer_token)