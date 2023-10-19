import streamlit as st
import preprocessor as pp
import helper
import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.title('WhatsApp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = pp.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show analysis of', user_list)

    if st.sidebar.button('Show Analysis'):
        num_msgs, words, media_msgs, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total messages')
            st.title(num_msgs)

        with col2:
            st.header('Total words')
            st.title(words)

        with col3:
            st.header('Media shared')
            st.title(media_msgs)
        with col4:
            st.header('Links shared')
            st.title(links)

        if selected_user == 'Overall':
            col1, col2 = st.columns(2)

            with col1:
                st.header('Most Active Users')
                df_new = helper.most_busy_users(df)
                fig = plt.figure(figsize=(10, 10))
                ax = sns.barplot(x=df_new.index[:5], y=df_new['Messages'].head())
                plt.xticks(rotation=90)
                ax.set(xlabel='Most Active Users', ylabel='Messages')
                st.pyplot(fig)

            with col2:
                st.header('Active Percentage')
                st.dataframe(df_new)
