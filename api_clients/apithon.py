import json
import xml.etree.ElementTree as XmlTree
from types import SimpleNamespace

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth

NOTHING = object()
DEFAULT_REQUEST_TIMEOUT = 30


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs["timeout"]
        del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Apithon(requests.Session):
    def __init__(self, env_data, logger):
        super().__init__()
        self.logger = logger
        self.hooks['response'].append(self._log_details)
        # Mount it for both http and https usage
        adapter = TimeoutHTTPAdapter(timeout=DEFAULT_REQUEST_TIMEOUT)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

        if env_data['env_metadata']['env'] == "docker" and env_data['env_metadata']['docker_proxy'] is True:
            proxy = 'localhost:1080'
            self.proxies = {
                'http': f'socks5h://{proxy}',
                'https': f'socks5h://{proxy}'
            }
            self.logger.info(f"Apithon proxy: {self.proxies}")

    def _log_details(self, response, *args, **kwargs):
        log_message_request = f"API request\n" \
                              f"{response.request.method} - {response.request.url}\n" \
                              f"headers: {response.request.headers}\n" \
                              f"request body:\n{response.request.body}"
        self.logger.info(log_message_request)

        log_message_response = f"API response\n" \
                               f"status {response.status_code}, reason: {response.reason}, " \
                               f"elapsed: {response.elapsed.total_seconds()}\n" \
                               f"headers: {response.headers}\n" \
                               f"response body:\n{response.text}"
        self.logger.info(log_message_response)

    def call_api(self, request):
        response = self.send(request.prepare())
        self._log_details(response)
        return response


