import os
import sys


import pytest
from osdu_api.providers.azure.azure_credentials import AzureCredentials
import msal
from azure import identity
from azure.keyvault import secrets

CLIENT_ID = "someClientId"
CLIENT_SECRET = "someClientSecret"
TENANT_ID = "someTenantId"
RESOURCE_ID = "someResourceId"
TOKEN = "someToken"
AUTHORITY_URI = 'https://login.microsoftonline.com/' + TENANT_ID
KEY_VAULT_URL = 'https://keyvault.com'
SCOPES = ["someResourceId/.default"]


class MockConfidentialClientApplication:
    def __init__(self, client_id: str, authority: str, client_credential: str):
        assert client_id == CLIENT_ID
        assert client_credential == CLIENT_SECRET
        assert authority == AUTHORITY_URI

    def acquire_token_for_client(self, scopes: list):
        assert scopes == SCOPES
        return {"access_token": TOKEN}


class MockDefaultAzureCredentials:
    def __init__(self):
        pass


class MockSecret:
    def __init__(self, value):
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class MockSecretClient:
    def __init__(self, vault_url: str, credential):
        assert vault_url == KEY_VAULT_URL
        assert isinstance(credential, MockDefaultAzureCredentials)

    def get_secret(self, key: str):
        if key == "app-dev-sp-username":
            return MockSecret(CLIENT_ID)
        elif key == "app-dev-sp-password":
            return MockSecret(CLIENT_SECRET)
        elif key == "app-dev-sp-tenant-id":
            return MockSecret(TENANT_ID)
        elif key == "aad-client-id":
            return MockSecret(RESOURCE_ID)
        else:
            raise ValueError("Invalid Key")


class TestAzureCredentials:
    @pytest.fixture()
    def azure_credentials(self, monkeypatch, mock_credentials: bool) -> AzureCredentials:
        azure_credentials = AzureCredentials()
        if mock_credentials:
            monkeypatch.setattr(azure_credentials, "_client_id", CLIENT_ID)
            monkeypatch.setattr(azure_credentials, "_client_secret", CLIENT_SECRET)
            monkeypatch.setattr(azure_credentials, "_tenant_id", TENANT_ID)
            monkeypatch.setattr(azure_credentials, "_resource_id", RESOURCE_ID)
        else:
            monkeypatch.setenv("AIRFLOW_VAR_KEYVAULT_URI", KEY_VAULT_URL)
            monkeypatch.setattr(identity,
                                "DefaultAzureCredential",
                                MockDefaultAzureCredentials)
            monkeypatch.setattr(secrets,
                                "SecretClient",
                                MockSecretClient)

        monkeypatch.setattr(msal,
                            "ConfidentialClientApplication",
                            MockConfidentialClientApplication)
        return azure_credentials

    @pytest.mark.parametrize("mock_credentials", [pytest.param(True)])
    def test_refresh_token_with_credential_information_available(
        self,
        azure_credentials: AzureCredentials,
        mock_credentials: bool):

        """
        Checks if token is fetched properly if credential information is already available.
        """
        assert azure_credentials.refresh_token() == TOKEN

    @pytest.mark.parametrize("mock_credentials", [pytest.param(False)])
    def test_refresh_token_with_credential_information_missing(
        self,
        azure_credentials: AzureCredentials,
        mock_credentials: bool):
        """
        Checks if credentials are fetched properly and then token is generated with fetched
        credentials.
        """
        assert azure_credentials.refresh_token() == TOKEN

