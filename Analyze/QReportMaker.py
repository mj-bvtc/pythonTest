import sys
import os
import math
import getpass
import traceback
import pandas as pd
import datetime as dt
from string import ascii_uppercase as alpha


try:
    fname = __file__.split('\\')[-1]
except:
    fname = "quote_rx.py"


version = ''
try:
	range = xrange
	version = '2'
except:
	version = '3'

home  = os.path.abspath(fname)
logpath = os.getcwd() + "\\usage.log"

os.chdir(os.path.expanduser("~") + '/Desktop')



comp_cols = ['Phase', 'Deleted', 'Client ID', 'Estimating ID', 'Survey ID', 'Block ID',
             'Profile', 'Sample', 'Sample Req', 'Description', 'Ornament', 'Page', 'Space', 'Form Method']

final_cols = ['Phase', 'Deleted', 'Client ID', 'Estimating ID', 'Survey ID', 'Block ID',
              'Profile', 'Sample', 'Sample Req', 'Description', 'Ornament', 'Page', 'Space', 'Form Method', '# Units',
              '# DWGS', '# Models', '# Molds']

price_cols = ['Model Price', 'Price/Mold', 'Price/Unit', 'M/M_Total', 'Unit_Total', 'Line_Total']

def reset_cols():
    global comp_cols, final_cols, price_cols

    comp_cols = ['Phase', 'Deleted', 'Client ID', 'Estimating ID', 'Survey ID', 'Block ID',
                 'Profile', 'Description', 'Ornament', 'Page', 'Space', 'Form Method']

    final_cols = ['Phase', 'Deleted', 'Client ID', 'Estimating ID', 'Survey ID', 'Block ID',
                  'Profile', 'Description', 'Ornament', 'Page', 'Space', 'Form Method', '# Units',
                  '# DWGS', '# Models', '# Molds']

    price_cols = ['Model Price', 'Price/Mold', 'Price/Unit', 'M/M_Total', 'Unit_Total', 'Line_Total']

    return


def read_in(path, projnum):
    """
        Reads in excel or CSV file
    """

    is_xlsx = path.endswith('xlsx')
    if is_xlsx:
        data = pd.read_excel(path, header = 1)
        for i,r in data.iterrows():
            if r.isnull().all():
                rmv = i - 1
                break
        data = data.loc[:rmv]
        proj_name = pd.read_excel(path, skiprows = range(1, 10000)).columns[0]

        if not (proj_name and proj_name != 'Phase'):
            proj_name = ' '.join(path.split('/')[-1].split(' --- ')[0].split()[:-2])

        return data, proj_name
    else:
        data = pd.read_csv(path)
        if data.shape[1] == 1:
            data = pd.read_csv(path, sep = '\t')

        # DEFAULT VALUES IF NECESSARY
        if 'Phase' not in data.columns:
            data['Phase'] = 'Base Bid'

        if 'Phase #' not in data.columns:
            data["Phase #"] = 1

        if 'Form Method' not in data.columns:
            data["Form Method"] = "HP"

        if 'Drafting ID' in data.columns:
            data.rename(columns = {'Drafting ID': 'Block ID'}, inplace = True)
        if 'Deleted' not in data.columns:
            data['Deleted'] = ''
        proj = [c for c in data.columns if 'Project #' in c]
        if proj:
            data.rename(columns = {proj[0]: 'Project #'}, inplace = True)
            if (data['Project #'] == '').all():
                data['Project #'] = 'TypeProjectNumberHere' if projnum == '-' else projnum

        else:
            data['Project #'] = 'TypeProjectNumberHere' if projnum == '-' else projnum
                

        return data



def clean_up(w):
    w = '' if str(w) == 'None' or pd.isnull(w) else w
    if isinstance(w, str):
        w = w.split('_')[-1].replace('.', '')
        if 'Page' in w:
            w = w.replace('Page ', '').title()
    return w


