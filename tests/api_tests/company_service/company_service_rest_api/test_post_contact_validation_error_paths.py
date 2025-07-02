from environment_data.data_generators import generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_post_contact_validation_with_empty_token(
        company_service_rest_api, company_id_with_name_and_validation_hash):
    _, _, validation_hash = company_id_with_name_and_validation_hash

    response, parsed_body = company_service_rest_api.post_contact_validation(
        access_token=None, validation_hash=validation_hash)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_post_contact_validation_with_invalid_token(
        company_service_rest_api, company_id_with_name_and_validation_hash,
        invalid_access_token_based_on_random_base64_encoded_string):
    _, _, validation_hash = company_id_with_name_and_validation_hash

    response, parsed_body = company_service_rest_api.post_contact_validation(
        access_token=invalid_access_token_based_on_random_base64_encoded_string, validation_hash=validation_hash)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_post_contact_validation_using_token_with_non_required_scope(
        company_service_rest_api, company_id_with_name_and_validation_hash,
        access_token_with_company_write_scope):
    _, _, validation_hash = company_id_with_name_and_validation_hash

    response, parsed_body = company_service_rest_api.post_contact_validation(
        access_token=access_token_with_company_write_scope, validation_hash=validation_hash)
    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."


def test_post_contact_validation_with_invalid_validation_hash(
        company_service_rest_api, access_token_with_company_contact_validate_scope):
    validation_hash = generate_uuid()
    response, parsed_body = company_service_rest_api.post_contact_validation(
        access_token=access_token_with_company_contact_validate_scope, validation_hash=validation_hash)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"
