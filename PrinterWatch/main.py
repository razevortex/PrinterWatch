from Packages.GraphicUserInterface import *
from Packages.RequestHandle import *
from Packages.QueHandle import *
from Packages.subs.foos import running, get_recent_data, data_dict_to_store, add_ip, run_background_requests, check_on_requests
from Packages.subs.const.ConstantParameter import data_dict_template
from Packages.createXLSX import *
import copy
import time
import pandas as pd
import subprocess as sp
from subprocess import Popen

###         Main Foo


def main():
    pending = []
    gui_handle = GUI()
    run = False
    request_active = False
    pipe = 0
    last_update = time.time()

    while running(True):
        if request_active == False:
             request_active = Popen(["python", "Background_Request.py"], creationflags=sp.CREATE_NEW_CONSOLE)
        else:
            if request_active.poll():
                print(request_active.poll())
                request_active = False

        if time.time() - last_update > 60:
            last_update = time.time()
            gui_handle.update_GUI(False)
            try:
                export_data_to_excel()
            except:
                print('updateing excel was not possible')
            print(last_update)
        gui_handle.get_event()
        pipe = gui_handle.Pipe2Main
        run = gui_handle.get_run()

        if run == 'Close':
            gui_handle.MainWindow.close()
            break

        if pipe != 0:
            eve, val = pipe
            if eve == 'add_client':
                gui_handle.RunState = 'busy'

                ip = {'IP': val['add_2_list']}
                pending.append(ip)
                get = ClientGet(ip)
                data = get.snmp_run_main()
                data_dict_to_store(data)
                gui_handle.update_GUI(False)
                gui_handle.RunState = True
                pipe = 0
                gui_handle.Pipe2Main = 0
            if eve == 'import_client':

                for ips in val:
                    ip = {'IP': ips}
                    pending.append(ip)
                gui_handle.RunState = True
                pipe = 0
                gui_handle.Pipe2Main = 0

        if pending != []:
            gui_handle.RunState = 'busy'
            pending, progress, last = add_ip(pending, ClientGet)
            print(f'{progress} ip´s pending to get added')
            print(f'added {last[0]} = {last[1]}')


if __name__ == '__main__':
    export_data_to_excel()
    main()
