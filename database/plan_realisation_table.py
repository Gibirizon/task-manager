# Create a table for tracking the realization of plans from a given category
def create_plan_realisation_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS plan_realisation (id integer PRIMARY KEY AUTOINCREMENT, day integer NOT NULL, plan_name varchar(20) NOT NULL, all_completed BOOLEAN NOT NULL CHECK (all_completed IN (0, 1)))"
    )
    self.con.commit()


def get_today_element(self, date, plan_name):
    return self.cur.execute(
        "SELECT id FROM plan_realisation WHERE day=? AND plan_name=?",
        (date, plan_name),
    ).fetchone()


def create_element(self, date, plan_name, all_completed):
    self.cur.execute(
        "INSERT INTO plan_realisation(day, plan_name, all_completed) VALUES(?,?,?)",
        (date, plan_name, all_completed),
    )

    self.con.commit()


def update_element(self, today_item, plan_name, all_completed):
    self.cur.execute(
        "UPDATE plan_realisation SET all_completed=? WHERE id=?",
        (all_completed, today_item),
    )
    self.con.commit()


def get_number_of_completed_days(self, plan_name):
    # Retrieve all completion statuses for the given plan_name
    category_realisation_of_all_days = self.cur.execute(
        "SELECT all_completed FROM plan_realisation WHERE plan_name=?",
        (plan_name,),
    ).fetchall()

    # Calculate the total number of completed days
    number_of_completed_days = [i[0] for i in category_realisation_of_all_days].count(1)
    return number_of_completed_days


def calculate_consecutive_days(self, plan_name, date):
    # Calculate the number of consecutive completed days
    consecutive_days = 0
    while True:
        # Decrement the date by one day (86400 seconds)
        date -= 86400

        # Check if the previous day's task was completed
        day_completed = self.cur.execute(
            "SELECT all_completed FROM plan_realisation WHERE day=? AND plan_name=?",
            (date, plan_name),
        ).fetchone()

        if (
            day_completed and day_completed[0]
        ):  # day_completed can be None if there is no entry for the date
            consecutive_days += 1
        else:
            break

    return consecutive_days
