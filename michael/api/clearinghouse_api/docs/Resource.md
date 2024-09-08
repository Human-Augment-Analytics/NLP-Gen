# Resource


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | **str** | URL to the PDF file of the resource (if applicable). If the resource is a webpage, then | [optional] 
**title** | **str** | The title of the resource, usually as it appears in the resource itself. | [optional] 
**author_role** | **str** | Identifies whether a resources was created by a student or faculty member. Used only for pieces published in law reviews or other periodicals. The options are: ***N/A*** - Resource is not a law review article or periodical. ***Faculty*** - Written by a professor. ***Law Student*** - Written by a law student. ***Student*** - Written by a non-law student.  | [optional] 
**abstract** | **str** | A brief description of the resource. For law review pieces and other periodicals, we copy and paste the abstract into this field. For other kinds of resources we usually copy a representative paragraph or compose a quick description of the resource. | [optional] 
**author** | **str** | The full name of the author or authors, if they are individuals. | [optional] 
**institution** | **str** | The author of the resource, if it&#39;s an institutional author. The institutional affiliation of an author, if the author is an individual. | [optional] 
**citation** | **str** | The citation for a resource. Usually used for law review articles or other periodicals. | [optional] 
**external_url** | **str** | A link to the resource elsewhere on the web. | [optional] 
**display_date** | **str** | A written version of the date the resource was published or created. This field allows us to differentiate different issues of periodicals (e.g. \&quot;Fall 2021\&quot;, \&quot;May 1996\&quot;). | [optional] 
**resource_type** | **List[str]** | We collect a several kinds of resources, which are usually different kinds of things. ***Clearinghouse Links to External Resources*** - Links to other websites with information relevant to a case. For example, an ACLU webpage describing a case it litigated or an Oyez entry for a case heard by the Supreme Court. ***Articles about the Clearinghouse*** - Articles or webpages, including news coverage, about the Clearinghouse or describing Clearinghouse projects. ***Articles that use the Clearinghouse*** - Law review or other periodicals that cite entries in the Clearinghouse. ***Case Studies*** - A law review article, book, or other resource that discusses a case in the Clearinghouse. ***Clearinghouse Report*** - A white paper or report produced by the Clearinghouse. | [optional] 
**cases** | **List[str]** | The cases that are related to the resource. If the resource also has related case types, causes of action, issues, special collections, or attorney organizations, individual cases that all under those related items will not be part of cases. | [optional] 
**case_types** | **List[str]** | The case types that are related to the resource. For a full list of case types, see [case_types](https://api.clearinghouse.net/api-reference/objects/case/case-details#case_types). | [optional] 
**var_date** | **str** | The date a resource was created or published. The format of this string is \&quot;YYYY-MM-DDThh:mm:ssTZ\&quot;. The time zone (TZ) will be either -5:00 for Eastern Standard Time or -4:00 for Eastern Daylight Time. | [optional] 
**causes** | **List[str]** | The causes of action that are related to the resource. For a full list of causes of action, see [causes](https://api.clearinghouse.net/api-reference/objects/case/causes-of-action#causes). | [optional] 
**issues** | **List[str]** | The issues that are related to the resource. For a full list of issues, see [issues](https://api.clearinghouse.net/api-reference/objects/case/issues#issues). | [optional] 
**special_collections** | **List[str]** | The special collections that are related to the resource. For a full list of special collections, see [special_collections](https://api.clearinghouse.net/api-reference/objects/case/case-details#special_collections). | [optional] 
**attorney_orgs** | **List[str]** | The attorney organizations that are related to the resource. For a full list of attorney organizations, see [attorney_orgs](https://api.clearinghouse.net/api-reference/objects/case/parties#attorney_orgs). | [optional] 
**source** | **str** | For articles in law reviews or other periodicals, this field is the name of the publication. For websites, this field is the root of website. | [optional] 

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


