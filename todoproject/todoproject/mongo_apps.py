from django.contrib.auth.apps import AuthConfig
from django.contrib.contenttypes.apps import ContentTypesConfig
from axes.apps import AppConfig as AxesConfig

MONGO_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'


class MongoAuthConfig(AuthConfig):
    default_auto_field = MONGO_AUTO_FIELD


class MongoContentTypesConfig(ContentTypesConfig):
    default_auto_field = MONGO_AUTO_FIELD


class MongoAxesConfig(AxesConfig):
    default_auto_field = MONGO_AUTO_FIELD
