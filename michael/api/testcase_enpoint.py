import openapi_client
from openapi_client.models.case import Case
from openapi_client.rest import ApiException
from pprint import pprint
import os
from ocr import read_doc
# Defining the host is optional and defaults to https://clearinghouse.net/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://clearinghouse.net/api/v1",
    api_key = {"ApiKey": os.environ['CLEARINGHOUSE_API_TOKEN']},
    api_key_prefix = {"ApiKey": "Token"}
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    case_id = 13279 # int | Numeric case ID

    try:
        # Get Case by ID
        api_response = api_instance.case_get(case_id)
        print("The response of DefaultApi->case_get:\n")
        pprint(api_response[0].available_documents)
        for doc in api_response[0].case_documents:
            print('-' * 100)
            print(doc.document_type)
            print('-' * 100)
            print(read_doc(doc))
    except Exception as e:
        print("Exception when calling DefaultApi->case_get: %s\n" % e)