def clean_row(r):
    try:
        if r.Deleted == 'Checked':
            r['# Units'] *= -1
            r.Deleted = 'Deleted'
        else:
            r.Deleted = ''
    except: pass
    try:
        if r['Phase #'] and r['Phase'] != 'Base Bid':
            r.Phase += ' ' + str(int(r['Phase #']))
    except: pass
    try:
        if not r['Sample']:
            r['Sample Req'] = ''
    except: pass
    return r

def default_vals(r):
    if r['Phase'] == '':
        r['Phase'] = 'Base Bid'
    if r['Phase #'] == '':
        r['Phase #'] = 1
    if r['Form Method'] == '':
        r['Form Method'] = 'HP'
    return r

def newest_id(df):
    ids = ['Block ID', 'Survey ID', 'Estimating ID', 'Client ID']
    for n in ids:
        if n in df.columns:
            if (df[n] != '').any():
                return n


def concat_values(data, id, cols, sep = ','):
    j = 1
    sec_id = [i for i in cols if 'ID' in i]
    if sec_id:
        sec_id = sec_id[-1]
    sep =  ' ' + sep.replace(' ', '') + ' '
    for n in pd.unique(data[id]):
        piece = data.loc[data[id] == n]
        for phase in pd.unique(data['Phase']):
            sing_phase = piece.loc[piece['Phase'] == phase]
            if n:
                for c in cols:
                    if 'ID' in c or c == 'Space' or 'Sample' in c:
                        data.loc[(data['Phase'] == phase) & (data[id] == n), c] = sep.join([i for i in sorted(pd.unique(sing_phase[c])) if i])
                    elif c == 'Page' and len(pd.unique(sing_phase[c])) > 1:
                        data.loc[(data['Phase'] == phase) & (data[id] == n), c] = 'Varies'
            elif sec_id:
                for f in pd.unique(piece[sec_id]):
                    data.loc[(data.Phase == phase) & (data[sec_id] == f) & (data[id] == n), id] = '.' * j
                    j += 1
    return data


def group(data):
    new_id = newest_id(data)

    # Makes sure all ID columns are strings
    ids = [col for col in data.columns if "ID" in col]
    for i in ids:
        data[i] = [str(val) for val in data[i]]

    cols = [c for c in data.columns if c != new_id and '#' not in c and (data[c]!='').any()]

    data = concat_values(data, new_id, cols)

    func = data.groupby(['Phase', new_id], as_index = False)
    sums = func.sum()
    new = func.min()
    new['# Units'] = sums['# Units']
    new = pd.concat([new[new.Phase == 'Base Bid'], new[new.Phase != 'Base Bid']], axis = 0)
    new.index = range(len(new))
    new.loc[:, new_id] = new[new_id].apply(lambda x: x.replace('.', ''))
    return new


def make_counts(df):
    def counts(row):
        if ('-1' in row[newest] or '-' not in row[newest] or newest == 'Estimating ID') and row['# Units'] > 0:
            if row['Phase'] != 'Base Bid' and len(df[df[newest] == row[newest]]) > 1:
                    row['# DWGS']   = 0
                    row['# Models'] = 0
                    try:
                        total = sum([x for x in df.loc[:row.name].loc[(df[newest].str.contains(row[newest].split('-')[0])), '# Units'] if x > 0])
                    except:
                        raise TypeError("# Units column contains types besides int/float")
                    other = total - sum([x for x in df.loc[(df.Phase == row.Phase) & (df[newest].str.contains(row[newest].split('-')[0])), '# Units'] if x > 0])
                    row['# Molds'] = int(math.ceil(total / 12.) - math.ceil(other / 12.))
            else:
                row['# DWGS'] = 1
                if row['Form Method'] in ['HP', 'Slip']:
                    row['# Models'] = 1
                    try:
                        total = sum([x for x in df.loc[(df.Phase == row.Phase) & (df[newest].apply(lambda x: x.split('-')[0]) == row[newest].split('-')[0]), '# Units'] if x > 0])
                    except:
                        raise TypeError("# Units column contains types besides int/float")
                    row['# Molds'] = int(math.ceil(total / 12.))
                else:
                    row['# Models'] = 0
                    row['# Molds']  = 0
        else:
            row['# DWGS']   = 0
            row['# Models'] = 0
            row['# Molds']  = 0
        return row

    newest = newest_id(df)
    count_cols = ['# DWGS', '# Models', '# Molds']
    df = pd.concat([df, pd.DataFrame(columns = count_cols)], axis = 1)

    return df.apply(counts, axis = 1)


