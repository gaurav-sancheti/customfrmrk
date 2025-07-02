from environment_data.data_generators import generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_delete_contact_with_empty_token(company_service_rest_api, env_data, company_id_with_contact_id_teardown):
    company_id, contact_id = company_id_with_contact_id_teardown
    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id, access_token=None)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_delete_contact_with_invalid_token(
        company_service_rest_api, invalid_access_token_based_on_random_base64_encoded_string, env_data,
        company_id_with_contact_id_teardown):
    company_id, contact_id = company_id_with_contact_id_teardown
    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id,
        access_token=invalid_access_token_based_on_random_base64_encoded_string)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_delete_contact_using_token_with_non_required_scope(
        company_service_rest_api, access_token_with_company_read_scope, env_data,
        company_id_with_contact_id_teardown):
    company_id, contact_id = company_id_with_contact_id_teardown
    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id, access_token=access_token_with_company_read_scope)
    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."


def test_delete_contact_with_non_existing_company(
        company_service_rest_api, access_token_with_company_write_scope, env_data,
        company_id_with_contact_id_teardown):
    _, contact_id = company_id_with_contact_id_teardown
    company_id = generate_uuid()
    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id, access_token=access_token_with_company_write_scope)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"


def test_delete_contact_with_non_existing_contact(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    contact_id = generate_uuid()
    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id, access_token=access_token_with_company_write_scope)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"
