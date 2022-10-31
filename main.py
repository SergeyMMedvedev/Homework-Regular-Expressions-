import re
import pandas as pd


df = pd.read_csv('phonebook_raw.csv', usecols=list(range(7)))
duplicates = {}


def update_phone(phone):
    phone = str(phone)
    pattern = re.compile(
        '(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?')
    match = pattern.match(phone)
    substitution = r'+7(\2)\3-\4-\5'
    if match:
        if match.group(6):
            substitution += r' \6\7'
    return pattern.sub(substitution, phone)


def get_full_name_list(*args):
    full_name = []
    for arg in args:
        full_name += str(arg).split()
    return full_name[:3]


def merge_rows(df, ind1, ind2):
    row = df.loc[ind1].values
    dupl_row = df.loc[ind2].values
    res = []
    for v1, v2 in zip(list(row), list(dupl_row)):
        res.append(v1 if str(v1) != 'nan' else v2)
    df.loc[ind1] = res
    df.drop(index=[ind2], inplace=True)


def update_columns(df):
    for row in df.itertuples():
        lastname, firstname, surname = get_full_name_list(
            row.lastname, row.firstname, row.surname)
        df.loc[row.Index, 'lastname'] = lastname
        df.loc[row.Index, 'firstname'] = firstname
        df.loc[row.Index, 'surname'] = surname
        df.loc[row.Index, 'phone'] = update_phone(row.phone)
        duplicate_ind = duplicates.get((lastname, firstname))
        if duplicate_ind:
            merge_rows(df, duplicate_ind, row.Index)
        else:
            duplicates[(lastname, firstname)] = row.Index
    return df


df = (df.pipe(update_columns))

print(df)
df.to_csv('phonebook.csv')
