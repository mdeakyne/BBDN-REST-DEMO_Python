# constants file for BBDN-REST_DEMO-Python

# Auth configuration
# Example Only. Change to your secret
SECRET = "YRtx6Irib8s9cvyTUgNYV83Y6tVPosOq"

# Example Only. Change to your key
KEY = "b83583be-85c5-4464-8398-02fde2d1737e"

CREDENTIALS = 'client_credentials'
PAYLOAD = {
    'grant_type': 'client_credentials',
    'token': None
}
TOKEN = None
EXPIRES_AT = ''

REST_BASE_PATH = '/learn/api/public/v1/'
REST_TYPE = {
    'courses': REST_BASE_PATH + 'courses',
    'users': REST_BASE_PATH + 'users',
    'terms': REST_BASE_PATH + 'terms',
    'memberships': REST_BASE_PATH + 'memberships',
    'data_sources': REST_BASE_PATH + 'dataSources',
}


#IDs for create
OBJECTEXTERNALID = 'BBDN-PYTHON-REST-DEMO-ID'
DSKEXTERNALID = 'BBDN-PYTHON-REST-DEMO-DSK'
COURSEEXTERNALID = 'BBDN-PYTHON-REST-DEMO-COURSE'
TERMEXTERNALID = 'BBDN-PYTHON-REST-DEMO-TERM'
USEREXTERNALID = 'BBDN-PYTHON-REST-DEMO-USER'
PAGINATIONLIMIT = 5
COURSEGETFIELDS = 'externalId,courseId,name,availability,id'
USERGETFIELDS = 'externalId,name'
TERMSGETFIELDS = 'externalId,name'
DSKSGETFIELDS = 'externalId,name'
CRSMEMBERSHIPGETFIELDS = "externalId,availability"
USRMEMBERSHIPGETFIELDS = "externalId,availability"
CERTPATH = "./trusted/keytool_crt.pem"

