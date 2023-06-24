import streamlit as st

st.title("to make a poll by admin")
# Poll question
question = st.text_input("Enter the poll question:" , key="beta")

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
st.title("to make a notice board for students by admin")
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
    st.title('Notice Board')

    # Add a new notice
    new_notice = st.text_input('Add a new notice:' , key="jdhwkj")
    if st.button('Add' , key="skjbdkj"):
        if new_notice:
            add_notice(new_notice)
            st.success('Notice added successfully!')
        else:
            st.warning('Please enter a notice.')

    # Display existing notices
    st.title('All Notices')
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
