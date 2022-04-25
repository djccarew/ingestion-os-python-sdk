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

import os
import sys


import pytest
import osdu_api.providers.credentials
from osdu_api.providers.credentials import get_credentials
from osdu_api.providers.factory import ProvidersFactory
from osdu_api.providers.types import BaseCredentials
from osdu_api.providers.gcp.gcp_credentials import GCPCredentials
from osdu_api.providers.azure.azure_credentials import AzureCredentials

DATA_PATH_PREFIX = f"{os.path.dirname(__file__)}/data"


class TestGetCredentials:
    """Test a credential object can be obtained from providers."""
    @pytest.fixture()
    def mock_os_environ(self, monkeypatch, provider: str):
        """Mock os environ with a custom provider.
        """
        monkeypatch.setattr(
            os, "environ", {
                "CLOUD_PROVIDER": provider,
                "GOOGLE_APPLICATION_CREDENTIALS": f"{DATA_PATH_PREFIX}/fake_sa_file.json"
            })

    @pytest.mark.parametrize("provider, instance_type", [
        pytest.param("gcp", GCPCredentials),
        pytest.param("azure", AzureCredentials)
    ])
    def test_get_credentials_inferred_env(self, monkeypatch, mock_os_environ, provider: str,
                                          instance_type: BaseCredentials):
        """Test get credentials from inferred env.
        """
        assert isinstance(get_credentials(), instance_type)

    @pytest.mark.parametrize("provider, instance_type", [
        pytest.param("gcp", GCPCredentials),
        pytest.param("azure", AzureCredentials)
    ])
    def test_get_credentials_explicit_env(self, monkeypatch, mock_os_environ, provider: str,
                                          instance_type: BaseCredentials):
        """Test get credentials from explicit env.
        """
        assert isinstance(get_credentials(provider), instance_type)

    @pytest.mark.parametrize("provider", [
        pytest.param("other"),
        pytest.param(""),
    ])
    def test_get_credential_raises(self, provider: str):
        """Test factory will raise if given provider has no implementation.
        """
        with pytest.raises(NotImplementedError):
            get_credentials(provider)

    @pytest.mark.parametrize("provider", [
        pytest.param("gcp"),
        pytest.param("azure")
    ])
    def test_verify_registries(self, monkeypatch, mock_os_environ, provider: str):
        """Test import actually registered in factory
        """
        assert ProvidersFactory.credentials_registry.get(provider) is not None
