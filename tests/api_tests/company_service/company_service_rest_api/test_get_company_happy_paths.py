from tests.api_tests.company_service.schemas import get_company_response


def test_get_company(company_service_rest_api, env_data, access_token_with_company_read_scope):
    company_id = env_data['companies']['cc_company_for_get_operations']['id']

    response, parsed_body = company_service_rest_api.get_company(company_id=company_id,
                                                                 access_token=access_token_with_company_read_scope)
    assert response.status_code == 200
    get_company_response.validate(parsed_body)
    assert parsed_body['name'] == env_data['companies']['cc_company_for_get_operations']['name']
    assert parsed_body['description'] == env_data['companies']['cc_company_for_get_operations']['description']
    assert parsed_body['logoUrl'] == env_data['companies']['cc_company_for_get_operations']['logo_url']
    assert parsed_body['digitallySignEmails'] == env_data['companies']['cc_company_for_get_operations']['digitally_sign_emails']
