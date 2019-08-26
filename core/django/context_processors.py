from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_TAG_MANAGER': settings.GOOGLE_TAG_MANAGER,
        'TERMS_OF_USE_URL': settings.TERMS_OF_USE_URL,
        'PRIVACY_POLICY_URL': settings.PRIVACY_POLICY_URL,
        'CONTACT_URL': settings.CONTACT_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'BASE_CMS_URL': settings.BASE_CMS_URL,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY
    }