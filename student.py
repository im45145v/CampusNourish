import streamlit as st

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


st.image("campus.png")
st.image("uni.png")

with open("items.txt", "r") as file:
    user_input = file.read()
with open("question.txt", "r") as file:
    ui = file.read()
# Check if there is any text
if user_input:
    # Split the text by comma
    options = user_input.split(',')
    st.write()
    st.header(ui)
    # Display the separated values as options
    selected_option = st.radio("Choose an option", options, key="pie")

    # Display a button to submit the vote
    submit_button = st.button("Submit Vote" , key="phi")

    # Check if vote has already been submitted
    vote_submitted = st.session_state.get("vote_submitted", False)
    # Show the selected option to the user
    if submit_button:
        if not vote_submitted:
            if selected_option:
                #st.success(f"You voted for {selected_option}!")
                #st.radio("Choose an option", options, key="pol", index=options.index(selected_option), disabled=True)

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



def display_notice_board():


    # Display existing notices
    st.title('Notices')
    with open('notices.txt', 'r') as f:
        notices = f.readlines()
        if notices:
            for i, notice in enumerate(notices, start=1):
                st.write(f'{i}. {notice.strip()}')
        else:
            st.write('No notices found.')

# Run the notice board app
display_notice_board()
