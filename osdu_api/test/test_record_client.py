#  Copyright © 2020 Amazon Web Services
#  Copyright 2020 Google LLC
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
import types
import unittest
import os
import mock

from osdu_api.clients.base_client import BaseClient
from osdu_api.clients.storage.record_client import RecordClient
from osdu_api.model.http_method import HttpMethod
from osdu_api.model.storage.acl import Acl
from osdu_api.model.storage.legal import Legal
from osdu_api.model.storage.record import Record
from osdu_api.model.storage.record_ancestry import RecordAncestry
from osdu_api.configuration.config_manager import DefaultConfigManager


class TestRecordClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.test_record_dict = {
                    'acl': {
                        'owners':[
                            'data.test1@opendes.testing.com'
                        ],
                        'viewers':[
                            'data.test1@opendes.testing.com'
                        ]
                    },
                    'ancestry':{
                        'parents':[]
                    },
                    'data':{'id':'test'},
                    'id':'opendes:welldb:123456',
                    'kind':'opendes:welldb:wellbore:1.0.0',
                    'legal':{
                        'legaltags':['opendes-storage-1579034803194'],
                        'otherRelevantDataCountries':['US'],
                        'status':'compliant'
                    },
                    'meta':[
                        {}
                    ],
                    'version':0
                }

        self.test_record_str = """{
                    "acl": {
                        "owners":[
                            "data.test1@opendes.testing.com"
                        ],
                        "viewers":[
                            "data.test1@opendes.testing.com"
                        ]
                    },
                    "ancestry":{
                        "parents":[]
                    },
                    "data":{"id":"test"},
                    "id":"opendes:welldb:123456",
                    "kind":"opendes:welldb:wellbore:1.0.0",
                    "legal":{
                        "legaltags":["opendes-storage-1579034803194"],
                        "otherRelevantDataCountries":["US"],
                        "status":"compliant"
                    },
                    "meta":[
                        {}
                    ],
                    "version":0
                }"""

        acl = Acl(['data.test1@opendes.testing.com'], ['data.test1@opendes.testing.com'])
        legal = Legal(['opendes-storage-1579034803194'], ['US'], 'compliant')
        ancestry = RecordAncestry([])
        id = 'opendes:welldb:123456'
        kind = 'opendes:welldb:wellbore:1.0.0'
        meta = [{}]
        version = 0
        data = {'id': 'test'}
        self.test_record = Record(kind, acl, legal, data, id, version, ancestry, meta)
        

    @mock.patch.object(BaseClient, 'make_request', return_value="response")
    @mock.patch.object(BaseClient, '_refresh_service_principal_token', return_value="stubbed")
    def test_create_update_records_model_record(self, get_bearer_token_mock, make_request_mock):
        # Arrange
        record_client = RecordClient(DefaultConfigManager(os.getcwd() + '/osdu_api/test/osdu_api.ini'), "opendes")
        record_client.service_principal_token = 'stubbed'
        record_client.storage_url = 'stubbed url'
        record_client.headers = {}

        # Act
        response = record_client.create_update_records([self.test_record])

        # Assert
        assert response == make_request_mock.return_value

    @mock.patch.object(BaseClient, 'make_request', return_value="response")
    @mock.patch.object(BaseClient, '_refresh_service_principal_token', return_value="stubbed")
    def test_get_latest_record_version(self, get_bearer_token_mock, make_request_mock):
        # Arrange
        record_client = RecordClient(DefaultConfigManager(os.getcwd() + '/osdu_api/test/osdu_api.ini'), "opendes")
        record_client.service_principal_token = 'stubbed'
        record_client.storage_url = 'stubbed url'
        record_client.headers = {}
        record_id = 'test'
        request_params = {'attribute': []}

        # Act
        response = record_client.get_latest_record(record_id)

        # Assert
        make_request_mock.assert_called_with(method=HttpMethod.GET, params=request_params, url=record_client.storage_url + '/records/test', bearer_token=None)

    @mock.patch.object(BaseClient, 'make_request', return_value="response")
    @mock.patch.object(BaseClient, '_refresh_service_principal_token', return_value="stubbed")
    def test_get_specific_record_version(self, get_bearer_token_mock, make_request_mock):
        # Arrange
        record_client = RecordClient(DefaultConfigManager(os.getcwd() + '/osdu_api/test/osdu_api.ini'), "opendes")
        record_client.service_principal_token = 'stubbed'
        record_client.storage_url = 'stubbed url'
        record_client.headers = {}
        record_id = 'test'
        request_params = {'attribute': []}
        version = 123

        # Act
        response = record_client.get_specific_record(record_id, version)

        # Assert
        make_request_mock.assert_called_with(method=HttpMethod.GET, params=request_params, url=record_client.storage_url + '/records/test/123', bearer_token=None)

    @mock.patch.object(BaseClient, 'make_request', return_value="response")
    @mock.patch.object(BaseClient, '_refresh_service_principal_token', return_value="stubbed")
    def test_get_record_versions(self, get_bearer_token_mock, make_request_mock):
        # Arrange
        record_client = RecordClient(DefaultConfigManager(os.getcwd() + '/osdu_api/test/osdu_api.ini'), "opendes")
        record_client.service_principal_token = 'stubbed'
        record_client.storage_url = 'stubbed url'
        record_client.headers = {}
        record_id = 'test'
        request_params = {'attribute': []}

        # Act
        response = record_client.get_record_versions(record_id)

        # Assert
        make_request_mock.assert_called_with(method=HttpMethod.GET, url=record_client.storage_url + '/records/versions/test', bearer_token=None)
