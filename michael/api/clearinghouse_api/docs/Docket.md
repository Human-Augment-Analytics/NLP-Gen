# Docket


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**docket_number_manual** | **str** |  | [optional] 
**docket_office_number** | **str** |  | [optional] 
**docket_year** | **int** |  | [optional] 
**docket_case_type** | **str** |  | [optional] 
**docket_filing_number** | **int** |  | [optional] 
**court** | **str** |  | [optional] 
**state** | **str** |  | [optional] 
**is_main_docket** | **bool** |  | [optional] 
**recap_link** | **str** |  | [optional] 
**docket_entries** | [**List[DocketEntry]**](DocketEntry.md) |  | [optional] 
**scales_html** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.docket import Docket

# TODO update the JSON string below
json = "{}"
# create an instance of Docket from a JSON string
docket_instance = Docket.from_json(json)
# print the JSON string representation of the object
print(Docket.to_json())

# convert the object into a dict
docket_dict = docket_instance.to_dict()
# create an instance of Docket from a dict
docket_from_dict = Docket.from_dict(docket_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


