import copy

import PySimpleGUI as sg
if __name__ == '__main__':
    from subs.const.ConstantParameter import header as _header, ROOT, data_dict_template
    from subs.foos import list_of_dicts_sorting as lod_sort, get_recent_data, import_ip_file
    from Packages.subs.csv_handles import *
else:
    from .subs.const.ConstantParameter import header as _header, ROOT, data_dict_template
    from .subs.foos import list_of_dicts_sorting as lod_sort, get_recent_data, import_ip_file
    from Packages.subs.csv_handles import *
import plotly.express as px
import pandas as pd


class PlotMenu(object):
    def __init__(self):
        self.ts = []
        self.selection_dict = self.get_dbs()
        self.selectors = {'client_amount': ['Multiple', 'Single', 'All', ''],
                          'client_filter': {'Multiple': ['Manufacture', 'Model', 'Cart', ''],
                                            'Single': ['Manufacture', 'Model'], '': ['']},
                          'available_client': [''],
                          'client': [''],
                          'value_filter': ['TonerBK', 'TonerC', 'TonerM', 'TonerY', 'TonerCYM',
                                           'TonerAll', 'MonochromePages', 'ColoredPages', 'TotalPages'],
                          'processing': ['instance', 'relative', 'absolute', 'ratio']}

        self.val_dict = {'TonerBK': ['TonerBK'],
                             'TonerAll': ['TonerBK', 'TonerC', 'TonerM', 'TonerY'],
                             'MonochromePages': ['Printed_BW', 'Copied_BW'],
                             'ColoredPages': ['Printed_BCYM', 'Copied_BCYM'],
                             'TotalPages': ['Printed_BW', 'Copied_BW', 'Printed_BCYM', 'Copied_BCYM']}

        self.PlotWindow = sg.Window('Plotting Menu', layout=[self.checkbox_layout(),
                                                             self.set_selectors(),
                                                             [sg.Button('CreatPlot', key='plotting', visible=False)],
                                                             [sg.Button('Efficiency BW', key='eff_bw', visible=False)],
                                                             [sg.Button('Efficiency Col', key='eff_col', visible=False)]])
        if __name__ == '__main__':
            self.run(None, None)

    def get_filtered_ip_list(self, filter, val):
        client = dbClient()
        client.updateData()
        t = []
        for i in client.ClientData:
            if i[filter] == val:
                t.append(i['IP'])
        return t

    #               WINDOW READ & EVENT HANDLE

    def run(self, event, values):
        if __name__ == '__main__':
            event, values = self.PlotWindow.read(timeout=100)
        if event == 'Close' or event == sg.WIN_CLOSED:
            if __name__ == '__main__':
                self.PlotWindow.close()
            return 'Close'
        if event == 'client_amount':
            if values['client_amount'] != '' and values['client_amount'] != 'All':
                self.PlotWindow.Element('client_filter').update(visible=True,
                                                                values=self.selectors['client_filter'][
                                                                    values['client_amount']])
                self.PlotWindow.Element('client_filter_label').update(visible=True)
            else:
                self.PlotWindow.Element('client').update(visible=False, values='')
                self.PlotWindow.Element('client_filter').update(visible=False)
                self.PlotWindow.Element('client_filter_label').update(visible=False)
                self.PlotWindow.Element('available_client_label').update(visible=False)
        if event == 'client_filter':
            if values['client_filter'] != '':
                self.PlotWindow.Element('available_client').update(values=self.selection_dict[values['client_filter']],
                                                                   visible=True)
                self.PlotWindow.Element('available_client_label').update(visible=True)
            else:
                self.PlotWindow.Element('client').update(visible=False)
                self.PlotWindow.Element('available_client').update(visible=False)
                self.PlotWindow.Element('available_client_label').update(visible=False)
        if event == 'available_client':
            if values['available_client'] != '' and values['client_amount'] == 'Single':
                self.PlotWindow.Element('client').update(values=self.get_filtered_ip_list(values['client_filter'],
                                                                                          values['available_client']),
                                                         visible=True)
                self.PlotWindow.Element('client_label').update(visible=True)
        if values['client'] != '' and values['client_amount'] == 'Single':
            self.PlotWindow.Element('plotting').update(visible=True)

        elif values['available_client'] != '' and values['client_amount'] == 'Multiple':
            self.PlotWindow.Element('plotting').update(visible=True)
        elif values['client_amount'] == 'All':
            self.PlotWindow.Element('client').update(visible=False, values='')
            self.PlotWindow.Element('client_filter').update(visible=False)
            self.PlotWindow.Element('client_filter_label').update(visible=False)
            self.PlotWindow.Element('available_client_label').update(visible=False)
            self.PlotWindow.Element('plotting').update(visible=True)
            self.PlotWindow.Element('eff_bw').update(visible=True)
            self.PlotWindow.Element('eff_col').update(visible=True)
        else:
            self.PlotWindow.Element('plotting').update(visible=False)
            self.PlotWindow.Element('eff_bw').update(visible=False)
            self.PlotWindow.Element('eff_col').update(visible=False)
        if event == 'plotting' or event == 'eff_bw' or event == 'eff_col':
            if event == 'plotting' and values['processing'] != '':
                eff = False
                req_id, req_val = self.creating_plot(values)
            elif event == 'eff_bw':
                eff = 'eff_bw'
                val = {'TonerBK': True, 'TonerC': False, 'TonerM': False, 'TonerY': False, 'TonerCYM': False,
                       'TonerAll': False, 'MonochromePages': False, 'ColoredPages': False, 'TotalPages': True,
                       'client_amount': 'All'}
                req_id, req_val = self.creating_plot(val)
            elif event == 'eff_col':
                eff = 'eff_col'
                val = {'TonerBK': False, 'TonerC': False, 'TonerM': False, 'TonerY': False, 'TonerCYM': True,
                       'TonerAll': False, 'MonochromePages': False, 'ColoredPages': True, 'TotalPages': False,
                       'client_amount': 'All'}
                req_id, req_val = self.creating_plot(val)
            t_dic = {}
            ts = []
            for id in req_id:
                # preprocessing var is for testing the output of get class
                req = dbRequest(id)
                result = req.getPlottingData(req_val)
                if len(result[req_val[0]]) > 1:
                    for val in result[req_val[0]]:
                        ts.append(val[1])
                    ts = list(set(ts))
                    ts.sort()
                for d in req_val:
                    if result[d] != '':
                        string = f'{id}{d}'
                        t_dic[string] = result[d]
            self.generate_plot(t_dic, ts, values['processing'], values['client_amount'], req_val, eff)

    def generate_plot(self, t_dic, ts, proc, client_amount, values, eff):

        temp = {}
        data = {}
        data_ts = {}
        for t in ts:
            temp[t] = 0
        total_dic = {'values': [], 'keys': []}
        for key in list(t_dic.keys()):
            fill_ts = copy.deepcopy(temp)
            for entry in t_dic[key]:
                fill_ts[entry[1]] = entry[0]
            data[key] = list(fill_ts.values())
            if proc == 'Over Time':
                for i in range(1, len(data[key])):
                    data[key][i] = data[key][i - 1] + data[key][i]
            if proc == 'Total':
                v = 0
                for i in range(len(data[key])):
                    v += data[key][i]
                total_dic['values'].append(v)
                total_dic['keys'].append(key)
        time_stamp_list = []
        for key in list(temp.keys()):
            time_stamp_list.append(key)
        data_ts['Time_Stamp'] = time_stamp_list
        data['Time_Stamp'] = time_stamp_list
        if client_amount == 'All':
            all_data = self.merge_ids(data, values, eff)
            if eff == 'eff_bw' or eff == 'eff_col':
                t = []
                i = []
                available = list(all_data.keys())
                for key in all_data['Index']:
                    if key in available:
                        t.append(all_data[key])
                        i.append(key)
                all_data = {'per Toner': t, 'index': i}
                df = pd.DataFrame(all_data)
                fig = px.bar(data_frame=df, x='index',
                             y='per Toner')
                fig.update_layout(title_text=eff)
                fig.show()
                return
            df = pd.DataFrame(all_data)
            keys = list(all_data.keys())
            keys.remove('Time_Stamp')

        else:
            df = pd.DataFrame(data)
            keys = list(data.keys())
            keys.remove('Time_Stamp')

        if proc == 'Over Time':
            fig = px.line(data_frame=df, x='Time_Stamp',
                          y=keys)

            fig.show()
        elif proc == 'per Time Periode':
            fig = px.line(data_frame=df, x='Time_Stamp',
                          y=keys)

            fig.show()
        elif proc == 'Total':
            df = pd.DataFrame(total_dic)
            fig = px.bar(data_frame=df, x='keys', y='values')
            fig.show()

    def merge_ids(self, data, values, eff):
        temp = {}
        print(data)
        print(values)

        t = []
        for i in range(len(data['Time_Stamp'])):
            t.append(0)
        for v in values:
            t_list = copy.copy(t)
        if eff is not False:
            client = dbClient()
            client.updateData()
            calc_eff = {}
            calc_val = [0, 0]
            serials = []
            for line in client.ClientData:
                serials.append(line['Serial_No'])
            for serial in serials:
                calc_val = [0, 0]
                for t_key, t_val in data.items():
                    if t_key.startswith(serial):
                        if t_key.endswith(values[0]):
                            calc_val[0] = sum(t_val)
                        if t_key.endswith(values[1]):
                            calc_val[1] = sum(t_val)
                if calc_val[0] != 0 and calc_val[1] != 0:
                    t = int((100 / calc_val[0]) * calc_val[1])
                    calc_eff[serial] = t
            calc_eff['Index'] = serials
            return calc_eff
        else:
            for key, val in data.items():
                if key != 'Time_Stamp' and v in key:
                    for i in range(len(t)):
                        t_list[i] += val[i]
            temp[v] = t_list
        temp['Time_Stamp'] = data['Time_Stamp']

        if eff != 'eff_bw' and eff != 'eff_col':
            return temp
        else:
            '''client = dbClient()
               client.updateData()
               calc_eff = {}
               calc_val = [0, 0]
               for line in client.ClientData:
                   for t_key, t_val in temp.items():
                       calc_val = [0, 0]
                       if t_key.startswith(line['Serial_No']):
                           if 'Toner' in t_key:
                               calc_val[0] = t_val
                           if 'Pages' in t_key:
                               calc_val[1] = t_val
                   if calc_val[0] != 0 and calc_val[1] != 0:
                       t = int((100 / calc_val[0]) * calc_val[1])
                       calc_eff[line['Serial_No']] = t
               calc_eff['Time_Stamp'] = data['Time_Stamp']
               return calc_eff
               '''

            t = []
            for key in temp.keys():
                if 'Toner' in key:
                    t.append(temp[key])
                if 'Pages' in key:
                    t.append(temp[key])
            calc = []
            for i in range(len(t)):
                if t[i][0] != 0 and t[i][1] != 0:
                    c = int((100 / t[i][0]) * t[i][1])
                    calc.append(c)
            temp = {'eff': calc, 'Time_Stamp': data['Time_Stamp']}
            return temp

    def fill_ts(self, ts_temp, id_data):
        t_id_data = []
        val_store = 0
        for ts in ts_temp.keys():
            found = False
            ts_temp[ts] = 0
            for val_list in id_data:
                if ts in val_list[1] and found is not True:
                    found = True
                    ts_temp[ts] += val_list[0]
                if found is not True:
                    ts_temp[ts] += val_store
            val_store = ts_temp[ts]
            t_id_data.append(val_store)
        return t_id_data

    #               LAYOUT GENERATING

    def checkbox_layout(self):
        layout = []
        for val in self.selectors['value_filter']:
            layout.append(sg.Checkbox(val, key=val))
        return layout

    def set_selectors(self):
        layout = []

        layout.append([[sg.Text('processing', key='processing_label')],
                     [sg.Combo(self.selectors['processing'], key='processing',
                               default_value='', size=(20, 10), enable_events=True)]])
        vis = True
        for i in list(self.selectors.keys()):
            if i != 'value_filter' or i != 'processing':
                t = [[sg.Text(i, visible=vis, key=f'{i}_label')],
                     [sg.Combo(self.selectors[i], key=i, visible=vis,
                               default_value='', size=(20, 10), enable_events=True)]]
                layout.append(t)
                vis = False
        print(layout)
        return layout

    #           GET DATA FOR SELECTION
    def creating_plot(self, values):
        requested_val = []
        for val in self.selectors['value_filter']:
            if values[val] is not False:
                requested_val.append(val)
        return self.get_plot_client_ids(values), requested_val

    def get_plot_client_ids(self, values):
        if values['client_amount'] == 'All':
            t = []
            client = dbClient()
            client.updateData()
            for line in client.ClientData:
                t.append(line['Serial_No'])
            return t
        if values['client_amount'] == 'Multiple':
            t = []
            if values['client_filter'] != 'Cart':
                client = dbClient()
                client.updateData()
                db = client.ClientData
                for line in db:
                    if line[values['client_filter']] == values['available_client']:
                        t.append(line['Serial_No'])
            else:
                spec = dbClientSpecs()
                spec.updateData()
                db = spec.ClientData
                for line in db:
                    if values['available_client'] in line.values():
                        t.append(line['Serial_No'])
            return t
        elif values['client_amount'] == 'Single':
            client = dbClient()
            client.updateData()
            db = client.ClientData
            t = []
            for line in db:
                if line['IP'] == values['client']:
                    return [line['Serial_No']]

    def get_dbs(self):
        client = dbClient()
        client.updateData()
        dict_t = {'Serial_No': [], 'IP': [], 'Manufacture': [], 'Model': [],
                  'Cart': []}
        key_t = list(dict_t.keys())
        for i in client.ClientData:
            for key in key_t:
                if key in list(i.keys()):
                    dict_t[key].append(i[key])
        spec = dbClientSpecs()
        spec.updateData()
        t = []
        for i in spec.Header:
            if 'Cart' in i:
                t.append(i)
        for i in spec.ClientData:
            for key in t:
                if i[key] != 'NaN':
                    dict_t['Cart'].append(i[key])
        for key in list(dict_t.keys()):
            dict_t[key] = list(set(dict_t[key]))
            dict_t[key].sort()
        return dict_t

if __name__ == '__main__':
    plotter = PlotMenu()
    start = True
    while start:
        exit = plotter.run(None, None)
        if exit == 'Close':
            start = False