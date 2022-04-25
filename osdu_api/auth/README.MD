## Authorization

### Introduction

The Python SDK's client classes or user-defined functions are made for invoking other OSDU services by sending HTTP requests to them. 
Such invoking other OSDU services requires authorization mechanisms. Also, it is understandable that each vendor or, for the instance, 
cloud provider has different authorization process. Thus, vendors or cloud providers need a possibility to implement different authorization strategies (e.g., generating a new access token on different cloud platforms).


### Authorization Decorator and Refresh Token Interface

This decorator is used for wrapping functions and method sending requests to the OSDU Services:

```
@osdu_api.libs.auth.authorization.authorize(
    token_refresher: TokenRefresher = None
)
``` 

The decorator updates the headers of requests with the `Authorization` field. If a response has the status 401 or 403, the decorator attempts to reauthorize and send request again with a new `Authorization` header.

The decorator can take a vendor-defined TokenRefresher object as a strategy for refreshing tokens.


If a user-defined strategy was not passed directly into the decorator, and if the decorator wraps any object's method, the decorator will attempt to use the object's attribute `token_refresher` as the authorization strategy.

The decorator expects a function or method to have the first parameter of the type **dict** (_headers_) and return a value of the type **requests.Response**. 

1. The decorator updates the first argument, which is supposed to be request headers, of a function/method with `{"Authorization": token_refresher.access_token}`, and calls this request function/method with updated headers. 
   
2. The decorator verifies if a return value is the type of `requests.Response` and the response status is OK. 
   
3. If the response status is **401** or **403**, the method `token_refresher.authorize()`, which updates the `attribute _token_refresher.access_token` with the new value, is called, and once again the request function/method is called with th headers updated with new "Authorization" value.

Each cloud provider/vendor has a different flow of how authorization tokens are generated. That is why the decorator must use different **strategies** of authorization for each concrete case.

The decorator uses an object of a user-defined implementation of the abstract class `TokenRefresher` as the 
**strategy** for refreshing the access token. 

```
classosdu_ingestion.libs.auth.authorization.TokenRefresher()
```


Methods and attributes of `TokenRefresher`

- `authorize`. This method is called immediately after response of the current request has been 401 or 403. This method
calls `refresh_token` method, get new access token and assign it to `_access_token` attribute.
  
- `access_token`. This is a property that returns `_access_token` attribute.

- `authorization_header`. This property returns authorization header with which request's headers updated (e.g. `{"Authorization": "Bearer: ..."}`).

The following abstract method of the abstract class `TokenRefresher` must be implemented for any vendor-specific strategy:

- `refresh_token()`. This method must generate a new access token and return its string value. This method is called when the last response of request was 401 or 403 (Authorization errors).


#### Example

```python
import requests
from osdu_ingestion.libs.auth.authorization import authorize, TokenRefresher


class VendorRefreshTokenStrategy(TokenRefresher):
    """
    An example of a class doing some OSDU actions.
    """
    
    ...

    def refresh_token(self) -> str:
        """
        This is an example of implementing the 'refresh_token' abstract method.
        Define your own refreshing the access token strategy.
        """
        new_access_token = ... #  some actions of authorization and getting new access token as a string.
        ...
        return new_access_token


vendor_refresh_token_strategy = VendorRefreshTokenStrategy()


#  use the 'authorize' decorator to wrap a request function.
@authorize(vendor_refresh_token_strategy)
def send_any_requests(headers: dict, *args, **kwargs) -> requests.Response:
    response = ...  # some request to OSDU services
    return response


#  use the 'authorize' to wrap a request method
class SomeOSDUStaff(object):

    def __init__(self, token_refresher: TokenRefresher):
        self.token_refresher = token_refresher  # this attribute will be
        # used inside the 'authorize' decorator

    @authorize()
    def send_request(self, headers: dict) -> requests.Response:
        response = ...  # send some request to the OSDU
        return response


some_osdu_staff = SomeOSDUStaff(token_refresher=vendor_refresh_token_strategy)
```

## Licence


Copyright © Google LLC

Copyright © EPAM Systems

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.