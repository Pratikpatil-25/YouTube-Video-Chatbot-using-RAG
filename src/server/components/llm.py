from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_llm_chain(retriever):

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", """
                                You are YouTubeGPT, an AI-powered assistant designed to answer questions about a YouTube video.

                                Answer ONLY using the provided transcript context.

                                Rules:
                                - Be clear, accurate, and concise.
                                - Base every answer strictly on the provided transcript.
                                - Use simple and easy-to-understand language whenever possible.
                                - If the transcript does not contain enough information to answer the question, say:
                                "I'm sorry, but I couldn't find relevant information in the provided video transcript."
                                - Never make up facts or assume information that is not present in the transcript.
                                - If appropriate, summarize the relevant parts of the transcript before answering.
                                - If the user asks about something unrelated to the provided transcript, politely explain that you can only answer questions based on the uploaded video's transcript.

                                Transcript Context:
                                {context}
                            """
            ),
            (
                "human", "{input}"
            )
        ]
    )

    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain