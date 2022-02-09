import random
import PySimpleGUI as sg
if __name__ == '__main__':
    from subs.const.ConstantParameter import header as _header, ROOT, data_dict_template
    from subs.foos import list_of_dicts_sorting as lod_sort, get_recent_data, import_ip_file
    from subs.csv_handles import ConfigLib, dbRequest, dbClientSpecs, LibOverride
else:
    from .subs.const.ConstantParameter import header as _header, ROOT, data_dict_template
    from .subs.foos import list_of_dicts_sorting as lod_sort, get_recent_data, import_ip_file
    from .subs.csv_handles import ConfigLib, dbRequest, dbClientSpecs, LibOverride
    from .PlotData import *
import datetime as dt

# from .Dev.processing_time import FooRunTime
''' for checking the run time of a function uncomment the import above and use the wrapper @FooRunTime on the function
@FooRunTime
def foo():
    return None
'''


class GUI(object):
    def __init__(self):
        self.ConfigDict = {}
        self.TableHeaderAll = _header['data_table']
        self.TableHeader = []
        self.TableData = []
        self.Sort_Key = ''
        self.TableColorCode = ()
        self.MainWindowPos = (0, 0)
        self.InfoWindow = None
        self.imgs = None
        self.img_num = 0
        self.PlotWindow = None
        self.plot = None
        self.WindowMin = False
        self.ThemeChanger(True)
        self.RunState = False
        self.Pipe2Main = 0
        self.select = {}
        self.ConfigWindow = None
        self.event = None
        self.right_click_menu = ['non', ['Config', 'Plotting', 'About', 'Help', 'Close']]
        now = dt.datetime.now()
        self.clock = now.strftime('%H:%M')
        print(self.clock)
        self.update_GUI(True)
        self.MainWindow = self.window_builder()

    def window_read(self):
        event, values = self.MainWindow.read(timeout=250)
        return event, values

    def update_GUI(self, first):
        self.select = None
        self.TableData = []
        for data in get_recent_data(data_dict_template()):
            self.TableData.append(data)
        conf = ConfigLib()
        self.ConfigDict = conf.getEntry('id', '0')
        temp = self.ConfigDict['data_table_displayed'].split('|')
        self.TableHeader = []
        for val in range(len(self.TableHeaderAll)):
            if temp[val] == '1':
                self.TableHeader.append(self.TableHeaderAll[val])
        self.Sort_Key = self.ConfigDict['Sort_Key']
        self.TableData = lod_sort(self.TableData, self.Sort_Key)
        if first is not True:
            self.MainWindowPos = self.MainWindow.current_location()
            self.MainWindow.close()
            self.MainWindow = self.window_builder()

    def window_config_read(self):
        event2, values2 = self.ConfigWindow.read(timeout=100)
        return (event2, values2)

    def update_clock(self, time):
        now = time
        if now.strftime('%H:%M') != self.clock:
            self.clock = now.strftime('%H:%M')
            return '_clock'
        else:
            return None

    def get_pipe(self):
        return self.Pipe2Main

    def get_run(self):
        return self.RunState

    '''    def update_run_state(self):
            if self.RunState is not False:
                if self.RunState == 'busy':
                    self.MainWindow['-State-'].update('Busy', button_color='Red')
                else:
                    self.MainWindow['-State-'].update('Idle', button_color='Green')
            else:
                self.MainWindow['-State-'].update('Sleeping', button_color='Blue')'''

    #   GET_EVENT Methods

    def get_event(self):
        event, values = self.window_read()
        if event != '__TIMEOUT__':
            print(event)
            if event == 'add_client':
                self.Pipe2Main = (event, values)
                self.get_pipe()
                return (event, values)
            if event == '_Table_':
                i = values['_Table_']
                self.select = self.TableData[i[0]]
                if self.InfoWindow is not None:
                    self.InfoWindow.close()
                    self.InfoWindow = None
                self.InfoWindow = self.info_window_builder()


        if event == 'Close' or event == sg.WIN_CLOSED:
            self.RunState = 'Close'
            if self.InfoWindow is not None:
                self.InfoWindow.close()
            if self.ConfigWindow is not None:
                self.ConfigWindow.close()
            return '_Exit'

        #if event == '-State-':
        #    self.RunState = True if self.RunState is not True else False
        #    self.Pipe2Main = (event, self.RunState)


        if event == '-Toolbar-':
            event = values['-Toolbar-']
        if event == 'Config' and self.ConfigWindow == None:
            self.ConfigWindow = self.config_window_builder()
        if event == 'Plotting':
            self.plot = PlotMenu()
            self.PlotWindow = self.plot.PlotWindow
        if self.update_clock(dt.datetime.now()) == '_clock':
            self.MainWindow['_clock'].update(self.clock)

        if event == 'import_client':
            file = None
            while file is None:
                file = sg.popup_get_file(default_path=ROOT, file_types=(("ALL Files", "*.txt"),),
                              message=f'Choose a text file that includes IPs they should get extracted based on their'
                                      f'ints/. pattern')
            values = import_ip_file(file)
            print(values)
            self.Pipe2Main = (event, values)
            self.get_pipe()
            return (event, values)
        if event == '_randomTheme':
            self.ThemeChanger(True)
            self.update_GUI(False)
        if self.PlotWindow is None:
            plot = None
        self.get_event_secondary_Window()

    def get_event_secondary_Window(self):
        if self.PlotWindow is not None:
            event, values = self.PlotWindow.read()
            if self.plot.run(event, values) == 'Close':
                self.PlotWindow.close()
                self.PlotWindow = None
        if self.InfoWindow is not None:

            event, values = self.InfoWindow.read()

            if event == 'Close' or event == sg.WIN_CLOSED:
                self.InfoWindow.close()
                self.InfoWindow = None
            if event == '_add_override':
                t_dic = {'ID': values['_target'], values['_override_key']: values['_override_val']}
                override = LibOverride()
                override.addEntry(t_dic)
            if event == '_plot' or event == '_plot+':
                try:
                    bw, cym, enough_data = get_cli_data(values['_target'], nill=True)
                    if enough_data:
                        if bw is not False:
                            self.InfoWindow['_bw_page'].update(f'{bw} € per Monochrome Page', visible=True)
                        else:
                            print('bw data invalid')
                        if cym is not False:
                            self.InfoWindow['_cym_page'].update(f'{cym} € per Colored Page', visible=True)
                        else:
                            print('cym data invalid')
                except:
                    print('received some invalid data for efficience')
                try:
                    if event == '_plot':
                        self.imgs = plot_client_statistics(values['_target'],in_browser=False, nill=True)
                    elif event == '_plot+':
                        self.imgs = plot_client_statistics(values['_target'], in_browser=True, nill=True)
                    self.img_num = 0
                    self.InfoWindow['_next_img'].update(visible=True)
                    self.InfoWindow[f'-IMAGE-'].update(data=self.imgs[self.img_num], visible=True)
                except:
                    print('something went wrong while trying to create plot')
            if event == '_next_img':
                self.img_num = self.img_num + 1 if self.img_num < 2 else 0
                self.InfoWindow[f'-IMAGE-'].update(data=self.imgs[self.img_num])
        if self.ConfigWindow is not None:
            event, values = self.window_config_read()
            if event == 'Close' or event == sg.WIN_CLOSED:
                self.ConfigWindow.close()
                self.ConfigWindow = None
            if event == 'SaveConf':
                self.store_configs(values)
                self.ConfigWindow.close()
                self.ConfigWindow = None
                self.update_GUI(False)

    #       MAIN WINDOW LAYOUT METHODS

    def getRowColors(self):
        trigger_vals = ['TonerBK', 'TonerC', 'TonerM', 'TonerY']
        temp = []
        for i in range(len(self.TableData)):
            data = self.TableData[i]
            val = 100
            for trigger in trigger_vals:
                if data[trigger] != 'NaN':
                    val = int(data[trigger]) if int(data[trigger]) < val else val
            if val <= 20:
                t = (i, 'yellow', 'black')
                temp.append(t)
            if val <= 10:
                t = (i, 'red', 'black')
                temp.append(t)
        return temp

    def layout_table(self):
        self.getRowColors()
        try:
            data = self.TableData
            display_data = []
            for row in data:
                temp = []
                for col in self.TableHeader:
                    temp.append(row[col])
                display_data.append(temp)
            table_layout = [[sg.Table(values=display_data,
                                      enable_events=True,
                                      key='_Table_',
                                      justification='top',
                                      headings=self.TableHeader,
                                      display_row_numbers=False,
                                      auto_size_columns=True,
                                      row_colors=self.getRowColors(),
                                      num_rows=min(25, len(display_data)))]]
            return table_layout
        except:
            return [sg.Text('Placeholder: here goes the table as soon it has something to display')]

    def layout_import(self):
        return [sg.Frame('Add Clients:',
                         [[sg.Column([
                             [sg.InputText(key='add_2_list', default_text='enter ip here',
                              visible=True, size=20, justification='left')],
                             [sg.Button('Add IP', key='add_client', bind_return_key=True, visible=True)]],
                           pad=(0, 0), justification='left'),
                           sg.Column([
                             [sg.Button('Import IP File', key='import_client', visible=True)]],
                           pad=(25, 5))]],
                size=(310, 90), relief=sg.RELIEF_RIDGE, pad=(0, 0),
                tooltip='Enter a IP and Click "Add IP" or press "Enter" to add a single client or pick a file.txt formated like : ip1,ip2,...')
                ]

    def layout_toolbar(self):
        if self.RunState is not False:
            if self.RunState == 'busy':
                button = [sg.Button(button_text='Busy', key='-State-', button_color='Red')]
            else:
                button = [sg.Button(button_text='Idle', key='-State-', button_color='Green')]
        else:
            button = [sg.Button(button_text='Sleeping', key='-State-', button_color='Grey')]

        return [[
            sg.Column([[sg.In(right_click_menu=self.right_click_menu, visible=False)],
                       [sg.ButtonMenu('Menu', self.right_click_menu, key='-Toolbar-')]],
                      justification='top', pad=(0, 0)),
            sg.Column([button], justification='top', pad=(0, 0), visible=False),
            sg.Column([[sg.Button(button_text=self.clock, key='_clock')]],
                      justification='top', pad=(0, 0)),
            sg.Column([[sg.Button(button_text='ain´t I pretty?',
                                  key='_randomTheme', visible=True)]],
                      justification='top', pad=(0, 0))
        ]]

    def selected_box(self):
        string = 'none selected'
        if self.select is not None:
            info = []
            for key, val in self.select.items():
                if key == 'Serial_No' or key == 'IP' or key == 'Manufacture' or key == 'Model':
                    string += f'{key}  :  {val}'
            info.append([sg.Text(string, visible=True, key='info_box')])
            return info
        else:
            return [sg.Text(string, visible=False, key='info_box')]


    # CONFIG WINDOW LAYOUT METHODS


    def layout_config_layout(self):
        layout = []
        for i in range(len(self.TableHeaderAll)):
            if self.TableHeaderAll[i] in self.TableHeader:
                active = True
            else:
                active = False
            layout.append([sg.Checkbox(self.TableHeaderAll[i], key=self.TableHeaderAll[i], default=active)])
        return [[
            layout]]


    def store_configs(self, value_dict):
        config = ConfigLib()
        dict = config.getEntry('id', '0')
        string = ''
        for i in self.TableHeaderAll:
            if value_dict[i]:
                string += '1'
            else:
                string += '0'
            if i != 'Notes':
                string += '|'
        dict['data_table_displayed'] = string
        dict['Sort_Key'] = value_dict['_sorting_']
        config.addingEntry(dict)

    # This is more of a little gimmik that adds to the random chosen theme on each start it will switch the window
    # window theme on the 'ain`t i pretty?'

    def ThemeChanger(self, event):
        if event:
            selection_failed = True
            while selection_failed:
                try:
                    themes = sg.theme_list()
                    num = random.randint(0, len(themes))
                    design = str(themes[num])
                    sg.theme(design)
                    selection_failed = False
                except:
                    selection_failed = True

    # CLIENT INFO WINDOW METHODS

    def layout_info_table(self):
        try:
            key = 'Time_Stamp'
            datadb = dbRequest(self.select['Serial_No'])
            temp = datadb.ClientData
            head = datadb.Header
            data = []
            for row in temp:
                t = []
                for val in list(row.keys()):
                    t.append(row[val])

                data.append(t)

            table_layout = [[sg.Table(values=data,
                                      enable_events=True,
                                      key='_Table_',
                                      justification='top',
                                      headings=head,
                                      display_row_numbers=False,
                                      auto_size_columns=True,
                                      num_rows=min(10, len(data)))]]
            return table_layout
        except:
            return [sg.Text('Placeholder: here goes the table as soon it has something to display')]

    #   WINDOW_BUILDER METHODS

    def window_builder(self):
        return sg.Window('PrinterWatch',
                         [[self.layout_toolbar()], [self.layout_table()],
                          [self.layout_import(), self.selected_box()],
                          [sg.Button('Exit', key='Close', visible=True)]],
                         location=self.MainWindowPos,
                         grab_anywhere=True,
                         no_titlebar=False,
                         right_click_menu=self.right_click_menu,
                         titlebar_icon=f'{ROOT}PrinterWatch.ico',
                         icon=f'{ROOT}PrinterWatch.ico'
                         )

    def config_window_builder(self):
        return sg.Window('Config', [self.layout_config_layout(),
                                    [sg.Combo(self.TableHeader,
                                              size=(20, 4),
                                              enable_events=True,
                                              default_value=self.Sort_Key,
                                              key='_sorting_')],
                                    [sg.Button('Save', key='SaveConf'),
                                     sg.Button('Discard', key='Close')]
                                    ],

                         grab_anywhere=True,
                         no_titlebar=False,
                         )

    def info_window_builder(self):
        head_vals = ['Serial_No', 'IP', 'Manufacture', 'Model', 'Location']
        string = 'Client : '
        for key, val in self.select.items():
            if key in head_vals:
                string += f' | {self.select[key]}'
        string += '|'
        head = [[sg.Text(string, key='_client')]]
        return sg.Window('Info', [head, [sg.Text('bypass data'),
                                         sg.Combo(_header['override'][1::], key='_override_key'),
                                         sg.InputText(key='_override_val'),
                                         sg.InputText(visible=False, key='_target', default_text=self.select['Serial_No']),
                                         sg.InputText(visible=False, key='_head', default_text=string),
                                         sg.Button('Override', key='_add_override', bind_return_key=True)],
                                  [self.layout_info_table()],
                                  [sg.Button('Statistics', key='_plot'), sg.Button('in Browser', key='_plot+')],
                                  [sg.Image(size=(500, 500), key='-IMAGE-', visible=False),
                                  [[sg.Text('nan', key='_bw_page', visible=False)],
                                   [sg.Text('nan', key='_cym_page', visible=False)]]],
                                  [sg.Button('next', key='_next_img', visible=False)]],

                         grab_anywhere=True,
                         no_titlebar=False,
                         )

