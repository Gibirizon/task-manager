from datetime import date


# create table for daily tasks
def create_plan_realisation_table(self):
    self.cur.execute(
        f"CREATE TABLE IF NOT EXISTS plan_realisation (id integer PRIMARY KEY AUTOINCREMENT, day date NOT NULL, plan_name varchar(20) NOT NULL, all_completed BOOLEAN NOT NULL CHECK (all_completed IN (0, 1)))"
    )
    self.con.commit()


# add new element if doesn't exist for current day or change if it already exists
def create_or_change_item_realisation(self, plan_name, all_completed):
    # get current date
    current_date = date.today()
    # checking if this option already exists
    today_elements = self.cur.execute(
        f"SELECT id FROM plan_realisation WHERE day=? AND plan_name=?",
        (current_date, plan_name),
    ).fetchone()
    if today_elements:
        self.cur.execute(
            f"UPDATE plan_realisation SET all_completed=? WHERE id=?",
            (all_completed, today_elements[0]),
        )
    else:
        self.cur.execute(
            f"INSERT INTO plan_realisation(day, plan_name, all_completed) VALUES(?,?,?)",
            (
                current_date,
                plan_name,
                all_completed,
            ),
        )
    self.con.commit()
