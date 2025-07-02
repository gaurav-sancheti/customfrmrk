def test_delete_email_domain(
        company_service_rest_api, env_data, access_token_with_company_write_scope,
        random_email_domain_for_existing_company, company_service_odata_api, access_token_with_company_read_scope):
    company_id, domain = random_email_domain_for_existing_company

    response, parsed_body = company_service_rest_api.delete_email_domain(
        company_id=company_id, domain=domain, access_token=access_token_with_company_write_scope)
    assert response.status_code == 204

    company_id_filter = {'$filter': f"companyId eq '{company_id}'", '$expand': 'emailDomains'}
    get_response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert get_response.status_code == 200

    domains = company_service_odata_api.get_domains(response_xml)
    assert len([domain for domain in domains if domain.text == domain]) == 0
