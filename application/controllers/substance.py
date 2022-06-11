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
            ],
            " RETURNING id"
        ).get("id")

    def find(self, id):
        return self.db.get_record("substances", "*", {"key":"id", "operator": "=", "value": str(id)})[0]

    def findByTitle(self, title):
        return self.db.get_record("substances", "*", {"key":"name", "operator": "LIKE", "value": f"'%{title}%'"})

    def findAll(self):
        result = self.db.execute("""
       SELECT * FROM images
       JOIN substances On images.substance_id = substances.id
        """, None, True)
        if isinstance(result, Exception):
            print(f"Findall Substance: {result}")
            return []
        else:
            print(result)
            return result

    def update(self, values, id):
        return self.db.update_record("substances", {
            "name": values['name'],
            "molecular_formula": values['molecular_formula'],
            "molecular_weight": values['molecular_weight'],
        }, id)

    def delete(self, id):
        return self.db.delete_record("substances", id)