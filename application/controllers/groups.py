from db import DB

class Group:
    def __init__(self):
        self.db = DB()

    def create(self, substance_id, form):
        for group_id in form.getlist('groups'):
            self.db.insert_record(
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
        return True

    def findAll(self):
        return self.db.get_record("groups", "*")