def make_desc(data):
    desc_cols = ['Description', 'Type', 'Orientation', 'Region']
    for c in desc_cols:
        if c not in data.columns:
            data[c] = ""
    data['Region'] = data.loc[:, 'Region'].apply(lambda x: 'at ' + x if x else x)
    new_col = pd.DataFrame(data[desc_cols].apply(lambda n: ', '.join([i.strip() for i in n if i != '']), axis = 1), columns = ['Description'])
    data = pd.concat([data.drop(desc_cols, axis = 1), new_col], axis = 1)
    return data[[c for c in final_cols if c in data.columns]]


def add_prices(data):
    price_df = pd.DataFrame({c: [0]*len(data.index) for c in price_cols}, index = data.index)
    price_df = price_df[price_cols]
    data = pd.concat([data, price_df], axis = 1)
    return data[[i for i in final_cols + price_cols if i in data.columns]]


def make_excel_sheet(df, writer, phase_ls, project_name, brainsheet):

        if brainsheet:
            final_cols.remove("Page")
            final_cols.remove("Profile")
            final_cols.remove("Space")
            df = df[[c for c in final_cols + price_cols if c in df.columns]]

        cols = df.columns

        sp = one = 0
        for num, sheet_name in enumerate(phase_ls):
            single = False
            new = df.copy()
            if sheet_name != 'Total':
                new = new[new.Phase == sheet_name]
                single = True

            new, line_spots = get_totals(new, cols)
            new = new[cols]

            if single:
                new = make_link(new, sp)

            if brainsheet:
                new = add_eqns(new) if not single else new

            if single:
                sp += len(new)
            else: 
                new = add_deleted(new)

            sheet_name = sheet_name.replace('/', '-')

            # Saves as excel file
            new.to_excel(writer, sheet_name = sheet_name, index = False, startrow = 1)

            # Formats the excel file
            format(new, writer, line_spots, sheet_name, project_name, brainsheet)

        writer.save()


def get_totals(data, cols):
    """
        Creates Summation rows for each phase
    """

    spots = [len(data[data.Phase == p]) for p in pd.unique(data.Phase)]
    j = 0
    added_rows = 0
    for i in range(len(spots)):
        spots[i] += j + added_rows
        j = spots[i]
        added_rows = 1
    spots = [0] + spots

    end = len(cols) - 1

    final = pd.DataFrame(columns = data.columns)
    blank = pd.DataFrame({c:'' for c in data.columns}, index = [-1])

    for ind, p in enumerate(pd.unique(data.Phase)):
        plu = 4 if ind else 3
        section = data.loc[data.Phase == p]
        sums = blank.copy()

        sums.loc[-1, 'Deleted'] = 'Total'

        for u in data.columns:
            if '#' in u:
                lett = alpha[list(data.columns).index(u)]
                if 'CO' not in u:
                    sums.loc[-1, u] = '=SUMIF(' + lett + str(spots[ind] + plu) + ':' + lett + str(spots[ind + 1] + 2) + ',">0")'
                else:
                    sums.loc[-1, u] = '=SUM(' + lett + str(spots[ind] + plu) + ':' + lett + str(spots[ind + 1] + 2) + ')'
        if 'Unit_Total' in cols:
            sums.loc[-1, 'M/M_Total'] = '=SUM(' + alpha[end -2] + str(spots[ind] + plu) + ':' + alpha[end -2] + str(spots[ind + 1] + 2) + ')'
            sums.loc[-1, 'Unit_Total'] = '=SUM(' + alpha[end -1] + str(spots[ind] + plu) + ':' + alpha[end -1] + str(spots[ind + 1] + 2) + ')'
            sums.loc[-1, 'Line_Total'] = '=SUM(' + alpha[end] + str(spots[ind] + plu) + ':' + alpha[end] + str(spots[ind + 1] + 2) + ')'

        section = pd.concat([section, sums])
        final = pd.concat([final, section], ignore_index = True)

    final = final[cols]

    spots = [t + 1 for t in spots[1:]]

    return final, spots


