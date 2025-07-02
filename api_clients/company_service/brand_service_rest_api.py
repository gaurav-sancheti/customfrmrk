import logging
import os

from api_clients.apithon import ApithonRestJWT

from environment_data.data_convertors import convert_file_from_location_to_base64_encoded_string


class BrandServiceRESTAPI(ApithonRestJWT):
    def __init__(self, env_data):
        logger = logging.getLogger("instr.log").getChild(__name__)
        base_url = f"{env_data['company_service']['base_url']}/rest/brand-service/v1"
        super().__init__(env_data=env_data, logger=logger, base_url=base_url)
        self.mxid3_client = "cc_brand_service_client"
        self.env_data = env_data

    def patch_brand(self, company_id, access_token, body):
        response, parsed_body = self.patch(resource_url=f'/companies/{company_id}/brand', token=access_token, json=body)
        return response, parsed_body

    def get_brand(self, company_id, access_token):
        response, parsed_body = self.get(resource_url=f'/companies/{company_id}/brand', token=access_token)
        return response, parsed_body

    @staticmethod
    def get_file_path(file_extension=None):

        if file_extension == 'png':
            file_path = "resources/images/CaptainComic.png"
        elif file_extension == 'bmp':
            file_path = "resources/images/marbles.bmp"
        elif file_extension == 'xlsx':
            file_path = "resources/files/example.xlsx"
        else:
            file_path = "resources/images/virtual_gaming.jpeg"

        return file_path

    @staticmethod
    def get_brand_request_body(file_extension1=None, file_extension2=None):

        return {

            "logo": {
                "base64Content": convert_file_from_location_to_base64_encoded_string(
                    os.path.abspath(BrandServiceRESTAPI.get_file_path(file_extension1)))
            },
            "coverImage": {
                "base64Content": convert_file_from_location_to_base64_encoded_string(
                    os.path.abspath(BrandServiceRESTAPI.get_file_path(file_extension2)))
            }

        }
