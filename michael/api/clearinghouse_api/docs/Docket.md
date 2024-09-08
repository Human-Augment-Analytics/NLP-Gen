# Docket

A docket lists, in chronological order, every document filed with the court in a case; this also serves as a timeline of events. A docket also includes the judge(s), parties, and lawyers in a case. A docket number is the individual identifier that a court gives to a case. (Some courts use different terms, but the idea is the same.) Docket numbers usually include some or all of the following information, though it can appear in different orders or formats: - The year the case was filed - The type of case (civil, criminal, etc.) - A unique serial number for the case - Information on which courthouse or jurisdiction it was filed in We collect complete docket numbers as they appear on case documents. We also collect the information it contains (year, case type, etc.) in separate fields. Our system is designed around the federal courts' docketing conventions. The fields on our website correspond to the normal format for federal court docket number: 1:18-cv-528 (office:year-case type-filing number). 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | The ID of the docket. This is different from the case ID and unique to the docket. | [optional] 
**docket_number_manual** | **str** | The complete docket number, as it appears on case documents. | [optional] 
**docket_office_number** | **str** | For federal courts, the courthouse or division where the case was filed. This will always be a one-digit number. | [optional] 
**docket_year** | **int** | The year the case was filed. We collect complete years (e.g. 2021, not 21). | [optional] 
**docket_case_type** | **str** | Usually a 2-character code corresponding to a particular type of case (e.g. \&quot;cv\&quot; &#x3D; civil; \&quot;cr\&quot; &#x3D; criminal). Not all dockets will have a case type code. | [optional] 
**docket_filing_number** | **int** | The unique portion of a docket number. The filing number is generally unique within a given court. | [optional] 
**court** | **str** | The court where the docket exists. The options are the same as the court field for cases – see [court](https://api.clearinghouse.net/api-reference/objects/case/case-details#court). | [optional] 
**state** | **str** | The state where the docket&#39;s court is located in. | [optional] 
**is_main_docket** | **bool** | If true, the docket is the main docket for the case. This is typically the trial docket where the case was first filed. On the Clearinghouse site, the main docket is displayed first. | [optional] 
**recap_link** | **str** | A link to a federal court docket in the RECAP Archive. The [RECAP Archive](https://www.courtlistener.com/recap) is a free, searchable collection of millions of federal court documents and dockets. | [optional] 
**docket_entries** | [**List[DocketEntry]**](DocketEntry.md) | A list of docket entries. See [Docket Entry](https://api.clearinghouse.net/api-reference/objects/docket-entry). Note: Many dockets are available only as a PDF, rather than as a parsed array of docket entries. In those cases, the docket is saved as a document (see [Documents](https://api.clearinghouse.net/api-reference/objects/case/documents)).  | [optional] 
**scales_html** | **str** | A URL to an HTML file that is a saved version of the PACER HTML header. PACER, which stands for Public Access to Court Electronic Records, is the federal government&#39;s electronic system for providing access to federal court records. | [optional] 

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


