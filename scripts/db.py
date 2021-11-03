import pylightxl

COLUMNS = []
IP_INDEX = 0
ENABLE_INDEX = 0


class Db:
    def __init__(self, file, sheet_name):
        self.data = {}
        self.sheet = list(pylightxl.readxl(file).ws(sheet_name).rows)
        COLUMNS = self.sheet[0]
        IP_INDEX = COLUMNS.index("IP")
        ENABLE_INDEX = COLUMNS.index("ENABLE")
        for row in self.sheet[1:]:
            if row[IP_INDEX] == "" or row[ENABLE_INDEX] != "True":
                continue

            row_dict = {}

            for i, col in enumerate(row, 0):
                row_dict[COLUMNS[i]] = str(col)

            if row[IP_INDEX] in self.data:
                self.data[row[IP_INDEX]].append(row_dict)
            else:
                self.data[row[IP_INDEX]] = [row_dict]
