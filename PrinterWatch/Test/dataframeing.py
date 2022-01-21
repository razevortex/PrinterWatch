import pandas as pd
import plotly.express as px
from Packages.subs.csv_handles import *


#   The Vars needed as input

client = pd.read_csv(filepath_or_buffer='../db/clients.csv', usecols=['Serial_No'])

column = list(client['Serial_No'])

value_list = ['Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM'] #['TonerBK'] #, 'TonerC', 'TonerM', 'TonerY'] #,['Printed_BW', 'Printed_BCYM', 'Copied_BW', 'Copied_BCYM'] ]


#   Foo that Handles the Collecting of the data from the csv files


def pre_processing(client, value_list, type='Pages', timemode='absolute', index='Time_Stamp'):
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
                if type == 'Toner':
                    for i in t[1::]:
                        if n > i:
                            counter += n - i
                        n = i
                    arr[val].append(counter)
                if type == 'Pages':
                    counter = t[-1] - n
                    arr[val].append(counter)

            if timemode == 'instance':
                for i in t[1::]:
                    if type == 'Toner':
                        if n > i:
                            arr[val].append(n - i)
                        else:
                            arr[val].append(0)
                        n = i
                    if type == 'Pages':
                        arr[val].append(i - n)
                        n = i

            if timemode == 'relative':
                counter = 0
                for i in t[1::]:
                    if type == 'Toner':
                        if n > i:
                            counter += n - i
                        arr[val].append(counter)
                        n = i
                    if type == 'Pages':
                        counter += i - n
                        arr[val].append(counter)
                        n = i

    t_df = pd.DataFrame(arr)
    t_df['sum'] = t_df.sum(axis=1)
    if timemode == 'absolute':
        df = pd.DataFrame({f'{client}': t_df['sum']})
        return df
    else:
        df = pd.DataFrame({f'{client}': t_df['sum']})
        df['Time_Stamp'] = pd.read_csv(filepath_or_buffer=f'../db/{client}.csv',
                                       usecols=['Time_Stamp'])
        df = df.set_index('Time_Stamp')
        return df


#   Foo that takes the input variables aswell offers some keys to offer options how the data should get plotted


def plotting(value_list, client_list, plot='', type='', mode=''):
    if type == '':
        if value_list[0].startswith('Toner'):
            type = 'Toner'
        else:
            type = 'Pages'
    if mode == '':
        if plot == 'bar':
            mode = 'absolute'
        else:
            plot = 'line'
            mode = 'relative'

    df = pre_processing(client_list[0], value_list, type=type, timemode=mode)
    for cli in client_list[1::]:
        if plot == 'bar':
            df[cli] = pre_processing(cli, value_list, type=type, timemode=mode)
        elif plot == 'line':
            df = df.append(pre_processing(cli, value_list, type=type, timemode=mode), sort=True)

    df.sort_index(inplace=True)
    df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)
    df.sort_index(inplace=True)


    if plot == 'bar':
        fig = px.bar(data_frame=df, y=df.columns, barmode='group')
    else:
        fig = px.line(data_frame=df, x=df.index, y=df.columns)
    fig.show()


plotting(value_list, column, plot='bar')
