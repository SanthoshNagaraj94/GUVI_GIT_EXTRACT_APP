try:
    import requests
    from bs4 import BeautifulSoup
except Exception as e:
    print("Somethonh Missing {}".format(e))
import pandas as pd
import streamlit as st
import time
import numpy as np
import re
from PIL import Image

st.set_page_config(
     page_title="GUVI_GIT_EXTRACT_APP",
     page_icon="🧊"

 )

img=Image.open('images/guvi.png')
st.image(img,width=600)
st.title("GUVI GIT-REPO EXTRACTION APP")
data_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

new=[]
if data_file is not None:
    df = pd.read_csv(data_file)
    new.append(df)
    st.title("INPUT FILE TABLE")
    st.dataframe(df)



def scrapy(x):

    url = x

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    li = soup.findAll('div', class_='d-inline-block mb-1')

    li2 = soup.findAll('a', class_='UnderlineNav-item js-responsive-underlinenav-item selected')

    for i in li2:
        x = i.find_all('span', class_='Counter')
    details = {'link': [], 'count': [], 'title': []}
    for i in x:
        y = i.text.strip()
        details['count'].append(int(y))

    base_url = "https://github.com/"
    for _, i in enumerate(li):
        for a in i.findAll('a'):
            newUrl = base_url + a["href"]
        details['title'].append(i.text.strip().replace('\nPublic', ''))
        details['link'].append(newUrl)

    return details
new2=[]
if new!=[]:
    convert=st.button(label="Extract GIT-HUB")
    if convert==True:
        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)

        with st.spinner('Running...'):



            data = new[0]  # use your csv file

            detail = []

            for i in data.link:

                x = i + '?tab=repositories'
                detail.append(scrapy(x))
            lk = []
            ct = []
            top = []

            for i in range(len(detail)):

                l = detail[i]['link']
                if l == []:
                    lk.append("EMPTY")
                else:
                    lk.append(l)

                c = detail[i]['count'][0]
                if c == 0:
                    ct.append(0)
                else:
                    ct.append(c)

                t = detail[i]['title']
                if t == []:
                    top.append("EMPTY")
                else:
                    top.append(t)

            Forked = []

            c = 0
            for i in top:
                for j in i:
                    if "Forked from" in j:
                        c = c + 1
                    else:
                        c = 0
                Forked.append(c)



            extracted={ "Name":data['name'],
                        "Link":data['link'],
                        "Total_Repo_count" : ct,
                        "Forked" : Forked,
                        "Actual_Repo_count" : np.array(ct) - np.array(Forked),
                        "Repo_titles" : top,
                        "Repo_link" : lk}
            out_data=pd.DataFrame.from_dict(extracted)
            out_data=out_data.astype(str)
            st.title("EXTRACTED FILE DETAILS")
            st.dataframe(out_data)

            new2.append(out_data)
        st.balloons()
        st.success('Done!')



if new2 !=[]:
    df = new2[0]
    @st.cache
    def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
         label="Download data as CSV",
         data=csv,
         file_name='Git_Validation.csv',
         mime='text/csv',
     )