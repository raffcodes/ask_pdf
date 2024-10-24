import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# user credentials for the login
credentials = os.getenv("ASK_PDF_CREDENTIALS")
username, password = credentials.split(':')

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.write(response["answer"])


def show_login_page():
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        if username_input == username and password_input == password:
            st.session_state["logged_in"] = True
            st.success("Login successful!")
            #st.experimental_rerun()  # Rerun the script after successful login
        else:
            st.error("Invalid username or password")


def main_app():
    st.header("Ask your PDF \U0001F4DA")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDF's here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # Get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # Create vector store
                vectorstore = get_vectorstore(text_chunks)
                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


def main():
    st.set_page_config(page_title="Ask your PDF")

    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Initialize session state for conversation chain
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    # Show login page if the user is not logged in
    if not st.session_state["logged_in"]:
        show_login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()
