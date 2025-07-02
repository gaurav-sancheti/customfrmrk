from environment_data.data_generators import generate_uuid
from tests.api_tests.company_service.schemas import error_response


def test_get_contact_request_invalid_username(
        contact_request_body_and_request_id_with_teardown, company_service_rest_api_apithon):
    _, request_id = contact_request_body_and_request_id_with_teardown

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(
        request_id=request_id, username='invalid_username')
    assert response.status_code == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Invalid credentials"


def test_get_contact_request_invalid_password(
        contact_request_body_and_request_id_with_teardown, company_service_rest_api_apithon):
    _, request_id = contact_request_body_and_request_id_with_teardown

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(
        request_id=request_id, password='invalid_password')
    assert response.status_code == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Invalid credentials"


def test_get_contact_request_empty_username_and_empty_password(
        contact_request_body_and_request_id_with_teardown, company_service_rest_api_apithon):
    _, request_id = contact_request_body_and_request_id_with_teardown

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(
        request_id=request_id, username=None, password=None)
    assert response.status_code == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Invalid credentials"


def test_get_contact_request_empty_username(
        contact_request_body_and_request_id_with_teardown, company_service_rest_api_apithon):
    _, request_id = contact_request_body_and_request_id_with_teardown

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(
        request_id=request_id, username=None)
    assert response.status_code == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Invalid credentials"


def test_get_contact_request_empty_password(
        contact_request_body_and_request_id_with_teardown, company_service_rest_api_apithon):
    _, request_id = contact_request_body_and_request_id_with_teardown

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(
        request_id=request_id, password=None)
    assert response.status_code == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Invalid credentials"


def test_get_contact_request_invalid_username_and_invalid_password(
        contact_request_body_and_request_id_with_teardown, company_service_rest_api_apithon):
    _, request_id = contact_request_body_and_request_id_with_teardown

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(
        request_id=request_id, username='invalid_username', password='invalid_password')
    assert response.status_code == 401
    assert parsed_body['error']['message'] == "Unauthorized"
    assert parsed_body['error']['detail'] == "Invalid credentials"


def test_get_contact_request_invalid_request_id(company_service_rest_api_apithon):
    request_id = generate_uuid()

    response, parsed_body = company_service_rest_api_apithon.get_contact_request(request_id=request_id)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"


def test_get_contact_request_empty_request_id(company_service_rest_api_apithon):
    response, parsed_body = company_service_rest_api_apithon.get_contact_request(request_id=None)
    assert response.status_code == 404
    error_response.validate(parsed_body)

    assert parsed_body['error']['code'] == 404
    assert parsed_body['error']['message'] == "Not Found"
