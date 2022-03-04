from Packages.RequestHandle import *
from Packages.subs.foos import running, get_recent_data, data_dict_to_store
from Packages.subs.const.ConstantParameter import data_dict_template, run_interval
from Packages.subs.csv_handles import *
import time


def coffee_break(min, start):
    sec = int(min * 60)
    running_for = time.time() - start
    early = running_for - sec
    print('run & early', running_for, early)
    if early > 0:
        print(f'doin´ ma {early / 60} minute coffee  break!')
        time.sleep(early)


while running(True):
    start = time.time()
    clients = dbClient()
    clients.updateData()
    listed = clients.ClientData
    progress = 0
    for cli in listed:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(f'request cycle progress : {progress}/{len(listed)}')
        get = ClientGet(cli)
        data = get.snmp_run_main()
        data_dict_to_store(data)
        progress += 1
    coffee_break(run_interval, start)
