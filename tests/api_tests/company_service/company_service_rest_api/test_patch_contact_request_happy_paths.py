def test_patch_contact_request(
        company_service_rest_api, company_service_odata_api, access_token_with_company_write_scope,
        access_token_with_company_read_scope, env_data, contact_request_body_and_request_id_with_teardown):
    company_id = env_data['companies']['cc_company_for_patch_operations']['id']
    body, request_id = contact_request_body_and_request_id_with_teardown
    response, parsed_body = company_service_rest_api.patch_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 200
    assert parsed_body['requestId'] == request_id
    assert parsed_body['name'] == body['name']

    request_id_filter = {'$filter': f"requestId eq '{request_id}'"}
    response, response_xml = company_service_odata_api.get_contact_request(
        access_token=access_token_with_company_read_scope, params=request_id_filter)
    assert response.status_code == 200
    assert company_service_odata_api.get_contact_request_id(response_xml) == request_id
    assert company_service_odata_api.get_contact_request_name(response_xml) == body['name']
