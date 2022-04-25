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
from osdu_api.model.dataset.create_dataset_registries_request import CreateDatasetRegistriesRequest
from osdu_api.model.dataset.get_dataset_registry_request import GetDatasetRegistryRequest
from osdu_api.model.http_method import HttpMethod


class DatasetRegistryClient(BaseClient):
    """
    Holds the logic for interfacing with Data Registry Service's api
    """

    def register_dataset(self, dataset_registries: CreateDatasetRegistriesRequest, bearer_token=None):
        return self.make_request(method=HttpMethod.PUT, url='{}{}'.format(self.dataset_url, '/registerDataset'), 
            data=dataset_registries.to_JSON(), bearer_token=bearer_token)
    
    def get_dataset_registry(self, record_id: str, bearer_token=None):
        params = {'id': record_id}
        return self.make_request(method=HttpMethod.GET, url='{}{}'.format(self.dataset_url, '/getDatasetRegistry'), 
            params=params, bearer_token=bearer_token)
    
    def get_dataset_registries(self, get_dataset_registry_request: GetDatasetRegistryRequest, bearer_token=None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.dataset_url, '/getDatasetRegistry'), 
            data=get_dataset_registry_request.to_JSON(), bearer_token=bearer_token)
