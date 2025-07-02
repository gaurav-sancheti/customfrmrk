from environment_data.data_generators import generate_uuid
from tests.api_tests.company_service.schemas import error_response_rfc7807


def test_get_company_with_non_existing_id(company_service_rest_api, access_token_with_company_read_scope):
    random_company_id = generate_uuid()

    response, parsed_body = company_service_rest_api.get_company(company_id=random_company_id,
                                                                 access_token=access_token_with_company_read_scope)
    assert response.status_code == 404
    error_response_rfc7807.validate(parsed_body)

    assert parsed_body['status'] == 404
    assert parsed_body['title'] == "Company not found"
    assert parsed_body['detail'] == f"No company found with UUID: {random_company_id}"


def test_get_company_without_access_token(company_service_rest_api, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']

    response, parsed_body = company_service_rest_api.get_company(
        company_id=company_id, access_token=None)

    assert response.status_code == 401
    error_response_rfc7807.validate(parsed_body)

    assert parsed_body['status'] == 401
    assert parsed_body['title'] == "Unauthorized"
    assert parsed_body['detail'] == "No access token provided in the request."


def test_get_company_with_invalid_token(company_service_rest_api, env_data,
                                        invalid_access_token_based_on_random_base64_encoded_string):
    company_id = env_data['companies']['cc_company_service_test_company']['id']

    response, parsed_body = company_service_rest_api.get_company(
        company_id=company_id, access_token=invalid_access_token_based_on_random_base64_encoded_string)

    assert response.status_code == 401
    error_response_rfc7807.validate(parsed_body)

    assert parsed_body['status'] == 401
    assert parsed_body['title'] == "Unauthorized"
    assert parsed_body['detail'] == "Access token is non-existent or expired."


def test_get_company_without_required_scope(company_service_rest_api, env_data,
                                            access_token_with_company_write_scope):
    company_id = env_data['companies']['cc_company_service_test_company']['id']

    response, parsed_body = company_service_rest_api.get_company(
        company_id=company_id, access_token=access_token_with_company_write_scope)

    assert response.status_code == 403
    error_response_rfc7807.validate(parsed_body)

    assert parsed_body['status'] == 403
    assert parsed_body['title'] == "Forbidden"
    assert parsed_body['detail'] == "Access token does not include the required scope."
