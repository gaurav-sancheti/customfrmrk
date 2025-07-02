def test_post_contact_request(
        company_service_rest_api, access_token_with_company_write_scope, env_data, company_service_odata_api,
        access_token_with_company_read_scope):
    company_id = env_data['companies']['cc_company_service_test_company']['id']
    body = company_service_rest_api.generate_random_post_contact_request_body()

    response, parsed_body = company_service_rest_api.post_contact_request(
        access_token=access_token_with_company_write_scope, company_id=company_id, body=body)
    assert response.status_code == 201
    assert parsed_body['name'] == body['name']
    assert parsed_body['emailAddress'] == body['emailAddress']

    request_id_filter = {'$filter': f"requestId eq '{parsed_body['requestId']}'"}
    response, response_xml = company_service_odata_api.get_contact_request(
        access_token=access_token_with_company_read_scope, params=request_id_filter)
    assert response.status_code == 200
    assert company_service_odata_api.get_contact_request_name(response_xml) == body['name']
    assert company_service_odata_api.get_contact_request_email_address(response_xml) == body['emailAddress']
