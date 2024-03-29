#  Copyright 2020 Google LLC
#  Copyright © 2020 Amazon Web Services
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

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_version_from_file():
    with open("VERSION", "r") as fh:
        return fh.read().strip()

def prepare_version():
    version = os.getenv("BUILD_TAG", '')

    if version.startswith('v'):
        # release tag version, e.g. v0.9.0
        version = version[1:]
    else:
        # we assume that it is commit version
        # https://packaging.python.org/guides/distributing-packages-using-setuptools/#local-version-identifiers
        commit = os.environ["CI_COMMIT_SHORT_SHA"]
        build_id = os.environ["BUILD_ID"]
        version = f"{get_version_from_file()}.dev{build_id}+{commit}"

    return version

setuptools.setup(
    name="osdu_api",
    version=prepare_version(),
    author="OSDU team",
    description="A package to interface with OSDU microservices",
    packages=setuptools.find_packages(exclude=["*test*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "jsonschema==3.2.0",
        "pyyaml==5.4.1",
        "toposort==1.6",
        "dataclasses==0.8;python_version<'3.7'"
    ],
    extras_require={
        "all": ["requests==2.25.1", "tenacity==6.2.0"]
    },
    python_requires='>=3.6',
)
