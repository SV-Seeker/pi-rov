import bison

scheme = bison.Scheme(
    bison.Option('log_level', default='info', choices=['debug', 'info', 'warn', 'error']),
    bison.Option('port', default=9000, field_type=int),
    bison.Option('redis')
)

config = bison.Bison(scheme)


config.config_name = 'rov_config'
config.add_config_paths(
    '.',
    '/tmp/app'
)

config.parse()

__all__ = ['config']
