from Packages.subs.csv_handles import *
from Packages.subs.foos import *
import pandas as pd


class dbExcel(object):
    def __init__(self):
        csv = fr'{ROOT}\excel_sheets\recent_stats.csv'
        _for_ini = (False,
                    csv,
                    [],
                    'Serial_No'
                   )
        if _for_ini[0]:
            self.TimeStamps = True
        else:
            self.TimeStamps = False
        self.CSV = _for_ini[1]
        self.Exel = self.CSV.replace('.csv', '.xlsx')
        data = []
        data = get_recent_data(data)
        head = list(data[0].keys())
        head.append('ID')
        head.append('Statistics')
        head.extend(header['ext'])
        self.Header = head
        self.Entry_ID = _for_ini[3]
        self.ClientData = data
        self.ClientPack = ([], ({}))
        self.Empty = False
        if self.CSV:
            self.Empty = self.create_file()

    def create_file(self):
        if os.path.exists(f'{self.CSV}') is not True:
            with open(f'{self.CSV}', 'x', newline='') as csvfile:
                file_writer = csv.DictWriter(csvfile, fieldnames=self.Header)
                file_writer.writeheader()
            return True
        else:
            return False

    def update_excel(self):
        data = ''
        self.ClientData = get_recent_data(data)
        stats = dbStats()
        seperator = {'Statistics': '|'}
        for client in self.ClientData:
            client.update(seperator)
            for stat_data in stats.ClientData:
                if client['Serial_No'] == stat_data['Serial_No']:
                    client.update(stat_data)
        with open(self.CSV, 'w', newline='') as client_csv:
            writeing = csv.DictWriter(client_csv, fieldnames=self.Header)
            writeing.writeheader()
            writeing.writerows(self.ClientData)
            print('updated CSV')
        file = pd.read_csv(self.CSV, encoding='unicode_escape')
        file.to_excel(self.Exel, index=None, header=True)


def export_data_to_excel():
    xlsx = dbExcel()
    xlsx.update_excel()
