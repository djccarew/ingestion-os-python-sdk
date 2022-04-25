# Copyright © 2020 Amazon Web Services
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
from typing import List

from osdu_api.model.base import Base


class LegalTagProperties(Base):
    def __init__(self, country_of_origin: List[str], contract_id: str, expiration_date: int, originator: str, 
        data_type: str, security_classification: str, personal_data: str, export_classification: str):
        self.countryOfOrigin = country_of_origin
        self.contractId = contract_id
        self.expirationDate = expiration_date
        self.originator = originator
        self.dataType = data_type
        self.securityClassification = security_classification
        self.personalData = personal_data
        self.exportClassification = export_classification