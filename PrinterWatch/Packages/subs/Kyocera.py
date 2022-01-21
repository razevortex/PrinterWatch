import copy
from Packages.subs.csv_handles import *
from .const.ConstantParameter import *
import subprocess as sp
import re

def read_snmp_response(file, key_list):
    with open(file) as infile:
        d = {}
        temp = []
        for line in infile:
            line = line.rstrip('\n')
            arr_proc = re.split(' = |::|: ', line)
            temp.append(arr_proc)
        for a in range(0, len(temp)):
            if len(temp[a]) == 4 and temp[a][3]:
                if temp[a][2] == 'STRING':
                    t = (str(temp[a][1]), str(temp[a][3].replace('"', '')))
                    if t[0] in key_list:
                        d[t[0]] = t[1]
                if temp[a][2] == 'Counter32' or temp[a][2] == 'INTEGER':
                    t = (str(temp[a][1]), str(int(re.search(r'\d+', temp[a][3]).group())))
                    if t[0] in key_list:
                        d[t[0]] = t[1]
            if t[0] == 'sysLocation.0':
                return d
    return d


def methodsKyocera(method_index):
    if 'KyoceraDefault' == method_index:
        return KyoceraDefault


class KyoceraDefault(object):
    def __init__(self, Dict, Specs):
        '''

        :param Dict: the Dict that stores all collected Data in it at this point only containing Serial_No,
                    Manufacture, Model, and IP gets filled with all data and returned
        :param Specs: a Dict that is used to choose certain functions and parameter for the specific Model
        '''
        self._dict = Dict
        if Specs['Color'] == '1':
            self.Max = copy.deepcopy(kyocera_color_toner_mib[0])
            self.Fill = copy.deepcopy(kyocera_color_toner_mib[1])
            self.Cart = copy.deepcopy(kyocera_color_toner_mib[2])
            if 'ECOSYS' in self._dict['Model']:
                self.t_dict = copy.deepcopy(kyocera_color_mib_ecosys)
                self.key_list = copy.deepcopy(kyocera_color_keys_ecosys)
            elif 'TASKalfa' in self._dict['Model']:
                self.t_dict = copy.deepcopy(kyocera_color_mib_taskalfa)
                self.key_list = copy.deepcopy(kyocera_color_keys_taskalfa)
        elif Specs['Color'] == '0':
            self.Max = copy.deepcopy(kyocera_bw_toner_mib[0])
            self.Fill = copy.deepcopy(kyocera_bw_toner_mib[1])
            self.Cart = copy.deepcopy(kyocera_bw_toner_mib[2])
            if 'FS-1320D' in self._dict['Model']:
                self.t_dict = copy.deepcopy(kyocera_bw_mib_fs1320d)
                self.key_list = copy.deepcopy(kyocera_bw_keys_fs1320d)
            else:
                self.t_dict = copy.deepcopy(kyocera_bw_mib)
                self.key_list = copy.deepcopy(kyocera_bw_keys)
        self.batch_path = fr'{ROOT}\snmp.bat'
        self.oids = kyocera_snmp_batch_oids
        self.snmp_response_path = []
        for oid in self.oids:
            temp = fr'{ROOT}\temp\*.txt'
            self.snmp_response_path.append(temp.replace('*', oid))
        id = Dict['Serial_No']
        clientSpecs = dbClientSpecs()
        cS = clientSpecs.getEntry('id', id)
        self._dict['Notes'] = cS['Notes']
        self.for_dump = []
        self.run_snmp_main()

    def create_batch(self):
        with open('snmp.bat', 'wt') as bat_file:
            bat_file.write('net user administrator /active:yes' '\n')
            for oid in self.oids:
                bat_file.write(
                    fr'snmpwalk -v1 -c public {self._dict["IP"]} {oid} mgmt > "%~dp0\temp\{oid}.txt"' '\n')

    def run_snmp_main(self):
        self.create_batch()
        p = sp.Popen(self.batch_path, shell=True, stdout=sp.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
            dic = {}
            for file in self.snmp_response_path:
                response = read_snmp_response(file, self.key_list)
                dic.update(response)
            for rkey, rval in dic.items():
                for key, val in self.Max.items():
                    if val == rkey:
                        self.Max[key] = rval
                for key, val in self.Fill.items():
                    if val == rkey:
                        self.Fill[key] = rval
                for key, val in self.Cart.items():
                    if val == rkey:
                        self.Cart[key] = rval
                for key, val in self.t_dict.items():
                    if val == rkey:
                        self.t_dict[key] = rval
            self.merge_dicts(dic)

    def merge_dicts(self, dic):
        for k, v in self._dict.items():
            for kk, vv in dic.items():
                if v == kk:
                    self._dict[k] = vv
        self._dict.update(self.toner_max_fill_calc())
        self._dict.update(self.Cart)
        self._dict.update(self.t_dict)
        for key, val in self._dict.items():
            if val in self.key_list:
                self._dict[key] = 'NaN'

    def return_dict(self):
        _dict = self._dict
        return _dict

    def toner_max_fill_calc(self):
        temp = {}
        for key, val in self.Max.items():
            m = float(100 / int(self.Max[key]))
            f = int(self.Fill[key])
            t = int(m * f)
            temp[key] = t
        return temp
