import os

import streamlit as st

import pymongo
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.ub5pbd6.mongodb.net/food?retryWrites=true&w=majority")
db = client["Food"]
collections = db['Credentials']
def check_user(usr,pas,log):
    chek= collections.find_one({"username":usr,"password":pas,"role":log})
    if log == "Student":
        os.system("streamlit run student.py")
    elif log == "Admin":
        os.system(("streamlit run admin.py"))


st.markdown("""
<style>
.css-nqowgj.e1ewe7hr3{
visibility:hidden;
}
.css-h5rgaw.e1g8pov61{
visibility:hidden;
}
</style>
""",unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center'>Food selecty</h1>",unsafe_allow_html=True)
with st.form("Login",clear_on_submit=True):
    usr=st.text_input("Username")
    pas=st.text_input("Password",type="password")
    log=st.selectbox("Login as",options=("select","Admin","Student"))
    state=st.form_submit_button("LOGIN")
    if state:
        if usr=="":
            st.warning("Fill the username")
        elif pas=="":
            st.warning("Don't act smart give the password")
        elif log=="select":
            st.warning("Select the login as")
        else:
            check_user(usr,pas,log)

st.markdown("<p style='text-align:center'>New user <a href='http://localhost:8502/'>signup</a></p>",unsafe_allow_html=True)
