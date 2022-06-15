from db import db

class Group:
    def __init__(self):
        self.db = DB()

    def create(self, substance_id, group_id):
        return self.db.insert_record(
            "substance_groups",
            [
                "substance_id",
                "group_id"
            ],
            [
                substance_id,
                group_id
            ]
        )