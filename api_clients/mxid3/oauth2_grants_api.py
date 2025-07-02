import logging

from api_clients.apithon import ApithonRestBasicAuth


class Oauth2GrantsAPI(ApithonRestBasicAuth):

    def __init__(self, env_data, client):
        self.base_url = env_data['mxid3']['base_url']
        self.client_id = env_data['mxid3'][client]['client_id']
        self.client_secret = env_data['mxid3'][client]['client_secret']
        logger = logging.getLogger("instr.log").getChild(__name__)
        super().__init__(env_data=env_data, logger=logger, base_url=self.base_url)

    def request_client_credentials_token(self, scopes):
        resource_url = '/oauth/token'
        response, response_body = self.post(resource_url, data={
            'grant_type': 'client_credentials',
            'scope': scopes,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })
        return response_body

    def request_custom_client_credentials_token(self, client_id, client_secret, scopes):
        resource_url = '/oauth/token'
        response, response_body = self.post(resource_url, data={
            'grant_type': 'client_credentials',
            'scope': scopes,
            'client_id': client_id,
            'client_secret': client_secret
        })
        return response_body
