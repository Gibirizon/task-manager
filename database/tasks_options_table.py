from sqlite3 import IntegrityError


# create table for daily tasks
def create_tasks_options_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS tasks_options (id integer PRIMARY KEY AUTOINCREMENT , task varchar(50) NOT NULL UNIQUE)"
    )
    self.con.commit()


# add default task options to table
def create_default_task_options(self, task):
    try:
        self.cur.executemany(
            "INSERT INTO tasks_options(task) VALUES(?)",
            task,
        )
        self.con.commit()
    except IntegrityError as err:
        print(f"An Error! {err}")


# add task option to table
def create_task_option(self, task):
    # checking if this option already exists
    try:
        self.cur.execute("INSERT INTO tasks_options(task) VALUES(?)", (task,))
        self.con.commit()
    except IntegrityError as err:
        print(f"An Error! {err}")


# deleting task function (after press on trash bin)
def delete_task_option(self, task):
    self.cur.execute("DELETE FROM tasks_options WHERE task=?", (task,))
    self.con.commit()


# get all the tasks_options when launching app
def get_all_tasks_options(self):
    return self.cur.execute("SELECT task FROM tasks_options ORDER BY task").fetchall()
