from environment_data.data_generators import generate_random_email_domain, generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_delete_email_domain_non_existing_company_id(
        company_service_rest_api, access_token_with_company_write_scope,
        random_email_domain_for_existing_company_with_teardown):
    random_company_id = generate_uuid()
    _, domain = random_email_domain_for_existing_company_with_teardown

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=random_company_id, domain=domain, access_token=access_token_with_company_write_scope)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid company ID"
    assert parsed_body['error']['detail'] == f'No company exists for the provided company ID: {random_company_id}.'


def test_delete_non_existing_email_domain_for_a_valid_company(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = generate_random_email_domain(lower_case_only=True)

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=domain, access_token=access_token_with_company_write_scope)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"


def test_delete_existing_email_domain_different_company(
        company_service_rest_api, access_token_with_company_write_scope, env_data,
        random_email_domain_for_existing_company_with_teardown):
    _, domain = random_email_domain_for_existing_company_with_teardown
    company_id = env_data['companies']['cc_company_for_get_operations']['id']

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=domain, access_token=access_token_with_company_write_scope)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"


def test_delete_email_domain_with_empty_access_token(
        company_service_rest_api, env_data, random_email_domain_for_existing_company_with_teardown):
    company_id, domain = random_email_domain_for_existing_company_with_teardown

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=domain, access_token=None)

    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_delete_email_domain_with_invalid_token(
        company_service_rest_api, env_data, invalid_access_token_based_on_random_base64_encoded_string,
        random_email_domain_for_existing_company_with_teardown):
    company_id, domain = random_email_domain_for_existing_company_with_teardown

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=domain, access_token=invalid_access_token_based_on_random_base64_encoded_string)

    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_delete_email_domain_without_required_scope(
        company_service_rest_api, env_data, access_token_with_company_read_scope,
        random_email_domain_for_existing_company_with_teardown):
    company_id, domain = random_email_domain_for_existing_company_with_teardown

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=domain, access_token=access_token_with_company_read_scope)

    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."
