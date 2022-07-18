import json
import uuid
import bleach
import secrets
import requests
from django.views import View
from smtplib import SMTPException
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template, render_to_string
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
import logging
from config.settings import CLIENT_ID, CLIENT_KEY
from .models import AH_Item

logger = logging.getLogger("logdrop")


def log(e):
    logger.warning(f"{time()} : {e}")


def push_msg(request, msg, tag):
    messages.add_message(request, messages.INFO, msg, extra_tags=tag)


def get_msgs(request):
    return render_to_string(
        "src/msgs.html",
        {"msg": get_messages(request)},
        request,
    )


def is_ajax(request):
    return (
        True if request.headers.get("x-requested-with") == "XMLHttpRequest" else False
    )


def is_post(request):
    return True if request.method == "POST" else False


def is_get(request):
    return True if request.method == "GET" else False


def forbidden():
    return HttpResponseForbidden()


def time():
    now = datetime.now()
    return now.strftime("%y/%m/%d %H:%M:%S.%f")


def deserialize_form(data):
    return dict(i.split("=") for i in data.split("&"))


def to_list(l):
    return list(i for i in l.split(","))


def much_speed_so_wow(_list):
    for i in _list:
        yield i


def api_auth():
    response = requests.post(
        url="https://eu.battle.net/oauth/token",
        params={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_KEY),
    )
    data = response.json()
    return data["access_token"]


def fmtGold(value):
    return "%sc %ss %sg" % (value % 100, value / 100 % 100, value / 10000 % 100)


def date_hour(time):
    return time.strftime("%H")


def format_time(time):
    return time.strftime("%m/%d/%Y, %H:%M:%S")
