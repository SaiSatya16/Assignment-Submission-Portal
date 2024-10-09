class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    MONGO_URI= 'mongodb+srv://satya1:Saisatya1610@clustersatyaproject1.i2sk1.mongodb.net/assignment_portal?tls=true&tlsAllowInvalidCertificates=true'
    JWT_SECRET_KEY='thisissaltt1'
    FLASK_DEBUG= False
    PROPAGATE_EXCEPTIONS= True
    JWT_ACCESS_TOKEN_EXPIRES= 3600