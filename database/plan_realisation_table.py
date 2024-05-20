from datetime import date, timedelta


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
    # checking if this option already exists - updating item
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

    all_tab_days = self.cur.execute(
        f"SELECT all_completed FROM plan_realisation WHERE plan_name=?",
        (plan_name,),
    ).fetchall()
    total_completed_days = [i[0] for i in all_tab_days].count(1)
    consecutive_days = 0 
    while True:
        current_date -= timedelta(days=1)
        day_completed = self.cur.execute(
            f"SELECT all_completed FROM plan_realisation WHERE day=? AND plan_name=?",
            (current_date, plan_name),
        ).fetchone()
        if day_completed and day_completed[0]: # day_completed can be a Nonetype if there is no date
            consecutive_days += 1
        else:
            break
    return total_completed_days, consecutive_days
    