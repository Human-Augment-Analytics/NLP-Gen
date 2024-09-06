import openapi_client
from openapi_client.models.test_get200_response import TestGet200Response
from openapi_client.rest import ApiException
from pprint import pprint
import os

# Defining the host is optional and defaults to https://www.clearinghouse.net/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://clearinghouse.net/api/v1",
    api_key = {"ApiKey": os.environ['CLEARINGHOUSE_API_TOKEN']},
    api_key_prefix = {"ApiKey": "Token"}
)


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

        
