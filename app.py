import os
import ollama
import streamlit as st

from dotenv import load_dotenv

from database import (
    create_database,
    save_conversation,
    get_conversations,
    delete_all_conversations
)


# ==========================================
# 1. CONFIGURATION
# ==========================================

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

st.set_page_config(
    page_title="AI Code Companion",
    page_icon="🤖",
    layout="wide"
)

create_database()


# Initialize latest response
if "latest_response" not in st.session_state:
    st.session_state.latest_response = None


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.title {
    font-size: 38px;
    font-weight: bold;
    color: #60A5FA;
}

.subtitle {
    color: #AAB4C3;
    font-size: 16px;
}

.response-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. APPLICATION HEADER
# ==========================================

st.markdown(
    '<div class="title">🤖 AI Code Companion</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent programming assistant powered by Generative AI.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 4. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("⚙️ Settings")

    option = st.selectbox(
        "Select AI Feature",
        [
            "Code Explanation",
            "Code Generation",
            "Code Debugging"
        ]
    )

    st.divider()

    st.write("🤖 AI Model")
    st.info(MODEL_NAME)

    if st.button("🗑️ Clear Chat History"):

        try:
            delete_all_conversations()

            st.session_state.latest_response = None

            st.success("Chat history cleared!")

            st.rerun()

        except Exception as e:

            st.error("Unable to clear chat history.")

            with st.expander("Technical error details"):
                st.code(str(e))

    st.divider()

    st.caption("AI Code Companion | GenAI Project")


# ==========================================
# 5. FEATURE INSTRUCTIONS
# ==========================================

if option == "Code Explanation":

    instruction = """
    Explain the following Python code step by step.
    Use simple English and provide examples.
    """

elif option == "Code Generation":

    instruction = """
    Generate clean and understandable Python code
    for the following requirement.
    Explain how the code works.
    """

else:

    instruction = """
    Debug the following Python code or error.
    Identify the problem and provide corrected code.
    Explain the solution.
    """


# ==========================================
# 6. FILE UPLOAD
# ==========================================

st.subheader("📂 Upload Your Python File")

uploaded_file = st.file_uploader(
    "Upload a Python or text file",
    type=["py", "txt"]
)

file_content = ""

if uploaded_file is not None:

    try:

        file_content = uploaded_file.getvalue().decode("utf-8")

        st.success(f"Uploaded: {uploaded_file.name}")

        with st.expander("View Uploaded File"):
            st.code(file_content)

    except UnicodeDecodeError:

        st.error("Unable to read this file. Please upload a UTF-8 text file.")


# ==========================================
# 7. PROMPT INPUT
# ==========================================

st.subheader(f"💻 {option}")

with st.form("prompt_form"):

    prompt = st.text_area(
        "Enter your prompt",
        height=140,
        placeholder="Ask something about Python programming..."
    )

    submitted = st.form_submit_button(
        "🚀 Generate Answer"
    )


# ==========================================
# 8. GENERATE AI RESPONSE
# ==========================================

if submitted:

    if not prompt.strip() and not file_content.strip():

        st.warning("Please enter a prompt or upload a valid file.")

    else:

        combined_input = instruction + "\n\n"

        if file_content:

            combined_input += (
                "Uploaded file content:\n"
                + file_content
                + "\n\n"
            )

        if prompt.strip():

            combined_input += "User request:\n" + prompt

        with st.spinner("🤖 AI is thinking..."):

            try:

                response = ollama.chat(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "user",
                            "content": combined_input
                        }
                    ]
                )

                answer = response["message"]["content"]

                question = prompt.strip()

                if not question and uploaded_file is not None:

                    question = f"Uploaded file: {uploaded_file.name}"

                # Save response in SQLite
                save_conversation(
                    option,
                    question,
                    answer
                )

                # Store latest response for immediate display
                st.session_state.latest_response = {
                    "feature": option,
                    "question": question,
                    "answer": answer
                }

                st.success("Conversation saved successfully!")

            except Exception as e:

                error_message = str(e).lower()

                if (
                    "connection" in error_message
                    or "refused" in error_message
                    or "connect" in error_message
                ):

                    st.error(
                        "Ollama is not running. Please start Ollama and try again."
                    )

                elif (
                    "not found" in error_message
                    or "404" in error_message
                ):

                    st.error(
                        f"Model '{MODEL_NAME}' was not found. "
                        "Please check your installed Ollama models."
                    )

                elif "timeout" in error_message:

                    st.error(
                        "The AI request timed out. Please try again."
                    )

                else:

                    st.error(
                        "Something went wrong while generating the AI response."
                    )

                    with st.expander("Technical error details"):
                        st.code(str(e))


# ==========================================
# 9. DISPLAY LATEST AI RESPONSE
# ==========================================

if st.session_state.latest_response is not None:

    latest = st.session_state.latest_response

    st.divider()

    st.subheader("🤖 AI Generated Answer")

    st.caption(f"Feature: {latest['feature']}")

    st.markdown("**Your Question:**")
    st.write(latest["question"])

    st.markdown("**AI Response:**")

    st.markdown(latest["answer"])

    st.download_button(
        label="📥 Download This Answer",
        data=latest["answer"],
        file_name="AI_Code_Companion_Response.md",
        mime="text/markdown",
        key="download_latest_answer"
    )


# ==========================================
# 10. CONVERSATION HISTORY
# ==========================================

st.divider()

st.subheader("💬 Conversation History")

try:

    conversations = get_conversations()

except Exception as e:

    conversations = []

    st.error("Unable to retrieve chat history.")

    with st.expander("Technical error details"):
        st.code(str(e))


if conversations:

    # Download complete history

    conversation_text = "# AI Code Companion - Chat History\n\n"

    for index, chat in enumerate(reversed(conversations), start=1):

        conversation_text += f"## Conversation {index}\n\n"
        conversation_text += f"**Feature:** {chat[1]}\n\n"
        conversation_text += f"**Question:**\n\n{chat[2]}\n\n"
        conversation_text += f"**AI Response:**\n\n{chat[3]}\n\n"
        conversation_text += "---\n\n"

    st.download_button(
        label="📥 Download Complete Chat History",
        data=conversation_text,
        file_name="AI_Code_Companion_History.md",
        mime="text/markdown"
    )

    st.divider()

    # Display previous conversations

    for chat in conversations:

        conversation_id = chat[0]
        feature = chat[1]
        question = chat[2]
        answer = chat[3]
        created_at = chat[4]

        with st.expander(f"{feature} | {created_at}"):

            st.markdown("**Your Question:**")
            st.write(question)

            st.markdown("**AI Response:**")
            st.markdown(answer)

            st.download_button(
                label="📥 Download AI Response",
                data=answer,
                file_name=f"ai_response_{conversation_id}.md",
                mime="text/markdown",
                key=f"download_{conversation_id}"
            )

else:

    st.info("No conversations found. Start chatting with your AI assistant!")


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption(
    "Powered by Python | Streamlit | Ollama | Qwen 2.5 | SQLite"
)