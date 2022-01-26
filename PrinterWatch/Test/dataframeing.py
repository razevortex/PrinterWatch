import pandas as pd
import plotly.express as px
from Packages.subs.csv_handles import *

#   The Vars needed as input
man_dic = {'Brother': [], 'Kyocera': []}
client = dbClient()
client.updateData()
all = []
dic = {}
arr = []
for line in client.ClientData:
    all.append(line['Serial_No'])
    man_dic[line['Manufacture']].append(line['Serial_No'])
    if line['Model'] == 'ECOSYS M6635cidn':
        arr.append(line['Serial_No'])
arr = list(set(arr))
for a in arr:
    dic[a] = []
#for line in client.ClientData:
#    dic[line['Model']].append(line['Serial_No'])
#print(dic)

value_list = [[['Printed_BW', 'Copied_BW', 'Printed_BCYM', 'Copied_BCYM'], ['TonerBK', 'TonerC', 'TonerM', 'TonerY']],
              [['Printed_BCYM', 'Copied_BCYM'], ['TonerC', 'TonerM', 'TonerY']]]

#   Foo that Handles the Collecting of the data from the csv files


def pre_processing(client, value_list, val_type='Pages', timemode='absolute', index='Time_Stamp'):
    value_list.append(index)
    df = pd.read_csv(filepath_or_buffer=f'../db/{client}.csv',
                     usecols=value_list, index_col='Time_Stamp')
    arr = {}
    for val in value_list:
        if val != 'Time_Stamp':
            t = list(df[val])
            n = t[0]
        else:
            continue
        if n != 'NaN':
            arr[val] = []

            if timemode == 'absolute':
                counter = 0
                if val_type == 'Toner':
                    for i in t[1::]:
                        if n > i:
                            counter += n - i
                        n = i
                    arr[val].append(counter)
                if val_type == 'Pages':
                    counter = t[-1] - n
                    arr[val].append(counter)

            if timemode == 'instance':
                for i in t[1::]:
                    if val_type == 'Toner':
                        if n > i:
                            arr[val].append(n - i)
                        else:
                            arr[val].append(0)
                        n = i
                    if val_type == 'Pages':
                        arr[val].append(i - n)
                        n = i

            if timemode == 'relative':
                counter = 0
                for i in t[1::]:
                    if val_type == 'Toner':
                        if n > i:
                            counter += n - i
                        arr[val].append(counter)
                        n = i
                    if val_type == 'Pages':
                        counter += i - n
                        arr[val].append(counter)
                        n = i

    t_df = pd.DataFrame(arr)
    t_df['sum'] = t_df.sum(numeric_only=True, axis=1)


    if timemode == 'absolute':
        df = pd.DataFrame({f'{client}': t_df['sum']})
        return df
    else:
        df = pd.DataFrame({f'{client}': t_df['sum']})

        df['Time_Stamp'] = pd.read_csv(filepath_or_buffer=f'../db/{client}.csv',
                                       usecols=['Time_Stamp'])

        #df['datetime'] = pd.to_datetime(df['Time_Stamp'])
        #position = df.columns.get_loc('datetime')
        #df['elapsed'] = df.iloc[1:, position] - df.iat[0, position]
        #print(df['elapsed'])
        df = df.set_index('Time_Stamp')
        print(df)
        return df


#   Foo that takes the input variables aswell offers some keys to offer options how the data should get plotted


def processing(value_list, client_list, plot='', val_type='', mode=''):
    if val_type == '':
        if value_list[0].startswith('Toner'):
            val_type = 'Toner'
        else:
            val_type = 'Pages'
    if mode == '':
        if plot == 'bar':
            mode = 'absolute'
        else:
            plot = 'line'
            mode = 'relative'
    #df = pd.DataFrame()
    df = pre_processing(client_list[0], value_list, val_type=val_type, timemode=mode)
    for cli in client_list[1::]:
        if plot == 'bar':
            df[cli] = pre_processing(cli, value_list, val_type=val_type, timemode=mode)
            print(df[cli])
        elif plot == 'line':
            df = df.append(pre_processing(cli, value_list, val_type=val_type, timemode=mode), sort=True)
            df.sort_index(inplace=True)
            df.fillna(method='ffill', inplace=True)
            #df.fillna(0, inplace=True)
            df.sort_index(inplace=True)
            print('used   ', df)
    df.sort_index(inplace=True)
    df.fillna(method='ffill', inplace=True)
    #df.fillna(0, inplace=True)
    df.sort_index(inplace=True)
    #print(plot, df)
    return df


def create_plot(value_list, client_list, plot='', val_type='', mode='', foo=''):
    '''
    :param value_list: a list of the values of the csv that get collected and summed up
    :param client_list: a list of the serial_no of the printers that get included in the plot
    :param plot: 'bar' or 'line' default is line
    :param val_type: should useualy not be needed it changes the sum method according to the collected values
                 since page counter and toner monitor working different as sayed it should pick the val_type by itself
    :param mode: 'absolute', 'relative' and 'instance' relative to the time data got collected and instance gets the difference between each messurement
    :param foo:
    :return:
    '''
    if foo == 'ratio':
        if type(client_list) is dict:
            df_total = pd.DataFrame()
            for key, val in client_list.items():
                df = 100 / processing(value_list[1], val, plot='bar') * processing(value_list[0], val, plot='bar')
                print(df)
                df[key] = df.sum(numeric_only=True, axis=1)
                df = pd.DataFrame({f'{key}': df[key]}, index=df.index)
                print(df)
                df_total = df_total.append(df, sort=True)
                df_total.sort_index(inplace=True)
                df_total.fillna(method='ffill', inplace=True)
                df_total.fillna(0, inplace=True)
                df_total.sort_index(inplace=True)
                df_total = df_total.tail(1)
            print(df_total)
            fig = px.bar(data_frame=df_total, y=df_total.columns, barmode='group')
            fig.show()
        else:
            df = 100 / processing(value_list[1][1], client_list, plot='bar') * processing(value_list[1][0], client_list,
                                                                                      plot='bar')
            fig = px.bar(data_frame=df, y=df.columns, barmode='group')
            fig.show()
    if foo == '':
        df = processing(value_list, client_list, plot=plot, val_type=val_type, mode=mode)
        if plot == 'bar':
            fig = px.bar(data_frame=df, y=df.columns, barmode='group')
        else:
            fig = px.line(data_frame=df, x=df.index, y=df.columns)
        fig.show()
    if foo == 'compare':
        df_total = pd.DataFrame()
        for key, val in client_list.items():
            df = processing(value_list, val, plot=plot, val_type=val_type, mode=mode)

            df[key] = df.sum(axis=1)
            df = pd.DataFrame({f'{key}': df[key]}, index=df.index)

            df_total = df_total.append(df, sort=True)

        df = copy.deepcopy(df_total)
        df.sort_index(inplace=True)
        df.fillna(method='ffill', inplace=True)
        df.fillna(0, inplace=True)
        df.sort_index(inplace=True)
        df_total['Total'] = df.sum(axis=1)
        df_total.sort_index(inplace=True)
        df_total.fillna(method='ffill', inplace=True)
        df_total.fillna(0, inplace=True)
        df_total.sort_index(inplace=True)

        if plot == 'bar':
            fig = px.bar(data_frame=df_total, y=df_total.columns, barmode='group')
        else:
            fig = px.line(data_frame=df_total, x=df_total.index, y=df_total.columns)
        fig.show()


create_plot(value_list[0][0], arr, plot='line')
