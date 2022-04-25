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
from osdu_api.model.storage.query_records_request import QueryRecordsRequest
from osdu_api.model.storage.record import Record


class RecordClient(BaseClient):
    """
    Holds the logic for interfacing with Storage's record api
    """

    def create_update_records(self, records: List[Record], bearer_token = None):
        """
        Calls storage's api endpoint createOrUpdateRecords taking a list of record objects and constructing
        the body of the request
        Returns the response object for the call

        Example of code to new up a record:
        acl = Acl(['data.test1@opendes.testing.com'], ['data.test1@opendes.testing.com'])
        legal = Legal(['opendes-storage-1579034803194'], ['US'], LegalCompliance.compliant)
        ancestry = RecordAncestry([])
        id = 'opendes:welldb:123456'
        kind = 'opendes:welldb:wellbore:1.0.0'
        meta = [{}]
        version = 0
        data = {'id': 'test'}
        record = Record(id, version, kind, acl, legal, data, ancestry, meta)
        """
        records_data = '['
        for record in records:
            records_data = '{}{}{}'.format(records_data, record.to_JSON(), ',')
        records_data = records_data[:-1]
        records_data = '{}{}'.format(records_data, ']')
        return self.make_request(method=HttpMethod.PUT, url='{}{}'.format(self.storage_url, '/records'), data=records_data, bearer_token=bearer_token)

    def get_latest_record(self, recordId: str, attributes: List[str] = [], bearer_token = None):
        """
        Calls storage's api endpoint getLatestRecordVersion taking the required attributes
        Returns the content for the response object
        """
        request_params = {'attribute': attributes}
        return self.make_request(method=HttpMethod.GET, params=request_params, url=('{}{}/{}'.format(self.storage_url, '/records', recordId)), bearer_token=bearer_token)

    def get_specific_record(self, recordId: str, version: str, attributes: List[str] = [], bearer_token = None):
        """
        Calls storage's api endpoint getSpecificRecordVersion taking the required attributes
        Returns the content for the response object
        """
        request_params = {'attribute': attributes}
        return self.make_request(method=HttpMethod.GET, params=request_params, url=('{}{}/{}/{}'.format(self.storage_url, '/records', recordId, version)), bearer_token=bearer_token)

    def get_record_versions(self, recordId: str, bearer_token = None):
        """
        Calls storage's api endpoint getRecordVersions taking the one required parameter record id
        Returns the content for the response object for the call containing the list of versions. 
        Find the versions in the response.content attribute
        """
        return self.make_request(method=HttpMethod.GET, url=('{}{}/{}'.format(self.storage_url, '/records/versions', recordId)), bearer_token=bearer_token)

    def delete_record(self, recordId: str, bearer_token = None):
        return self.make_request(method=HttpMethod.DELETE, url=('{}{}/{}'.format(self.storage_url, '/records', recordId)), bearer_token=bearer_token)
    
    def query_records(self, query_records_request: QueryRecordsRequest, bearer_token = None):
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.storage_url, '/query/records'), 
            data=query_records_request.to_JSON(), bearer_token=bearer_token)

    #ingest bulk records which is coming as JSON response -- Start
    def ingest_records(self, records, bearer_token = None):
        """
        Calls storage's api endpoint createOrUpdateRecords taking a list of record objects and constructing
        the body of the request
        Returns the response object for the call
        Example of code to new up a record:
        """
        return self.make_request(method=HttpMethod.POST, url='{}{}'.format(self.data_workflow_url, '/workflowRun'), data=records, bearer_token=bearer_token)

    def query_record(self, recordId: str, bearer_token = None):
        return self.make_request(method=HttpMethod.GET, url=('{}{}/{}'.format(self.storage_url, '/records', recordId)), bearer_token=bearer_token)
    
