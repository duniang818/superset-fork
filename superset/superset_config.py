# Superset specific config
ROW_LIMIT = 10000
SUPERSET_WEBSERVER_PORT = 9587
# Flask App Builder configuration
# Your App secret key will be used for securely signing the session cookie
# and encrypting sensitive information on the database
# Make sure you are changing this key for your deployment with a strong key.
# Alternatively you can set it with `SUPERSET_SECRET_KEY` environment variable.
# You MUST set this for production environments or the server will not refuse
# to start and you will see an error in the logs accordingly.
# You can generate a strong secure key with openssl rand -base64 42.
SECRET_KEY = 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk'

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# The check_same_thread=false property ensures the sqlite client does not attempt
# to enforce single-threaded access, which may be problematic in some edge cases
# SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/wang.yumei7/.superset/examples.db?check_same_thread=false'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:wym2023@localhost/pam_test?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql://root:wym2023@localhost/ss_dev?charset=utf8'
# SESSION_COOKIE_SAMESITE = None

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = False
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''
LOGO_TARGET_PATH = "/static/assets/images/superset-logo.png"
APP_ICON = "/static/assets/images/app.png"
#在ALLOWED_EXTENSIONS中添加xls和xlsx
# ALLOWED_EXTENSIONS = {"csv", "tsv","xls","xlsx"}
# 默认语言为中文
BABEL_DEFAULT_LOCALE = "zh"

