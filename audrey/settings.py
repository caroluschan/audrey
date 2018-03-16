"""
Django settings for audrey project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
#import telepot
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'juu^jg=5cnz19z5k85wl(2&8&b8z5d-!u)tf8ixwhcfag9o&@!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'stages.apps.StagesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'audrey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'audrey.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

BOT_TOKEN = str('462615061:AAHqdSi1rMiMpQ9vEpVn3COOkrnSbHrfWm4')

#bot = telepot.Bot(BOT_TOKEN)

SUPERADMIN = '47237387'

SCORE_SECTIONS = 20

STAGES= [

    ##########################
    ###Normal User Function###
    ##########################

    #Conversation: authorization
   {
      'command_pattern_check':'command == "/signup"',
      'is_first':True,
      'stage_code':'auth_1',
      'function_call':'auth_stage_1(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'auth_2',
      'function_call':'auth_stage_2(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'auth_3',
      'function_call':'auth_stage_3(command,person)'
   },

   #Conversation: get master list of scores
   {
      'command_pattern_check':'command == "/listscores"',
      'is_first':True,
      'stage_code':'listScores_1',
      'function_call':'get_master_scores_stage_1(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'listScores_2',
      'function_call':'get_master_scores_stage_2(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'listScores_3',
      'function_call':'get_master_scores_stage_3(command,person)'
   },

   #Conversation: get score by code
   {
      'command_pattern_check':'command[:9] == "/songcode"',
      'is_first':True,
      'stage_code':'songCode_1',
      'function_call':'get_score_by_code_stage_1(command,person)'
   },

   #Conversation: get score by song name
   {  
      'command_pattern_check':'command == "/scorebyname"',
      'is_first':True,
      'stage_code':'scoreByName_1',
      'function_call':'get_score_by_name_stage_1(command,person)'
   },
   {  
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'scoreByName_2',
      'function_call':'get_score_by_name_stage_2(command,person)'
   },

   #Conversation: get score by lyrics
   {
      'command_pattern_check':'command[:14] == "/scorebylyrics"',
      'is_first':True,
      'stage_code':'scoreByLyrics_1',
      'function_call':'get_score_by_lyrics_stage_1(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'scoreByLyrics_2',
      'function_call':'get_score_by_lyrics_stage_2(command,person)'
   },

   #Conversation: get lyrics by song name

   #Conversation: get lyrics by part of the lyrics

   #Conversation: cancel
   {
      'command_pattern_check':'command == "/cancel"',
      'is_first':True,
      'stage_code':'cancel_1',
      'function_call':'cancel_stage_1(command,person)'
   },

    #########################
    ###Admin User Function###
    #########################

    #Conversation: user approval  
   {
      'command_pattern_check':'command[:8] == "/approve"',
      'is_first':True,
      'stage_code':'approve_1',
      'function_call':'approve_stage_1(command,person)'
   },

   #Conversation: list users
   {
      'command_pattern_check':'command == "/listusers"',
      'is_first':True,
      'stage_code':'listUsers_1',
      'function_call':'list_users_stage_1(command,person)'
   },

   #Conversation: list admin users
   {
      'command_pattern_check':'command == "/listadmins"',
      'is_first':True,
      'stage_code':'listAdmins_1',
      'function_call':'list_admin_users_stage_1(command,person)'
   },

   #Conversation: set user as admin
   {
      'command_pattern_check':'command == "/setadmin"',
      'is_first':True,
      'stage_code':'setAdmin_1',
      'function_call':'set_admin_stage_1(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'setAdmin_2',
      'function_call':'set_admin_stage_2(command,person)'
   },

   #Conversation: unset admin
   {
      'command_pattern_check':'command == "/unsetadmin"',
      'is_first':True,
      'stage_code':'unsetAdmin_1',
      'function_call':'unset_admin_stage_1(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'unsetAdmin_2',
      'function_call':'unset_admin_stage_2(command,person)'
   },

   #Conversation: delete user
   {
      'command_pattern_check':'command == "/deleteuser"',
      'is_first':True,
      'stage_code':'deleteUser_1',
      'function_call':'delete_user_stage_1(command,person)'
   },
   {
      'command_pattern_check':None,
      'is_first':False,
      'stage_code':'deleteUser_2',
      'function_call':'delete_user_stage_2(command,person)'
   },

   #Conversation: List Admin functions
   {
      'command_pattern_check':'command == "/adminmenu"',
      'is_first':True,
      'stage_code':'listAdminFunctions_1',
      'function_call':'list_admin_functions_stage_1(command,person)'
   },
   #Conversation: upload score???
]