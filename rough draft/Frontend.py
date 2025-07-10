import streamlit as st
import requests

st.title("OFFICIAL CPE DICTIONARY ")

title_keyword=st.text_input("title keyword","fly")

url_keyword=st.text_input("url keyword","github")

if title_keyword!="" and url_keyword!="":
    request=f"http://127.0.0.1:5000/search?title={title_keyword}&url={url_keyword}"
elif title_keyword=="":
    request=f"http://127.0.0.1:5000/search?url={url_keyword}"
elif url_keyword=="":
    request=f"http://127.0.0.1:5000/search?url={title_keyword}"
else:
    request=f"http://127.0.0.1:5000/"

final_requrest=st.text_input("API Request",request.strip())
if st.button('Check availability'):
    response = requests.get(final_requrest,verify=False)
    if response.status_code == 200:

        data = response.json()
        st.write("API response (JSON):")
        st.markdown('---')
        for i in range(len(data)):
            x=data[i]
            st.markdown(f"**ID**  \t: {x['id']}")
            st.markdown(f"**Title**  \t:{x['title']}")
            st.markdown(f"**URLs:**")
            st.write(x['urls'])
            st.markdown("---")
            
    else:

        st.write(f"Error: {response.status_code} - {response.text}")