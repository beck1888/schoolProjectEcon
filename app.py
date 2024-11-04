# Import libraries
import streamlit as st # Web app framework
import streamlit_lottie as st_lottie # Lottie animation library for Streamlit
import json # JSON library (loading in lottie animation data)
import ai # AI model

# Set up the Streamlit app
st.set_page_config(
    page_title="Prop 32: Change My View",
    page_icon="static_assets/favicon.ico",
)
# st.title("Prop 32: Change My View")

hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>

"""
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Configure session states
if "screen" not in st.session_state:
    st.session_state.screen = -1

# Get user AI policy opt-in
if st.session_state.screen == -1:
    with open("static_assets/terms.md") as f:
        content = ""
        for line in f:
            content += line
        st.markdown(content)

    agree = st.checkbox("I agree", key="accept_policy")
    if agree:
        st.session_state.screen = 0
        st.rerun()
    else:
        st.markdown("*You must agree to the terms and conditions above to continue.*")
        st.stop()


# Home screen
if st.session_state.screen == 0:
    with open("static_assets/prop_32_description.md") as f:
        content = ""
        for line in f:
            content += line
        st.markdown(content)
    next = st.button("Next →", use_container_width=True, type="primary", key="next_button")
    if next:
        st.session_state.screen = 1 # Move to the next screen
        st.rerun() # Rerun the app to display the next screen

# Question screen
if st.session_state.screen == 1:
    with st.form("question_r1_form", border=False):

        st.markdown("*Please fill out the following information so our AI can give you the best possible response. You may skip any question you would prefer not to answer, but it's best to answer all.*")

        st.session_state.name = st.text_input("What's your name?", key="name_input")


        # Collect info about the user (to use against them)
        age = st.number_input("About how old are you?", key="age_input", step=1, value=None)
        occupation = st.text_input("What is your occupation?", key="occupation_input")
        income = st.number_input("What is your approximate annual income?", key="income_input", step=1000, value=None)
        location = st.radio("What part of California do you live in?", key="location_input", options=["Northern California", "Central California", "Southern California"], index=None)
        party = st.radio("What political party do you identify with closest?", key="party_input", options=["Democratic", "Republican"], index=None)

        submit = st.form_submit_button("Next →", use_container_width=True, type="primary")
        if submit:
            if len(str(age)) == 0:
                age = "Not provided"
            if len(occupation) == 0:
                occupation = "Not provided"
            if len(str(income)) == 0:
                income = "Not provided"
            if len(location) == 0:
                location = "Not provided"
            if len(party) == 0:
                party = "Not provided"

            st.session_state.user_profile = "Age: " + str(age) + ", Occupation: " + occupation + ", Income: " + str(income) + ", Location: " + location + ", Party: " + party
            st.session_state.screen = 2
            st.rerun()

# Get support screen
if st.session_state.screen == 2:
    st.markdown("## Do you support Proposition 32?")

    screen1_col1, screen1_col2 = st.columns(2)

    with screen1_col1:
        no = st.button("No", use_container_width=True, key="no_button")

    with screen1_col2:
        yes = st.button("Yes", use_container_width=True, key="yes_button")

    # Button logic
    if no:
        st.session_state.screen = 3
        st.session_state.prop_32_support = False
        st.rerun()

    if yes:
        st.session_state.screen = 3
        st.session_state.prop_32_support = True
        st.rerun()

# Get reason screen
if st.session_state.screen == 3:
    # Display the appropriate question based on the user's support for Prop 32
    support = st.session_state.prop_32_support

    if support:
        st.markdown(f"### Why do you support Proposition 32, {st.session_state.name}?")
        with st.form("support_form", border=False):
            st.session_state.reasons = st.multiselect(
                label="Select all reasons you support Prop 32",
                key = "why_u_support",
                options= [
                    "Improve quality of life",
                    "The cost of living is too high",
                    "Fewer people would rely on government benefits",
                    "Prices only projected to increase by 0.5%"
                ]
            )
            # st.html("<br>")
            # st.html("<br>")
            # st.html("<br>")
            support_reason = st.text_area("Explain why you have selected these reasons", key="support_reason_input", height=400, placeholder="I support Proposition 32 because...")
            submit = st.form_submit_button("Submit", use_container_width=True, type="primary")
            if submit:
                st.session_state.screen = 4
                st.rerun()

    else:
        st.markdown(f"### Why do you not support Proposition 32, {st.session_state.name}?")
        with st.form("no_support_form", border=False):
            st.session_state.reasons = st.multiselect(
                label="Select all the reasons you don't support Prop 32",
                key="why_u_no_support",
                options= [
                    "Increased taxes",
                    "Layoffs",
                    "Will be disproportionally harmful to small businesses",
                    "Consumers will have to pay more as businesses adjust prices to maintain profit margins"
                ]
            )
            # st.html("<br>")
            # st.html("<br>")
            # st.html("<br>")
            no_support_reason = st.text_area("Explain why you chose these reasons", key="no_support_reason_input", height=400, placeholder="I oppose Proposition 32 because...")
            submit = st.form_submit_button("Submit", use_container_width=True, type="primary")
            if submit:
                st.session_state.screen = 4
                st.rerun()

# Generating AI response screen
if st.session_state.screen == 4:
    # Show a message
    st.markdown("## Preparing counter points, hang tight!")

    # Load the Lottie animation
    with open("static_assets/debate.json") as f:
        animation_data = json.load(f)

    # Display the animation
    st_lottie.st_lottie(animation_data, speed=2, key="animation")

    # Generate the AI response
    st.session_state.counter_point = ai.debate_me(
        name=st.session_state.name,
        supports_prop_32=st.session_state.prop_32_support,
        reasons=st.session_state.reasons,
        justification=st.session_state.reasons,
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        user_profile=st.session_state.user_profile
    )

    # Display the AI response
    st.session_state.screen = 5
    st.rerun()

# Display the AI response
if st.session_state.screen == 5:

    st.markdown("## Your friend, Jane Doe, has written you a letter:")


    message = st.session_state.counter_point
    for line in message.split("\n"):
        st.write(line)

    st.divider()

    with open("static_assets/debrief.md") as f:
        content = ""
        for line in f:
            content += line
        st.markdown(content)