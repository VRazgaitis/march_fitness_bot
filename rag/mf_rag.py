# https://medium.com/@kv742000/creating-a-python-server-for-document-q-a-using-langchain-31a123b67935
from flask import Flask, request, jsonify
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain.output_parsers import RegexParser
from dotenv import load_dotenv

import streamlit as st 
import pandas as pd
import numpy as np
import pprint

import json
from pathlib import Path
from pprint import pprint

os.environ['PATH'] = '/path/to/dir/'
load_dotenv()

app = Flask(__name__)

# Load docs describing March Fitness
loader = DirectoryLoader(f'./rag/mf_rules', glob="./*.docx", loader_cls=Docx2txtLoader)
documents = loader.load()
chunk_size_value = 1000
chunk_overlap=100
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size_value, chunk_overlap=chunk_overlap,length_function=len)
texts = text_splitter.split_documents(documents)
docembeddings = FAISS.from_documents(texts, OpenAIEmbeddings())
docembeddings.save_local("llm_faiss_index")
docembeddings = FAISS.load_local("llm_faiss_index",OpenAIEmbeddings())

prompt_template = """

# CONTEXT # 
You are an assistant, helping competitors in an annual fitness competition called March Fitness to better understand rules and scoring 
#########

# OBJECTIVE #
Your task is to clarify rules and scoring, based off of later provided documents. If the answer to a question is not contained in the documents, simply say: 'I have not been trained on this information'

#########

# STYLE #
Write in an informative and instructional style, that is also cheerful and humorous. For some responses, you can add phrases supporting the competitor to go exercise. 

#########

# Tone #
Maintain a positive and motivational tone throughout, fostering a sense of empowerment and encouragement. It should feel like a friendly guide offering valuable insights.

# AUDIENCE #
The target audience is competitors in March Fitness, who are looking for clarification on rules.

#########

# RESPONSE FORMAT #

Use the following pieces of context, that explain the rules to a fitness competition, to answer questions pertaining to rules and scoring. If you don't know the answer, just say that you don't know, don't try to make up an answer.

This should be in the following format:

Question: [question here]
Helpful Answer: [answer here]
Score: [score between 0 and 100]

Begin!

Context:
---------
{context}
---------
Question: {question}
Helpful Answer:"""
output_parser = RegexParser(
    regex=r"(.*?)\nScore: (.*)",
    output_keys=["answer", "score"],
)
PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"],
    output_parser=output_parser
)

chain = load_qa_chain(OpenAI(temperature=0), chain_type="map_rerank", return_intermediate_steps=True, prompt=PROMPT)

@st.cache_data
def getanswer(query):
    relevant_chunks = docembeddings.similarity_search_with_score(query,k=2)
    chunk_docs=[]
    for chunk in relevant_chunks:
        chunk_docs.append(chunk[0])
    results = chain({"input_documents": chunk_docs, "question": query})
    output={"Answer":results["output_text"]}
    return results["output_text"]

# Streamlit app
if __name__ == "__main__":
    st.title("March fitness rules chatbot")
    question = st.text_input("Enter a question about rules or scoring in March fitness:")
    st.write("🦾MF admin commitee🦾:  ", getanswer(question))