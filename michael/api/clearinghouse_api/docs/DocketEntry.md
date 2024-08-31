# DocketEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**row_number** | **int** |  | [optional] 
**entry_number** | **str** |  | [optional] 
**date_filled** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**attachments** | [**List[DocketEntryAttachmentsInner]**](DocketEntryAttachmentsInner.md) |  | [optional] 
**url** | **str** |  | [optional] 
**recap_pdf_url** | **str** |  | [optional] 
**pacer_doc_id** | **str** |  | [optional] 
**id** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.docket_entry import DocketEntry

# TODO update the JSON string below
json = "{}"
# create an instance of DocketEntry from a JSON string
docket_entry_instance = DocketEntry.from_json(json)
# print the JSON string representation of the object
print(DocketEntry.to_json())

# convert the object into a dict
docket_entry_dict = docket_entry_instance.to_dict()
# create an instance of DocketEntry from a dict
docket_entry_from_dict = DocketEntry.from_dict(docket_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