'''    def info_window_builder(self):
        head_vals = ['Serial_No', 'IP', 'Manufacture', 'Model', 'Location']
        string = 'Client : '
        for key, val in self.select.items():
            if key in head_vals:
                string += f' | {self.select[key]}'
        string += '|'
        head = [[sg.Text(string, key='_client')]]
        return sg.Window('Info', [head,  [sg.Button('Statistics', key='_plot')],
                                  [self.layout_info_table(),
                                   [sg.Combo(_header['override'][1::], key='_override_key'), sg.InputText(key='_override_val'),
                                    sg.InputText(visible=False, key='_target', default_text=self.select['Serial_No']),
                                    sg.InputText(visible=False, key='_head', default_text=string),
                                    sg.Button('Override', key='_add_override', bind_return_key=True)]],
                                  [sg.Image(size=(500, 500), key='-IMAGE-', visible=False),
                                  [[sg.Text('nan', key='_bw_page', visible=False)],
                                   [sg.Text('nan', key='_cym_page', visible=False)]]],
                                  [sg.Button('next', key='_next_img', visible=False)]],

                         grab_anywhere=True,
                         no_titlebar=False,
                         )
'''
# THIS IS ONLY A TEST ENV TO RUM THE GUI ON ITS OWN FOR DEBUG & DEV PURPOSES
'''

def test():
    now = dt.datetime.now()
    gui = GUI()
    gui.update_clock(now)
    while True:
        if '_Exit' == gui.get_event():
            break


if __name__ == '__main__':
    test()
'''