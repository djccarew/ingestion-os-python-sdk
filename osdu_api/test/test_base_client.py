# Copyright © 2020 Amazon Web Services
# Copyright 2020 Google LLC
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
import unittest
import os
import mock
import responses

from osdu_api.clients.base_client import BaseClient
from osdu_api.model.http_method import HttpMethod
from osdu_api.configuration.config_manager import DefaultConfigManager

class TestBaseClient(unittest.TestCase):

    @mock.patch.object(BaseClient, '_refresh_service_principal_token', return_value="stubbed")
    def test_init(self, mocked_token_method):
        # Arrange

        # Act
        client = BaseClient(DefaultConfigManager(os.getcwd() + '/osdu_api/test/osdu_api.ini'), "opendes")

        # Assert
        mocked_token_method.assert_called()

    @responses.activate
    @mock.patch.object(BaseClient, '_refresh_service_principal_token', return_value="stubbed")
    def test_make_request(self, mocked_token_method):
        # Arrange
        client = BaseClient(DefaultConfigManager(os.getcwd() + '/osdu_api/test/osdu_api.ini'), "opendes")
        client.service_principal_token = 'stubbed'
        responses.add(responses.PUT, 'http://stubbed', json={'response': 'true'}, status=200)

        # Act
        response = client.make_request(method=HttpMethod.PUT, url='http://stubbed', data={})

        # Assert
        mocked_token_method.assert_called()
        assert response.content == b'{"response": "true"}'
