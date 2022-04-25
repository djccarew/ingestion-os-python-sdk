#  Copyright © Microsoft Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Azure Credential Module."""

import logging
from osdu_api.providers.constants import AZURE_CLOUD_PROVIDER
from osdu_api.providers.factory import ProvidersFactory
from osdu_api.providers.types import BaseCredentials
from tenacity import retry, stop_after_attempt
import msal
import os
from azure.keyvault import secrets
from azure import identity
import requests
import json


logger = logging.getLogger(__name__)
RETRIES = 3

@ProvidersFactory.register(AZURE_CLOUD_PROVIDER)
class AzureCredentials(BaseCredentials):
    """Azure Credential Provider"""

    def __init__(self):
        """Initialize Azure Credentials object"""
        self._access_token = None
        self._client_id = None
        self._client_secret = None
        self._tenant_id = None
        self._resource_id = None
        self._azure_paas_podidentity_isEnabled= os.getenv("AIRFLOW_VAR_AZURE_ENABLE_MSI")

    def _populate_ad_credentials(self) -> None:
        uri = os.getenv("AIRFLOW_VAR_KEYVAULT_URI")
        credential = identity.DefaultAzureCredential()
        client = secrets.SecretClient(vault_url=uri, credential=credential)
        self._client_id = client.get_secret("app-dev-sp-username").value
        self._client_secret = client.get_secret('app-dev-sp-password').value
        self._tenant_id = client.get_secret('app-dev-sp-tenant-id').value
        self._resource_id = client.get_secret("aad-client-id").value

    def _generate_token(self) -> str:
        if self._azure_paas_podidentity_isEnabled == "true":
            try:
                print("MSI Token generation")
                headers = {
                    'Metadata': 'true'
                }
                url = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com%2F'
                response = requests.request("GET", url, headers=headers)
                data_msi = json.loads(response.text)
                token = data_msi["access_token"]
                return token
            except Exception as e:
                logger.error(e)
                raise e
        else:
            if self._client_id is None:
                self._populate_ad_credentials()
            if self._tenant_id is None:
                logger.error('TenantId is not set properly')
                raise ValueError("TenantId is not set properly")
            if self._resource_id is None:
                logger.error('ResourceId is not set properly')
                raise ValueError("ResourceId is not set properly")
            if self._client_id is None:
                logger.error('Please pass client Id to generate token')
                raise ValueError("Please pass client Id to generate token")
            if self._client_secret is None:
                logger.error('Please pass client secret to generate token')
                raise ValueError("Please pass client secret to generate token")

            try:
                authority_host_uri = 'https://login.microsoftonline.com'
                authority_uri = authority_host_uri + '/' + self._tenant_id
                scopes = [self._resource_id + '/.default']
                app = msal.ConfidentialClientApplication(client_id = self._client_id,
                                                         authority = authority_uri,
                                                         client_credential = self._client_secret)
                result = app.acquire_token_for_client(scopes=scopes)
                return result.get('access_token')
            except Exception as e:
                logger.error(e)
                raise e

    @retry(stop=stop_after_attempt(RETRIES))
    def refresh_token(self) -> str:
        """Refresh token.

        :return: Refreshed token
        :rtype: str
        """
        token = self._generate_token()
        self._access_token = token
        return self._access_token

    @property
    def access_token(self) -> str:
        """The access token.

        :return: Access token string.
        :rtype: str
        """
        return self._access_token

