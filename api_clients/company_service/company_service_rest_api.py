import logging

from api_clients.apithon import ApithonRestBasicAuth, ApithonRestJWT

from environment_data.data_generators import generate_random_email_address, generate_random_email_domain, \
    generate_random_string_of_letters


class CompanyServiceRESTAPI(ApithonRestJWT):
    def __init__(self, env_data):
        logger = logging.getLogger("instr.log").getChild(__name__)
        base_url = 'https://quality.mendixcloud.com/rest/company-service/v1'
        super().__init__(env_data=env_data, logger=logger, base_url=base_url)

    def post_company(self, access_token, body):
        response, parsed_body = self.post("/companies", token=access_token, json=body)
        return response, parsed_body

    def put_company(self, company_id, access_token, body, initiating_user_id=None):
        headers = None if initiating_user_id is None else {'User-Id': initiating_user_id}
        response, parsed_body = self.put(
            resource_url=f'/companies/{company_id}', token=access_token, json=body, headers=headers)
        return response, parsed_body

    def patch_company(self, company_id, access_token, body, initiating_user_id=None):
        headers = None if initiating_user_id is None else {'User-Id': initiating_user_id}
        response, parsed_body = self.patch(
            resource_url=f'/companies/{company_id}', token=access_token, json=body, headers=headers)
        return response, parsed_body

    def get_company(self, company_id, access_token):
        response, parsed_body = self.get(resource_url=f'/companies/{company_id}', token=access_token)
        return response, parsed_body

    def get_company_brand(self, company_id, access_token):
        response, parsed_body = self.get(resource_url=f'/companies/{company_id}/brand', token=access_token)
        return response, parsed_body

    def post_email_domains(self, company_id, access_token, body):
        response, parsed_body = self.post(resource_url=f'/companies/{company_id}/email-domains',
                                          token=access_token, json=body)
        return response, parsed_body

    def delete_email_domain(self, company_id, domain, access_token):
        response, parsed_body = self.delete(resource_url=f'/companies/{company_id}/email-domains/{domain}',
                                            token=access_token)
        return response, parsed_body

    def patch_contact(self, access_token, body, company_id, contact_id):
        response, parsed_body = self.patch(
            f'/companies/{company_id}/contacts/{contact_id}', token=access_token, json=body)
        return response, parsed_body

    def delete_contact(self, access_token, company_id, contact_id):
        response, parsed_body = self.delete(f'/companies/{company_id}/contacts/{contact_id}', token=access_token)
        return response, parsed_body

    def post_contact_request(self, access_token, body, company_id):
        response, parsed_body = self.post(f'/companies/{company_id}/contact-requests', token=access_token, json=body)
        return response, parsed_body

    def patch_contact_request(self, access_token, body, company_id, request_id):
        response, parsed_body = self.patch(
            f'/companies/{company_id}/contact-requests/{request_id}', token=access_token, json=body)
        return response, parsed_body

    def delete_contact_request(self, access_token, company_id, request_id):
        response, parsed_body = self.delete(
            f'/companies/{company_id}/contact-requests/{request_id}', token=access_token)
        return response, parsed_body

    def post_contact_validation(self, access_token, validation_hash):
        response, parsed_body = self.post(f'/contact-validations/{validation_hash}', token=access_token)
        return response, parsed_body

    @staticmethod
    def generate_random_post_company_request_body(name=None, description=None, domain=None):
        name = generate_random_string_of_letters(7) if name is None else name
        description = generate_random_string_of_letters(20) if description is None else description
        domain = generate_random_email_domain(lower_case_only=True) if domain is None else domain
        return {
            "name": name,
            "emailDomains": [
                {
                    "domain": domain
                }
            ],
            "description": description
        }

    @staticmethod
    def generate_random_put_company_request_body(name=None, description=None):
        name = generate_random_string_of_letters(7) if name is None else name
        description = generate_random_string_of_letters(20) if description is None else description
        return {
            "name": name,
            "description": description
        }

    @staticmethod
    def generate_random_patch_company_request_body(attribute_name=None, attribute_value=None):
        attribute_name = generate_random_string_of_letters(7) if attribute_name is None else attribute_name
        attribute_value = generate_random_string_of_letters(7) if attribute_value is None else attribute_value
        return [
            {
                "attributeName": attribute_name,
                "attributeValue": attribute_value
            }
        ]

    @staticmethod
    def generate_random_post_contact_request_body(type_id=None, email_address=None, name=None):
        type_id = 'security' if type_id is None else type_id
        email_address = generate_random_email_address() if email_address is None else email_address
        name = generate_random_string_of_letters(7) if name is None else name
        return {
            "typeId": type_id,
            "emailAddress": email_address,
            "name": name
        }

    @staticmethod
    def generate_random_patch_contact_request_body(name=None):
        name = generate_random_string_of_letters(7) if name is None else name
        return {
            "name": name
        }


class CompanyServiceRESTAPIApithon(ApithonRestBasicAuth):
    # Endpoints of the Company Service REST API that should only be used by Apithon and use basic auth instead of JWT.
    def __init__(self, env_data):
        logger = logging.getLogger("instr.log").getChild(__name__)
        base_url = f"{env_data['company_service']['base_url']}/rest/company-service/v1"
        default_username = env_data['company_service']['company_service_rest_api_apithon']['username']
        default_password = env_data['company_service']['company_service_rest_api_apithon']['password']
        super().__init__(env_data=env_data, logger=logger, base_url=base_url, default_username=default_username,
                         default_password=default_password)

    def get_contact_request(self, request_id, **kwargs):
        response, parsed_body = self.get(resource_url=f'/contact-requests/{request_id}/apithon', **kwargs)
        return response, parsed_body
