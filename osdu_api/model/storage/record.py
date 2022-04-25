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
from osdu_api.model.base import Base
from osdu_api.model.storage.acl import Acl
from osdu_api.model.storage.legal import Legal
from osdu_api.model.storage.record_ancestry import RecordAncestry


class Record(Base):
    """
    A record model mirroring what's found in core common
    """

    def __init__(self, kind: str, acl: Acl, legal: Legal, data: dict, id: str = None, version: int = None, ancestry: RecordAncestry = None,
            meta: dict = None):
        self.id = id
        self.version = version
        self.kind = kind
        self.acl = acl
        self.legal = legal
        self.data = data
        self.ancestry = ancestry
        self.meta = meta
