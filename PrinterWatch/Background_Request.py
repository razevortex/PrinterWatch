from Packages.RequestHandle import *
from Packages.subs.foos import running, get_recent_data, data_dict_to_store
from Packages.subs.const.ConstantParameter import data_dict_template
from Packages.subs.csv_handles import *
import time

print('start')
while running(True):
    clients = dbClient()
    clients.updateData()
    listed = clients.ClientData
    for cli in listed:
        get = ClientGet(cli)
        data = get.snmp_run_main()
        data_dict_to_store(data)
    time.sleep(1800)
