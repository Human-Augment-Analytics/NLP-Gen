# Case


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attorney_orgs** | **List[str]** |  | [optional] 
**available_documents** | **List[str]** |  | [optional] 
**case_defendants** | [**List[Defendant]**](Defendant.md) |  | [optional] 
**case_documents** | [**List[Document]**](Document.md) |  | [optional] 
**case_dockets** | [**List[Docket]**](Docket.md) |  | [optional] 
**case_resources** | [**List[Resource]**](Resource.md) |  | [optional] 
**case_ongoing** | **str** |  | [optional] 
**case_status** | **str** |  | [optional] 
**case_types** | **List[str]** |  | [optional] 
**cause_other** | **str** |  | [optional] 
**causes** | **List[str]** |  | [optional] 
**class_action_granted** | **str** |  | [optional] 
**class_action_sought** | **str** |  | [optional] 
**closing_year** | **int** |  | [optional] 
**court** | **str** |  | [optional] 
**custom_issues** | **List[str]** |  | [optional] 
**defendant_payment** | **str** |  | [optional] 
**docket_status** | **str** |  | [optional] 
**filing_date** | **str** |  | [optional] 
**filing_year** | **int** |  | [optional] 
**id** | **int** |  | [optional] 
**injuction_duration** | **int** |  | [optional] 
**issues** | **List[str]** |  | [optional] 
**last_checked_date** | **str** |  | [optional] 
**main_docket** | [**Docket**](Docket.md) |  | [optional] 
**name** | **str** |  | [optional] 
**never_filed** | **bool** |  | [optional] 
**non_docket_case_number** | **str** |  | [optional] 
**non_docket_case_number_type** | **str** |  | [optional] 
**non_docket_case_number_type_other** | **str** |  | [optional] 
**order_end_year** | **int** |  | [optional] 
**order_start_year** | **int** |  | [optional] 
**permanent_injuction** | **bool** |  | [optional] 
**plaintiff_description** | **str** |  | [optional] 
**prevailing_party** | **str** |  | [optional] 
**pro_se_status** | **str** |  | [optional] 
**public_interest_lawyer** | **str** |  | [optional] 
**relief_natures** | **List[str]** |  | [optional] 
**relief_nature_other** | **str** |  | [optional] 
**relief_sources** | **List[str]** |  | [optional] 
**settlement_agreement** | **List[str]** |  | [optional] 
**settlement_judgment_date** | **str** |  | [optional] 
**settlement_judgment_year** | **int** |  | [optional] 
**special_collections** | **List[str]** |  | [optional] 
**state** | **str** |  | [optional] 
**summary** | **str** |  | [optional] 
**summary_published_date** | **str** |  | [optional] 
**summary_short** | **str** |  | [optional] 
**summary_tiny** | **str** |  | [optional] 
**terminating_date** | **str** |  | [optional] 
**clearinghouse_link** | **str** |  | [optional] 
**is_action** | **bool** |  | [optional] 
**plaintiff_type** | [**List[CasePlaintiffTypeInner]**](CasePlaintiffTypeInner.md) |  | [optional] 
**defendant_type** | [**List[CasePlaintiffTypeInner]**](CasePlaintiffTypeInner.md) |  | [optional] 
**facility_type** | [**List[CasePlaintiffTypeInner]**](CasePlaintiffTypeInner.md) |  | [optional] 
**constitutional_clause** | [**List[CasePlaintiffTypeInner]**](CasePlaintiffTypeInner.md) |  | [optional] 
**special_case_type** | [**List[CasePlaintiffTypeInner]**](CasePlaintiffTypeInner.md) |  | [optional] 
**content_of_injunction** | [**List[CasePlaintiffTypeInner]**](CasePlaintiffTypeInner.md) |  | [optional] 

## Example

```python
from openapi_client.models.case import Case

# TODO update the JSON string below
json = "{}"
# create an instance of Case from a JSON string
case_instance = Case.from_json(json)
# print the JSON string representation of the object
print(Case.to_json())

# convert the object into a dict
case_dict = case_instance.to_dict()
# create an instance of Case from a dict
case_from_dict = Case.from_dict(case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


