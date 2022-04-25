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
import importlib
import os
from configparser import SafeConfigParser
import logging
import os
import requests

from osdu_api.configuration.base_config_manager import BaseConfigManager
from osdu_api.configuration.config_manager import DefaultConfigManager
from osdu_api.model.http_method import HttpMethod


class BaseClient:
    """
    Base client that is meant to be extended by service specific clients
    """

    def __init__(self, config_manager: BaseConfigManager = None, data_partition_id = None, logger = None):
        """
        Base client gets initialized with configuration values and a bearer token
        based on provider-specific logic
        """
        self._parse_config(config_manager, data_partition_id)
        self.unauth_retries = 0
        if self.use_service_principal:
            self._refresh_service_principal_token()
        
        self.logger = logger
        if self.logger is None:
            self.logger = logging.getLogger(__name__)

    def _parse_config(self, config_manager: BaseConfigManager = None, data_partition_id = None):
        """
        Parse config.

        :param config_manager: ConfigManager to get configs, defaults to None
        :type config_manager: BaseConfigManager, optional
        """
        self.config_manager = config_manager or DefaultConfigManager()

        self.provider = self.config_manager.get('provider', 'name')

        self.data_workflow_url = self.config_manager.get('environment', 'data_workflow_url')
        self.dataset_url = self.config_manager.get('environment', 'dataset_url')
        self.entitlements_url = self.config_manager.get('environment', 'entitlements_url')
        self.file_dms_url = self.config_manager.get('environment', 'file_dms_url')
        self.legal_url = self.config_manager.get('environment', 'legal_url')
        self.schema_url = self.config_manager.get('environment', 'schema_url')
        self.search_url = self.config_manager.get('environment', 'search_url')
        self.storage_url = self.config_manager.get('environment', 'storage_url')
        self.partition_url = self.config_manager.get('environment', 'partition_url')
        self.ingestion_workflow_url = self.config_manager.get('environment', 'ingestion_workflow_url')
        self.provider = self.config_manager.get('provider', 'name')

        self.use_service_principal = self.config_manager.getbool('environment', 'use_service_principal', False)
        if self.use_service_principal:
            self.service_principal_module_name = self.config_manager.get('provider', 'service_principal_module_name')

        if data_partition_id is None:
            self.data_partition_id = self.config_manager.get('environment', 'data_partition_id')
        else:
            self.data_partition_id = data_partition_id

    def _refresh_service_principal_token(self):
        """
        The path to the logic to get a valid bearer token is dynamically injected based on
        what provider and entitlements module name is provided in the configuration yaml
        """
        entitlements_client = importlib.import_module('osdu_api.providers.%s.%s' % (self.provider, self.service_principal_module_name))
        self.service_principal_token = entitlements_client.get_service_principal_token()

    def make_request(self, method: HttpMethod, url: str, data = '', add_headers = {}, params = {}, bearer_token = None):
        """
        Makes a request using python's built in requests library. Takes additional headers if
        necessary
        """
        if bearer_token is None:
            bearer_token = self.service_principal_token

        if bearer_token is not None and 'Bearer ' not in bearer_token:
            bearer_token = 'Bearer ' + bearer_token

        headers = {
            'content-type': 'application/json',
            'data-partition-id': self.data_partition_id,
            'Authorization': bearer_token
        }

        if (len(add_headers) > 0):
            for key, value in add_headers.items():
                headers[key] = value

        response = object

        if (method == HttpMethod.GET):
            response = requests.get(url=url, params=params, headers=headers, verify=False)
        elif (method == HttpMethod.DELETE):
            response = requests.delete(url=url, params=params, headers=headers, verify=False)
        elif (method == HttpMethod.POST):
            response = requests.post(url=url, params=params, data=data, headers=headers, verify=False)
        elif (method == HttpMethod.PUT):
            response = requests.put(url=url, params=params, data=data, headers=headers, verify=False)

        if (response.status_code == 401 or response.status_code == 403) and self.unauth_retries < 1:
            if self.use_service_principal == 'True' or self.use_service_principal == 'true':
                self.unauth_retries += 1
                self._refresh_service_principal_token()
                self.make_request(method, url, data, add_headers, params, None)

        self.unauth_retries = 0

        return response
