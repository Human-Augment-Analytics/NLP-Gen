# Defendant

When adding entries for defendants, we record only the \"real party in interest\" – that is, who is really being sued. This may be different from the names listed on a complaint, as sometimes a suit will be filed naming an individual who represents or works for a government agency, but it’s the agency that defends the lawsuit, obeys the injunction, and pays the damages. For example, if a plaintiff sues a state, the state's governor, and the state's attorney general, we usually would record only the state as a defendant.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the \&quot;real party in interest\&quot; – typically the institution being sued or the institution represented by the individuals being sued. Sometimes, this might also be the title of a position that a person holds. In very rare cases, name will refer to an actual person. | [optional] 
**institution** | **str** | The institution or agency that took the action that formed the basis of the lawsuit. If this is the same as name, then institution should be an empty string. | [optional] 
**institution_city** | **str** | The city of the defendant&#39;s location. This is not where the challenged action(s) took place. If the defendant is a state or federal entity (i.e. applies to the whole state or country), then institution_city is an empty string. | [optional] 
**institution_county** | **str** | The county of the defendant&#39;s location. This is not where the challenged action(s) took place. The choices for this field are limited to the counties in the case&#39;s state. If the defendant is a state or federal entity (i.e. applies to the whole state or country), then institution_county is null.  | [optional] 
**institution_alt_state** | **str** | The state of the defendant&#39;s location if the state is different from the case&#39;s state (see [state](https://api.clearinghouse.net/api-reference/objects/case/case-details#state)). If the defendant&#39;s state is the same as the case&#39;s state is null. If the defendant is a federal entity, then institution_alt_state is \&quot;- United States (national) -\&quot;. Similarly, if the defendant is an international entity, then institution_alt_state is \&quot;- International -\&quot;. For a full list of possible states, see [state](https://api.clearinghouse.net/api-reference/objects/case/case-details#state).  | [optional] 
**defendant_level** | **str** | The type or category of the defendant in terms of what the defendant governs. ***null*** - The defendant&#39;s level does not fit within one of the Clearinghouse&#39;s predefined choices. See [defendant_level_other-not-in-api-yet](https://api.clearinghouse.net/api-reference/objects/defendant#defendant_level_other-not-in-api-yet). ***City*** - A city or city-level entity. ***County*** - A county or county-level entity. ***Federal*** - A country or federal entity. ***Non-profit or advocacy*** - A nonprofit or advocacy organization that is not a governmental body. ***Political Party*** - A political party. ***Private Entity/Person*** - A private entity or individual person. ***Regional*** - An entity associated with a region that is not a city, county, state, or country. ***School District*** - A public school district. ***State*** - A state or state entity. ***Tribe*** - An indigenous tribe. ***Union*** - A labor union. Note: This is different from [the \&quot;Defendant-type\&quot; case issue](https://api.clearinghouse.net/api-reference/objects/case/issues#defendant-type).  | [optional] 
**defendant_level_other** | **str** | The type or category of the defendant in terms of what the defendant governs if it does not fall under one of the options for [defendent_level](https://api.clearinghouse.net/api-reference/objects/defendant#defendent_level). Note: This is different from [the \&quot;Defendant-type\&quot; case issue](https://api.clearinghouse.net/api-reference/objects/defendant#defendent_level).  | [optional] 

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


