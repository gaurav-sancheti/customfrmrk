from environment_data.data_generators import generate_random_email_domain, generate_random_string_of_letters, \
    generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_post_existing_email_domain_different_company(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = env_data['companies']['cc_company_service_test_company']['email_domain']
    different_company_id = env_data['companies']['cc_company_for_get_operations']['id']
    body = [
        {
            "domain": domain
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=different_company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] ==\
           f'The email domain already exists for company with ID: {company_id}'


def test_post_email_domain_more_than_maximum_allowed_character_length(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = generate_random_string_of_letters(300) + '.test'
    body = [
        {
            "domain": domain
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Email domain cannot exceed 256 characters."


def test_post_empty_email_domain_list(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    body = []

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid request"
    assert parsed_body['error']['detail'] == "No email domains are provided in the request body."


def test_post_email_domain_zero_character_length(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = ''
    body = [
        {
            "domain": domain
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == "The email domain cannot be empty."


def test_post_email_domain_invalid_company(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    random_company_id = generate_uuid()
    body = [
        {
            "domain": generate_random_email_domain(lower_case_only=True)
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=random_company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid company ID"
    assert parsed_body['error']['detail'] == f'No company exists for the provided company ID: {random_company_id}'


def test_post_email_domain_containing_spaces(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = 'domain containing . spaces'
    body = [
        {
            "domain": domain
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Email domain cannot contain spaces."


def test_post_email_domain_containing_html(
        company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    domain = '<script>alert("hello!");</script>'
    body = [
        {
            "domain": domain
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 400
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 400
    assert parsed_body['error']['message'] == "Invalid email domain"
    assert parsed_body['error']['detail'] == "One or more email domains are invalid."
    assert parsed_body['error']['invalid-params'][0]['name'] == domain
    assert parsed_body['error']['invalid-params'][0]['reason'] == "Email domain cannot contain html tags."


def test_post_email_domain_empty_access_token(company_service_rest_api, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    body = [
        {
            "domain": generate_random_email_domain(lower_case_only=True)
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=None, body=body)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "No access token provided in the request."


def test_post_email_domain_invalid_token(
        company_service_rest_api, invalid_access_token_based_on_random_base64_encoded_string, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    body = [
        {
            "domain": generate_random_email_domain(lower_case_only=True)
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=invalid_access_token_based_on_random_base64_encoded_string, body=body)
    assert response.status_code == 401
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Access token is non-existent or expired."


def test_post_email_domain_non_required_scope(
        company_service_rest_api, access_token_with_company_read_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    body = [
        {
            "domain": generate_random_email_domain(lower_case_only=True)
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_read_scope, body=body)
    assert response.status_code == 403
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 403
    assert parsed_body['error']['message'] == "Forbidden"
    assert parsed_body['error']['detail'] == "Access token does not include the required scope."
