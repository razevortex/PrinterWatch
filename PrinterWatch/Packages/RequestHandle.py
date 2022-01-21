import subprocess as sp
import re
import os

if __name__ == '__main__':
    from subs.const.ConstantParameter import *
    from subs.Brother import *
    from subs.csv_handles import *
    from subs.foos import *
else:
    from .subs.const.ConstantParameter import *
    from .subs.Brother import *
    from .subs.csv_handles import *
    from .subs.foos import *

test_dict = {'IP': '172.20.10.58'}
mib = mib_head_snmp


class ClientGet(object):
    def __init__(self, dict):
        self.dict = data_dict_template()
        self.dict.update(dict)
        self.batch_path = fr'{ROOT}\snmp.bat'
        self.snmp_response_path = fr'{ROOT}\temp\*.txt'
        self.snmp_run_oid = ['1.3.6.1.2']
        self.for_dump = [fr'{ROOT}\temp\{self.snmp_run_main}.txt']


    def snmp_run_main(self):
        oid = self.snmp_run_oid
        self.create_batch(oid)
        p = sp.Popen(self.batch_path, shell=True, stdout=sp.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
            response_files = ''
            for id in oid:
                _file = self.snmp_response_path.replace('*', id)
                response_files = self.read_response_file(_file)
            got_mandatory = [False, False, False, False]
            count_mandatorys = 0
            mib_manuf = mib_head_snmp
            for entry in response_files:
                if 'sysDescr.0' in entry[0]:
                    for manuf in ManufacturerList:
                        if manuf in entry[1]:
                            manuf = 'Kyocera' if manuf == 'KYOCERA' else manuf
                            self.dict['Manufacture'] = manuf
                            mib_manuf = mib_manuf[manuf]
                            got_mandatory[count_mandatorys] = True
                            count_mandatorys += 1
                elif got_mandatory[0]:
                    for keys, vals in mib_manuf.items():
                        if keys in entry[0]:
                            self.dict[vals] = entry[1]
                            got_mandatory[count_mandatorys] = True
                            count_mandatorys += 1
            specs_lib = SpecsLib(self.dict['Manufacture'])
            for i in specs_lib.ClientData:
                if i['Model'] in self.dict['Model']:
                    self.dict['Model'] = i['Model']
                    specs_method = method_selector(specs_lib, self.dict['Manufacture'], self.dict['Model'])
                    method = specs_method(self.dict, i)
                    self.dict.update(method.return_dict())
                    return self.dict

    def create_batch(self, oids):
        with open('snmp.bat', 'wt') as bat_file:
            bat_file.write('net user administrator /active:yes' '\n')
            for oid in oids:
                string = fr'{ROOT}\temp\{oid}.txt'
                self.for_dump.append(string)
                bat_file.write(fr'snmpwalk -v1 -c public {self.dict["IP"]} {oid} mgmt > "%~dp0\temp\{oid}.txt"' '\n')

    def read_response_file(self, file):
        with open(file) as infile:
            arr = []
            temp = []
            for line in infile:
                line = line.rstrip('\n')
                arr_proc = re.split(' = |::|: ', line)
                temp.append(arr_proc)
            for a in range(0, len(temp)):
                if len(temp[a]) == 4 and temp[a][3]:
                    if temp[a][2] == 'STRING':
                        t = (str(temp[a][1]), str(temp[a][3].replace('"', '')))
                        arr.append(t)
                    if temp[a][2] == 'Counter32' or temp[a][2] == 'INTEGER':
                        t = (str(temp[a][1]), str(int(re.search(r'\d+', temp[a][3]).group())))
                        arr.append(t)
        return arr