def make_link(df, spot):
    """
        Links the sub sheets' price values
        back to the "Total" sheet
    """

    strings = ['Phase', 'Deleted', 'Client ID', 'Estimating ID', 'Survey ID', 'Block ID',
              'Profile', 'Sample', 'Sample Req', 'Description', 'Ornament', 'Page', 'Space', 'Form Method']
    end = len(df.columns) - 1
    lbls = ['Model Price', 'Price/Mold',
            'Price/Unit', 'M/M_Total',
            'Unit_Total', 'Line_Total']
    additions = zip(df.columns[1:], [alpha[list(df.columns).index(a)] for a in df.columns][1:])  

    for i in df.index:
        row = str(i + spot + 3)
        if df.loc[i, 'Deleted'] != 'Total':
            for n,let in additions:
                add = let + row
                if n in strings:
                    add += ' & ""'
                if n in df.columns:
                    df.loc[i, n] = '=Total!' + add
    return df


def add_eqns(df):
    """
        Adds equations to calculate prices
    """

    def lett(col): return alpha[list(df.columns).index(col)]
    for i in df.index:
        row = str(i + 3)
        if df.loc[i, 'Deleted'] != 'Total':
            df.loc[i, 'M/M_Total'] = '=IF(' + lett('Deleted') + row + '<>"",0,' + lett('# Molds') + row + '*' + lett('Price/Mold') + row + '+' + lett('Model Price') + row + ')'
            df.loc[i, 'Unit_Total'] = '=IF(' + lett('Deleted') + row + '<>"",0,' + lett('# Units') + row + '*' + lett('Price/Unit') + row + ')'
            df.loc[i, 'Line_Total'] = '=IF(' + lett('Deleted') + row + '<>"",0,' + 'SUM(' + lett('M/M_Total') + row + ',' + lett('Unit_Total') + row + '))'
    return df


def add_deleted(df):
    """
        Adds eqn for deleted column
    """
    units = "# Units"
    if units not in df.columns:
        units = newest_id(df).split()[0] + ' ' + units 
    lett = alpha[list(df.columns).index(units)]

    for i, row in df.iterrows():
        if row.Deleted != "Total":
            df.loc[i, "Deleted"] = "=IF(" + lett + str(i + 3) + '<=0,"Deleted","") & ""'
    return df


