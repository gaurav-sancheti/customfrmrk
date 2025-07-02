import logging

from api_clients.apithon import ApithonRestBasicAuth
from api_clients.mxid3.oauth2_grants_api import Oauth2GrantsAPI
from api_clients.mxid3.scopes_list import Scopes


class MxID3TokenHelper(ApithonRestBasicAuth):

    def __init__(self, env_data, client):
        base_url = env_data['mxid3']['base_url']
        self.oauth2_grants_api = Oauth2GrantsAPI(env_data, client)
        self.direct_authz_token = None

        logger = logging.getLogger("instr.log").getChild(__name__)
        super().__init__(env_data=env_data, logger=logger, base_url=base_url)

    def _retrieve_direct_authz_token(self):
        response_body = self.oauth2_grants_api.request_client_credentials_token(Scopes.mx_client_auth_direct_v1)
        self.direct_authz_token = response_body['access_token']
        return self.direct_authz_token

    def _perform_direct_authz_request(self, openid_uuid, scopes, access_token_expiry, id_token_expiry,
                                      refresh_token_expiry):
        resource_url = '/oauth/direct'
        request_body = {
            'sub': openid_uuid,
            'scp': ' '.join(scopes),
            'access_token_exp': access_token_expiry,
            'id_token_exp': id_token_expiry,
            'refresh_token_exp': refresh_token_expiry
        }

        counter = 0
        while counter < 3:
            if self.direct_authz_token is None:
                self._retrieve_direct_authz_token()

            response, response_body = self.post(resource_url,
                                                data=request_body,
                                                headers={
                                                    'Authorization': f'Bearer {self.direct_authz_token}'
                                                })
            if response.status_code == 200:
                break
            elif response.status_code == 403:
                self.direct_authz_token = None
                self.logger.info('Current bearer token has expired. Retrieving a new bearer token.')
                counter += 1
            else:
                raise Exception(
                    f'Unexpected response. Response was {response.status_code} : {response.reason}, \n{response.text}')
        else:
            raise Exception('Unable to get bearer token. Giving up...')

        return response_body

    def generate_tokens_for_user(self, openid_uuid, scopes, access_token_expiry=900, id_token_expiry=1800,
                                 refresh_token_expiry=3600):
        response_body = self._perform_direct_authz_request(openid_uuid, scopes, access_token_expiry, id_token_expiry,
                                                           refresh_token_expiry)

        access_token = response_body['access_token'] if 'access_token' in response_body else None
        id_token = response_body['id_token'] if 'id_token' in response_body else None
        refresh_token = response_body['refresh_token'] if 'refresh_token' in response_body else None
        return access_token, id_token, refresh_token

    def generate_tokens_as_backend_credentials(self, scopes):
        response_body = self.oauth2_grants_api.request_client_credentials_token(scopes)
        access_token = response_body['access_token'] if 'access_token' in response_body else None
        return access_token
