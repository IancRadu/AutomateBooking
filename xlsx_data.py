import pandas as pd
from datetime import date

from booking import convert_to_hours


class get_data:
    @staticmethod
    def read_config_xlsx():
        try:
            df = pd.read_excel("./Config.xlsx", "Config", header=0).to_dict()
            config = {}
            for i in df["Name"]:
                config[df["User_Name"][i]] = df["Name"][i]
            return config
        except PermissionError:
            pass  # returns None if Config Excel file is open

    @staticmethod
    def create_new_xlsx():
        df = pd.DataFrame({'Name': [],
                           'Status': []})

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(f'Booking_{date.today()}.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        writer.close()

    @staticmethod
    def status_logic(remaining_data):
        projects = []
        print(f'from status logic {remaining_data}')
        for key in remaining_data[0]:
            print(key)
            print(remaining_data[0][key][0])
            if key == 'Hours not booked':
                if remaining_data[0][key][1] > 0:
                    return f'Add new project, {convert_to_hours(remaining_data[key][1])} hours need to be booked.'
            else:
                if remaining_data[0][key][0] > 0:
                    projects.append(f'{key}: {convert_to_hours(remaining_data[0][key][0])} hours left')
        print(projects)
        return projects

    @staticmethod
    def append_new_data(data, name):
        # Read old values
        df1 = pd.read_excel(f'Booking_{date.today()}.xlsx', "Sheet1", header=1)
        # Add new values
        df2 = pd.DataFrame({'Name': [name],
                            'Status': [data]})
        # Merge all values
        df = pd.concat([df1, df2])

        writer = pd.ExcelWriter(f'Booking_{date.today()}.xlsx', engine='openpyxl')

        df.to_excel(writer, sheet_name="Sheet1", index=False)
        # Exit writer
        writer.close()

# data = get_data()
# print(data.read_config_xlsx())
# print(data.read_values(data.read_config_xlsx()[1]))
