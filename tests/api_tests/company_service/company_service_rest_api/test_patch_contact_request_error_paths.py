from environment_data.data_generators import generate_random_string_of_letters, generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_patch_contact_request_with_empty_token(
        company_service_rest_api, env_data, contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=None, body=body)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_patch_contact_request_with_invalid_token(
        company_service_rest_api, invalid_access_token_based_on_random_base64_encoded_string, env_data,
        contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id,
        access_token=invalid_access_token_based_on_random_base64_encoded_string, body=body)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_patch_contact_request_using_token_with_non_required_scope(
        company_service_rest_api, access_token_with_company_read_scope, env_data,
        contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_read_scope, body=body)
    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."


def test_patch_contact_request_with_empty_name(
        company_service_rest_api, access_token_with_company_write_scope, env_data,
        contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    body['name'] = ''
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "The request data did not validate"
    assert parsed_body['error']['detail'] == "One or more attributes in the request are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == "name"
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Contact name cannot be empty."
    assert len(parsed_body['error']['invalid-params']) == 1


def test_patch_contact_request_with_too_long_name(
        company_service_rest_api, access_token_with_company_write_scope, env_data,
        contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    body['name'] = generate_random_string_of_letters(201)
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "The request data did not validate"
    assert parsed_body['error']['detail'] == "One or more attributes in the request are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == "name"
    assert parsed_body['error']['invalid-params'][0]['reason'] == \
           "Contact name exceeds the maximum amount of characters (200)."
    assert len(parsed_body['error']['invalid-params']) == 1


def test_patch_contact_request_with_non_existing_company(
        company_service_rest_api, access_token_with_company_write_scope, env_data,
        contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = generate_uuid()
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"


def test_patch_contact_request_with_non_existing_contact_request(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    request_id = generate_uuid()
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"


def test_patch_contact_request_with_html_in_name(
        company_service_rest_api, access_token_with_company_write_scope, env_data,
        contact_request_body_and_request_id_with_teardown):
    body, request_id = contact_request_body_and_request_id_with_teardown
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    body['name'] = '<script src="file.js"></script>'
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "The request data did not validate"
    assert parsed_body['error']['detail'] == "One or more attributes in the request are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == "name"
    assert parsed_body['error']['invalid-params'][0]['reason'] == \
           "Contact name cannot contain any HTML."
    assert len(parsed_body['error']['invalid-params']) == 1
