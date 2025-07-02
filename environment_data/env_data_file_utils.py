from pathlib import Path

import yaml


def get_env_data(environment, docker_proxy=True):
    envdata_dir = Path(__file__).absolute().parent

    env_data = {}

    if environment.startswith('local_'):
        restofit = environment.split('_', 1)[1]
        envdata_file = envdata_dir.joinpath('local').joinpath(f'{restofit}.yml')
        with envdata_file.open() as yaml_file:
            yaml_contents = yaml.full_load(yaml_file)
            env_data.update(yaml_contents)

    else:
        for envdata_file in envdata_dir.joinpath(environment).glob('*.yml'):
            with envdata_file.open() as yaml_file:
                yaml_contents = yaml.full_load(yaml_file)
                env_data.update(yaml_contents)

        base_urls = _get_base_urls(environment)
        env_data = _dict_iterate(env_data, base_urls)

    env_metadata = {
            'env': environment,
            'docker_proxy': docker_proxy if environment == "docker" else None
    }
    env_data.update({'env_metadata': env_metadata})
    return env_data


def _dict_iterate(dictionary, replacements):
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            _dict_iterate(dictionary[key], replacements)
        elif isinstance(dictionary[key], str):
            dictionary[key] = dictionary[key].format(**replacements)
        else:
            continue
    return dictionary


def _get_base_urls(environment):
    base_url_file = Path(__file__).absolute().parent.joinpath("base_urls.yml")

    with base_url_file.open() as yaml_file:
        base_urls = yaml.full_load(yaml_file)

    environment_base_urls = base_urls[environment]

    return environment_base_urls
