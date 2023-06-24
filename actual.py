import streamlit as st

st.title("to display poll to the students")
question = "What do you want to eat today?"

# Poll options
options = ["Pizza", "Curry-rice", "Pasta", "Fish n chips", "burger"]

# Display the poll question
st.header(question)
# Display the radio buttons for options
show_options = True
if st.button("Submit Vote"):
    show_options = False
    st.success("submitted succesfully")

if show_options:
    selected_option = st.radio("Choose an option", options)

st.markdown("---")


########################################################################

st.title("to make a poll by admin")
# Poll question
question = st.text_input("Enter the poll question:" , key="beta")

# Poll options
options = st.text_input("Enter the poll options (separated by commas):" , key="omega")
options = [option.strip() for option in options.split(",")]

# Display the poll question
if question:
    st.header(question)

    # Display the radio buttons for options
    selected_option = st.radio("Choose an option", options, key="pie")

    # Display a button to submit the vote
    submit_button = st.button("Submit Vote" , key="phi")

    # Check if vote has already been submitted
    vote_submitted = st.session_state.get("vote_submitted", False)

    # Handle vote submission
    if submit_button:
        if not vote_submitted:
            if selected_option:
                st.success(f"You voted for {selected_option}!")
                st.radio("Choose an option", options, key="pol", index=options.index(selected_option), disabled=True)

                # Store the vote
                votes = st.session_state.get("votes", {})
                votes[selected_option] = votes.get(selected_option, 0) + 1
                st.write("Current Votes:")
                for option, count in votes.items():
                    st.write(f"{option}: {count}")
                st.session_state["votes"] = votes

                # Mark vote as submitted
                st.session_state["vote_submitted"] = True
            else:
                st.warning("Please select an option.")
        else:
            st.warning("Vote already submitted.")

#######################################################################

st.title("to make a notice board for students by admin")
def add_notice(notice):
    # Append the notice to a persistent data source
    with open('notices.txt', 'a') as f:
        f.write(notice + '\n')

# Function to delete a notice from the board
def delete_notice(notice):
    # Remove the notice from the persistent data source
    with open('notices.txt', 'r') as f:
        notices = f.readlines()

    with open('notices.txt', 'w') as f:
        for n in notices:
            if n.strip() != notice.strip():
                f.write(n)

# Function to display all the notices
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

# Run the notice board app
display_notice_board()

st.markdown("---")
####################################################################################

st.title("to see all notices made by admin ")
def display_notice_board():
    st.title('Notice Board')

    # Display existing notices
    st.title('All Notices')
    with open('notices.txt', 'r') as f:
        notices = f.readlines()
        if notices:
            for i, notice in enumerate(notices, start=1):
                st.write(f'{i}. {notice.strip()}')
        else:
            st.write('No notices found.')

# Run the notice board app
display_notice_board()

#####################################################################
st.markdown("---")


########################################################################################################



