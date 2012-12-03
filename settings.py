# Settings for this app.

settings = dict(
    # You MUST update the author, uin, and agree_to_honor_code fields before you
    # turn this assignment in.
    author = "Brandon Adame",
    uin = '417-00-3871',
    agree_to_honor_code = True,

    # the collaborators list contains tuples of 2 items, the name of the helper
    # and their contribution to your homework assignments
    collaborators = {
        ('Dr. Caverlee','taught csce 470'),
        ('http://stackoverflow.com/questions/9171158/how-do-you-get-the-magnitude-of-a-vector-in-numpy','quick function for the magnitude of a vector'),
    },

    # You probably don't need to mess with these settings.
    http_host = 'localhost',
    http_port = 8080,
    couch_host = 'localhost',
    couch_port = 5984,
    couch_password = '',
)

try:
    # pull in settings_local if it exists
    from settings_local import settings as s
    settings.update(s)
except ImportError:
    pass
