import os
import sqlite3


class Database:
    from database.tasks_options_table import (
        create_default_task_options,
        create_task_option,
        create_tasks_options_table,
        delete_task_option,
        get_all_tasks_options,
    )
    from database.tasks_table import (
        create_task,
        create_tasks_table,
        delete_task,
        get_all_tasks,
        set_completed,
        update_task_name,
    )

    def __init__(self):
        # print(os.path.dirname(__file__))
        path = os.path.dirname(__file__)
        self.con = sqlite3.connect(f"{path}/database.db")
        self.cur = self.con.cursor()
        self.create_tasks_table()
        self.create_tasks_options_table()
        if not os.path.isfile(f"{path}/first_initialisation.txt"):
            with open(f"{path}/first_initialisation.txt", "w"):
                pass
            self.create_default_task_options(task=[("maths",), ("polish",)])

    # close connection to database
    def close_connection(self):
        self.con.close()
