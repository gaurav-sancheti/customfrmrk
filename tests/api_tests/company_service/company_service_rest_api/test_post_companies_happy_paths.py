from environment_data.data_generators import generate_random_email_domain, generate_random_string_of_letters
from environment_data.data_validators import validate_uuid4
from tests.api_tests.company_service.schemas import post_company_full_success_response, \
    post_company_partial_success_response


def test_create_company(
        company_service_rest_api, company_service_odata_api, access_token_with_company_write_scope,
        access_token_with_company_read_scope, env_data):
    body = company_service_rest_api.generate_random_post_company_request_body()
    email_domain = body['emailDomains'][0]['domain']

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 201
    post_company_full_success_response.validate(parsed_body)
    validate_uuid4(parsed_body['companyId'])
    assert parsed_body['name'] == body['name']
    assert parsed_body['description'] == body['description']
    assert parsed_body['emailDomains'][0]['domain'] == email_domain

    company_id_filter = {'$filter': f"companyId eq '{parsed_body['companyId']}'", '$expand': 'emailDomains'}
    get_response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert get_response.status_code == 200
    assert company_service_odata_api.get_company_name(response_xml) == body['name']

    domains = company_service_odata_api.get_domains(response_xml)
    assert len([domain for domain in domains if domain.text == email_domain]) == 1


def test_create_company_partial_success(
        company_service_rest_api, company_service_odata_api,
        access_token_with_company_write_scope, access_token_with_company_read_scope, env_data):
    domain1 = ''
    domain2 = generate_random_email_domain(lower_case_only=True)
    body = {
            "name": generate_random_string_of_letters(7),
            "emailDomains": [
                {
                    "domain": domain1
                },
                {
                    "domain": domain2
                }
            ],
            "description": generate_random_string_of_letters(20)
        }

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 207
    post_company_partial_success_response.validate(parsed_body)
    validate_uuid4(parsed_body['companyId'])
    assert parsed_body['name'] == body['name']
    assert parsed_body['description'] == body['description']
    assert [domain for domain in parsed_body['emailDomains'] if domain['name'] == domain2][0]['code'] == 201
    assert [domain for domain in parsed_body['emailDomains'] if domain['name'] == domain1][0]['code'] == 400
    assert [domain for domain in parsed_body['emailDomains'] if domain['name'] == domain1][0]['reason'] == \
           "The email domain cannot be empty."

    company_id_filter = {'$filter': f"companyId eq '{parsed_body['companyId']}'", '$expand': 'emailDomains'}
    get_response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert get_response.status_code == 200
    assert company_service_odata_api.get_company_name(response_xml) == body['name']

    domains = company_service_odata_api.get_domains(response_xml)
    assert len([domain for domain in domains if domain.text == domain2]) == 1


def test_create_company_without_description(
        company_service_rest_api, company_service_odata_api, access_token_with_company_write_scope,
        access_token_with_company_read_scope, env_data):
    email_domain = generate_random_email_domain(lower_case_only=True)
    body = {
        "name": generate_random_string_of_letters(7),
        "emailDomains": [
            {
                "domain": email_domain
            }
        ]
    }

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 201
    post_company_full_success_response.validate(parsed_body)
    validate_uuid4(parsed_body['companyId'])
    assert parsed_body['name'] == body['name']
    assert parsed_body['emailDomains'][0]['domain'] == email_domain

    company_id_filter = {'$filter': f"companyId eq '{parsed_body['companyId']}'", '$expand': 'emailDomains'}
    get_response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert get_response.status_code == 200
    assert company_service_odata_api.get_company_name(response_xml) == body['name']

    domains = company_service_odata_api.get_domains(response_xml)
    assert len([domain for domain in domains if domain.text == email_domain]) == 1
