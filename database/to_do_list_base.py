# Create table for goals or weekly tasks
def create_to_do_list_table(self, table_name):
    self.cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, name varchar(50) NOT NULL, completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))"
    )
    self.con.commit()


# Add a new item to the specified table
def create_item(self, table, item):
    self.cur.execute(
        f"INSERT INTO {table}(name, completed) VALUES(?,?)",
        item,
    )
    self.con.commit()

    # Retrieve information about the newly added item
    item_info = self.cur.execute(
        f"SELECT id, name FROM {table} WHERE name=?",
        (item[0],),
    ).fetchall()

    # Return the last added item information
    return item_info[-1]


# Delete an item from the specified table by id
def delete_item(self, table, id):
    self.cur.execute(f"DELETE FROM {table} WHERE id=?", (id,))
    self.con.commit()


# Set the completed status of an item by id
# 'completed' should be a boolean value (0 or 1)
def set_item_completed(self, table, id, completed):
    self.cur.execute(f"UPDATE {table} SET completed=? WHERE id=?", (completed, id))
    self.con.commit()

    # Retrieve the name of the item that was updated
    item_text = self.cur.execute(
        f"SELECT name FROM {table} WHERE id=?", (id,)
    ).fetchone()

    # Return the name of the updated item
    return item_text[0]


# Update the name of an item by id
def update_item_name(self, table, id, item):
    self.cur.execute(f"UPDATE {table} SET name=? WHERE id=?", (item, id))
    self.con.commit()


# Retrieve all items from the specified table
def get_all_items(self, table):
    return self.cur.execute(
        f"SELECT id, name, completed FROM {table} ORDER BY name"
    ).fetchall()
