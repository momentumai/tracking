import yaml


def get_config(environ):
    config = dict()
    with open('./config/base.yaml', 'r') as f:
        config.update(yaml.load(f))

    if ('SERVER_SOFTWARE' in environ and
            environ['SERVER_SOFTWARE'].startswith('Dev')):
        with open('./config/dev.yaml', 'r') as f:
            config.update(yaml.load(f))
    else:
        with open('./config/prod.yaml', 'r') as f:
            config.update(yaml.load(f))

    return config
