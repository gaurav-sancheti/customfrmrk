import logging

from api_clients.apithon import ApithonODataJWT


class CompanyServiceODataAPI(ApithonODataJWT):
    def __init__(self, env_data):
        logger = logging.getLogger("instr.log").getChild(__name__)
        base_url = "https://quality.mendixcloud.com/odata/company-service/v1"
        super().__init__(env_data=env_data, logger=logger, base_url=base_url)
        self.namespaces = {'dataservices': "http://schemas.microsoft.com/ado/2007/08/dataservices",
                           'atom': "http://www.w3.org/2005/Atom",
                           'metadata': "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"}

    def get_company(self, access_token, **kwargs):
        response, parsed_body = self.get_odata("/companies", token=access_token, **kwargs)
        return response, parsed_body

    def get_contact(self, access_token, **kwargs):
        response, parsed_body = self.get_odata("/contacts", token=access_token, **kwargs)
        return response, parsed_body

    def get_contact_request(self, access_token, **kwargs):
        response, parsed_body = self.get_odata("/contactRequests", token=access_token, **kwargs)
        return response, parsed_body

    def _get_attributes_from_response(self, attribute, response_xml):
        return response_xml.findall(f'.//atom:entry/atom:content/metadata:properties/dataservices:{attribute}',
                                    self.namespaces)

    def _get_attribute_from_response(self, attribute, response_xml):
        return response_xml.find(f'.//atom:entry/atom:content/metadata:properties/dataservices:{attribute}',
                                 self.namespaces).text

    def _get_attribute_from_response_single_entry(self, attribute, response_xml):
        return response_xml.find(f'.//atom:content/metadata:properties/dataservices:{attribute}', self.namespaces).text

    def get_company_id(self, response_xml):
        return self._get_attribute_from_response('companyId', response_xml)

    def get_company_name(self, response_xml):
        return self._get_attribute_from_response('name', response_xml)

    def get_company_description(self, response_xml):
        return self._get_attribute_from_response('description', response_xml)

    def get_created_date(self, response_xml):
        return self._get_attribute_from_response('createdAt', response_xml)

    def get_company_count(self, response_xml):
        return len(self._get_attributes_from_response("companyId", response_xml))

    def get_contact_count(self, response_xml):
        return len(self._get_attributes_from_response("contactId", response_xml))

    def get_contact_request_count(self, response_xml):
        return len(self._get_attributes_from_response("requestId", response_xml))

    def get_domains(self, response_xml):
        return self._get_attributes_from_response('domain', response_xml)

    def get_contact_id(self, response_xml):
        return self._get_attribute_from_response('contactId', response_xml)

    def get_contact_name(self, response_xml):
        return self._get_attribute_from_response('name', response_xml)

    def get_contact_email_address(self, response_xml):
        return self._get_attribute_from_response('emailAddress', response_xml)

    def get_contacts(self, response_xml):
        return self._get_attributes_from_response('contactId', response_xml)

    def get_contact_requests(self, response_xml):
        return self._get_attributes_from_response('requestId', response_xml)

    def get_contact_request_id(self, response_xml):
        return self._get_attribute_from_response('requestId', response_xml)

    def get_contact_request_name(self, response_xml):
        return self._get_attribute_from_response('name', response_xml)

    def get_contact_request_email_address(self, response_xml):
        return self._get_attribute_from_response('emailAddress', response_xml)

    def get_contact_request_created_date(self, response_xml):
        return self._get_attribute_from_response('createdDate', response_xml)
