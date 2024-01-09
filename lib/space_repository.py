from lib.space import Space

class SpaceRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute("SELECT * FROM spaces")
        spaces = []
        for row in rows:
            item = Space(row["id"], row["address"], row["name"], row["price"], row["image_path"], row["description"], row['date_added'], row["date_available"], row["user_id"])
            spaces.append(item)
        return spaces

    def create(self, space):
        self.connection.execute("INSERT INTO spaces (address, name, price, image_path, description, date_added, date_available, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                                        [space.address, space.name, space.price, space.image_path, space.description, space.date_added, space.date_available, space.user_id])
        return None
    
    def find(self, id):
        rows = self.connection.execute("SELECT * FROM spaces WHERE id = %s", [id])
        row = rows[0]
        return Space(row["id"], row["address"], row["name"], row["price"], row["image_path"], row["description"], row['date_added'], row["date_available"], row["user_id"])
    
    def delete(self, id):
        self.connection.execute("DELETE FROM spaces WHERE id = %s", [id])
        return None


    def update(self, space_id, new_values):
        if isinstance(new_values, str):
            new_values = {"": new_values}
        existing_space = self.find(space_id)
        for field, value in new_values.items():
            setattr(existing_space, field, value)
        set_clause = ', '.join([f'{field} = %s' for field in new_values.keys()])
        query = f'UPDATE spaces SET {set_clause} WHERE id = %s'
        self.connection.execute(query, list(new_values.values()) + [space_id])
        return None



