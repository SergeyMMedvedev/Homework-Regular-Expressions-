import re
import pandas as pd


df = pd.read_csv('phonebook_raw.csv')


def update_phone(phone, ind, df):
    phone = str(phone)
    pattern = re.compile('(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?')
    match = pattern.match(phone)
    substitution = r'8(\2)\3-\4-\5'
    if match:
        if match.group(6):
            substitution += r' \6\7'
    df.loc[ind, 'phone'] = pattern.sub(substitution, phone)


def update_lastname(name, ind, data):
    name_data = name.split()

    if len(name_data) == 2:
        lastname, firstname = name_data
        set_new_values(
            ind, data,
            lastname=lastname,
            firstname=firstname
        )

    if len(name_data) == 3:
        lastname, firstname, surname = name_data
        set_new_values(
            ind, data,
            lastname=lastname,
            firstname=firstname,
            surname=surname
        )

def update_firstname(name, ind, data):
    name_data = name.split()
    if len(name_data) == 2:
        firstname, surname = name_data
        set_new_values(
            ind, data,
            firstname=firstname,
            surname=surname
        )

def set_new_values(ind, data, **kwargs):
    for k, v in kwargs.items():
        data.loc[ind, k] = v

def update_column(df, column):
    for ind, val in df[[column]].itertuples():
        {
            'phone': update_phone,
            'lastname': update_lastname,
            'firstname': update_firstname
        }[column](val, ind, df)
    return df

def merge_duplicates(df):
    for row in df.itertuples():
        df_rem = df.loc[row.Index+1:]
        dublicate = (df_rem.loc[(df_rem['lastname'] == row.lastname) 
                     & (df_rem['firstname'] == row.firstname)])
        if not dublicate.empty:
            for row_d in dublicate.itertuples():
                for v1, v2, col in zip(row[1:], row_d[1:], list(df.columns)):
                    df.loc[row.Index, col] = v1 if str(v1) != 'nan' else v2
                df = df.drop(index=[row_d.Index])
    return df


df = (df.pipe(update_column, 'phone')
        .pipe(update_column, 'lastname')
        .pipe(update_column, 'firstname')
        .pipe(merge_duplicates))

print(df)
df.to_csv('phonebook.csv')
