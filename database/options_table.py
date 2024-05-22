from sqlite3 import IntegrityError


# create table for daily tasks
def create_options_table(self, table_name):
    self.cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT , item varchar(50) NOT NULL UNIQUE)"
    )
    self.con.commit()


# Add multiple default task options to a specified table
# 'item' should be a list of tuples, where each tuple contains a single item string
def create_default_options(self, table, item):
    self.cur.executemany(
        f"INSERT INTO {table}(item) VALUES(?)",
        item,
    )
    self.con.commit()


# Add a single task option to a specified table
# Returns 1 if the item was added successfully, or 0 if there was an IntegrityError (e.g., item already exists)
def create_option(self, table, item):
    # Try to insert the item into the table, handling the case where the item already exists
    try:
        self.cur.execute(f"INSERT INTO {table}(item) VALUES(?)", (item,))
        self.con.commit()
        return 1
    except IntegrityError as err:
        return 0


# Delete a specific item from the specified table
def delete_option(self, table, item):
    self.cur.execute(f"DELETE FROM {table} WHERE item=?", (item,))
    self.con.commit()


# Retrieve all task options from the specified table
# Returns a list of tuples, where each tuple contains a single item string
def get_all_options(self, table):
    return self.cur.execute(f"SELECT item FROM {table} ORDER BY item").fetchall()
