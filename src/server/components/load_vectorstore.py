import os
import time
from pathlib import Path
from tqdm.auto import tqdm
from dotenv import load_dotenv
from logger import logger
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from constants.constants import transcript_path
from components.transcript_extraction import extract_transcript

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")            # Your vector database is named "medical-index"
PINECONE_ENV = "us-east-1"


# UPLOAD_DIR =          # Uploaded PDFs are stored here.
# os.makedirs(UPLOAD_DIR, exist_ok=True)

pc = Pinecone(api_key = PINECONE_API_KEY)      # Creates a client to communicate with Pinecone.
spec = ServerlessSpec(cloud = "aws", region = PINECONE_ENV)    # This tells Pinecone where to deploy your vector database.
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:        # Avoids creating the same index repeatedly.
    pc.create_index(
        name = PINECONE_INDEX_NAME,
        dimension = 768,
        metric = "dotproduct",    # Options include: cosine, dotproduct, euclidean - Google recommends dot product for models/embedding-001, so it's a suitable choice here.
        spec = spec
    )

    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:   # Index creation isn't instantaneous. 
        time.sleep(1)                                                   #This loop waits until Pinecone reports the index is ready before proceeding.       

    logger.info("Pinecone Index is Ready")                                     

# Connect to the index : 
index=pc.Index(PINECONE_INDEX_NAME)   # From now on, all operations use "medical-index"


# load,split,embed and upsert pdf docs content
def load_vectorstore(url : str):
    embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", output_dimensionality=768)   # Creates the embedding model once so it can be reused for all documents.

    # Save uploaded file
    # save_path = Path(UPLOAD_DIR) / uploaded_file.filename
    # with open(save_path, "wb") as f:    # The "wb" mode means write binary, which is appropriate for PDFs.
    #     f.write(uploaded_file.file.read())

    extract_transcript(url)

    # Load PDF
    loader = TextLoader(transcript_path)
    documents = loader.load()      # Reads the PDF and returns a list of Document objects, usually one per page.

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]
    metadatas = []

    for chunk in chunks:
        metadata = chunk.metadata.copy()
        metadata["text"] = chunk.page_content
        metadatas.append(metadata)
    ids = [f"{Path(transcript_path).stem}-{i}" for i in range(len(chunks))]  # for eg. For heart.pdf:
                                                                        #    heart-0
                                                                        #    heart-1
                                                                        #    heart-2
                                                                        # Every vector needs a unique ID within the index.

    # create embeddings...
    print(f"🔍 Embedding {len(texts)} chunks...")
    embeddings = embed_model.embed_documents(texts)

    print("📤 Uploading to Pinecone...")
    with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
        index.upsert(vectors=zip(ids, embeddings, metadatas))      # zip combines the three parallel lists into tuples:
                                                                    # For example:
                                                                    # (
                                                                    #   "heart-0",
                                                                    #   [0.12, 0.44, ...],
                                                                    #   {"page": 1}
                                                                    # ) 
                                                                    # upsert inserts new vectors or updates existing ones with the same IDs.
        progress.update(len(embeddings[0]))

        print(f"✅ Upload complete for {transcript_path}")



# User uploads url
#         │
#         ▼
# extract video_id and eventually transcript
#         │
#         ▼
# Save transcript locally
#         │
#         ▼
# Read Document pages
#         │
#         ▼
# Split into 500-character chunks
#         │
#         ▼
# Generate 768-dimensional embeddings
#         │
#         ▼
# Attach metadata and IDs
#         │
#         ▼
# Upsert vectors into Pinecone index
#         │
#         ▼
# YT Video RAG knowledge base ready for retrieval