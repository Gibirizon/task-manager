from sqlite3 import IntegrityError


# create table for daily tasks
def create_options_table(self, table_name):
    self.cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT , item varchar(50) NOT NULL UNIQUE)"
    )
    self.con.commit()


# add default task options to table
def create_default_options(self, table, item):
    try:
        self.cur.executemany(
            f"INSERT INTO {table}(item) VALUES(?)",
            item,
        )
        self.con.commit()
    except IntegrityError as err:
        print(f"An Error! {err}")


# add item option to table
def create_option(self, table, item):
    # checking if this option already exists
    try:
        self.cur.execute(f"INSERT INTO {table}(item) VALUES(?)", (item,))
        self.con.commit()
    except IntegrityError as err:
        print(f"An Error! {err}")


# deleting item function (after press on trash bin)
def delete_option(self, table, item):
    self.cur.execute(f"DELETE FROM {table} WHERE item=?", (item,))
    self.con.commit()


# get all the options when launching app
def get_all_options(self, table):
    return self.cur.execute(f"SELECT item FROM {table} ORDER by item").fetchall()
