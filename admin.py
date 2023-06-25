import streamlit as st
from pymongo import MongoClient

st.markdown("""
<style>

[data-testid="stAppViewContainer"]  {
background-color: #FAD025;
background-image: url("https://i.ibb.co/z7g7FVk/Untitled-design-10.png");
background-repeat: no-repeat;
background-size: 100% auto;
}

.css-18ni7ap.e13qjvis2{
     visibility:hidden;
}
.css-nqowgj.e1ewe7hr3{
visibility:hidden;
}





</style>
""", unsafe_allow_html=True)


client = MongoClient('mongodb+srv://<username>:<pass>@cluster0.ub5pbd6.mongodb.net/?retryWrites=true&w=majority',serverSelectionTimeoutMS=60000)
db = client["Food"]
collection = db["Recipes"]

st.image("Campus.png")
st.image("uni.png")




question = st.text_input("Enter the poll question:" , key="beta")

ingredients_str = st.text_input("Enter the ingredients available (seperated by commas):", key="gamma")
ingredients = ingredients_str.split(',')


results = collection.find()
iterator = iter(results)
for document in iterator:
    if set(ingredients) <= set(document['ingredients']) :
        st.write(document['dish_name'])

client.close()

# Poll options
options = st.text_input("Enter the poll options (separated by commas):" , key="omega")
if question:
    with open("question.txt", "w") as file:
        file.write(question)
if  options:
    # Save the user's input as a text file
    with open("items.txt", "w") as file:
        file.write(options)
    st.success("question saved successfully!")

#############################################################################

def add_notice(notice):
    with open('notices.txt', 'a') as f:
        f.write(notice + '\n')

def delete_notice(notice):
    # Remove the notice from the persistent data source
    with open('notices.txt', 'r') as f:
        notices = f.readlines()

    with open('notices.txt', 'w') as f:
        for n in notices:
            if n.strip() != notice.strip():
                f.write(n)

def display_notice_board():
    st.title('Add Notice')

    # Add a new notice
    new_notice = st.text_input('Add a new notice:' , key="jdhwkj")
    if st.button('Add' , key="skjbdkj"):
        if new_notice:
            add_notice(new_notice)
            st.success('Notice added successfully!')
        else:
            st.warning('Please enter a notice.')

    # Display existing notices
    st.title('Notices')
    with open('notices.txt', 'r') as f:
        notices = f.readlines()
        if notices:
            for i, notice in enumerate(notices, start=1):
                st.write(f'{i}. {notice.strip()}')
                if st.button(f'Delete Notice {i}'):
                    delete_notice(notice)
                    st.success('Notice deleted successfully!')
        else:
            st.write('No notices found.')

display_notice_board()
