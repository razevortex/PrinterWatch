from .subs.foos import data_dict_to_store, method_selector, list_of_dicts_sorting as lod_sort
from .subs.csv_handles import dbClient, dbClientSpecs, SpecsLib
from .subs.const.ConstantParameter import data_dict_template
from .RequestHandle import *
import datetime as dt

request_first = dt.timedelta(seconds=0)
request_frequency = dt.timedelta(minutes=30)    #  send a request every 30 minuest to each client
re_request_frequency = dt.timedelta(minutes=5)  #  if last request wasnt succesful try again in 5 minutes
frequency_list = (request_first, request_frequency, re_request_frequency)


class QueingClients(object):
    def __init__(self):
        self.que_listing = []
        self.next_client = None

    def que_list(self):
        client = dbClient()
        client.updateData()
        client_list = lod_sort(client.ClientData, 'Time_Stamp')
        for row in client_list:
            time = row['Time_Stamp']
            request_time = dt.datetime.fromisoformat(time) + request_frequency
            self.que_listing.append((request_time, frequency_list[0], row))

    def check_que(self):
        for client in self.que_listing:
            now = dt.datetime.now()
            last, add, cli = client
            print(now, last + add)
            if now > last + add:
                print('true')
                return 'busy'
            else:
                return False

    '''        for client in self.que_listing:
                                now = dt.datetime.now()
                                last, add, cli = client
                                if now > last + add:
                    '''

    def run_through_que(self):
        for client in self.que_listing:
            now = dt.datetime.now()
            last, add, cli = client
            data_dict = data_dict_template()
            data_dict.update(cli)
            get = ClientGet(data_dict)
            data = get.snmp_run_main()
            if data_dict_to_store(data):
                self.que_listing.remove(client)
                client = (now, frequency_list[1], cli)
                self.que_listing.append(client)
                return True
            else:
                self.que_listing.remove(client)
                client = (now, frequency_list[2], cli)
                self.que_listing.append(client)
                return False




