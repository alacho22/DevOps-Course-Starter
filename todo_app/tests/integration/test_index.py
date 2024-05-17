import os
from dotenv import load_dotenv, find_dotenv
import pytest
import requests
from todo_app import app


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv(".env.test")
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, "get", stub)

    # Make a request to our app's index page
    response = client.get("/")

    assert response.status_code == 200
    response_text = response.data.decode()

    assert "Test to do card" in response_text
    assert "Test to do card 2" in response_text
    assert "Test done card" in response_text


class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

    def raise_for_status(self):
        pass


def stub(url, params={}, headers={}, timeout=3):
    test_board_id = os.environ.get("TRELLO_BOARD_ID")
    todo_list_id = os.environ.get("TRELLO_TODO_LIST_ID")
    done_list_id = os.environ.get("TRELLO_DONE_LIST_ID")
    fake_response_data = None
    if (
        url == f"https://api.trello.com/1/boards/{test_board_id}/lists"
        and params["cards"] == "open"
    ):
        fake_response_data = [
            {
                "id": todo_list_id,
                "name": "To Do",
                "cards": [
                    {"id": "123", "name": "Test to do card"},
                    {"id": "456", "name": "Test to do card 2"},
                ],
            },
            {
                "id": done_list_id,
                "name": "Done",
                "cards": [{"id": "789", "name": "Test done card"}],
            },
        ]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')
