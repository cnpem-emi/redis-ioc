import pandas


class Db:
    def __init__(self, file, sheet_name):
        self.data = {}
        self.sheet = pandas.read_excel(file, sheet_name=sheet_name, dtype=str, engine='openpyxl').fillna(
            ""
        )
        for _, row in self.sheet.iterrows():
            if row["IP"] == "" or row["ENABLE"] != "True":
                continue

            if row["IP"] in self.data:
                self.data[row["IP"]].append(row.to_dict())
            else:
                self.data[row["IP"]] = [row.to_dict()]
