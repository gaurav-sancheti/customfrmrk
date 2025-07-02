def test_get_companies(company_service_odata_api, access_token_with_company_read_scope):
    response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope)
    assert response.status_code == 200
    assert company_service_odata_api.get_company_count(response_xml) > 0


def test_get_company_by_company_id(env_data, company_service_odata_api, access_token_with_company_read_scope):
    company_id = env_data['companies']['cc_company_for_get_operations']['id']
    company_id_filter = {'$filter': f"companyId eq '{company_id}'"}
    response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_id_filter)
    assert response.status_code == 200
    assert company_service_odata_api.get_company_name(response_xml) == \
           env_data['companies']['cc_company_for_get_operations']['name']


def test_get_company_by_company_name(env_data, company_service_odata_api, access_token_with_company_read_scope):
    company_name = env_data['companies']['cc_company_for_get_operations']['name']
    company_name_filter = {'$filter': f"name eq '{company_name}'"}
    response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_name_filter)
    assert response.status_code == 200
    assert company_service_odata_api.get_company_id(response_xml) == \
           env_data['companies']['cc_company_for_get_operations']['id']


def test_get_company_modified_between_a_period_of_time(env_data, company_service_odata_api,
                                                       access_token_with_company_read_scope):
    company_modified_date_filter =\
        {'$filter': "modifiedAt gt '2024-02-11' and modifiedAt lt '2024-03-05'"}
    response, response_xml = company_service_odata_api.get_company(
        access_token=access_token_with_company_read_scope, params=company_modified_date_filter)
    assert response.status_code == 200
    assert company_service_odata_api.get_company_id(response_xml) == \
           env_data['companies']['cc_test_company_modified_on_a_specific_date']['id']