class ApithonRestBasicAuth(Apithon):
    def __init__(self, env_data, logger, base_url, default_username=None, default_password=None):
        self.base_url = base_url
        self.default_username = default_username
        self.default_password = default_password
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def delete(self, resource_url, username=NOTHING, password=NOTHING, **kwargs):
        username = self.default_username if username is NOTHING else username
        password = self.default_password if password is NOTHING else password
        url = f"{self.base_url}{resource_url}"

        response = super().delete(url, auth=None if username is None and password is None else HTTPBasicAuth(username,
                                                                                                             password),
                                  **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def get(self, resource_url, username=NOTHING, password=NOTHING, **kwargs):
        username = self.default_username if username is NOTHING else username
        password = self.default_password if password is NOTHING else password
        url = f"{self.base_url}{resource_url}"

        response = super().get(url, auth=None if username is None and password is None else HTTPBasicAuth(username,
                                                                                                          password),
                               **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def post(self, resource_url, username=NOTHING, password=NOTHING, **kwargs):
        username = self.default_username if username is NOTHING else username
        password = self.default_password if password is NOTHING else password
        url = f"{self.base_url}{resource_url}"

        response = super().post(url,
                                auth=None if username is None and password is None
                                else HTTPBasicAuth(username, password),
                                **kwargs
                                )
        response_body = self._parse_response(response)

        return response, response_body

    def put(self, resource_url, username=NOTHING, password=NOTHING, **kwargs):
        username = self.default_username if username is NOTHING else username
        password = self.default_password if password is NOTHING else password
        url = f"{self.base_url}{resource_url}"

        response = super().put(url,
                               auth=None if username is None and password is None
                               else HTTPBasicAuth(username, password),
                               **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def patch(self, resource_url, username=NOTHING, password=NOTHING, **kwargs):
        username = self.default_username if username is NOTHING else username
        password = self.default_password if password is NOTHING else password
        url = f"{self.base_url}{resource_url}"

        response = super().patch(url,
                                 auth=None if username is None and password is None
                                 else HTTPBasicAuth(username, password),
                                 **kwargs)
        response_body = self._parse_response(response)

        return response, response_body


class ApithonRestJWT(Apithon):
    def __init__(self, env_data, logger, base_url, auth_header=None, accept_header=None):
        self.base_url = base_url
        self.auth_header = auth_header
        self.accept_header = accept_header
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def post(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().post(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def get(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def put(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().put(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def delete(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().delete(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def patch(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().patch(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body


class ApithonRestApiKey(Apithon):
    def __init__(self, env_data, logger, base_url):
        self.base_url = base_url
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def get(self, resource_url, username=NOTHING, apikey=NOTHING, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if username is not NOTHING:
            headers['Mendix-Username'] = username
        if apikey is not NOTHING:
            headers['Mendix-ApiKey'] = apikey

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def post(self, resource_url, username=NOTHING, apikey=NOTHING, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if username is not NOTHING:
            headers['Mendix-Username'] = username
        if apikey is not NOTHING:
            headers['Mendix-ApiKey'] = apikey

        url = f'{self.base_url}{resource_url}'

        response = super().post(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body


class ApithonRestCPUserSession(Apithon):
    def __init__(self, env_data, logger, base_url):
        self.base_url = base_url
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def get(self, resource_url, username=NOTHING, password=NOTHING, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if username is not NOTHING:
            headers['Mendix-Username'] = username
        if password is not NOTHING:
            headers['Mendix-Password'] = password

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body


class ApithonSoap(Apithon):
    def __init__(self, env_data, logger):
        super().__init__(env_data=env_data, logger=logger)

    def soap(self, url, xml_template, data, **kwargs):
        xmltpl = open(xml_template, 'r').read()
        request_message = xmltpl.format(**data)

        response = super().post(url,
                                data=request_message,
                                headers={'Content-Type': 'application/xml'},
                                **kwargs)

        try:
            response_xml = XmlTree.fromstring(response.text)
        except XmlTree.ParseError as err:
            err.msg = "Failed to parse response with status %s:\n %s" % (response.status_code, response.text)
            raise

        return response, response_xml


class ApithonOData(Apithon):
    def __init__(self, env_data, logger, url, default_username, default_password):
        self.url = url
        self.default_username = default_username
        self.default_password = default_password
        super().__init__(env_data=env_data, logger=logger)

    def get_odata(self, entity, username=NOTHING, password=NOTHING, **kwargs):
        username = self.default_username if username is NOTHING else username
        password = self.default_password if password is NOTHING else password
        response = super().get(self.url + entity,
                               auth=None if username is None and password is None
                               else HTTPBasicAuth(username, password),
                               **kwargs)

        try:
            response_xml = XmlTree.fromstring(response.text)
        except XmlTree.ParseError as err:
            err.msg = "Failed to parse response with status %s:\n %s" % (response.status_code, response.text)
            raise

        return response, response_xml


class ApithonRestPAT(Apithon):
    def __init__(self, env_data, logger, base_url, auth_header=None, accept_header=None):
        self.base_url = base_url
        self.auth_header = auth_header
        self.accept_header = accept_header
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def post(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"MxToken {token}"

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().post(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def patch(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"MxToken {token}"

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().patch(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def get(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"MxToken {token}"

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def put(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"MxToken {token}"

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().put(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def delete(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"MxToken {token}"

        if self.accept_header is not None:
            headers.update(self.accept_header)

        url = f"{self.base_url}{resource_url}"

        response = super().delete(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body


class ApithonODataJWT(Apithon):
    def __init__(self, env_data, logger, base_url, auth_header=None):
        self.base_url = base_url
        self.auth_header = auth_header
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response, json_resp):
        if response.text and json_resp is False:
            try:
                response_xml = XmlTree.fromstring(response.text)
                return response_xml
            except XmlTree.ParseError as err:
                err.msg = "Failed to parse response with status %s:\n %s" % (response.status_code, response.text)
                raise
        else:
            parsed_body = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
            return parsed_body

    def get_odata(self, resource_url, token=None, headers=None, json_resp=False, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response, json_resp)

        return response, response_body


class ApithonODataJsonJWT(Apithon):
    def __init__(self, env_data, logger, base_url, auth_header=None):
        self.base_url = base_url
        self.auth_header = auth_header
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def get_odata(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def post_odata(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        url = f"{self.base_url}{resource_url}"

        response = super().post(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def patch_odata(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        url = f"{self.base_url}{resource_url}"

        response = super().patch(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def delete_odata(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            if self.auth_header is None:
                headers['Authorization'] = f"Bearer {token}"
            else:
                headers[self.auth_header] = token

        url = f"{self.base_url}{resource_url}"

        response = super().delete(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body


class ApithonCustomAuthToken(Apithon):
    def __init__(self, env_data, logger, base_url, auth_header=None):
        self.base_url = base_url
        self.auth_header = auth_header
        super().__init__(env_data=env_data, logger=logger)

    @staticmethod
    def _parse_response(response):
        if response.text:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return None

    def post(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"Custom-Auth {token}"

        url = f"{self.base_url}{resource_url}"

        response = super().post(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def get(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"Custom-Auth {token}"

        url = f"{self.base_url}{resource_url}"

        response = super().get(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def put(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"Custom-Auth {token}"

        url = f"{self.base_url}{resource_url}"

        response = super().put(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def delete(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"Custom-Auth {token}"

        url = f"{self.base_url}{resource_url}"

        response = super().delete(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body

    def patch(self, resource_url, token=None, headers=None, **kwargs):
        headers = {} if headers is None else headers
        if token is not None:
            headers['Authorization'] = f"Custom-Auth {token}"

        url = f"{self.base_url}{resource_url}"

        response = super().patch(url, headers=headers, **kwargs)
        response_body = self._parse_response(response)

        return response, response_body
