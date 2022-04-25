# Copyright © 2021 Amazon Web Services
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
from osdu_api.model.base import Base


class GetWorkflowSchedulesRequest(Base):
    """
    Request body to data workflow's start workflow endpoint. Input parameters is a dynamic object
    but the API expects "datasetRegistryIds"
    """
    def __init__(self, schedule_names: list):
        self.scheduleNames = schedule_names
