from locust import HttpUser, task, between

from api_clients.mxid3.mxid3_token_helper import MxID3TokenHelper
from api_clients.mxid3.scopes_list import Scopes
from environment_data import env_data_file_utils

ENV_TO_USE = 'test'
env_data = env_data_file_utils.get_env_data(ENV_TO_USE)
scopes = [Scopes.mx_company_read]
access_token = (
    MxID3TokenHelper(env_data, 'cc_company_service_client').generate_tokens_as_backend_credentials(scopes))


class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def my_task(self):
        with self.client.get(
                "https://quality.mendixcloud.com/odata/company-service/v1/companies",
                headers={'Authorization': f"'Bearer {access_token}'"}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Unexpected response content")
