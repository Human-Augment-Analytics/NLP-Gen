# Defendant


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**institution** | **str** |  | [optional] 
**institution_city** | **str** |  | [optional] 
**institution_county** | **str** |  | [optional] 
**institution_alt_state** | **str** |  | [optional] 
**defendant_level** | **str** |  | [optional] 
**defendant_level_other** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.defendant import Defendant

# TODO update the JSON string below
json = "{}"
# create an instance of Defendant from a JSON string
defendant_instance = Defendant.from_json(json)
# print the JSON string representation of the object
print(Defendant.to_json())

# convert the object into a dict
defendant_dict = defendant_instance.to_dict()
# create an instance of Defendant from a dict
defendant_from_dict = Defendant.from_dict(defendant_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


