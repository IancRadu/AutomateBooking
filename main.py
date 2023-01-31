from xlsx_data import get_data
from booking import Booking

# Import all employee names and for each employee complete the booking, then add the hours left into an excel file
data = get_data()
data.create_new_xlsx()
for employee_username in data.read_config_xlsx():
    try:
        name = Booking(employee_username)
        name.login()
        name.go_to_project_workpackages()
        projects_assigned = name.read_projects_workpackages()
        name.go_to_daily_bookings()
        status_of_booked_hours = name.add_project_hours(projects_assigned)
        # Add username and remaining project hours to the Excel file
        data.append_new_data(data.status_logic(status_of_booked_hours), data.read_config_xlsx()[employee_username])
    except Exception:
        print('Error ********************************************************************************************')
        continue
