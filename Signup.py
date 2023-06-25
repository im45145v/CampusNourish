import streamlit as st
import pymongo
import os

client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.ub5pbd6.mongodb.net/food?retryWrites=true&w=majority")
db = client["Food"]
collections = db['Credentials']
def create_user(usr,pas,fulname):
    db["Credentials"].insert_one({"username":usr,"pasword":pas,"role":"student","full_name":fulname})
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
with st.form("signup",clear_on_submit=True):
    usr=st.text_input("Username")
    fulname=st.text_input("Full name")
    pas=st.text_input("Password",type="password")
    cpas=st.text_input("Confirm Password",type="password")
    state=st.form_submit_button("SIGNUP")
    if state:
        if usr=="" or fulname=="" or pas=="" or cpas=="":
            st.warning("Fill the above details")
        elif pas!=cpas:
            st.warning("Don't try to cheat give the password and confirm password same")
        else:
            create_user(usr,pas,fulname)
            st.success("User Created")
            os.system("streamlit run login.py")

