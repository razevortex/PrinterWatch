import os

_HERE = os.path.join(os.path.dirname(__file__))
temp = _HERE.split(r'Packages')
# ROOT stores the absolute path to the project directory with \ at its end
ROOT = temp[0]
# example : 'D:\pypro\PrinterWatch2.1.1\'

# the header dict stores the csv/dict keys of each file/dict as list
header = {'request_db': ['TonerBK', 'TonerC', 'TonerM', 'TonerY',
                         'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM',
                         'Status_Report', 'Time_Stamp'],
          'client_db': ['Serial_No', 'IP', 'Manufacture', 'Model', 'Time_Stamp'],
          'client_specs': ['Serial_No', 'CartBK', 'CartC', 'CartM', 'CartY', 'Location', 'Contact', 'Notes'],
          'model_specs': ['Model', 'Color', 'Scanner', 'Cart', 'MethodIndex'],
          'data_table': ['Serial_No', 'IP', 'Manufacture', 'Model', 'TonerBK', 'TonerC', 'TonerM', 'TonerY',
                         'Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM', 'Status_Report', 'Time_Stamp',
                         'CartBK', 'CartC', 'CartM', 'CartY', 'Location', 'Contact', 'Notes'],
          'config': ['Config_ID', 'data_table_displayed', 'Sort_Key'],
          'override': ['ID', 'Key', 'Val']
          }

# kyocera mib list index´s 0 = Max, 1 = Fill, 2 = Cart
kyocera_color_toner_mib = [{'TonerC': 'mib-2.43.11.1.1.8.1.1', 'TonerM': 'mib-2.43.11.1.1.8.1.2',
                            'TonerY': 'mib-2.43.11.1.1.8.1.3', 'TonerBK': 'mib-2.43.11.1.1.8.1.4'},
                           {'TonerC': 'mib-2.43.11.1.1.9.1.1', 'TonerM': 'mib-2.43.11.1.1.9.1.2',
                            'TonerY': 'mib-2.43.11.1.1.9.1.3', 'TonerBK': 'mib-2.43.11.1.1.9.1.4'},
                           {'CartC': 'mib-2.43.11.1.1.6.1.1', 'CartM': 'mib-2.43.11.1.1.6.1.2',
                            'CartY': 'mib-2.43.11.1.1.6.1.3', 'CartBK': 'mib-2.43.11.1.1.6.1.4'}]

kyocera_color_mib_ecosys = {'Printed_BW': 'enterprises.1347.42.3.1.2.1.1.1.1',
                             'Printed_BCYM': 'enterprises.1347.42.3.1.2.1.1.1.2',
                             'Copied_BW': 'enterprises.1347.42.3.1.2.1.1.2.1',
                             'Copied_BCYM': 'enterprises.1347.42.3.1.2.1.1.2.2',
                             'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                             'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}
kyocera_color_mib_taskalfa = {'Printed_BW': 'enterprises.1347.42.3.1.2.1.1.1.1',
                             'Printed_BCYM': 'enterprises.1347.42.3.1.2.1.1.1.3',
                             'Copied_BW': 'enterprises.1347.42.3.1.2.1.1.2.1',
                             'Copied_BCYM': 'enterprises.1347.42.3.1.2.1.1.2.3',
                             'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                             'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}


kyocera_bw_toner_mib = [{'TonerBK': 'mib-2.43.11.1.1.8.1.1'},
                        {'TonerBK': 'mib-2.43.11.1.1.9.1.1'},
                        {'CartBK': 'mib-2.43.11.1.1.6.1.1'}]

kyocera_bw_mib = {'Printed_BW': 'enterprises.1347.42.3.1.1.1.1.1',
                  'Copied_BW': 'enterprises.1347.42.3.1.1.1.1.2',
                  'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                  'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}
kyocera_bw_mib_fs1320d = {'Printed_BW': 'enterprises.1347.42.3.1.1.1.1.1',
                          'Copied_BW': 'enterprises.1347.42.3.1.1.1.1.2',
                          'Status_Report': 'enterprises.1347.43.18.2.1.2.1.1',
                          'Contact': 'sysContact.0', 'Location': 'sysLocation.0'}
kyocera_color_keys_ecosys = []
for d in kyocera_color_toner_mib:
    for keys, vals in d.items():
        kyocera_color_keys_ecosys.append(vals)
for keys, vals in kyocera_color_mib_ecosys.items():
    kyocera_color_keys_ecosys.append(vals)

kyocera_color_keys_taskalfa = []
for d in kyocera_color_toner_mib:
    for keys, vals in d.items():
        kyocera_color_keys_taskalfa.append(vals)
for keys, vals in kyocera_color_mib_taskalfa.items():
    kyocera_color_keys_taskalfa.append(vals)

kyocera_bw_keys_fs1320d = []
for d in kyocera_bw_toner_mib:
    for keys, vals in d.items():
        kyocera_bw_keys_fs1320d.append(vals)
for keys, vals in kyocera_bw_mib.items():
    kyocera_bw_keys_fs1320d.append(vals)


kyocera_bw_keys = []
for d in kyocera_bw_toner_mib:
    for keys, vals in d.items():
        kyocera_bw_keys.append(vals)
for keys, vals in kyocera_bw_mib.items():
    kyocera_bw_keys.append(vals)

kyocera_snmp_batch_oids = ['1.3.6.1.2.1.43.11',  # oid part for all the toner values
                           '1.3.6.1.4.1.1347.42.3.1',  # oid part for all the Page counter
                           '1.3.6.1.4.1.1347.43.18.2.1.2.1.1',  # oid part for status monitor
                           '1.3.6.1.2'  # base walk for location and contact i would like to have a more specific oid
                                        # but did not find a working one yet
                           ]

# the data_dict_template creates an empty dict that gets filled with the gathered client data and then updated in a list
# of all these dicts from the clients the gui table pulls its data out of this list
def data_dict_template():
    data_dict_temp = {}
    for val in header['data_table']:
        data_dict_temp[val] = 'NaN'
    return data_dict_temp


# error_code is not implemented yet but is planed to store certain outputs
# of common occuring errors for helping with debugging
error_code = ['csv_handles 404 no matching key was found',
              'csv_handles the entry tryed to add didnt had the expected amount of values']

# this group of lists/dicts is used by the RequestHandle.ClientGet initiating the request and gathering the data
# needed to identify the method used for the request
ManufacturerList = ['KYOCERA', 'Brother']
translate_Kyocera = {'Manufacture': 'Kyocera', '2.43.5.1.1.16.1': 'Model', '2.43.5.1.1.17.1': 'Serial_No'}
translate_Brother = {'Manufacture': 'Brother', 'hrDeviceDescr.1': 'Model', '2.43.5.1.1.17.1': 'Serial_No'}
mib_head_snmp = {'Kyocera': translate_Kyocera, 'Brother': translate_Brother}
'''
>> manufacture_oid, string
if manufacturerList in string
mib = mib_head_snmp[manufacturerList[entry]
data_dict[Manufacture] = mib[Manufacture]   

>> oid, string
for key, val in mib.items():
    if oid in key:
        data_dict[mib[key]] = string   
'''
