# openapi_client.DefaultApi

All URIs are relative to *https://clearinghouse.net/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**case_get**](DefaultApi.md#case_get) | **GET** /case | Get Case by ID
[**test_get**](DefaultApi.md#test_get) | **GET** /test | UMich Test Endpoint


# **case_get**
> List[Case] case_get(case_id)

Get Case by ID

### Example

* Api Key Authentication (ApiKey):

```python
import openapi_client
from openapi_client.models.case import Case
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://clearinghouse.net/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://clearinghouse.net/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    case_id = 56 # int | Numeric case ID

    try:
        # Get Case by ID
        api_response = api_instance.case_get(case_id)
        print("The response of DefaultApi->case_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->case_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **case_id** | **int**| Numeric case ID | 

### Return type

[**List[Case]**](Case.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Case successfull retrieved |  -  |
**400** | Bad Request No results, key not found, or invalid parameter. |  -  |
**401** | Authentication credentials were not provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_get**
> TestGet200Response test_get()

UMich Test Endpoint

### Example

* Api Key Authentication (ApiKey):

```python
import openapi_client
from openapi_client.models.test_get200_response import TestGet200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://clearinghouse.net/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://clearinghouse.net/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)

    try:
        # UMich Test Endpoint
        api_response = api_instance.test_get()
        print("The response of DefaultApi->test_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->test_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TestGet200Response**](TestGet200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Test, Authorization Token working |  -  |
**401** | Authentication credentials were not provided. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

