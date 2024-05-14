class Item:
    def __init__(self, id, title, status="To Do"):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, trello_card_response, status):
        return cls(
            trello_card_response["id"],
            trello_card_response["name"],
            status,
        )
