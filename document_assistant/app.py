# =============================================
# PROJECT 3: Intelligent Document Assistant
# Author: Ashim
# =============================================

from dotenv import load_dotenv
import os
import streamlit as st

#loading the api_key
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

if api_key:
    print("API key loaded successfully")
else:
    print("API key not found")

from groq import Groq

client = Groq(api_key=api_key)

response= client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "say hello in one sentence"}]
)

print("Groq Response:", response.choices[0].message.content)


#extracting text from pdf
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    reader=PdfReader(pdf_path)
    text=""
    for page in reader.pages:
        text+=page.extract_text()
    return text

text=extract_text_from_pdf('computer.pdf')
print(f"there are {len(text)} characters")
print("\n first 500 characters")
print(text[:500])

#converting text to relevant chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_into_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,chunk_overlap=200,length_function=len
    )
    chunks=text_splitter.split_text(text)
    return chunks

chunks=split_text_into_chunks(text)
print("the number of chunks is",len(chunks))
print("\nFirst Chunk")
print(chunks[0])
print("\nSecond Chunk")
print(chunks[1])

#converting chunks to embeddings and adding them to vector database
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def create_vector_store(chunks):
    embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
    embeddings=embedding_model.encode(chunks)
    dimension=embeddings.shape[1]
    index=faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index,embedding_model

index,embedding_model=create_vector_store(chunks)
print("Vector store created! ✅")
print("Total vectors stored:", index.ntotal)

def search_and_answer(question,index,embedding_model,chunks,client):
    question_embedding=embedding_model.encode([question])
    distances,indices=index.search(np.array(question_embedding),k=3)
    relevant_chunks=[chunks[i] for i in indices[0]]
    context="\n\n".join(relevant_chunks)

    prompt=f"""Use the following context to answer the question

    Context:{context}

    Question:{question}


    Answer based only on the context provided."""


    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
)

    return response.choices[0].message.content

question="what is computer"
answer=search_and_answer(question,index,embedding_model,chunks,client)
print("Question:", question)
print("\nAnswer:", answer)

#UI using streamlit

st.title("📄 Intelligent Document Assistant")
st.subheader("Upload a PDF and ask questions about it!")

# File uploader
pdf_file = st.file_uploader("Upload your PDF", type="pdf")

if pdf_file is not None:
    with st.spinner("Processing your PDF..."):
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        
        # Split into chunks
        chunks = split_text_into_chunks(text)
        
        # Create vector store
        index, embedding_model = create_vector_store(chunks)
    
    st.success(f"✅ PDF processed! {len(chunks)} chunks created.")
    
    # Question input
    question = st.text_input("Ask a question about your document:")
    
    if question:
        with st.spinner("Finding answer..."):
            answer = search_and_answer(
                question, index, embedding_model, chunks,client
            )
        
        st.subheader("Answer:")
        st.write(answer)
    
# After st.title() add:
    st.markdown("---")  # adds a divider line

# Show PDF stats after upload
    st.info(f"📊 Document Stats: {len(text)} characters, {len(chunks)} chunks")

# Show sources with answer
    st.subheader("Answer:")
    st.write(answer)
    st.markdown("---")
    st.caption("⚡ Powered by Groq LLaMA 3.1 & FAISS")
