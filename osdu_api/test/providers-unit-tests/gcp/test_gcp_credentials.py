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


import json
import os
import sys

import pytest
from google.oauth2 import service_account

from osdu_api.providers.gcp.gcp_credentials import GCPCredentials
from osdu_api.providers.exceptions import SAFilePathError

DATA_PATH_PREFIX = f"{os.path.dirname(__file__)}/data"


class MockCredentials:

    def __init__(self, access_token):
        self.access_token = access_token

    def refresh(self, *args, **kwargs):
        self.token = self.access_token


class TestGCPCredentials:

    @pytest.fixture()
    def gcp_credentials(self, monkeypatch, sa_file_path: str) -> GCPCredentials:
        """Build fake credentials."""

        monkeypatch.setattr(
            os, "environ", {
                "CLOUD_PROVIDER": "gcp",
                "GOOGLE_APPLICATION_CREDENTIALS": f"{DATA_PATH_PREFIX}/fake_sa_file.json",
                "SA_FILE_PATH": sa_file_path,
            })

        gcp_credentials = GCPCredentials()
        return gcp_credentials

    @pytest.fixture()
    def mock_sa_file_info(self, monkeypatch, gcp_credentials: GCPCredentials,
                          sa_file_path: str):
        """
        Return fake sa_file_info from fake path in environment.
        """
        monkeypatch.setattr(json, "load", lambda *args, **kwargs: "test")
        monkeypatch.setattr(os.path, "isfile", lambda *args, **kwargs: True)
        monkeypatch.setattr(gcp_credentials, "_get_sa_info_from_file",
                            lambda *args, **kwargs: "test")
        monkeypatch.setattr(gcp_credentials, "_get_sa_info_from_google_storage",
                            lambda *args, **kwargs: "test")

    @pytest.fixture()
    def mock_sa_credentials(self, monkeypatch, expected_token: str):
        """
        Return fake service account credentials having expected token.
        """
        monkeypatch.setattr(service_account.Credentials,
                            "from_service_account_info",
                            lambda *args, **kwargs: MockCredentials(expected_token))

    @pytest.mark.parametrize(
        "sa_file_path",
        [
            pytest.param(""),
            pytest.param(None)
        ]
    )
    def test_raise_sa_path_error_on_getting_absent_sa_file(self, monkeypatch,
                                                           gcp_credentials: GCPCredentials,
                                                           sa_file_path: str):
        """
        Check if error raises if sa file path is empty
        """
        with pytest.raises(SAFilePathError):
            gcp_credentials._get_sa_info()

    @pytest.mark.parametrize(
        "expected_token, sa_file_path",
        [
            pytest.param("test1", "/test", id="Local file"),
            pytest.param("test2", "gs://test/test", id="GCS")
        ]
    )
    def test_refresh_token_using_sa_file(
        self,
        monkeypatch,
        mock_sa_file_info,
        mock_sa_credentials,
        gcp_credentials: GCPCredentials,
        sa_file_path: str,
        expected_token: str,
    ):
        gcp_credentials.refresh_token()
        assert gcp_credentials.access_token == expected_token
