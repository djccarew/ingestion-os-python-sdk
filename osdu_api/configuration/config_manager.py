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

import configparser
import os


from osdu_api.configuration.base_config_manager import BaseConfigManager

""" 
Default Config Manager to work with .ini files.
The .ini file's path can be:
1. passed directely to DefaultConfigManager,
2. obtained from OSDU_API_CONFIG_INI Env Var,

If both of this options are not provided, the file 'osdu_api.ini' will be taken from current working directory.
"""


class DefaultConfigManager(BaseConfigManager):
    """
    This configuration manager is used for getting different configurations for OSDU clients. 
    """

    def __init__(self, config_file_path: str = None):
        """
        Read the .ini config file by its path and parse it.

        :param config_file_path: Path to config .ini file; if it is not provided, then 'OSDU_API_CONFIG_INI' env var will be used, defaults to None
        :type config_file_path: str, optional
        """
        self._parser = self._read_config(config_file_path) 

    def _read_config(self, config_file_path: str = None) -> configparser.ConfigParser:
        """
        The .ini file's path can be:
        1. passed directely to DefaultConfigManager,
        2. obtained from OSDU_API_CONFIG_INI Env Var,
        If both of this options are not provided, the file will be taken from current working directory.

        Example config file:
        [environment]
        data_partition_id=opendes
        storage_url=https://[STORAGE_ENDPOINT]/api/storage/v2
        search_url=https://[SEARCH_ENDPOINT]/api/search/v2
        data_workflow_url=https://[WORKFLOW_ENDPOINT]/api/data-workflow/v1
        file_dms_url=https://[FILE_DMS_ENDPOINT]/api/filedms/v2
        dataset_registry_url=https://[DATASET_REGISTRY_URL]/api/dataset-registry/v1

        [provider]
        name=aws
        entitlements_module_name=entitlements_client

        :raises Exception: If the .ini file can't be opened.
        :return: ConfigParser with parsed configs.
        :rtype: configparser.ConfigParser
        """
        config_file_path = config_file_path or os.environ.get("OSDU_API_CONFIG_INI") or "osdu_api.ini"
        parser = configparser.ConfigParser(os.environ)
        config_read_results = parser.read(config_file_path)
        if not config_read_results:
            raise configparser.Error(f"Could not find the config file in '{config_file_path}'.")

        return parser

    def get(self, section: str, option: str, default: str = None) -> str:
        """       
         Get config value.

        :param section: Section of ini file.
        :type section: str
        :param option: Param of the section.
        :type option: str
        :param default: Default value, defaults to None.
        :type default: int, optional
        :return: Config value.
        :rtype: str
        """
        fallback = default if isinstance(default, str) else configparser._UNSET
        config_value = self._parser.get(section=section, option=option, fallback=fallback)
        return config_value

    def getint(self, section: str, option: str, default: str = None) -> int:
        """
        Get config value. as int

        :param section: Section of ini file.
        :type section: str
        :param option: Param of the section.
        :type option: str
        :param default: Default value, defaults to None
        :type default: int, optional
        :return: Config value.
        :rtype: int
        """
        fallback = default if isinstance(default, int) else configparser._UNSET
        config_value = self._parser.getint(section=section, option=option, fallback=fallback)
        return config_value

    def getfloat(self, section: str, option: str, default: str = None) -> int:
        """
        Get config value as float.

        :param section: Section of ini file.
        :type section: str
        :param option: Param of the section.
        :type option: str
        :param default: Default value, defaults to None
        :type default: float, optional
        :return: Config value.
        :rtype: float
        """
        fallback = default if isinstance(default, float) else configparser._UNSET
        config_value = self._parser.getfloat(section=section, option=option, fallback=fallback)
        return config_value

    def getbool(self, section: str, option: str, default: bool = None) -> bool:
        """
        Get config value as bool.

        :param section: Section of ini file.
        :type section: str
        :param option: Param of the section.
        :type option: str
        :param default: Default value, defaults to None
        :type default: bool, optional
        :return: Config value
        :rtype: bool
        """
        fallback = default if isinstance(default, bool) else configparser._UNSET
        config_value = self._parser.getboolean(section=section, option=option, fallback=fallback)
        return config_value
