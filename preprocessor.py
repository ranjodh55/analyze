import re
import pandas as pd


def preprocess(chat):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s[aApP]M - '
    messages = re.split(pattern, chat)[1:]
    if not messages:
        pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s[ap]m - '
        messages = re.split(pattern, chat)[1:]
    dates = re.findall(pattern, chat)
    for i in range(0, len(dates)):
        dates[i] = dates[i].replace(u'\u202f', ' ')

    df = pd.DataFrame({'message': messages, 'date': dates})
    try:

        df['AM/PM'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p - ').dt.strftime('%p')
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M %p - ')
    except ValueError:
        df['AM/PM'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p - ').dt.strftime('%p')
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M %p - ')

    df['message'] = df['message'].replace('\n', '', regex=True)
    users = []
    messages = []

    for message in df['message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df.drop(columns=['message'], inplace=True)
    df['user'] = users
    df['message'] = messages
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['year'] = df['date'].dt.year

    return df
