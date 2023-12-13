# -*- coding: utf-8 -*-
import os
from lms.envs.devstack import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "ssl": False,
    "authSource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "Guetbest Platform - https://www.benouind.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)

import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://www.benouind.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "u0Zm6QiCTzNd98U7aCcEuniJ"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "DQFcNZOVaDNOw0YfBa6ELLoEe7wOqI6J2wWCAQVfIfdgeupRXrxHMZflbQlsBuMjlqfR6FbrIMMWUmUJstWLnfq6lyQh-XE7soGpaQT8s9T1JD89Sje0O9xrTnfW0Q-zI4ct5rjsuOjkdUFAGwQwYgHFVAbaaQAQfHM4CVti04S6rxIRG4jC6eRraPaZKCjWbWoaw8k0m4fbTYPJeUD7ReEh_bYnCJx8-9YKE7bxHzsyAHUiIh5bREs8EVvLbedZLpo7U_fXK_cu8FktmI28g4McONwlyVu-qjkltrtukAx9Dv7WGwr2lwds-2z90PsV9uRBUAFD-y1-fCS-Y_LFGw",
        "n": "leLtbUYpRcn5xL_5VA1Rsp8EJzDXN89O4DXjht78TRhl2I3plT6M8sp-80Z63tneLnpXepnlShaab8DMMzKN1UrqIzE7vlOmwsSYA7WdwrbGiuaFXdd1UntE8P4lAEVWjyEhd5W6-oNKq6TaWovYwJkIysX3wUPXxrkBLIUslkJSeYEqW1em9ApQDvYCSB3vxc4lv7FsMdFZ4vNzVdLyY8VttVoq67LDL6IaQN_svX22ateg2bZQErpNu2ngtEGcaIsRZal4fQVG2R2YCSYNxf0d4leHlkfj5hKUnjrJUHQ_9IxDqviTwVrdqI27Z3jHA8fphY30bNA-ST6GmrEnQQ",
        "p": "vu4KQmerBwOPQ4wI702wlRJvI6HqMFVjXyOcrqO0dNh5Pn8pa5-JGOxLFi9PGfnJXUE_sdxDUHWAix-PBQpnIrBCx5WnJBWs0Dyk_Tciap4yudoKw80gMQEeeG-2Ne1YYzC-z6eWsjjPyeZGEIeE9Hc8jcpPeTtPwaaZeeO3YN8",
        "q": "yPf-Z6p6vwSckwh_LXXTAMlchi8oKhFlXajkmdYATdSR8nFzi1V1SuX9_rMux4wGOij6yn2p2_PRxdLOgoolycnGrpnSPkNcBizRp5hlxodzPwF2fZ-frFKyEffEsR989ps-yKG18qQSVgLLERdrjX2zZLk29rSNlH05RduL298",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "leLtbUYpRcn5xL_5VA1Rsp8EJzDXN89O4DXjht78TRhl2I3plT6M8sp-80Z63tneLnpXepnlShaab8DMMzKN1UrqIzE7vlOmwsSYA7WdwrbGiuaFXdd1UntE8P4lAEVWjyEhd5W6-oNKq6TaWovYwJkIysX3wUPXxrkBLIUslkJSeYEqW1em9ApQDvYCSB3vxc4lv7FsMdFZ4vNzVdLyY8VttVoq67LDL6IaQN_svX22ateg2bZQErpNu2ngtEGcaIsRZal4fQVG2R2YCSYNxf0d4leHlkfj5hKUnjrJUHQ_9IxDqviTwVrdqI27Z3jHA8fphY30bNA-ST6GmrEnQQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://www.benouind.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "u0Zm6QiCTzNd98U7aCcEuniJ"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = False
CORS_ALLOW_HEADERS = corsheaders_default_headers + ('use-jwt-cookie',)

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.www.benouind.io"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "required"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}
CACHES["ora2-storage"] = {
    "KEY_PREFIX": "ora2-storage",
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://@redis:6379/1",
}

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# MFE: enable API and set a low cache timeout for the settings. otherwise, weird
# configuration bugs occur. Also, the view is not costly at all, and it's also cached on
# the frontend. (5 minutes, hardcoded)
ENABLE_MFE_CONFIG_API = True
MFE_CONFIG_API_CACHE_TIMEOUT = 1

FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True



######## End of common LMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

LMS_BASE = "www.benouind.io:8000"
LMS_ROOT_URL = "http://{}".format(LMS_BASE)
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL
SITE_NAME = LMS_BASE
CMS_BASE = "studio.www.benouind.io:8001"
CMS_ROOT_URL = "http://{}".format(CMS_BASE)
LOGIN_REDIRECT_WHITELIST.append(CMS_BASE)

# Session cookie
SESSION_COOKIE_DOMAIN = "www.benouind.io"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# CMS authentication
IDA_LOGOUT_URI_LIST.append("http://studio.www.benouind.io:8001/logout/")

FEATURES["ENABLE_COURSEWARE_MICROFRONTEND"] = False

# Disable enterprise integration
FEATURES["ENABLE_ENTERPRISE_INTEGRATION"] = False
SYSTEM_WIDE_ROLE_CLASSES.remove("enterprise.SystemWideEnterpriseUserRoleAssignment")

LOGGING["loggers"]["oauth2_provider"] = {
    "handlers": ["console"],
    "level": "DEBUG"
}



ACCOUNT_MICROFRONTEND_URL = "http://apps.www.benouind.io:1997/account"


WRITABLE_GRADEBOOK_URL = "http://apps.www.benouind.io:1994/gradebook"


LEARNING_MICROFRONTEND_URL = "http://apps.www.benouind.io:2000/learning"


PROFILE_MICROFRONTEND_URL = "https://apps.www.benouind.io:1995/profile/u/"


AUTHN_MICROFRONTEND_URL = "http://apps.www.benouind.io:1999/authn"
AUTHN_MICROFRONTEND_DOMAIN  = "apps.www.benouind.io/authn"



DISCUSSIONS_MICROFRONTEND_URL = "http://apps.www.benouind.io:2002/discussions"
DISCUSSIONS_MFE_FEEDBACK_URL = None



# authn MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:1999")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:1999")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:1999")

# account MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:1997")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:1997")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:1997")

# course-authoring MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:2001")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:2001")

# discussions MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:2002")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:2002")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:2002")

# gradebook MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:1994")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:1994")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:1994")

# learning MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:2000")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:2000")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:2000")

# profile MFE
CORS_ORIGIN_WHITELIST.append("http://apps.www.benouind.io:1995")
LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io:1995")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io:1995")


# Dynamic config API settings
# https://openedx.github.io/frontend-platform/module-Config.html
MFE_CONFIG = {
    "BASE_URL": "apps.www.benouind.io",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "ACCOUNT_SETTINGS_URL": ACCOUNT_MICROFRONTEND_URL,
    "ACCOUNT_PROFILE_URL": "http://apps.www.benouind.io:1995",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "",
    "FAVICON_URL": "http://www.benouind.io/favicon.ico",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "http://www.benouind.io:8000",
    "LOGIN_URL": "http://www.benouind.io:8000/login",
    "LOGO_URL": "http://www.benouind.io:8000/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "http://www.benouind.io:8000/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "http://www.benouind.io:8000/theming/asset/images/logo.png",
    "LOGOUT_URL": "http://www.benouind.io:8000/logout",
    "MARKETING_SITE_BASE_URL": "http://www.benouind.io:8000",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://www.benouind.io:8000/login_refresh",
    "SITE_NAME": "Guetbest Platform",
    "STUDIO_BASE_URL": "http://studio.www.benouind.io:8001",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
    "LEARNING_BASE_URL": "http://apps.www.benouind.io:2000",
    "ENABLE_NEW_EDITOR_PAGES": True,
    "ENABLE_PROGRESS_GRAPH_SETTINGS": True,
    "DISABLE_ENTERPRISE_LOGIN": True,
}


