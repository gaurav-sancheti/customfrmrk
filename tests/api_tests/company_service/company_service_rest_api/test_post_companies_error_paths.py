from environment_data.data_generators import generate_random_string_of_letters
from tests.api_tests.company_service.schemas import error_response


def test_post_company_too_long_company_name(company_service_rest_api, access_token_with_company_write_scope):
    name = generate_random_string_of_letters(102)
    body = company_service_rest_api.generate_random_post_company_request_body(name=name)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid request"
    assert parsed_body['error']['detail'] == "The company name exceeded the maximum character length (100)."


def test_post_company_empty_company_name(company_service_rest_api, access_token_with_company_write_scope):
    name = ''
    body = company_service_rest_api.generate_random_post_company_request_body(name=name)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid request"
    assert parsed_body['error']['detail'] == "The company name cannot be empty."


def test_post_company_with_html_in_name(company_service_rest_api, access_token_with_company_write_scope):
    name = '<script src="file.js"></script>'
    body = company_service_rest_api.generate_random_post_company_request_body(name=name)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid request"
    assert parsed_body['error']['detail'] == "The company name cannot contain html tags."


def test_post_company_with_html_in_description(company_service_rest_api, access_token_with_company_write_scope):
    description = '<script src="file.js"></script>'
    body = company_service_rest_api.generate_random_post_company_request_body(description=description)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid request"
    assert parsed_body['error']['detail'] == "The company description cannot contain html tags."


def test_post_company_invalid_token(company_service_rest_api,
                                    invalid_access_token_based_on_random_base64_encoded_string):
    body = company_service_rest_api.generate_random_post_company_request_body()

    response, parsed_body = company_service_rest_api.post_company(
        access_token=invalid_access_token_based_on_random_base64_encoded_string, body=body)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_post_company_token_with_non_required_scope(
        company_service_rest_api, access_token_with_company_read_scope):
    body = company_service_rest_api.generate_random_post_company_request_body()

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_read_scope, body=body)
    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."


def test_post_company_empty_token(company_service_rest_api):
    body = company_service_rest_api.generate_random_post_company_request_body()

    response, parsed_body = company_service_rest_api.post_company(access_token=None, body=body)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_post_company_email_domain_having_zero_character_length(
        company_service_rest_api, access_token_with_company_write_scope):
    domain = ''
    body = company_service_rest_api.generate_random_post_company_request_body(domain=domain)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == "The email domain cannot be empty."


def test_post_company_empty_email_domain_list(company_service_rest_api, access_token_with_company_write_scope):
    body = company_service_rest_api.generate_random_post_company_request_body()
    body['emailDomains'] = []

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid request"
    assert parsed_body['error']['detail'] == "No email domains are provided in the request body."


def test_post_company_email_domain_having_more_than_maximum_allowed_character_length(
        company_service_rest_api, access_token_with_company_write_scope):
    domain = generate_random_string_of_letters(300) + '.test'
    body = company_service_rest_api.generate_random_post_company_request_body(domain=domain)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Email domain cannot exceed 256 characters."


def test_post_company_email_domain_containing_spaces(
        company_service_rest_api, access_token_with_company_write_scope):
    domain = 'domain containing . spaces'
    body = company_service_rest_api.generate_random_post_company_request_body(domain=domain)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Email domain cannot contain spaces."


def test_post_company_email_domain_containing_html(
        company_service_rest_api, access_token_with_company_write_scope):
    domain = '<script>alert("hello!");</script>'
    body = company_service_rest_api.generate_random_post_company_request_body(domain=domain)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Email domain cannot contain html tags."


def test_post_company_already_existing_email_domain(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = env_data['companies']['cc_company_service_test_company']['email_domain']
    body = company_service_rest_api.generate_random_post_company_request_body(domain=domain)

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == \
           f'The email domain already exists for company with ID: {company_id}'
