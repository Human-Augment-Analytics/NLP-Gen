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

class DocketEntry(object):
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
        'row_number': 'int',
        'entry_number': 'str',
        'date_filled': 'str',
        'description': 'str',
        'attachments': 'list[DocketEntryAttachments]',
        'url': 'str',
        'recap_pdf_url': 'str',
        'pacer_doc_id': 'str',
        'id': 'int'
    }

    attribute_map = {
        'row_number': 'row_number',
        'entry_number': 'entry_number',
        'date_filled': 'date_filled',
        'description': 'description',
        'attachments': 'attachments',
        'url': 'url',
        'recap_pdf_url': 'recap_pdf_url',
        'pacer_doc_id': 'pacer_doc_id',
        'id': 'id'
    }

    def __init__(self, row_number=None, entry_number=None, date_filled=None, description=None, attachments=None, url=None, recap_pdf_url=None, pacer_doc_id=None, id=None):  # noqa: E501
        """DocketEntry - a model defined in Swagger"""  # noqa: E501
        self._row_number = None
        self._entry_number = None
        self._date_filled = None
        self._description = None
        self._attachments = None
        self._url = None
        self._recap_pdf_url = None
        self._pacer_doc_id = None
        self._id = None
        self.discriminator = None
        if row_number is not None:
            self.row_number = row_number
        if entry_number is not None:
            self.entry_number = entry_number
        if date_filled is not None:
            self.date_filled = date_filled
        if description is not None:
            self.description = description
        if attachments is not None:
            self.attachments = attachments
        if url is not None:
            self.url = url
        if recap_pdf_url is not None:
            self.recap_pdf_url = recap_pdf_url
        if pacer_doc_id is not None:
            self.pacer_doc_id = pacer_doc_id
        if id is not None:
            self.id = id

    @property
    def row_number(self):
        """Gets the row_number of this DocketEntry.  # noqa: E501


        :return: The row_number of this DocketEntry.  # noqa: E501
        :rtype: int
        """
        return self._row_number

    @row_number.setter
    def row_number(self, row_number):
        """Sets the row_number of this DocketEntry.


        :param row_number: The row_number of this DocketEntry.  # noqa: E501
        :type: int
        """

        self._row_number = row_number

    @property
    def entry_number(self):
        """Gets the entry_number of this DocketEntry.  # noqa: E501


        :return: The entry_number of this DocketEntry.  # noqa: E501
        :rtype: str
        """
        return self._entry_number

    @entry_number.setter
    def entry_number(self, entry_number):
        """Sets the entry_number of this DocketEntry.


        :param entry_number: The entry_number of this DocketEntry.  # noqa: E501
        :type: str
        """

        self._entry_number = entry_number

    @property
    def date_filled(self):
        """Gets the date_filled of this DocketEntry.  # noqa: E501


        :return: The date_filled of this DocketEntry.  # noqa: E501
        :rtype: str
        """
        return self._date_filled

    @date_filled.setter
    def date_filled(self, date_filled):
        """Sets the date_filled of this DocketEntry.


        :param date_filled: The date_filled of this DocketEntry.  # noqa: E501
        :type: str
        """

        self._date_filled = date_filled

    @property
    def description(self):
        """Gets the description of this DocketEntry.  # noqa: E501


        :return: The description of this DocketEntry.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DocketEntry.


        :param description: The description of this DocketEntry.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def attachments(self):
        """Gets the attachments of this DocketEntry.  # noqa: E501


        :return: The attachments of this DocketEntry.  # noqa: E501
        :rtype: list[DocketEntryAttachments]
        """
        return self._attachments

    @attachments.setter
    def attachments(self, attachments):
        """Sets the attachments of this DocketEntry.


        :param attachments: The attachments of this DocketEntry.  # noqa: E501
        :type: list[DocketEntryAttachments]
        """

        self._attachments = attachments

    @property
    def url(self):
        """Gets the url of this DocketEntry.  # noqa: E501


        :return: The url of this DocketEntry.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this DocketEntry.


        :param url: The url of this DocketEntry.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def recap_pdf_url(self):
        """Gets the recap_pdf_url of this DocketEntry.  # noqa: E501


        :return: The recap_pdf_url of this DocketEntry.  # noqa: E501
        :rtype: str
        """
        return self._recap_pdf_url

    @recap_pdf_url.setter
    def recap_pdf_url(self, recap_pdf_url):
        """Sets the recap_pdf_url of this DocketEntry.


        :param recap_pdf_url: The recap_pdf_url of this DocketEntry.  # noqa: E501
        :type: str
        """

        self._recap_pdf_url = recap_pdf_url

    @property
    def pacer_doc_id(self):
        """Gets the pacer_doc_id of this DocketEntry.  # noqa: E501


        :return: The pacer_doc_id of this DocketEntry.  # noqa: E501
        :rtype: str
        """
        return self._pacer_doc_id

    @pacer_doc_id.setter
    def pacer_doc_id(self, pacer_doc_id):
        """Sets the pacer_doc_id of this DocketEntry.


        :param pacer_doc_id: The pacer_doc_id of this DocketEntry.  # noqa: E501
        :type: str
        """

        self._pacer_doc_id = pacer_doc_id

    @property
    def id(self):
        """Gets the id of this DocketEntry.  # noqa: E501


        :return: The id of this DocketEntry.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DocketEntry.


        :param id: The id of this DocketEntry.  # noqa: E501
        :type: int
        """

        self._id = id

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
        if issubclass(DocketEntry, dict):
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
        if not isinstance(other, DocketEntry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other