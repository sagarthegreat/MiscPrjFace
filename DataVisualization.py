from matplotlib import pyplot as plt
from datetime import datetime, timedelta


class DataVis:
    def __init__(self, database):
        self.database = database

    def display_total_hours(self, name, start_date, end_date):
        start_date = datetime.strptime(start_date, "%m%d%Y").date()
        end_date = datetime.strptime(end_date, "%m%d%Y").date()

        current_date = start_date
        dates = []
        hours = []

        while current_date <= end_date:
            date_string = "table_" + current_date.strftime("%m%d%Y")
            curr_result = self.database.select_from_table(name, current=date_string)
            if not curr_result:
                current_date += timedelta(days=1)
                continue

            entry_time_str = curr_result[0][2]
            exit_time_str = curr_result[0][3]

            entry_time = datetime.strptime(entry_time_str, "%H:%M:%S").time()
            exit_time = datetime.strptime(exit_time_str, "%H:%M:%S").time()

            duration = datetime.combine(datetime.min, exit_time) - datetime.combine(datetime.min, entry_time)

            dates.append(current_date.strftime("%m%d%Y"))
            hours.append(duration.total_seconds() / 3600)  # Convert timedelta to hours

            current_date += timedelta(days=1)

        total_sum_hours = sum(hours)
        plt.bar(dates, hours)
        plt.xlabel("Date")
        plt.ylabel("Total Hours")
        plt.title("Total Hours Worked per Day")
        plt.xticks(rotation=45)
        plt.text(0.05, 0.95, f"Total Hours: {total_sum_hours:.2f}", transform=plt.gca().transAxes, va='center')
        plt.show()
