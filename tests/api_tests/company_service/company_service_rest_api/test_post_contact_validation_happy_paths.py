def test_post_contact_validation(
        company_service_rest_api, access_token_with_company_contact_validate_scope,
        company_id_with_name_and_validation_hash):
    _, _, validation_hash = company_id_with_name_and_validation_hash

    response, parsed_body = company_service_rest_api.post_contact_validation(
        access_token=access_token_with_company_contact_validate_scope, validation_hash=validation_hash)
    assert response.status_code == 200
    assert parsed_body is None
