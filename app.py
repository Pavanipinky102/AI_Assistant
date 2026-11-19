import streamlit as st

# Page configuration
st.set_page_config(
    page_title="LLM",
    layout="centered"
)

# Application title
st.title("AI Interview")
st.caption("Practice and Prepare for your placement")
st.caption("launched by pavani")

# Import Groq safely
try:
    from groq import Groq
except ImportError:
    st.error("Groq package is not installed.")
    st.info("Add groq to your requirements.txt file and redeploy.")
    st.stop()

# API configuration
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
    st.error("API key is missing. Add it in Streamlit Secrets.")
    st.stop()

# Success message
st.success("Groq API connected successfully!")

st.write("Welcome to your AI Interview Assistant.")

role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineering",
        "data analysis",
        "cyber security",
        "software develovper",
        "Others",
    ],
)

if role == "Others":
    role = st.text_input("Enter your Job Title", "XXXXXX")

model = st.selectbox(
    "choose your model",
    [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ],
)

level = st.selectbox(
    "choose your level",
    ["begginer", "intermideate", "advanced"],
)

mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve answers",
    ],
)

if mode == "Generate Questions":
    count = st.slider("Number Of Questions", 1, 10, 5)

elif mode == "Generate Code Questions":
    topic = st.selectbox(
        "Select Topic",
        ["Python", "C++", "C", "DSA", "Aptitude", "Java"],
    )
    count = st.slider("Number of Questions", 1, 10, 5)

else:
    question = st.text_area("Enter Interview Question Here")
    answer = st.text_area("Enter Your Answer", height=160)

if st.button("Generate AI Response", type="primary"):
    background = (
        f"Job title: {role}\n"
        f"Experience level: {level}\n"
    )

    if mode == "Generate Questions":
        task = (
            f"Generate {count} frequently asked interview questions for this job. "
            "Include both situation-based and theory questions."
        )

    elif mode == "Generate Code Questions":
        task = (
            f"Generate {count} frequently asked coding or technical interview "
            f"questions about {topic}. Include hints and accurate explanations."
        )

    elif mode == "Evaluate Answers":
        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid question and answer.")
            st.stop()

        task = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Evaluate the answer based on the question and identify its drawbacks."
        )

    else:  # Improve answers
        if not question.strip() or not answer.strip():
            st.warning("Please enter a valid question and answer.")
            st.stop()

        task = (
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            "Improve the answer and highlight the important points."
        )

    try:
        req = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Act as an expert technical interviewer and HR interviewer."
                    ),
                },
                {
                    "role": "user",
                    "content": background + task,
                },
            ],
            temperature=0.7,
            max_tokens=1800,
        )

        output = req.choices[0].message.content

        st.subheader("AI Response")
        st.markdown(output)

        st.download_button(
            label="Download Response",
            data=output,
            file_name="Interview_Response.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"API connection was unsuccessful: {e}")
        st.info("Please check your API key and rate limits.")

st.caption("Powered by Streamlit and the Groq API.")
