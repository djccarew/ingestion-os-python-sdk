#  Copyright 2021 Google LLC
#  Copyright 2021 EPAM Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import io
import os
import sys


import pytest
from pytest_mock import MockerFixture
from osdu_api.providers.exceptions import GCSObjectURIError
from osdu_api.providers.gcp.gcp_blob_storage_client import GoogleCloudStorageClient


class TestGoogleCloudStorageClient:
    """Test for GCP Blob Storage Client."""

    DATA_PATH_PREFIX = f"{os.path.dirname(__file__)}/data"
    GCP_STORAGE_CLIENT_CLASS_IMPORT = "osdu_api.providers.gcp.gcp_blob_storage_client.storage.Client"

    @pytest.fixture()
    def gcp_blob_storage_client(self, monkeypatch):
        """Build a fake client."""

        monkeypatch.setattr(
            os, "environ", {
                "CLOUD_PROVIDER": "gcp",
                "GOOGLE_APPLICATION_CREDENTIALS": f"{self.DATA_PATH_PREFIX}/fake_sa_file.json"
            })

        return GoogleCloudStorageClient()

    @pytest.fixture()
    def mock_file_exist_under_uri(self, monkeypatch, file_exists: bool):
        """
        Mock response from GCS if file exists or not.
        """
        monkeypatch.setattr(GoogleCloudStorageClient, "_does_file_exist_in_bucket",
                            lambda *args, **kwargs: file_exists)

    @pytest.mark.parametrize("file_path, file_exists",
                             [pytest.param("gs://test/test", True, id="Valid URI")])
    def test_does_file_exist_in_bucket(self, monkeypatch, mock_file_exist_under_uri,
                                       file_exists: bool,
                                       gcp_blob_storage_client: GoogleCloudStorageClient,
                                       file_path: str):
        """
        Test if file does really exist.
        """
        gcp_blob_storage_client.does_file_exist(file_path)

    @pytest.mark.parametrize("file_path, file_exists", [pytest.param("gs://test/test", False)])
    def test_file_does_not_exist_in_bucket(self, monkeypatch, mock_file_exist_under_uri,
                                           file_exists: bool,
                                           gcp_blob_storage_client: GoogleCloudStorageClient,
                                           file_path: str):
        """
        Test if file doesn't exist.
        """
        assert gcp_blob_storage_client.does_file_exist(file_path) == False

    @pytest.mark.parametrize("file_path", [
        pytest.param("gs://test"),
        pytest.param("://test"),
        pytest.param("test"),
    ])
    def test_invalid_gcs_object_uri(self, gcp_blob_storage_client: GoogleCloudStorageClient,
                                    file_path):
        with pytest.raises(GCSObjectURIError):
            gcp_blob_storage_client._parse_gcs_uri(file_path)

    @pytest.fixture()
    def mock_gcp_storage_objects(self, mocker: MockerFixture):
        """
        Mock gcp storage objects. Returns client, bucket and blob mocks.
        """
        blob_mock = mocker.Mock()
        client_mock = mocker.Mock()
        bucket_mock = mocker.Mock()
        bucket_mock.get_blob = mocker.Mock(return_value=blob_mock)
        bucket_mock.blob = mocker.Mock(return_value=blob_mock)
        client_mock.bucket = mocker.Mock(return_value=bucket_mock)

        return client_mock, bucket_mock, blob_mock

    def test_client_created_at_init(self, mocker: MockerFixture):
        """
        Test GCP Storage client is built on init.
        """
        client = mocker.patch(self.GCP_STORAGE_CLIENT_CLASS_IMPORT)
        GoogleCloudStorageClient()
        client.assert_called_with()

    @pytest.mark.parametrize("uri, bucket_name, blob_name", [
        pytest.param("gs://bucket_test/name_test", "bucket_test", "name_test"),
        pytest.param("gs://bucket_test_2/name_test_2", "bucket_test_2", "name_test_2"),
    ])
    def test_client_download_to_file(self, mocker: MockerFixture, mock_gcp_storage_objects, uri,
                                     bucket_name, blob_name):
        """
        Test GCP Storage client is properly called when downloading to a file.
        """
        client_mock, bucket_mock, blob_mock = mock_gcp_storage_objects

        mocker.patch(self.GCP_STORAGE_CLIENT_CLASS_IMPORT,
                     return_value=client_mock)
        test_client = GoogleCloudStorageClient()

        with io.BytesIO() as file:
            test_client.download_to_file(uri, file)
            client_mock.bucket.assert_called_with(bucket_name)
            bucket_mock.get_blob.assert_called_with(blob_name)
            blob_mock.download_to_file.assert_called_with(file)

    @pytest.mark.parametrize("uri, bucket_name, blob_name", [
        pytest.param("gs://bucket_test/name_test", "bucket_test", "name_test"),
        pytest.param("gs://bucket_test_2/name_test_2", "bucket_test_2", "name_test_2"),
    ])
    def test_client_download_file_as_bytes(self, mocker: MockerFixture, mock_gcp_storage_objects,
                                           uri, bucket_name, blob_name):
        """
        Test GCP Storage client is properly called when downloading a file as bytes.
        """
        client_mock, bucket_mock, blob_mock = mock_gcp_storage_objects
        mocker.patch(self.GCP_STORAGE_CLIENT_CLASS_IMPORT,
                     return_value=client_mock)
        test_client = GoogleCloudStorageClient()

        test_client.download_file_as_bytes(uri)

        client_mock.bucket.assert_called_with(bucket_name)
        bucket_mock.get_blob.assert_called_with(blob_name)
        blob_mock.download_as_bytes.assert_called_with()

    @pytest.mark.parametrize("uri, bucket_name, blob_name, content_type", [
        pytest.param("gs://bucket_test/name_test", "bucket_test", "name_test", "text/html"),
        pytest.param("gs://bucket_test_2/name_test_2", "bucket_test_2", "name_test_2",
                     "application/json"),
    ])
    def test_client_upload_file(self, mocker: MockerFixture, mock_gcp_storage_objects, uri,
                                bucket_name, blob_name, content_type):
        """
        Test GCP Storage client is properly called when uploading a file.
        """
        client_mock, bucket_mock, blob_mock = mock_gcp_storage_objects
        mocker.patch(self.GCP_STORAGE_CLIENT_CLASS_IMPORT,
                     return_value=client_mock)
        test_client = GoogleCloudStorageClient()

        with io.BytesIO() as file:
            test_client.upload_file(uri, file, content_type)

            client_mock.bucket.assert_called_with(bucket_name)
            bucket_mock.blob.assert_called_with(blob_name)
            blob_mock.upload_from_file.assert_called_with(file, content_type=content_type)

    @pytest.mark.parametrize("uri, bucket_name, blob_name", [
        pytest.param("gs://bucket_test/name_test", "bucket_test", "name_test"),
        pytest.param("gs://bucket_test_2/name_test_2", "bucket_test_2", "name_test_2"),
    ])
    def test_client_file_exist(self, mocker: MockerFixture, mock_gcp_storage_objects, uri,
                               bucket_name, blob_name):
        """
        Test GCP Storage client is properly called when checking a file exists.
        """
        client_mock, bucket_mock, blob_mock = mock_gcp_storage_objects
        mocker.patch(self.GCP_STORAGE_CLIENT_CLASS_IMPORT,
                     return_value=client_mock)
        test_client = GoogleCloudStorageClient()

        test_client.does_file_exist(uri)

        client_mock.bucket.assert_called_with(bucket_name)
        bucket_mock.blob.assert_called_with(blob_name)
        blob_mock.exists.assert_called_with()
