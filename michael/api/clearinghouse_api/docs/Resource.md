# Resource


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**author_role** | **str** |  | [optional] 
**abstract** | **str** |  | [optional] 
**author** | **str** |  | [optional] 
**institution** | **str** |  | [optional] 
**citation** | **str** |  | [optional] 
**external_url** | **str** |  | [optional] 
**display_date** | **str** |  | [optional] 
**resource_type** | **List[str]** |  | [optional] 
**cases** | **List[str]** |  | [optional] 
**case_types** | **List[str]** |  | [optional] 
**var_date** | **str** |  | [optional] 
**causes** | **List[str]** |  | [optional] 
**issues** | **List[str]** |  | [optional] 
**special_collections** | **List[str]** |  | [optional] 
**attorney_orgs** | **List[str]** |  | [optional] 
**source** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.resource import Resource

# TODO update the JSON string below
json = "{}"
# create an instance of Resource from a JSON string
resource_instance = Resource.from_json(json)
# print the JSON string representation of the object
print(Resource.to_json())

# convert the object into a dict
resource_dict = resource_instance.to_dict()
# create an instance of Resource from a dict
resource_from_dict = Resource.from_dict(resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


