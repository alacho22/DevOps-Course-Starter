from todo_app.models.item import Item
from todo_app.models.view import ViewModel


def test_done_items_returns_done_items():
    # arrange
    items = [
        Item(1, "item-1", "Done"),
        Item(2, "item-2", "To Do"),
        Item(3, "item-3", "Done"),
    ]

    # act
    view_model = ViewModel(items)

    # assert
    done_items = view_model.done_items

    item_1 = next((item for item in done_items if item.id == 1), None)
    assert item_1 is not None
    assert item_1.title == "item-1"
    assert item_1.status == "Done"

    item_3 = next((item for item in done_items if item.id == 3), None)
    assert item_3 is not None
    assert item_3.title == "item-3"
    assert item_3.status == "Done"


def test_done_items_does_not_return_to_do_items():
    # arrange
    items = [
        Item(1, "item 1", "Done"),
        Item(2, "item 2", "To Do"),
        Item(3, "item-3", "Done"),
    ]

    # act
    view_model = ViewModel(items)

    # assert
    done_items = view_model.done_items

    item_2 = next((item for item in done_items if item.id == 2), None)
    assert item_2 is None


def test_to_do_items_returns_to_do_items():
    # arrange
    items = [
        Item(1, "item-1", "Done"),
        Item(2, "item-2", "To Do"),
        Item(3, "item-3", "Done"),
        Item(4, "item-4", "To Do"),
    ]

    # act
    view_model = ViewModel(items)

    # assert
    to_do_items = view_model.to_do_items

    item_2 = next((item for item in to_do_items if item.id == 2), None)
    assert item_2 is not None
    assert item_2.title == "item-2"
    assert item_2.status == "To Do"

    item_4 = next((item for item in to_do_items if item.id == 4), None)
    assert item_4 is not None
    assert item_4.title == "item-4"
    assert item_4.status == "To Do"


def test_to_do_items_does_not_return_done_items():
    # arrange
    todo_items = [
        Item(1, "item 1", "Done"),
        Item(2, "item 2", "To Do"),
        Item(3, "item-3", "Done"),
        Item(4, "item-4", "To Do"),
    ]

    # act
    view_model = ViewModel(todo_items)

    # assert
    to_do_items = view_model.to_do_items

    item_1 = next((item for item in to_do_items if item.id == 1), None)
    assert item_1 is None

    item_3 = next((item for item in to_do_items if item.id == 3), None)
    assert item_3 is None
