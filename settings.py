# Settings for this app.

settings = dict(
    # Server Settings
    http_host = 'localhost',
    http_port = 8080,
)

try:
    # pull in settings_local if it exists
    from settings_local import settings as s
    settings.update(s)
except ImportError:
    pass