def format(df, writer, line_spots, sheet_name, project_name, brainsheet):
    if not isinstance(line_spots, list):
        line_spots = [line_spots]

    wb = writer.book
    ws = writer.sheets[sheet_name]

    center_form = {'align': 'center', 'valign': 'vcenter', 'border': 1}

    fmt = wb.add_format(center_form)


    # "Totals" row format dictionary
    totals = {'bold': True, 'bg_color': '#ccf7f9', 'font_size': 12}
    totals.update(center_form)

    # "Totals" row format
    tot_fmt = wb.add_format(totals)

    # Determining the last Letter in excel columns
    col_end = len(df.columns) - 1
    end_lett = alpha[col_end]

    # Determining "Totals" rows positions
    rows = [str(i + 2) for i in line_spots]
    lines = [('B' + r + ':' + end_lett + r) for r in rows]

    # Adding formats to the "Totals" rows
    for l in lines:
        ws.conditional_format(l, {'type': 'no_errors', 'format': tot_fmt})

    if sheet_name == 'Total':
        # Finding total sums and the excel index row
        tot_row = str(int(rows[-1]) + 4)
        tot_sum_line, tot_list = tot_sum(df, rows[-1], brainsheet)

        # Adding total sums row to excel with total format
        for r in range(len(tot_sum_line)):
            if tot_list[r]:
                ws.write(alpha[r + 1] + str(int(tot_row) - 1), tot_list[r], tot_fmt)
            if tot_sum_line[r]:
                ws.write(alpha[r + 1] + tot_row, tot_sum_line[r], tot_fmt)


    # Create color format for 'Total' rows
    color_fmt = wb.add_format(center_form)
    if brainsheet:
        color_fmt.set_bg_color('#dddddd')


    # Setting the rest of the cells' format
    for b in range(3, int(rows[-1])):
        if str(b) not in rows:
            norm = 'B' + str(b) + ':' + alpha[col_end] + str(b)

            ws.conditional_format(norm, {'type': 'no_errors', 'format': fmt})

            other = alpha[col_end -2] + str(b) + ':' + end_lett + str(b)
            ws.conditional_format(other, {'type': 'no_errors', 'format': color_fmt})


    # Merging same Phase rows
    merge_fmt = wb.add_format(center_form)
    merge_fmt.set_bold()
    merge_fmt.set_border()

    # Determining which rows to merge together
    mg = [('3', rows[0])]
    for p in range(1, len(rows)):
        mg.append([str(int(rows[p-1]) + 1), rows[p]])

    # Getting list of different phases
    phases = [q for q in pd.unique(df.Phase) if q]

    # Applying merge
    for ind, name in zip(mg, phases):
        ws.merge_range('A' + ind[0] + ':' + 'A' + ind[1], name, merge_fmt)

    # Setting size of columns
    size_fmt = wb.add_format(center_form)
    size_fmt.set_border(0)
    size_fmt.set_text_wrap()

    # Determine what each column size should be
    col_sizes = get_col_sizes(df)

    # Adjusting column sizes
    for cn in range(len(df.columns)):
        ws.set_column(cn, cn, col_sizes[cn] + 3, size_fmt)

    # Adding title
    title_fmt = wb.add_format(center_form)
    title_fmt.set_border(0)
    title_fmt.set_bold()
    title_fmt.set_font_size(20)
    ws.merge_range('A1:F1', project_name, title_fmt)

    if brainsheet:
        fmt_money(df, wb, ws, sheet_name)


def tot_sum(df, end, brainsheet):
    """
        Creates the count and price totals at bottom of
        "Total" sheet
    """

    columns = [c for c in df.columns if '#' in c] + ['M/M_Total', 'Unit_Total', 'Line_Total']
    ans = []
    tot_list = []
    statement = '=SUMIFS(' + 'B3:' + 'B' + str(end) + ',"<>Total",'
    for i, col in enumerate(df):
        if col in columns:
            sum_range = alpha[i] + '3:' + alpha[i] + str(end)
            #ans.append('=SUMIFS(' + sum_range + ',B3:B' + str(end) + ',"<>Total",' + sum_range + ',">0")')
            ans.append('=SUMIF(B3:B' + str(end) + ',"=Total",' + sum_range + ')')
            tot_list.append(col) 
        else:
            ans.append('')
            tot_list.append('')

    un = [i for i in columns if '# Units' in i][0]
    ans[tot_list.index(un) - 1] = 'Count Totals'
    if brainsheet:
        ans[tot_list.index('M/M_Total') - 1] = 'Price Totals'
    return ans[1:], tot_list[1:]


