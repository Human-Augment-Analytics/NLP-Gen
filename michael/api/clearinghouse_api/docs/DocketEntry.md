# DocketEntry

A docket lists, in chronological order, every document filed with the court in a case. Each document and its accompanying information is a \"docket entry.\" For more information about dockets, see [Docket](https://api.clearinghouse.net/api-reference/objects/docket). Dockets can be saved one of two ways in the Clearinghouse: (1) as parsed docket entries, or (2) as a PDF. This docket entry object is for parsed docket entries. For PDF dockets, the docket is saved as a document (see [Documents](https://api.clearinghouse.net/api-reference/objects/case/documents)). For federal docket entries from RECAP, some entries might be taken from PACER's RSS feed. These \"RSS\" entries have incomplete information. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**row_number** | **int** | The position of the docket entry within the docket, where the docket is a zero-indexed array of entries. | [optional] 
**entry_number** | **str** | For dockets that are numbered by the court, the number assigned to the docket entry. Unlike row_number, these numbers start with 1. In federal court, this is known as an \&quot;ECF number,\&quot; and every federal docket entry should have an ECF number. If the docket entry is part of a federal docket but entry_number is null, then the docket entry is likely an \&quot;RSS entry\&quot; (see above). For state courts, states vary as to whether they assign numbers to docket entries, so whether entry_number is null depends on the state.  | [optional] 
**date_filled** | **str** | The date of the docket entry, i.e. when the document was filed. This is in the format \&quot;YYYY-MM-DDTHH:MM:ssTZ\&quot;. | [optional] 
**description** | **str** | The text that describes the document in a docket entry. For RSS entries in federal dockets (see above), this will be an abbreviated version of the actual docket entry description (often just the type of document). | [optional] 
**attachments** | [**List[DocketEntryAttachmentsInner]**](DocketEntryAttachmentsInner.md) | Sometimes documents are attached to another document in PACER/RECAP. If so, the attached documents (\&quot;attachments\&quot;) are gathered in an array associated with a docket entry. Attachments have the following fields: ***recap_ip*** - The ID number given by RECAP. ***pacer_url*** - The URL to the document in PACER. ***description*** - A short description of the document. Unlike a docket entry&#39;s overall description, an attachment description tends to be very short. ***attachment_number*** - Starting from 1, position of the attachment among the attachments for the docket entry.  | [optional] 
**url** | **str** | A URL to a page that embeds the document. For federal cases, this is a link to a [CourtListener (RECAP)](https://www.courtlistener.com/) page. For state cases, this is a link to a [Docket Alarm](https://www.docketalarm.com/) page. For RSS entries in federal dockets (see above), this link is simply \&quot;https://www.courtlistener.com\&quot;. | [optional] 
**recap_pdf_url** | **str** | A URL to the document (i.e. the PDF itself). If there is no such URL available or if this an RSS entry in a federal docket (see above), this field is null. | [optional] 
**pacer_doc_id** | **str** | The ID of the document in PACER. PACER, which stands for Public Access to Court Electronic Records, is the federal government&#39;s electronic system for providing access to federal court records. For RSS entries in federal dockets (see above), this field is null.  | [optional] 
**id** | **int** | The ID of the docket entry in the Clearinghouse. | [optional] 

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


