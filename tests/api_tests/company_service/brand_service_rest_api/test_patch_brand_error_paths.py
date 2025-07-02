from environment_data.data_generators import generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_patch_brand_for_non_existing_company_id(
        brand_service_rest_api, access_token_with_brand_write_scope, env_data):
    random_company_id = generate_uuid()
    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=random_company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid company ID"
    assert parsed_body['error']['detail'] == f"No company exists for the provided company ID: {random_company_id}"


def test_patch_brand_with_invalid_file_extensions(brand_service_rest_api, access_token_with_brand_write_scope,
                                                  env_data, get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body(file_extension1='bmp', file_extension2='xlsx')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "The request data did not validate"
    assert parsed_body['error']['detail'] == "One or more attributes in the request are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == "logo"
    assert parsed_body['error']['invalid-params'][1]['name'] == "coverImage"


def test_patch_brand_with_invalid_file_extension_for_logo(brand_service_rest_api,
                                                          access_token_with_brand_write_scope,
                                                          env_data, get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body(file_extension1='bmp')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)

    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "The request data did not validate"
    assert parsed_body['error']['detail'] == "One or more attributes in the request are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == "logo"
    assert len(parsed_body['error']['invalid-params']) == 1


def test_patch_brand_with_invalid_file_extension_for_cover_image(brand_service_rest_api,
                                                                 access_token_with_brand_write_scope,
                                                                 env_data,
                                                                 get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body(file_extension2='xlsx')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)

    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "The request data did not validate"
    assert parsed_body['error']['detail'] == "One or more attributes in the request are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == "coverImage"
    assert len(parsed_body['error']['invalid-params']) == 1


def test_patch_brand_without_access_token(brand_service_rest_api, env_data):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id, access_token=None, body=body)

    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_patch_brand_with_invalid_token(brand_service_rest_api, env_data,
                                        invalid_access_token_based_on_random_base64_encoded_string):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(
        company_id=company_id, access_token=invalid_access_token_based_on_random_base64_encoded_string, body=body)

    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_patch_brand_without_required_scope(brand_service_rest_api, env_data, access_token_with_company_read_scope):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope, body=body)

    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."
