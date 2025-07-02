from environment_data.data_generators import generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_get_brand_for_company_without_custom_brand(brand_service_rest_api, env_data,
                                                    access_token_with_company_read_scope):
    company_id = env_data['companies']['company_without_brand']['id']

    response, parsed_body = brand_service_rest_api.get_brand(company_id=company_id,
                                                             access_token=access_token_with_company_read_scope)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"
    assert parsed_body['error']['detail'] == f"GET /rest/brand-service/v1/companies/{company_id}/brand"


def test_get_brand_for_non_existing_company(brand_service_rest_api, access_token_with_company_read_scope):
    random_company_id = generate_uuid()

    response, parsed_body = brand_service_rest_api.get_brand(company_id=random_company_id,
                                                             access_token=access_token_with_company_read_scope)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid company ID"
    assert parsed_body['error']['detail'] == f"No company exists for the provided company ID: {random_company_id}"


def test_get_brand_without_access_token(brand_service_rest_api, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']

    response, parsed_body = brand_service_rest_api.get_brand(company_id=company_id, access_token=None)

    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_get_brand_with_invalid_token(brand_service_rest_api, env_data,
                                      invalid_access_token_based_on_random_base64_encoded_string):
    company_id = env_data['companies']['cc_company_service_test_company']['id']

    response, parsed_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=invalid_access_token_based_on_random_base64_encoded_string)

    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_get_brand_without_required_scope(brand_service_rest_api, env_data, access_token_with_company_write_scope):
    company_id = env_data['companies']['cc_company_service_test_company']['id']

    response, parsed_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_write_scope)

    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."
