import os
from pinecone import Pinecone
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import streamlit as st
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
    
class Chatbot:
    def __init__(self):
        print("New sales assistant chatbot object created")
        os.environ["GROQ_API_KEY"] = "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"
        os.environ["PINECONE_API_KEY"] = "b42579ff-88c9-460f-bcac-2b5c32d2a4a6"

        conversational_memory_length = 40
        self.memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)
        self.system_prompt = '''You are an AI-powered sales assistant. Your role is to help sales professionals by providing insights, 
        recommending products, qualifying leads, and offering sales strategies. Use the provided context to give accurate and relevant information.
        Be concise, professional, and focus on driving sales performance.'''
        self.embedding_model = load_embedding_model()
        self.context = None

        llm_model = 'llama-3.1-70b-versatile'
        self.groq_chat = ChatGroq(groq_api_key=os.environ['GROQ_API_KEY'], model_name=llm_model)
        
        self.pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        self.index_name = 'customer-service'
        self.index = self.pc.Index(self.index_name)

    def run_chatbot(self, user_input):
        context = self.retrieve_context(user_input)
        chatbot_response = self.generate_response(user_input, context)
        return chatbot_response

    def retrieve_context(self, query):
        query_vector = self.embedding_model.encode(query).tolist()
        response = self.index.query(vector=query_vector, top_k=5, include_metadata=True)
        context = [item['metadata']['text'] for item in response['matches']]
        return context

    def generate_response(self, user_input, context):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessage(content=f"Use this context to inform your response: {context}"),
            HumanMessagePromptTemplate.from_template("User query: {human_input}"),
        ])

        conversation = LLMChain(
            llm=self.groq_chat,
            prompt=prompt,
            verbose=False,
            memory=self.memory,
        )
        response = conversation.predict(human_input=user_input)
        return response

    def process_and_upload_data(self, dataframe):
        try:
            logging.info(f"Processing dataframe with shape: {dataframe.shape}")
            text_chunks = self.create_text_chunks(dataframe)
            logging.info(f"Created {len(text_chunks)} text chunks")
            self.upload_to_pinecone(text_chunks)
            logging.info("Data upload to Pinecone completed")
            return True
        except Exception as e:
            logging.error(f"Error in process_and_upload_data: {str(e)}")
            return False

    def create_text_chunks(self, dataframe):
        text_chunks = []
        try:
            for _, row in dataframe.iterrows():
                chunk = f"Invoice ID: {row['Invoice ID']}, Branch: {row['Branch']}, City: {row['City']}, " \
                        f"Customer type: {row['Customer type']}, Gender: {row['Gender']}, " \
                        f"Product line: {row['Product line']}, Unit price: {row['Unit price']}, " \
                        f"Quantity: {row['Quantity']}, Tax 5%: {row['Tax 5%']}, Total: {row['Total']}, " \
                        f"Date: {row['Date']}, Time: {row['Time']}, Payment: {row['Payment']}, " \
                        f"COGS: {row['cogs']}, Gross margin percentage: {row['gross margin percentage']}, " \
                        f"Gross income: {row['gross income']}, Rating: {row['Rating']}"
                text_chunks.append(chunk)
            logging.info(f"Successfully created {len(text_chunks)} text chunks")
        except KeyError as e:
            logging.error(f"KeyError in create_text_chunks: {str(e)}. Check if all expected columns are present.")
        except Exception as e:
            logging.error(f"Error in create_text_chunks: {str(e)}")
        return text_chunks

    def upload_to_pinecone(self, text_chunks):
        try:
            vectors = []
            for i, chunk in enumerate(text_chunks):
                vector = self.embedding_model.encode(chunk).tolist()
                vectors.append((f"chunk_{i}", vector, {"text": chunk}))
            
            logging.info(f"Uploading {len(vectors)} vectors to Pinecone")
            self.index.upsert(vectors=vectors)
            logging.info("Upload to Pinecone completed successfully")
        except Exception as e:
            logging.error(f"Error in upload_to_pinecone: {str(e)}")

    def update_knowledge_base(self, new_information):
        vector = self.embedding_model.encode(new_information).tolist()
        self.index.upsert(vectors=[(f"update_{len(vector)}", vector, {"text": new_information})])