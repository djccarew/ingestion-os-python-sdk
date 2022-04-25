# OSDU Python SDK


## Contents

* [Introduction](#introduction)
* [Getting Started](#getting-started)
* * [Installation from source](#installation-from-source)
* * [Installation from Package Registry](#installation-from-package-registry)
* [Testing](#testing)
* * [Running E2E Tests](#running-e2e-tests)
* * [Running CSP Tests](#running-csp-tests)
* [Licence](#licence)


# Introduction
The Python SDK is a package to interface with OSDU microservices.

Interactions with OSDU services are cloud platform-agnostic by design. However, there are specific implementation requirements by cloud
platforms, and the OSDU R3 Prototype provides a dedicated Python SDK to make sure that interactions are independent from the
cloud platforms.

The Python SDK must be installed on the machine that uses OSDU services.

In OSDU R3 Prototype, the SDK encapsulates calls to the ODES Storage and Search services.


Also, in `osdu_api.providers` folder the SDK provides common interfaces for writing cloud-specific implementations for authorization and accessing
cloud storages. In this `osdu_api.providers` folder CSP code is stored.

# Getting Started

## Installation from source


1. Pull the latest Python SDK's changes from https://community.opengroup.org/osdu/platform/system/sdks/common-python-sdk

2. Use Python 3.6. Also, it is highly recommended using an isolated virtual environment for development purposes
  (Creation of virtual environments: https://docs.python.org/3.6/library/venv.html)

3.  Make sure you have setuptools and wheel installed
```sh
pip install --upgrade setuptools wheel
```

4.  Change directory to the root of PythonSDK project

```sh
cd path/to/python-sdk
```

5. Make sure osdu-api isn't already installed
```sh
pip uninstall osdu-api
````

6. Install Python SDK

```sh
python setup.py install
```

Example import after installing:
`from osdu_api.clients.storage.record_client import RecordClient`


## Installation from Package Registry

```sh
pip install 'osdu-api' --extra-index-url=https://community.opengroup.org/api/v4/projects/148/packages/pypi/simple
```

**Note**: If the SDK is installing on environment where the packages `requests` and `tenacity` are not installed then run:
```sh
pip install 'osdu-api[all]' --extra-index-url=https://community.opengroup.org/api/v4/projects/148/packages/pypi/simple
```


## Testing
### Running E2E Tests
Specify of end-services URLs into `tests/osdu_api.yaml` and run

```sh
pytest test
```

### Running CSP tests

```shell
    export CLOUD_PROVIDER=<cloud_provider>
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r ./osdu_api/test/providers-unit-tests/<cloud_provider>/requirements-test.txt
    pytest ./osdu_api/test/libs-unit-tests
```

## Licence
Copyright © Amazon Web Services
Copyright © Google LLC
Copyright © EPAM Systems

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
A package to interface with OSDU microservices

