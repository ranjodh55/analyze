from urlextract import URLExtract
import pandas as pd


def fetch_stats(selected_user, df):
    extractor = URLExtract()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_msgs = df.shape[0]
    words = []
    links = []
    media_msgs = df[df['message'] == '<Media omitted>'].shape[0]
    for message in df['message']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))

    print(links)

    return num_msgs, len(words), media_msgs, len(links)


def most_busy_users(df):
    df_new = pd.DataFrame({'Messages': df['user'].value_counts(),  # counts the messages
                           # counts the percentage
                           'Activity Percentage': round(df['user'].value_counts() / df['user'].shape[0] * 100, 2)})
    return df_new
