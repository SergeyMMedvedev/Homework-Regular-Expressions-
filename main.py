import re
import pandas as pd


df = pd.read_csv('phonebook_raw.csv')


def update_phone(phone):
    phone = str(phone)
    pattern = re.compile(
        '(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?')
    match = pattern.match(phone)
    substitution = r'8(\2)\3-\4-\5'
    if match:
        if match.group(6):
            substitution += r' \6\7'
    return pattern.sub(substitution, phone)


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


def get_full_name_list(*args):
    full_name = []
    for arg in args:
        full_name += str(arg).split()
    return full_name[:3]


def update_columns(df):
    for row in df.itertuples():
        lastname, firstname, surname = get_full_name_list(
            row.lastname, row.firstname, row.surname)
        df.loc[row.Index, 'lastname'] = lastname
        df.loc[row.Index, 'firstname'] = firstname
        df.loc[row.Index, 'surname'] = surname
        df.loc[row.Index, 'phone'] = update_phone(row.phone)
    return df


df = (df.pipe(update_columns)
        .pipe(merge_duplicates))

print(df)
df.to_csv('phonebook.csv')
