# create table for daily tasks
def create_tasks_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT , name varchar(50) NOT NULL, start_time varchar(10), finish_time varchar(10), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))"
    )
    self.con.commit()


# add tasks to table
def create_task(self, task):
    self.cur.execute(
        "INSERT INTO tasks(name, start_time, finish_time, completed) VALUES(?,?,?,?)",
        task,
    )
    self.con.commit()

    # take id of this task
    task_info = self.cur.execute(
        "SELECT id, name, start_time, finish_time FROM tasks WHERE name=?",
        (task[0],),
    )
    # return this task
    return task_info.fetchall()[-1]


# get all the tasks when launching app
def get_all_tasks(self):
    return self.cur.execute(
        "SELECT id, name, start_time, finish_time, completed FROM tasks ORDER BY start_time"
    ).fetchall()
