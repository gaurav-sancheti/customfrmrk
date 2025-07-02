import re

from tests.api_tests.company_service.schemas import brand_response


def assert_asset_location(asset_location, file_base_url, file_extension):
    uuid_regex = r"[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    asset_regex = file_base_url + uuid_regex + file_extension
    assert re.match(asset_regex, asset_location)


def test_patch_brand_with_jpg_logo_and_cover_image(brand_service_rest_api, env_data,
                                                   access_token_with_brand_write_scope,
                                                   access_token_with_company_read_scope,
                                                   get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert get_response.status_code == 200

    assert_asset_location(get_response_body['logo']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['logo_base_url'], '.jpg')

    assert_asset_location(get_response_body['coverImage']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['cover_image_base_url'], '.jpg')


def test_patch_brand_with_png_logo_and_cover_image(brand_service_rest_api, env_data,
                                                   access_token_with_brand_write_scope,
                                                   access_token_with_company_read_scope,
                                                   get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body(file_extension1='png', file_extension2='png')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert get_response.status_code == 200

    assert_asset_location(get_response_body['logo']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['logo_base_url'], '.png')

    assert_asset_location(get_response_body['coverImage']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['cover_image_base_url'], '.png')


def test_patch_brand_with_png_logo_and_jpg_cover_image(brand_service_rest_api, env_data,
                                                       access_token_with_brand_write_scope,
                                                       access_token_with_company_read_scope,
                                                       get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body(file_extension1='png', file_extension2='jpg')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert get_response.status_code == 200

    assert_asset_location(get_response_body['logo']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['logo_base_url'], '.png')

    assert_asset_location(get_response_body['coverImage']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['cover_image_base_url'], '.jpg')


def test_patch_brand_without_cover_image(brand_service_rest_api, env_data,
                                         access_token_with_brand_write_scope,
                                         access_token_with_company_read_scope, get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body()
    body.pop('coverImage')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert_asset_location(get_response_body['logo']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['logo_base_url'], '.jpg')

    assert_asset_location(get_response_body['coverImage']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['cover_image_base_url'], '.jpg')


def test_patch_brand_without_logo(brand_service_rest_api, env_data, access_token_with_brand_write_scope,
                                  access_token_with_company_read_scope, get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body()
    body.pop("logo")

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert_asset_location(get_response_body['logo']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['logo_base_url'], '.jpg')

    assert_asset_location(get_response_body['coverImage']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['cover_image_base_url'], '.jpg')


def test_patch_brand_with_empty_logo(brand_service_rest_api, env_data,
                                     access_token_with_brand_write_scope,
                                     access_token_with_company_read_scope, get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body()
    body['logo'].pop('base64Content')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert get_response_body['logo']['location'] is None

    assert_asset_location(get_response_body['coverImage']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['cover_image_base_url'], '.jpg')


def test_patch_brand_with_empty_cover_image(brand_service_rest_api, env_data,
                                            access_token_with_brand_write_scope,
                                            access_token_with_company_read_scope, get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body()
    body['coverImage'].pop('base64Content')
    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert_asset_location(get_response_body['logo']['location'],
                          env_data['companies']['cc_company_for_patch_operations']['logo_base_url'], '.jpg')

    assert get_response_body['coverImage']['location'] is None


def test_patch_brand_with_empty_logo_and_cover_image(brand_service_rest_api, env_data,
                                                     access_token_with_brand_write_scope,
                                                     access_token_with_company_read_scope,
                                                     get_uuid_of_company_with_images):
    company_id = get_uuid_of_company_with_images
    body = brand_service_rest_api.get_brand_request_body()
    body['logo'].pop('base64Content')
    body['coverImage'].pop('base64Content')

    response, parsed_body = brand_service_rest_api.patch_brand(company_id=company_id,
                                                               access_token=access_token_with_brand_write_scope,
                                                               body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)

    assert get_response_body['logo']['location'] is None
    assert get_response_body['coverImage']['location'] is None


def test_patch_company_without_brand(
        new_company_without_brand, brand_service_rest_api, access_token_with_brand_write_scope,
        access_token_with_company_read_scope, env_data):
    company_id = new_company_without_brand

    body = brand_service_rest_api.get_brand_request_body()

    response, parsed_body = brand_service_rest_api.patch_brand(
        company_id=company_id, access_token=access_token_with_brand_write_scope, body=body)
    assert response.status_code == 200
    brand_response.validate(parsed_body)

    get_response, get_response_body = brand_service_rest_api.get_brand(
        company_id=company_id, access_token=access_token_with_company_read_scope)
    assert get_response.status_code == 200

    assert get_response_body['logo']['location'] == parsed_body['logo']['location']
    assert get_response_body['coverImage']['location'] == parsed_body['coverImage']['location']
