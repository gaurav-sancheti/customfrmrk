def test_delete_contact_request(
        company_service_rest_api, env_data, access_token_with_company_write_scope, company_service_odata_api,
        access_token_with_company_read_scope, company_id_with_request_id_contact_name_and_request_body):
    company_id, request_id, _, _ = company_id_with_request_id_contact_name_and_request_body
    response, parsed_body = company_service_rest_api.delete_contact_request(
        company_id=company_id, request_id=request_id, access_token=access_token_with_company_write_scope)
    assert response.status_code == 204

    request_id_filter = {'$filter': f"requestId eq '{request_id}'"}
    response, response_xml = company_service_odata_api.get_contact_request(
        access_token=access_token_with_company_read_scope, params=request_id_filter)
    assert response.status_code == 200

    assert len(company_service_odata_api.get_contact_requests(response_xml)) == 0
