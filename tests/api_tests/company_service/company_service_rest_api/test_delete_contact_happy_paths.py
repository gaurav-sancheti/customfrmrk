def test_delete_contact(
        company_service_rest_api, env_data, access_token_with_company_write_scope,
        company_service_odata_api, access_token_with_company_read_scope,
        company_id_and_name_having_contact_validated):
    company_id, name = company_id_and_name_having_contact_validated

    name_filter = {'$filter': f"name eq '{name}'"}
    response, response_xml = company_service_odata_api.get_contact(
        access_token=access_token_with_company_read_scope, params=name_filter)
    assert response.status_code == 200

    contact_id = company_service_odata_api.get_contact_id(response_xml)

    response, parsed_body = company_service_rest_api.delete_contact(
        company_id=company_id, contact_id=contact_id, access_token=access_token_with_company_write_scope)
    assert response.status_code == 204

    contact_id_filter = {'$filter': f"contactId eq '{contact_id}'"}
    response, response_xml = company_service_odata_api.get_contact(
        access_token=access_token_with_company_read_scope, params=contact_id_filter)
    assert response.status_code == 200

    assert len(company_service_odata_api.get_contacts(response_xml)) == 0
