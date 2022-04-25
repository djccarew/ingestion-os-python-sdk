# Copyright © 2020 Amazon Web Services
# Copyright 2020 Google LLC
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

import configparser
import os
import shutil


import pytest
from osdu_api.configuration.config_manager import DefaultConfigManager

class TestDefaultConfigManager:
    """Test DefaultConfigManager."""

    @pytest.fixture
    def default_config_file(self):
        cwd = os.getcwd()
        config_file = f"{os.path.dirname(__file__)}/fake_config/osdu_api/test/osdu_api.ini"
        path = shutil.copy(config_file, cwd)
        yield path
        os.remove(path)

    def test_config_manager_with_default_file(self, default_config_file):
        a = os.getcwd()
        DefaultConfigManager()

    def test_configmanager_with_env_var(self):
        config_file = f"{os.path.dirname(__file__)}/fake_config/osdu_api/test/osdu_api.ini"
        os.environ["OSDU_API_CONFIG_INI"] = config_file
        DefaultConfigManager()

    def test_configmanager_with_passed_directly(self):
        config_file = f"{os.path.dirname(__file__)}/fake_config/osdu_api/test/osdu_api.ini"
        DefaultConfigManager(config_file)

    def test_raise_error_if_no_file(self):
        with pytest.raises(configparser.Error):
            DefaultConfigManager()
