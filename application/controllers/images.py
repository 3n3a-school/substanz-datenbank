from db import DB

class Image:
    def __init__(self):
        self.db = DB()

    def create(self, files, substance_id):
        ids = []
        for image in files.getlist('images'):
            if "image/" in image.mimetype:
                print(f"image-name: {image.filename} mimetpye: {image.mimetype}")
                image_id = self.db.execute(
                    "INSERT INTO images (content, mimetype, substance_id) VALUES (%s, %s, %s) RETURNING id",
                    [
                        image.read(),
                        str(image.mimetype),
                        substance_id
                    ],
                    True
                )[0].get('id')
                print(f"image-status: {image_id}")
                if not isinstance(image_id, Exception):
                    ids.append(image_id)
        print(f"images: {ids}")
        return ids

    def find(self, id):
        return self.db.get_record("images", "*", {"key":"id", "operator":"=", "value": id})[0]

    def update(self, files, id):
        self.db.execute(
            "DELETE FROM images WHERE substance_id = %s",
            [
                id
            ]
        )
        return len(self.create(files, id)) > 0