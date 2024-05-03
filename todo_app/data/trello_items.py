from functools import reduce
import os
import json
import requests

from todo_app.models.item import Item


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    board_id = os.getenv("TRELLO_BOARD_ID")
    url = f"https://api.trello.com/1/boards/{board_id}/lists"

    headers = {"Accept": "application/json"}

    api_key = os.getenv("TRELLO_API_KEY")
    api_token = os.getenv("TRELLO_API_TOKEN")
    query = {"key": api_key, "token": api_token, "cards": "open"}

    response = requests.request("GET", url, headers=headers, params=query, timeout=3)

    response.raise_for_status()

    board_lists_response = json.loads(response.text)
    cards_per_status = [
        board_list_to_cards(board_list_response)
        for board_list_response in board_lists_response
    ]

    all_cards = reduce(list.__add__, cards_per_status)

    return all_cards


def board_list_to_cards(board_list_response):
    status = board_list_response["name"]
    return [
        card_response_to_card(status, card_response)
        for card_response in board_list_response["cards"]
    ]


def card_response_to_card(status, card_response):
    return Item.from_trello_card(card_response, status)


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

    list_id_to_add_to = os.getenv("TRELLO_TODO_LIST_ID")
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

    card_response = json.loads(response.text)

    return {
        "id": card_response["id"],
        "title": card_response["name"],
        "status": "Not Started",
    }


def complete_item(id):
    url = f"https://api.trello.com/1/cards/{id}"

    headers = {"Accept": "application/json"}

    list_id_to_move_to = os.getenv("TRELLO_DONE_LIST_ID")
    api_key = os.getenv("TRELLO_API_KEY")
    api_token = os.getenv("TRELLO_API_TOKEN")

    query = {"idList": list_id_to_move_to, "key": api_key, "token": api_token}

    response = requests.request("PUT", url, headers=headers, params=query, timeout=3)

    response.raise_for_status()
