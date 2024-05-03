from todo_app.models.item import Item
from todo_app.models.view import ViewModel


def test_done_items_returns_done_items():
    # arrange
    todo_items = [
        Item(1, "item-1", "Done"),
        Item(2, "item-2", "To Do"),
        Item(3, "item-3", "Done"),
    ]

    # act
    view_model = ViewModel(todo_items)

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
    todo_items = [
        Item(1, "item 1", "Done"),
        Item(2, "item 2", "To Do"),
        Item(3, "item-3", "Done"),
    ]

    # act
    view_model = ViewModel(todo_items)

    # assert
    done_items = view_model.done_items

    item_2 = next((item for item in done_items if item.id == 2), None)
    assert item_2 is None
