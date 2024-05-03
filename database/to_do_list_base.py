# create table for goals
def create_to_do_list_table(self, table_name):
    self.cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT , name varchar(50) NOT NULL, completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))"
    )
    self.con.commit()


# add item to table
def create_item(self, table, item):
    self.cur.execute(
        f"INSERT INTO {table}(name, completed) VALUES(?,?)",
        item,
    )
    self.con.commit()

    # take id of this item
    item_info = self.cur.execute(
        f"SELECT id, name FROM {table} WHERE name=?",
        (item[0],),
    )
    # return this item
    return item_info.fetchall()[-1]


# deleting item function (after press on trash bin)
def delete_item(self, table, id):
    self.cur.execute(f"DELETE FROM {table} WHERE id=?", (id,))
    self.con.commit()


# set as completed or not
def set_item_completed(self, table, id, completed):
    self.cur.execute(f"UPDATE {table} SET completed=? WHERE id=?", (completed, id))
    self.con.commit()

    item_text = self.cur.execute(
        f"SELECT name FROM {table} WHERE id=?", (id,)
    ).fetchone()

    return item_text[0]


# edit name item function after double tap on item
def update_item_name(self, table, id, item):
    self.cur.execute(f"UPDATE {table} SET name=? WHERE id=?", (item, id))
    self.con.commit()


# get all the items when launching app
def get_all_items(self, table):
    return self.cur.execute(
        f"SELECT id, name, completed FROM {table} ORDER BY name"
    ).fetchall()
