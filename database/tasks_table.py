# create table for daily tasks
def create_tasks_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT , task varchar(50) NOT NULL, start_time varchar(10), finish_time varchar(10), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))"
    )
    self.con.commit()

# add tasks to table
def create_task(self, task):
    self.cur.execute(
        "INSERT INTO tasks(task, start_time, finish_time, completed) VALUES(?,?,?,?)",
        task,
    )
    self.con.commit()

    # take id of this task
    task_info = self.cur.execute(
        "SELECT id, task, start_time, finish_time FROM tasks WHERE task=?",
        (task[0],),
    )
    # return this task
    return task_info.fetchall()[-1]

# deleting task function (after press on trash bin)
def delete_task(self, id):
    self.cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    self.con.commit()

# set as completed or not
def set_completed(self, id, completed):
    self.cur.execute(f"UPDATE tasks SET completed=? WHERE id=?", (completed, id))
    self.con.commit()

    task_text = self.cur.execute(
        "SELECT task FROM tasks WHERE id=?", (id,)
    ).fetchone()

    return task_text[0]

# edit name task function after double tap on task
def update_task_name(self, id, task):
    self.cur.execute("UPDATE tasks SET task=? WHERE id=?", (task, id))
    self.con.commit()

# get all the tasks when launching app
def get_all_tasks(self):
    return self.cur.execute(
        "SELECT id, task, start_time, finish_time, completed FROM tasks ORDER BY start_time"
    ).fetchall()