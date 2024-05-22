import os
import sqlite3


class Database:
    # Importing functions from files to handle different tables and their operations
    from database.options_table import (
        create_default_options,
        create_option,
        create_options_table,
        delete_option,
        get_all_options,
    )
    from database.plan_realisation_table import (
        create_or_change_item_realisation,
        create_plan_realisation_table,
    )
    from database.tasks_table import create_task, create_tasks_table, get_all_tasks
    from database.to_do_list_base import (
        create_item,
        create_to_do_list_table,
        delete_item,
        get_all_items,
        set_item_completed,
        update_item_name,
    )

    def __init__(self):
        # Initialize the database connection and cursor
        path = os.path.dirname(__file__)
        self.con = sqlite3.connect(f"{path}/database.db")
        self.cur = self.con.cursor()

        # Create necessary tables in the database
        self.create_tasks_table()
        self.create_to_do_list_table("goals")
        self.create_to_do_list_table("weekly_tasks")
        self.create_options_table("tasks_options")
        self.create_options_table("goals_options")
        self.create_options_table("weekly_tasks_options")
        self.create_plan_realisation_table()

        # Populate the options tables with default values if table is empty
        if not self.cur.execute("SELECT id FROM plan_realisation").fetchall():
            self.create_default_options(
                "tasks_options",
                item=[("Python",), ("English",), ("Workout",)],
            )
            self.create_default_options("goals_options", item=[("Focus on better",)])
            self.create_default_options(
                "weekly_tasks_options", item=[("Maths test",), ("Python project",)]
            )

    # Close the connection to the database
    def close_connection(self):
        self.con.close()
