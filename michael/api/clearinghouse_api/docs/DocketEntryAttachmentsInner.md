# DocketEntryAttachmentsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recap_id** | **int** |  | [optional] 
**pacer_url** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**attachment_number** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.docket_entry_attachments_inner import DocketEntryAttachmentsInner

# TODO update the JSON string below
json = "{}"
# create an instance of DocketEntryAttachmentsInner from a JSON string
docket_entry_attachments_inner_instance = DocketEntryAttachmentsInner.from_json(json)
# print the JSON string representation of the object
print(DocketEntryAttachmentsInner.to_json())

# convert the object into a dict
docket_entry_attachments_inner_dict = docket_entry_attachments_inner_instance.to_dict()
# create an instance of DocketEntryAttachmentsInner from a dict
docket_entry_attachments_inner_from_dict = DocketEntryAttachmentsInner.from_dict(docket_entry_attachments_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


