import logging

from django.db import transaction
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from google.oauth2 import id_token
from google.auth.transport import requests

from .models import GoogleUser


logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def auth(request):
    token = request.POST.get('token')
    if not token:
        return HttpResponseBadRequest("Missing token.")

    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

        if idinfo['aud'] not in (settings.GOOGLE_CLIENT_ID,):
            raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']

        email = idinfo['email']
    except ValueError as e:
        logger.exception(e)

        return HttpResponseBadRequest("Invalid token.")

    else:
        try:
            guser = GoogleUser.objects.get(google_userid=userid)
            user = guser.user
        except GoogleUser.DoesNotExist:
            with transaction.atomic():
                UserModel = get_user_model()
                username_field = getattr(UserModel, 'USERNAME_FIELD', 'username')

                user = UserModel.objects.create_user(
                    username=email,
                    email=email,
                    password=None,
                    )
                # user.set_unusable_password()
                # user.save()
                guser = GoogleUser.objects.create(
                    user=user,
                    google_userid=userid,
                    )

        # sign in the user
        login(request, user)
        # request.session.set_expiry(0)

    return HttpResponse("Authenticated.")
