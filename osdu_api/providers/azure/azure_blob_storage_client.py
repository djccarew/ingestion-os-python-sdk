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
"""Blob storage Azure client module"""

import tenacity
from osdu_api.providers.constants import AZURE_CLOUD_PROVIDER
import logging
from osdu_api.providers.factory import ProvidersFactory
from osdu_api.providers.types import BlobStorageClient, FileLikeObject
from typing import Tuple

logger = logging.getLogger(__name__)

RETRY_SETTINGS = {
    "stop": tenacity.stop_after_attempt(3),
    "wait": tenacity.wait_fixed(10),
    "reraise": True,
}

@ProvidersFactory.register(AZURE_CLOUD_PROVIDER)
class AzureCloudStorageClient(BlobStorageClient):
    """Implementation of blob storage client for the Azure provider."""
    def __init__(self):
        """Initialize storage client."""
        pass

    def does_file_exist(self, uri: str) -> bool:
        """Verify if a file exists in the given URI.

        :param uri: The GCS URI of the file.
        :type uri: str
        :return: A boolean indicating if the file exists
        :rtype: bool
        """
        pass

    def download_to_file(self, uri: str, file: FileLikeObject) -> Tuple[FileLikeObject, str]:
        """Download file from the given URI.

        :param uri: The GCS URI of the file.
        :type uri: str
        :param file: The file where to download the blob content
        :type file: FileLikeObject
        :return: A tuple containing the file and its content-type
        :rtype: Tuple[io.BytesIO, str]
        """
        pass

    def download_file_as_bytes(self, uri: str) -> Tuple[bytes, str]:
        """Download file as bytes from the given URI.

        :param uri: The GCS URI of the file
        :type uri: str
        :return: The file as bytes and its content-type
        :rtype: Tuple[bytes, str]
        """
        pass

    def upload_file(self, uri: str, blob_file: FileLikeObject, content_type: str):
        """Upload a file to the given uri.

        :param uri: The GCS URI of the file
        :type uri: str
        :param blob: The file
        :type blob: FileLikeObject
        :param content_type: [description]
        :type content_type: str
        """
        pass
