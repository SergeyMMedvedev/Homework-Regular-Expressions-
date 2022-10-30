import re
import pandas as pd


df = pd.read_csv('phonebook_raw.csv')


def update_phone(phone, ind, df):
    phone = str(phone)
    pattern = re.compile(
        '(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?')
    match = pattern.match(phone)
    substitution = r'8(\2)\3-\4-\5'
    if match:
        if match.group(6):
            substitution += r' \6\7'
    df.loc[ind, 'phone'] = pattern.sub(substitution, phone)


def set_new_values(ind, data, **kwargs):
    for k, v in kwargs.items():
        data.loc[ind, k] = v


def update_name_fields(cols, name_data, ind, data):
    kw = {cols[i]: name_data[i]
          for i in range(len(list(zip(name_data, cols))))}
    if len(kw) > 1:
        set_new_values(ind, data, **kw)


def update_lastname(name, ind, data):
    cols = ['lastname', 'firstname', 'surname']
    update_name_fields(cols, name.split(), ind, data)


def update_firstname(name, ind, data):
    cols = ['firstname', 'surname']
    update_name_fields(cols, name.split(), ind, data)


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
