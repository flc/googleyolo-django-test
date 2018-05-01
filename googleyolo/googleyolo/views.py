import logging

from django.db import transaction
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from google.oauth2 import id_token
from google.auth.transport import requests

from google_user.models import GoogleUser


logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_authenticated:
        return redirect("protected")

    context = {
        "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
    }
    return render(request, 'home.html', context)


@login_required
def protected(request):
    context = {}
    return render(request, 'protected.html', context)


def logout_view(request):
    logout(request)
    return redirect("home")
