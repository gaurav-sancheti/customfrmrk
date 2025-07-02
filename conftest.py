import logging

import pytest

from environment_data import env_data_file_utils

pytest.register_assert_rewrite("openid_connect.token_helpers", "selenium_wd.userflow_helpers.stories",
                               "api_clients.sprintr.rfc_7807_validator")


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None,
                     help="Default: None. Supported envs: local, docker, test, accp")
    parser.addoption("--no_docker_proxy", action="store_true", default=False,
                     help="Do not use docker proxy if this flag is provided and --env is docker. Ignored otherwise.")
    parser.addoption("--ngrok", action="store", default=None,
                     help="Provide subdomain,port for ngrok.")
    parser.addoption("--env-overrides", action="store", help="section:option:value separated by ;")
    parser.addoption("--browser", action="store", default=None, help="chrome, firefox")
    parser.addoption("--headless", action="store_true", default=False, help="run in headless mode")
    parser.addoption("--service", action="store", default=None,
                     help="WD service: docker-selenium, default None")


def pytest_report_header(config):
    print(f"{'Environment':12s}: {config.getoption('env')}")

    if config.getoption('browser') is not None:
        browser = f"{config.getoption('browser')} headless" if config.getoption('headless') else config.getoption('browser')
        service = config.getoption('service') if config.getoption('service') is not None else "local"
        print(f"{'Browser':12s}: {browser}")
        print(f"{'Service':12s}: {service}")

    if config.getoption('ngrok') is not None:
        subdomain, port = config.getoption('ngrok').split(',')
        print(f"Ngrok subdomain: {subdomain}, Ngrok localhost port: {port}")


def pytest_configure(config):
    if config.getoption("--collect-only"):
        pass
    else:
        if config.getoption('browser') not in [None, 'chrome', 'firefox']:
            raise pytest.UsageError("browser not supported - %s" % config.getoption('browser'))


def pytest_sessionstart():
    """filters out urllib3 logging in favor of apithon custom logging; urllib3 used by requests library"""
    logging.getLogger("urllib3").setLevel(logging.INFO)


@pytest.fixture(scope="session")
def env_data(request):
    """returns the data from the environment files for the specified environment"""
    environment = request.config.getoption("env")
    docker_proxy = not request.config.getoption("no_docker_proxy")
    return env_data_file_utils.get_env_data(environment, docker_proxy=docker_proxy)


@pytest.hookimpl(tryfirst=True)
def pytest_metadata(metadata):
    """filter metadata because we don't want to show everything in the report"""
    for key in list(metadata.keys()):
        if key not in ["Packages", "Plugins", "Python",
                       "CI_JOB_ID", "CI_PIPELINE_ID"]:
            del metadata[key]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)
