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
        result = self.db.execute("""
        SELECT array(
            SELECT id FROM images i
            WHERE i.substance_id = s.id
        ) as images, array(
            SELECT name FROM synonyms syn
            WHERE syn.substance_id = s.id
        ) as synonyms, array(
         SELECT g.name FROM substance_groups sg
         JOIN groups g ON g.id = sg.group_id
         WHERE sg.substance_id = s.id
       ) as groups, * FROM substances s
        WHERE s.id = %s
            """, [ id ], True)
        if isinstance(result, Exception):
            print(f"Error in FindByTitle Substance: {result}")
            return []
        else:
            print(result[0])
            return result[0]

    def findByTitle(self, title):
        result = self.db.execute("""
        SELECT array(
            SELECT id FROM images i
            WHERE i.substance_id = s.id
        ) as images, array(
            SELECT name FROM synonyms syn
            WHERE syn.substance_id = s.id
        ) as synonyms, array(
         SELECT g.name FROM substance_groups sg
         JOIN groups g ON g.id = sg.group_id
         WHERE sg.substance_id = s.id
       ) as groups, * FROM substances s
        WHERE s.name LIKE %s
            """, [ f"%{title}%" ], True)
        if isinstance(result, Exception):
            print(f"Error in FindByTitle Substance: {result}")
            return []
        else:
            print(result)
            return result

    def findAll(self):
        result = self.db.execute("""
       SELECT array(
         SELECT id FROM images i
         WHERE i.substance_id = s.id
       ) as images, array(
            SELECT name FROM synonyms syn
            WHERE syn.substance_id = s.id
        ) as synonyms, array(
         SELECT g.name FROM substance_groups sg
         JOIN groups g ON g.id = sg.group_id
         WHERE sg.substance_id = s.id
       ) as groups, * FROM substances s
        """, None, True)
        if isinstance(result, Exception):
            print(f"Error in Findall Substance: {result}")
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
