from django.shortcuts import get_object_or_404
import requests
import json
from .core import api_auth, time, much_speed_so_wow
from .models import AH_Dump, AH_Item, Item
from celery import shared_task


@shared_task
def fetch_ah_data(relm=4476, ah=6):
    """
    This task pulls a dump of the specified 'auction house' from specified 'relm'
    
    """
    access_token = api_auth()
    ah_data = requests.get(
        url=f"https://eu.api.blizzard.com/data/wow/connected-realm/{relm}/auctions/{ah}",
        params={":region": "eu", "namespace": "dynamic-classic-eu", "locale": "en_EU"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = ah_data.json()
    ah_dump = AH_Dump(name=f"ah_dump {time()}")
    ah_dump.save()
    _data = much_speed_so_wow(data["auctions"])
    t = len(data["auctions"])
    for i in range(t):
        a = next(_data)
        if AH_Item.objects.filter(a_id=a["id"]).exists():
            continue
        else:
            ah_item = AH_Item(
                ah=ah_dump,
                a_id=a["id"],
                item_id=a["item"]["id"],
                item=a["item"],
                bid=a["bid"],
                buyout=a["buyout"],
                quantity=a["quantity"],
                time_left=a["time_left"],
            )
            ah_item.save()

    return t


@shared_task
def fetch_item_data():
    """
     update the item table with any new items the auctoin house dump
    TODO: async / subroutine the get requests
    """
    count = 0
    access_token = api_auth()
    item_ids = AH_Item.objects.values_list("item_id", flat=True).distinct()
    _ids = much_speed_so_wow(item_ids)
    l = Item.objects.all()
    for i in range(len(item_ids)):
        id = next(_ids)
        if l.filter(item_id=id).exists():
            """
            This is just a hack to update the database with any new fields overtime without much effort    
            """
            _item = get_object_or_404(Item, item_id=id)
            if _item.item_data == "":
                try:
                    item_data = requests.get(
                        url=f"https://us.api.blizzard.com/data/wow/item/{id}?namespace=static-classic-us",
                        params={":region": "us", "locale": "en_US"},
                        headers={
                            "Authorization": f"Bearer {access_token}",
                        },
                    )
                    item_media = requests.get(
                        url=f"https://us.api.blizzard.com/data/wow/media/item/{id}?namespace=static-classic-us",
                        params={":region":"us", "locale":"en_US"},
                        headers={
                            "Authorization": f"Bearer {access_token}",
                        },
                    )
                    item = item_data.json()
                    media = item_media.json()
                    _item.item_url = media['assets'][0]['value']
                    _item.item_data = item
                    _item.item_media = media
                    _item.save()
                except:
                    continue

            continue

        try:
            item_data = requests.get(
                url=f"https://us.api.blizzard.com/data/wow/item/{id}?namespace=static-classic-us",
                params={":region": "us", "locale": "en_US"},
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
            item_media = requests.get(
                url=f"https://us.api.blizzard.com/data/wow/media/item/{id}?namespace=static-classic-us",
                params={":region":"us", "locale":"en_US"},
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
        except:
            continue

        item = item_data.json()
        if "code" in item:
            continue
        
        media = item_media.json()
        if "code" in media:
            continue

        count += 1
        _item = Item(
            item_id=item["id"],
            name=item["name"],
            item_url=media['assets'][0]['value'],
            item_data=item,
            item_media=media,
        )
        _item.save()

    return f"{count} updated"
