from environment_data.data_generators import generate_random_email_domain
from tests.api_tests.company_service.schemas import post_email_domains_full_success_response, \
    post_email_domains_partial_success_response


def test_create_email_domains_with_full_success(
        company_service_rest_api, company_service_odata_api, access_token_with_company_write_scope,
        access_token_with_company_read_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain1 = generate_random_email_domain(lower_case_only=True)
    domain2 = generate_random_email_domain()
    domain2_formatted = domain2.lower()
    domain3 = '   @' + generate_random_email_domain(lower_case_only=True) + '   '
    domain3_formatted = domain3.strip(' ,@')
    body = [
        {
            "domain": domain1
        },
        {
            "domain": domain2
        },
        {
            "domain": domain3
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 201
    post_email_domains_full_success_response.validate(parsed_body)
    assert parsed_body[0]['domain'] == domain1
    assert parsed_body[1]['domain'] == domain2_formatted
    assert parsed_body[2]['domain'] == domain3_formatted

    company_id_filter = {'$filter': f"companyId eq '{company_id}'", '$expand': 'emailDomains'}
    get_response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert get_response.status_code == 200

    domains = company_service_odata_api.get_domains(response_xml)
    assert len([domain for domain in domains if domain.text == domain1]) == 1
    assert len([domain for domain in domains if domain.text == domain2_formatted]) == 1
    assert len([domain for domain in domains if domain.text == domain3_formatted]) == 1


def test_create_email_domains_with_partial_success(
        company_service_rest_api, company_service_odata_api, access_token_with_company_write_scope,
        access_token_with_company_read_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain1 = ''
    domain2 = generate_random_email_domain(lower_case_only=True)
    body = [
        {
            "domain": domain1
        },
        {
            "domain": domain2
        },
        {
            "domain": domain2
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 207
    post_email_domains_partial_success_response.validate(parsed_body)

    assert [item for item in parsed_body['items'] if item['name'] == domain2][0]['code'] == 201
    assert [item for item in parsed_body['items'] if item['name'] == domain1][0]['code'] == 400
    assert [item for item in parsed_body['items'] if item['name'] == domain1][0]['reason'] == \
           "The email domain cannot be empty."
    assert [item for item in parsed_body['items'] if item['name'] == domain2][1]['code'] == 400
    assert [item for item in parsed_body['items'] if item['name'] == domain2][1]['reason'] ==\
           f'The email domain already exists for company with ID: {company_id}'

    company_id_filter = {'$filter': f"companyId eq '{company_id}'", '$expand': 'emailDomains'}
    get_response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert get_response.status_code == 200

    domains = company_service_odata_api.get_domains(response_xml)
    assert len([domain for domain in domains if domain.text == domain2]) == 1