def get_col_sizes(df):
    """
        Determines and sets the column sizes in excel
        based on most text in a cell
    """

    sol = []
    for c in df:
        val = df[[c]].astype(str).applymap(lambda x: len(x) if '=' not in x else 0).max().max()
        if c in ['Description', 'Page']:
            sol.append(16)
        elif '#' not in c:
            sol.append(max(len(c), val))
        else:
            sol.append(len(c))
    return sol


def fmt_money(df, wb, ws, sheet_name):
    """
        Formats price columns to be
        written as currency
    """

    money_dict = {'num_format': '$0.00', 'align': 'center', 'valign': 'vcenter', 'border': 1}
    money_fmt = wb.add_format(money_dict)
    ind = len(df.columns)
    ws.conditional_format(alpha[ind - 6] + '3' + ':' + alpha[ind - 1] + str(len(df.index) + 2),
                            {'type': 'no_errors', 'format': money_fmt})
    if sheet_name == 'Total':
        row = str(len(df.index) + 6)
        ws.conditional_format(alpha[ind - 4] + row + ':' + alpha[ind -1] + row,
                            {'type': 'no_errors', 'format': money_fmt})


def fix_phase_rows(df):
    phases = [i for i in pd.unique(df.Phase) if pd.notnull(i)]
    if not phases:
        raise ValueError("No phase found in spreadsheet")
    for i, row in df.iterrows():
        if not i:
            prev = row.Phase
        if pd.isnull(row.Phase):
            df.loc[i, 'Phase'] = prev
        else:
            prev = row.Phase
    return df


def concat_old_ids(old, new):
    """
        Fixes older ids when comparing two df's
    """

    ids = [x for x in new.columns if 'ID' in x]

    for i, row in new.iterrows():
        info = pd.DataFrame()
        for c in ids:
            if row[c].find(',') != -1:
                for sp in row[c].split(' , '):
                    info = info.append(old.loc[(old.Phase == row.Phase) & (old[c] == sp)])
                for col in info.columns:
                    if col == 'Page' and len(pd.unique(info[col])) > 1:
                        info.loc[:, col] = 'Varies'
                    if '#' not in col and 'Description' not in col:
                        info.loc[:, col] = ' , '.join([t for t in sorted(pd.unique(info[col])) if t])
                    elif '#' in col:
                        info.loc[:, col] = info.loc[:,col].sum()
                info = info.drop_duplicates()
                info.index = range(len(info))
                if not info.empty:
                    for sp in row[c].split(' , '):
                        old.loc[(old.Phase == row.Phase) & (old[c] == sp)] = info.loc[0].tolist()
    old = old.drop_duplicates()
    return old


