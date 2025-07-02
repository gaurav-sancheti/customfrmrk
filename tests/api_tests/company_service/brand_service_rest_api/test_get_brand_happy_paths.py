from tests.api_tests.company_service.schemas import brand_response


def test_get_brand_with_only_logo_for_company(brand_service_rest_api, env_data,
                                              access_token_with_company_read_scope):
    company_id = env_data['companies']['company_with_only_logo']['id']

    response, parsed_body = brand_service_rest_api.get_brand(company_id=company_id,
                                                             access_token=access_token_with_company_read_scope)
    assert response.status_code == 200
    brand_response.validate(parsed_body)
    assert parsed_body['logo']['location'] == env_data['companies']['company_with_only_logo']['logo_url']
    assert parsed_body['coverImage']['location'] is None


def test_get_brand_with_only_cover_image_for_company(brand_service_rest_api, env_data,
                                                     access_token_with_company_read_scope):
    company_id = env_data['companies']['company_with_only_cover_image']['id']

    response, parsed_body = brand_service_rest_api.get_brand(company_id=company_id,
                                                             access_token=access_token_with_company_read_scope)
    assert response.status_code == 200
    brand_response.validate(parsed_body)
    assert parsed_body['logo']['location'] is None
    assert parsed_body['coverImage']['location'] == env_data['companies']['company_with_only_cover_image'][
        'cover_image_url']


def test_get_brand_for_company(brand_service_rest_api, env_data, access_token_with_company_read_scope):
    company_id = env_data['companies']['cc_company_for_get_operations']['id']

    response, parsed_body = brand_service_rest_api.get_brand(company_id=company_id,
                                                             access_token=access_token_with_company_read_scope)
    assert response.status_code == 200
    brand_response.validate(parsed_body)
    assert parsed_body['logo']['location'] == env_data['companies']['cc_company_for_get_operations']['logo_url']
    assert parsed_body['coverImage']['location'] == env_data['companies']['cc_company_for_get_operations'][
        'cover_image_url']
