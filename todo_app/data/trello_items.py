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
    raise NotImplementedError
