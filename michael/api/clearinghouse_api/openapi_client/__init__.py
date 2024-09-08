# coding: utf-8

# flake8: noqa

"""
    Civil Rights Clearinghouse Simple API

    Python Client to Scrapte the University of Michigan Civil Rights Clearinghouse.  Basic installation: ```sh pip install git+https://github.com/calexander/law-data-design-vip.git ``` 

    The version of the OpenAPI document: 0.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "1.0.0"

# import apis into sdk package
from openapi_client.api.default_api import DefaultApi

# import ApiClient
from openapi_client.api_response import ApiResponse
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from openapi_client.exceptions import OpenApiException
from openapi_client.exceptions import ApiTypeError
from openapi_client.exceptions import ApiValueError
from openapi_client.exceptions import ApiKeyError
from openapi_client.exceptions import ApiAttributeError
from openapi_client.exceptions import ApiException

# import models into sdk package
from openapi_client.models.case import Case
from openapi_client.models.case_plaintiff_type_inner import CasePlaintiffTypeInner
from openapi_client.models.defendant import Defendant
from openapi_client.models.docket import Docket
from openapi_client.models.docket_entry import DocketEntry
from openapi_client.models.docket_entry_attachments_inner import DocketEntryAttachmentsInner
from openapi_client.models.document import Document
from openapi_client.models.resource import Resource
from openapi_client.models.test_get200_response import TestGet200Response
