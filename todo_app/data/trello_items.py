import os
import json
import requests


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    raise NotImplementedError


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    url = "https://api.trello.com/1/cards"

    headers = {"Accept": "application/json"}

    list_id_to_add_to = os.getenv("TRELLO_LIST_ID")
    api_key = os.getenv("TRELLO_API_KEY")
    api_token = os.getenv("TRELLO_API_TOKEN")

    query = {
        "idList": list_id_to_add_to,
        "key": api_key,
        "token": api_token,
        "name": title,
    }

    response = requests.request("POST", url, headers=headers, params=query, timeout=3)

    response.raise_for_status()

    item_response = json.loads(response.text)

    return {
        "id": item_response["id"],
        "title": item_response["name"],
        "status": "Not Started",
    }
