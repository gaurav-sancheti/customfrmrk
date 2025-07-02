def test_get_company_using_token_with_non_required_scope(
        company_service_odata_api, access_token_with_company_write_scope):

    response, parsed_body = company_service_odata_api.get_company(
        access_token=access_token_with_company_write_scope, headers={'Accept': 'application/xml'})
    assert response.status_code == 401
    assert "You are not authorized to access this resource" in response.text


def test_get_company_with_invalid_token(company_service_odata_api,
                                        invalid_access_token_based_on_random_base64_encoded_string):

    response, parsed_body = company_service_odata_api.get_company(
        access_token=invalid_access_token_based_on_random_base64_encoded_string, headers={'Accept': 'application/xml'})
    assert response.status_code == 401
    assert "You are not authorized to access this resource" in response.text
