
user = 'username'
password = '1234567'
dbname = 'name of database'
host = 'host address'

try:
    from _settings_local import *
except ImportError:
    pass

user = local_user
password = local_password
dbname = local_dbname
host = local_host




