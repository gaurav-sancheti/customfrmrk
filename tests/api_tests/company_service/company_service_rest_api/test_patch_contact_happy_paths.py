def test_patch_contact(company_service_odata_api, company_service_rest_api,
                       access_token_with_company_write_scope, env_data, access_token_with_company_read_scope,
                       company_id_with_contact_id_teardown):
    company_id, contact_id = company_id_with_contact_id_teardown
    body = company_service_rest_api.generate_random_patch_contact_request_body()
    response, parsed_body = company_service_rest_api.patch_contact(
        company_id=company_id, contact_id=contact_id,
        access_token=access_token_with_company_write_scope, body=body)
    assert response.status_code == 200
    assert parsed_body['contactId'] == contact_id
    assert parsed_body['name'] == body['name']

    contact_id_filter = {'$filter': f"contactId eq '{contact_id}'"}
    response, response_xml = company_service_odata_api.get_contact(
        access_token=access_token_with_company_read_scope, params=contact_id_filter)
    assert response.status_code == 200
    assert company_service_odata_api.get_company_name(response_xml) == body['name']
