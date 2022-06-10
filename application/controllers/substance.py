from db import DB

class Substance:
    def __init__(self):
        self.db = DB()
        self.db.create_table()

    def create(self, values):
        return self.db.insert_record(
            "substances", 
            ["name", "molecular_formula", "molecular_weight"],
            [
                values['name'],
                values['molecular_formula'],
                values['molecular_weight'],
            ]
        )

    def read():
        pass

    def update():
        pass

    def delete():
        pass