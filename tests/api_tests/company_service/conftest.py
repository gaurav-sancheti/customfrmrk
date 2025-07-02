import pytest
from api_clients.company_service.brand_service_rest_api import BrandServiceRESTAPI
from api_clients.company_service.company_service_odata_api import CompanyServiceODataAPI
from api_clients.company_service.company_service_rest_api import CompanyServiceRESTAPI, CompanyServiceRESTAPIApithon
from api_clients.mxid3.mxid3_token_helper import MxID3TokenHelper
from api_clients.mxid3.scopes_list import Scopes

from environment_data.data_convertors import convert_string_to_base64_encoded_string
from environment_data.data_generators import generate_random_email_domain, generate_random_string_of_letters
from tests.api_tests.company_service.schemas import brand_response


@pytest.fixture(scope='function')
def company_service_rest_api(env_data):
    company_service_rest_api = CompanyServiceRESTAPI(env_data=env_data)
    return company_service_rest_api


@pytest.fixture(scope='function')
def brand_service_rest_api(env_data):
    brand_service_rest_api = BrandServiceRESTAPI(env_data=env_data)
    return brand_service_rest_api


@pytest.fixture(scope='function')
def company_service_odata_api(env_data):
    company_service_odata_api = CompanyServiceODataAPI(env_data=env_data)
    return company_service_odata_api


@pytest.fixture(scope='function')
def company_service_rest_api_apithon(env_data):
    company_service_rest_api_apithon = CompanyServiceRESTAPIApithon(env_data=env_data)
    return company_service_rest_api_apithon


@pytest.fixture(scope="function")
def access_token_with_company_read_scope(env_data):
    scopes = [Scopes.mx_company_read]
    access_token = \
        MxID3TokenHelper(env_data, 'cc_company_service_client').generate_tokens_as_backend_credentials(scopes)
    return access_token


@pytest.fixture(scope="function")
def access_token_with_company_write_scope(env_data):
    scopes = [Scopes.mx_company_write]
    access_token = \
        MxID3TokenHelper(env_data, 'cc_company_service_client').generate_tokens_as_backend_credentials(scopes)
    return access_token


@pytest.fixture(scope="function")
def access_token_with_company_contact_validate_scope(env_data):
    scopes = [Scopes.mx_company_contact_validate]
    access_token = \
        MxID3TokenHelper(env_data, 'evs_company_service_client').generate_tokens_as_backend_credentials(scopes)
    return access_token


@pytest.fixture(scope="function")
def access_token_with_brand_write_scope(env_data):
    scopes = [Scopes.mx_company_brand_write]
    access_token = MxID3TokenHelper(env_data, 'cc_brand_service_client').generate_tokens_as_backend_credentials(scopes)
    return access_token


@pytest.fixture(scope="function")
def invalid_access_token_based_on_random_base64_encoded_string():
    random_string = generate_random_string_of_letters(100)
    convert_string_to_base64_encoded_string(random_string)
    return convert_string_to_base64_encoded_string


@pytest.fixture(scope="function")
def random_email_domain_for_existing_company(
        env_data, company_service_rest_api, access_token_with_company_write_scope):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    random_email_body = [
        {
            "domain": generate_random_email_domain(lower_case_only=True)
        }
    ]

    response, parsed_body = company_service_rest_api.post_email_domains(
        company_id=company_id, access_token=access_token_with_company_write_scope, body=random_email_body)
    assert response.status_code == 201
    email_domain = parsed_body[0]['domain']

    return company_id, email_domain


@pytest.fixture(scope="function")
def random_email_domain_for_existing_company_with_teardown(
        random_email_domain_for_existing_company, env_data, access_token_with_company_write_scope,
        company_service_rest_api):
    company_id, email_domain = random_email_domain_for_existing_company

    yield company_id, email_domain

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=email_domain, access_token=access_token_with_company_write_scope)
    assert response.status_code == 204


@pytest.fixture(scope="function")
def get_uuid_of_company_with_images(brand_service_rest_api, env_data,
                                    access_token_with_brand_write_scope,
                                    access_token_with_company_read_scope):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    return company_id


@pytest.fixture(scope='function')
def new_company_without_brand(env_data, company_service_rest_api, access_token_with_company_write_scope):
    body = company_service_rest_api.generate_random_post_company_request_body()

    response, parsed_body = company_service_rest_api.post_company(
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 201

    return parsed_body['companyId']


@pytest.fixture(scope='function')
def company_id_with_request_id_contact_name_and_request_body(
        company_service_odata_api, company_service_rest_api, access_token_with_company_write_scope, env_data):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    body = company_service_rest_api.generate_random_post_contact_request_body()
    name = body['name']

    response, parsed_body = company_service_rest_api.post_contact_request(
        access_token=access_token_with_company_write_scope, company_id=company_id, body=body)
    assert response.status_code == 201
    request_id = parsed_body['requestId']
    return company_id, request_id, name, body


@pytest.fixture(scope='function')
def contact_request_body_and_request_id_with_teardown(
        company_service_odata_api, company_service_rest_api, access_token_with_company_write_scope, env_data,
        company_id_with_request_id_contact_name_and_request_body):
    company_id, request_id, _, body = company_id_with_request_id_contact_name_and_request_body
    yield body, request_id

    response, parsed_body = company_service_rest_api.delete_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope)
    assert response.status_code == 204


@pytest.fixture(scope='function')
def company_id_and_name_having_contact_validated(
        company_service_rest_api, access_token_with_company_contact_validate_scope,
        company_id_with_name_and_validation_hash):

    company_id, name, validation_hash = company_id_with_name_and_validation_hash

    response, parsed_body = company_service_rest_api.post_contact_validation(
        access_token=access_token_with_company_contact_validate_scope, validation_hash=validation_hash)
    assert response.status_code == 200
    return company_id, name


@pytest.fixture(scope='function')
def company_id_with_name_and_validation_hash(
        company_id_with_request_id_contact_name_and_request_body, company_service_rest_api_apithon):
    company_id, request_id, name, _ = company_id_with_request_id_contact_name_and_request_body

    get_response, get_response_body = company_service_rest_api_apithon.get_contact_request(request_id=request_id)
    assert get_response.status_code == 200

    validation_hash = get_response_body['validationHash']
    return company_id, name, validation_hash


@pytest.fixture(scope='function')
def company_id_with_contact_id_teardown(
        company_service_rest_api, company_service_odata_api, company_id_and_name_having_contact_validated,
        access_token_with_company_read_scope, access_token_with_company_write_scope):
    company_id, name = company_id_and_name_having_contact_validated

    name_filter = {'$filter': f"name eq '{name}'"}
    response, response_xml = company_service_odata_api.get_contact(
        access_token=access_token_with_company_read_scope, params=name_filter)
    assert response.status_code == 200

    contact_id = company_service_odata_api.get_contact_id(response_xml)

    yield company_id, contact_id

    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id, access_token=access_token_with_company_write_scope)
    assert response.status_code == 204