def create_co_df(old_df, new_df):
    """
        Wrapped function that creates change order
        dataframe
    """

    old_id = newest_id(old_df)
    new_id = newest_id(new_df)
    old_id, new_id = [j.split()[0] + ' ' for j in [old_id, new_id]]

    if old_id == new_id:
        old_id = 'Prev. '
        new_id = 'New '

    old_df, new_df = [df.rename(columns = {a: id + a for a in ['# Units',
                                                               '# DWGS',
                                                               '# Models',
                                                               '# Molds']}) for df, id in zip([old_df, 
                                                                                               new_df], [old_id, 
                                                                                                         new_id])]

    unit_cols = [old_id + '# Units',  new_id + '# Units',  'CO # Units',
                 old_id + '# DWGS',   new_id + '# DWGS',   'CO # DWGS',
                 old_id + '# Models', new_id + '# Models', 'CO # Models',
                 old_id + '# Molds',  new_id + '# Molds',  'CO # Molds']

    
    # Adds the newer IDs to the old_df
    if old_id != 'Prev. ':
        old_df = concat_old_ids(old_df, new_df)
        old_df[new_id + 'ID'] = ''
        p = 1
        for j in old_df.index:
            phase = old_df.loc[j, 'Phase']
            id = old_df.loc[j, old_id + 'ID']

            # Checks to see if the old ID is located in one of the new_DF's rows
            #   If not, a new row is made
            check = new_df.loc[(new_df.Phase == phase) & ((new_df[old_id + 'ID'] == id) | (new_df[old_id + 'ID'].str.contains(id + ',')) | (new_df[old_id + 'ID'].str.contains(' ' + id)))
                                , new_id + 'ID']
            if not check.empty:
                old_df.loc[j, new_id + 'ID'] = check.values[0]
            else:
                old_df.loc[j, new_id + 'ID'] = ''
            if old_df.loc[j, new_id + 'ID'] == '':
                new_df = new_df.append(old_df.loc[j], ignore_index = True)
                p += 1

    old_units = [col for col in unit_cols if old_id in col]
    for c in old_units:
        new_df[c] = 0


    # Adds old counts to co dataframe
    for k, row in old_df.iterrows():
        for u in old_units:
            if row[newest_id(new_df)] != '':
                new_df.loc[(new_df.Phase == row.Phase) & (new_df[newest_id(new_df)] == row[newest_id(new_df)]), u] += row[u]
            else:
                new_df.loc[(new_df.Phase == row.Phase) & (new_df[old_id + 'ID'].str.contains(row[old_id + 'ID'])), u] += row[u]


    co_df = new_df.copy()


    for col in ['CO # Units', 'CO # DWGS', 'CO # Models', 'CO # Molds']:
        co_df[col] = 0

    co_df = co_df[[k for k in comp_cols + unit_cols if k in co_df.columns]]

    co_df = pd.concat([co_df.loc[co_df.Phase == 'Base Bid'].sort_values(by = newest_id(co_df)),
                       co_df.loc[co_df.Phase != 'Base Bid'].sort_values(by = ['Phase', newest_id(co_df)])],
                       axis = 0, ignore_index = True)

    cols = list(co_df.columns)

    for c in unit_cols:
        if 'CO' not in c:
            co_df[c] = co_df[c].apply(lambda x: 0 if pd.isnull(x) else int(x))
        else:
            plu = 3
            phase = 'Base Bid'
            for i, row in co_df.iterrows():
                if row.Deleted != "Total":
                    if row.Phase != phase:
                        plu += 1
                        phase = row.Phase
                    num = str(i + plu)
                    o = alpha[cols.index(c) -2]
                    n = alpha[cols.index(c) -1]
                    co_df.loc[i, c] = '=IF(AND(' + o + num + '>=0,' + n + num + '>=0), ' + n + num + '-' + o + num + ', 0)'

    return co_df


def fix_deleted(r):
    r.Deleted = "Deleted" if r['# Units'] <= 0 else ""
    return r




##### MAIN FUNCTION #####
def create_spreadsheet(csv_path, save_path, brainsheet, projnum):

    # Read in file
    if csv_path:
        data = read_in(csv_path, projnum)
    else:
        data = pd.DataFrame()

    if data.empty:
        print(0)

    # Make proper changes / calcs
    data = data.applymap(clean_up).apply(clean_row, axis = 1)

    # Adds in default values
    data = data.apply(default_vals, axis = 1)

    # Find project number if available
    project_num = ''
    if 'Project #' in data.columns:
        project_num = data.loc[data['Project #'] != '', 'Project #'].tolist()[0]



    # Defines project name
    project_name = csv_path.split('/')[-1][:-4]

    # Remove unused ID columns
    for c in ['Block ID', 'Survey ID', 'Estimating ID', 'Client ID']:
        if c in data.columns:
            if (data[c] == '').all():
                data.pop(c)
                final_cols.remove(c)
            else:
                break

    # Remove columns not found in final_cols list
    data = data[[col for col in data.columns if col in final_cols]]

    # Group rows and calculate counts
    data = group(data)
    data = make_counts(data)

    # Concatenate Descriptive columns for spreadsheet/brainsheet
    data = make_desc(data)

    if brainsheet:
        data = add_prices(data)

    # Creates writer to save excel file
    writer = pd.ExcelWriter(save_path, engine='xlsxwriter')

    phase_ls = ['Total'] + [i for i in pd.unique(data.Phase)]

    # Use Project # as title if available
    title = project_num if project_num else project_name

    make_excel_sheet(data, writer, phase_ls, title, brainsheet)






