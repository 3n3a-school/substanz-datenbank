from db import DB

class Synonym:
    def __init__(self):
        self.db = DB()

    def create(self, substance_id, form):
        for synonym in form.getlist('synonyms'):
            self.db.insert_record(
                "synonyms",
                [
                    "substance_id",
                    "name"
                ],
                [
                    substance_id,
                    synonym
                ]
            )
        return True