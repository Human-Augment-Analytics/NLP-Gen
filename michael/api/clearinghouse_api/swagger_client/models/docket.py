# coding: utf-8

"""
    Civil Rights Clearinghouse Simple API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Docket(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'int',
        'docket_number_manual': 'str',
        'docket_office_number': 'str',
        'docket_year': 'int',
        'docket_case_type': 'str',
        'docket_filing_number': 'int',
        'court': 'str',
        'state': 'str',
        'is_main_docket': 'bool',
        'recap_link': 'str',
        'docket_entries': 'list[DocketEntry]',
        'scales_html': 'str'
    }

    attribute_map = {
        'id': 'id',
        'docket_number_manual': 'docket_number_manual',
        'docket_office_number': 'docket_office_number',
        'docket_year': 'docket_year',
        'docket_case_type': 'docket_case_type',
        'docket_filing_number': 'docket_filing_number',
        'court': 'court',
        'state': 'state',
        'is_main_docket': 'is_main_docket',
        'recap_link': 'recap_link',
        'docket_entries': 'docket_entries',
        'scales_html': 'scales_html'
    }

    def __init__(self, id=None, docket_number_manual=None, docket_office_number=None, docket_year=None, docket_case_type=None, docket_filing_number=None, court=None, state=None, is_main_docket=None, recap_link=None, docket_entries=None, scales_html=None):  # noqa: E501
        """Docket - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._docket_number_manual = None
        self._docket_office_number = None
        self._docket_year = None
        self._docket_case_type = None
        self._docket_filing_number = None
        self._court = None
        self._state = None
        self._is_main_docket = None
        self._recap_link = None
        self._docket_entries = None
        self._scales_html = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if docket_number_manual is not None:
            self.docket_number_manual = docket_number_manual
        if docket_office_number is not None:
            self.docket_office_number = docket_office_number
        if docket_year is not None:
            self.docket_year = docket_year
        if docket_case_type is not None:
            self.docket_case_type = docket_case_type
        if docket_filing_number is not None:
            self.docket_filing_number = docket_filing_number
        if court is not None:
            self.court = court
        if state is not None:
            self.state = state
        if is_main_docket is not None:
            self.is_main_docket = is_main_docket
        if recap_link is not None:
            self.recap_link = recap_link
        if docket_entries is not None:
            self.docket_entries = docket_entries
        if scales_html is not None:
            self.scales_html = scales_html

    @property
    def id(self):
        """Gets the id of this Docket.  # noqa: E501


        :return: The id of this Docket.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Docket.


        :param id: The id of this Docket.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def docket_number_manual(self):
        """Gets the docket_number_manual of this Docket.  # noqa: E501


        :return: The docket_number_manual of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._docket_number_manual

    @docket_number_manual.setter
    def docket_number_manual(self, docket_number_manual):
        """Sets the docket_number_manual of this Docket.


        :param docket_number_manual: The docket_number_manual of this Docket.  # noqa: E501
        :type: str
        """

        self._docket_number_manual = docket_number_manual

    @property
    def docket_office_number(self):
        """Gets the docket_office_number of this Docket.  # noqa: E501


        :return: The docket_office_number of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._docket_office_number

    @docket_office_number.setter
    def docket_office_number(self, docket_office_number):
        """Sets the docket_office_number of this Docket.


        :param docket_office_number: The docket_office_number of this Docket.  # noqa: E501
        :type: str
        """

        self._docket_office_number = docket_office_number

    @property
    def docket_year(self):
        """Gets the docket_year of this Docket.  # noqa: E501


        :return: The docket_year of this Docket.  # noqa: E501
        :rtype: int
        """
        return self._docket_year

    @docket_year.setter
    def docket_year(self, docket_year):
        """Sets the docket_year of this Docket.


        :param docket_year: The docket_year of this Docket.  # noqa: E501
        :type: int
        """

        self._docket_year = docket_year

    @property
    def docket_case_type(self):
        """Gets the docket_case_type of this Docket.  # noqa: E501


        :return: The docket_case_type of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._docket_case_type

    @docket_case_type.setter
    def docket_case_type(self, docket_case_type):
        """Sets the docket_case_type of this Docket.


        :param docket_case_type: The docket_case_type of this Docket.  # noqa: E501
        :type: str
        """

        self._docket_case_type = docket_case_type

    @property
    def docket_filing_number(self):
        """Gets the docket_filing_number of this Docket.  # noqa: E501


        :return: The docket_filing_number of this Docket.  # noqa: E501
        :rtype: int
        """
        return self._docket_filing_number

    @docket_filing_number.setter
    def docket_filing_number(self, docket_filing_number):
        """Sets the docket_filing_number of this Docket.


        :param docket_filing_number: The docket_filing_number of this Docket.  # noqa: E501
        :type: int
        """

        self._docket_filing_number = docket_filing_number

    @property
    def court(self):
        """Gets the court of this Docket.  # noqa: E501


        :return: The court of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._court

    @court.setter
    def court(self, court):
        """Sets the court of this Docket.


        :param court: The court of this Docket.  # noqa: E501
        :type: str
        """

        self._court = court

    @property
    def state(self):
        """Gets the state of this Docket.  # noqa: E501


        :return: The state of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Docket.


        :param state: The state of this Docket.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def is_main_docket(self):
        """Gets the is_main_docket of this Docket.  # noqa: E501


        :return: The is_main_docket of this Docket.  # noqa: E501
        :rtype: bool
        """
        return self._is_main_docket

    @is_main_docket.setter
    def is_main_docket(self, is_main_docket):
        """Sets the is_main_docket of this Docket.


        :param is_main_docket: The is_main_docket of this Docket.  # noqa: E501
        :type: bool
        """

        self._is_main_docket = is_main_docket

    @property
    def recap_link(self):
        """Gets the recap_link of this Docket.  # noqa: E501


        :return: The recap_link of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._recap_link

    @recap_link.setter
    def recap_link(self, recap_link):
        """Sets the recap_link of this Docket.


        :param recap_link: The recap_link of this Docket.  # noqa: E501
        :type: str
        """

        self._recap_link = recap_link

    @property
    def docket_entries(self):
        """Gets the docket_entries of this Docket.  # noqa: E501


        :return: The docket_entries of this Docket.  # noqa: E501
        :rtype: list[DocketEntry]
        """
        return self._docket_entries

    @docket_entries.setter
    def docket_entries(self, docket_entries):
        """Sets the docket_entries of this Docket.


        :param docket_entries: The docket_entries of this Docket.  # noqa: E501
        :type: list[DocketEntry]
        """

        self._docket_entries = docket_entries

    @property
    def scales_html(self):
        """Gets the scales_html of this Docket.  # noqa: E501


        :return: The scales_html of this Docket.  # noqa: E501
        :rtype: str
        """
        return self._scales_html

    @scales_html.setter
    def scales_html(self, scales_html):
        """Sets the scales_html of this Docket.


        :param scales_html: The scales_html of this Docket.  # noqa: E501
        :type: str
        """

        self._scales_html = scales_html

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Docket, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Docket):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
