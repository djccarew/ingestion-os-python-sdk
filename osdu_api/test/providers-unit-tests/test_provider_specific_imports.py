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
import importlib
import os
import sys


import pytest
from osdu_api.providers.credentials import _import_provider_specific_credential_module
from osdu_api.providers.blob_storage import _import_provider_specific_storage_client_module


DATA_PATH_PREFIX = f"{os.path.dirname(__file__)}/data"


class TestCloudSpecificImport:
    """Test providers modules can be import successfully."""
    @pytest.fixture()
    def mock_os_environ(self, monkeypatch, provider: str):
        """Mock os environ with a custom provider.
        """
        monkeypatch.setattr(
            os, "environ", {
                "CLOUD_PROVIDER": provider,
                "GOOGLE_APPLICATION_CREDENTIALS": f"{DATA_PATH_PREFIX}/fake_sa_file.json"
            })

    @pytest.mark.parametrize("provider, module_name", [
        pytest.param("gcp", "osdu_api.providers.gcp.gcp_credentials"),
        pytest.param("azure", "osdu_api.providers.azure.azure_credentials"),
        pytest.param("ibm", "osdu_api.providers.ibm.ibm_credentials"),
    ])
    def test_import_credentials_module(self, monkeypatch, mock_os_environ,
                                       provider: str, module_name: str):
        """Test import credential module.
        """
        assert _import_provider_specific_credential_module(provider) == module_name

    @pytest.mark.parametrize("provider", [
        pytest.param("other"),
    ])
    def test_import_credentials_module_raises(self, monkeypatch, mock_os_environ, provider: str):
        """Test import credential module raises error if module doesn't exist.
        """
        with pytest.raises(ModuleNotFoundError):
            _import_provider_specific_credential_module(provider)

    @pytest.mark.parametrize("provider, module_name", [
        pytest.param("gcp", "osdu_api.providers.gcp.gcp_blob_storage_client"),
        pytest.param("azure", "osdu_api.providers.azure.azure_blob_storage_client"),
        pytest.param("ibm", "osdu_api.providers.ibm.ibm_blob_storage_client"),
    ])
    def test_import_blob_storage_client_module(self, monkeypatch, mock_os_environ, provider: str, module_name: str):
        """Test import blob storage client module.
        """
        assert _import_provider_specific_storage_client_module(provider) == module_name

    @pytest.mark.parametrize("provider", [
        pytest.param("other"),
    ])
    def test_import_blob_storage_client_module_raises(self, monkeypatch, mock_os_environ, provider: str):
        """Test import blob storage client module raises error if module doesn't exist.
        """
        with pytest.raises(ModuleNotFoundError):
            _import_provider_specific_storage_client_module(provider)
