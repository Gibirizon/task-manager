# create table for daily tasks
def create_tasks_options_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS tasks_options (id integer PRIMARY KEY AUTOINCREMENT , task varchar(50) NOT NULL UNIQUE)"
    )
    self.con.commit()


# add default task options to table
def create_default_task_options(self, task):
    self.cur.executemany(
        "INSERT INTO tasks_options(task) VALUES(?)",
        task,
    )
    self.con.commit()


# add task option to table
def create_task_option(self, task):
    # checking if this option already exists
    existing_task = self.cur.execute(
        "SELECT task FROM tasks_options WHERE task=?", (task,)
    )
    if not existing_task.fetchone():
        self.cur.execute("INSERT INTO tasks_options(task) VALUES(?)", (task,))
        self.con.commit()


# deleting task function (after press on trash bin)
def delete_task_option(self, id):
    self.cur.execute("DELETE FROM tasks_options WHERE id=?", (id,))
    self.con.commit()


# get all the tasks_options when launching app
def get_all_tasks_options(self):
    return self.cur.execute(
        "SELECT task FROM tasks_options ORDER BY task"
    ).fetchall()
