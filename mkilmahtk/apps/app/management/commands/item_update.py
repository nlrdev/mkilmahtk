from urllib import response
import requests
import json
from app.core import api_auth, much_speed_so_wow
from django.core.management.base import BaseCommand
from app.models import Item, AH_Item
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
     pass