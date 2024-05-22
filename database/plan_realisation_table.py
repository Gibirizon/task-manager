from datetime import date, timedelta


# Create a table for tracking the realization of plans from a given category
def create_plan_realisation_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS plan_realisation (id integer PRIMARY KEY AUTOINCREMENT, day date NOT NULL, plan_name varchar(20) NOT NULL, all_completed BOOLEAN NOT NULL CHECK (all_completed IN (0, 1)))"
    )
    self.con.commit()


# Add a new task realization or update an existing one for the current day, calculate consecutive days
def create_or_change_item_realisation(self, plan_name, all_completed):
    current_date = date.today()

    # Check if there is already an entry for the current date and plan_name
    today_elements = self.cur.execute(
        "SELECT id FROM plan_realisation WHERE day=? AND plan_name=?",
        (current_date, plan_name),
    ).fetchone()

    if today_elements:
        # If an entry exists, update the all_completed field
        self.cur.execute(
            "UPDATE plan_realisation SET all_completed=? WHERE id=?",
            (all_completed, today_elements[0]),
        )
    else:
        # If no entry exists, insert a new record
        self.cur.execute(
            "INSERT INTO plan_realisation(day, plan_name, all_completed) VALUES(?,?,?)",
            (current_date, plan_name, all_completed),
        )

    self.con.commit()

    # Retrieve all completion statuses for the given plan_name
    category_realisation_of_all_days = self.cur.execute(
        "SELECT all_completed FROM plan_realisation WHERE plan_name=?",
        (plan_name,),
    ).fetchall()

    # Calculate the total number of completed days
    number_of_completed_days = [i[0] for i in category_realisation_of_all_days].count(1)

    # Calculate the number of consecutive completed days
    consecutive_days = 0
    while True:
        # Decrement the date by one day
        current_date -= timedelta(days=1)

        # Check if the previous day's task was completed
        day_completed = self.cur.execute(
            "SELECT all_completed FROM plan_realisation WHERE day=? AND plan_name=?",
            (current_date, plan_name),
        ).fetchone()

        if (
            day_completed and day_completed[0]
        ):  # day_completed can be None if there is no entry for the date
            consecutive_days += 1
        else:
            break

    return number_of_completed_days, consecutive_days