def compare_read_in(path):
    df = pd.DataFrame()
    if path:
        if path.endswith('csv'):
            df, proj_name = read_in(create_spreadsheet(compare = True))
            reset_cols()
        else:
            df, proj_name = read_in(path)
    if not df.empty:
        # Adds Phase name to all rows
        df = fix_phase_rows(df)

        # All unit cols contain numbers and not null
        units = [c for c in df.columns if '#' in c]
        for u in units:
            df.loc[pd.isnull(df[u]), u] = 0

        # Remove "Total" rows and fix Deleted column
        df = df[df.Deleted != 'Total']
        df = df.apply(fix_deleted, axis = 1)
        return df.applymap(clean_up), proj_name
    return pd.DataFrame([]), None


def compare_spreadsheet():

    # Checks to see if comparison excel file should be opened after creation
    open_excel = False


    # Read in paths from each text box
    old_path = ""
    new_path = ""

    try:
 
        # If either path is a CSV, excel "counts" spreadsheet is created        
        (old_df, p1), (new_df, p2) = map(self.compare_read_in, [old_path, new_path])

        proj_name = p1 + ' | ' + p2 if p1 != p2 else p1

        # Error check each df
        if old_df.empty and new_df.empty:
            return
        for empty, name in zip([bool(j.empty) for j in [old_df, new_df]], ["Previous", "New"]):
            if empty:
                return



        co_df = create_co_df(old_df, new_df)

        # Path of output file
        save_path = '/'.join([i for i in new_path.split('/') if i != new_path.split('/')[-1]])


        # Defines new_file name
        new_file_name = new_path.split('/')[-1]
        if new_path.endswith('xlsx'):
            new_file_name = ' '.join(new_file_name.split(' --- ')[0].split()[:-2])
        else:
            new_file_name = new_file_name[:-4]

        # Defines type of spreadsheet
        typ = ' Comparison Spreadsheet'

        # Name of output file; uses input name + date
        filename = '/' + new_file_name \
                    + typ + ' --- ' \
                    + dt.datetime.now().strftime("%I%M%p on %B %d %Y")

        # Creates writer to save excel file
        writer = pd.ExcelWriter( save_path + filename + '.xlsx',
                                    engine='xlsxwriter')

        phase_ls = ['Total'] + [i for i in pd.unique(co_df.Phase)]
        make_excel_sheet(co_df, writer, phase_ls, proj_name, brainsheet)

    except:
        exception_log(sys.exc_info())
        return






def log(action, error = ''):
    with open(logpath, 'a') as fid:
        fid.write(dt.datetime.now().strftime("%m/%d/%Y - %H:%M") + '     ')
        fid.write(action + '     ')
        fid.write(getpass.getuser())
        if action == "ERROR      ":
            fid.write(' '*(14 - len(getpass.getuser())) + error)
        fid.write('\n')


def exception_log(exc):
    if exc:
        tb = str([t for t in traceback.extract_tb(exc[-1]) if home in t or fname in t][-1][1])        
        tb = "Line " + tb + ': ' + exc[0].__name__ + ': ' + str(exc[1])
    else:
        tb = 'UNKNOWN'
    log("ERROR      ", tb)










if __name__ == '__main__':
    csv_path   = sys.argv[1]
    save_path  = sys.argv[2]
    brainsheet = int(sys.argv[3])
    projnum    = sys.argv[4]

    create_spreadsheet(csv_path, save_path, brainsheet, projnum)

