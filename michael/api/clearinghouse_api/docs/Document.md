# Document


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** |  | [optional] 
**date_is_estimate** | **bool** |  | [optional] 
**date_not_available** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 
**document_source** | **str** |  | [optional] 
**document_type** | **str** |  | [optional] 
**order_type** | **str** |  | [optional] 
**citation_paren** | **str** |  | [optional] 
**cite_1_page** | **int** |  | [optional] 
**cite_1_reporter** | **str** |  | [optional] 
**cite_1_vol** | **int** |  | [optional] 
**cite_2_page** | **int** |  | [optional] 
**cite_2_reporter** | **str** |  | [optional] 
**cite_2_vol** | **int** |  | [optional] 
**cite_3_page** | **int** |  | [optional] 
**cite_3_reporter** | **str** |  | [optional] 
**cite_3_vol** | **int** |  | [optional] 
**citation_status** | **str** |  | [optional] 
**court** | **str** |  | [optional] 
**no_title** | **bool** |  | [optional] 
**party_types** | **List[str]** |  | [optional] 
**per_curium** | **bool** |  | [optional] 
**is_core_document** | **bool** |  | [optional] 
**file** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**public_note** | **str** |  | [optional] 
**document_type_other** | **str** |  | [optional] 
**external_url** | **str** |  | [optional] 
**ecf_number** | **str** |  | [optional] 
**clearinghouse_link** | **str** |  | [optional] 
**id** | **int** |  | [optional] 
**document_status** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.document import Document

# TODO update the JSON string below
json = "{}"
# create an instance of Document from a JSON string
document_instance = Document.from_json(json)
# print the JSON string representation of the object
print(Document.to_json())

# convert the object into a dict
document_dict = document_instance.to_dict()
# create an instance of Document from a dict
document_from_dict = Document.from_dict(document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


