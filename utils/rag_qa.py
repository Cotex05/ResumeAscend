"""
RAG (Retrieval Augmented Generation) Q&A module for resume queries
Uses LangChain and FAISS for efficient document retrieval and Groq for generation
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from typing import Optional, Dict
import streamlit as st


class ResumeRAG:
    """Resume RAG Q&A system using LangChain"""
    
    def __init__(self, api_key: str):
        """
        Initialize RAG system
        
        Args:
            api_key (str): Groq API key for LLM
        """
        self.api_key = api_key
        self.vectorstore = None
        self.qa_chain = None
        self.resume_text = None
        self.retriever = None
    
    def setup_rag_pipeline(self, resume_text: str) -> bool:
        """
        Setup RAG pipeline with resume text
        
        Args:
            resume_text (str): Full resume text content
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not resume_text or len(resume_text.strip()) < 50:
                return False
            
            self.resume_text = resume_text
            
            # Step 1: Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = text_splitter.split_text(resume_text)
            
            if not chunks:
                return False
            
            # Step 2: Create embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                encode_kwargs={"normalize_embeddings": True}
            )
            
            # Step 3: Create vector store
            self.vectorstore = FAISS.from_texts(
                texts=chunks,
                embedding=embeddings
            )
            
            # Step 4: Initialize LLM
            llm = ChatGroq(
                temperature=0.2,
                model_name="llama-3.1-8b-instant",
                groq_api_key=self.api_key,
                max_tokens=500
            )
            
            # Step 5: Create retriever
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            
            # Step 6: Create RAG chain using LCEL (LangChain Expression Language)
            template = """You are an expert resume analyst. Answer questions about the provided resume accurately and concisely.

Resume Context:
{context}

Question: {question}

Instructions:
1. Base your answer only on the information in the resume
2. If information is not in the resume, clearly state "This information is not available in the resume"
3. Be specific and cite relevant sections when possible
4. For technical details (CGPA, dates, etc.), provide exact values if available
5. Keep answers concise (2-3 sentences max)

Answer:"""
            
            prompt = PromptTemplate.from_template(template)
            
            # Create chain: retrieve docs, format context, pass to LLM
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            self.qa_chain = (
                {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
            )
            
            return True
            
        except Exception as e:
            print(f"Error setting up RAG pipeline: {e}")
            return False
    
    def query(self, question: str) -> Optional[Dict]:
        """
        Ask a question about the resume
        
        Args:
            question (str): User question about the resume
            
        Returns:
            Dict: Contains 'answer' and 'confidence' or None if error
        """
        if not self.qa_chain or not self.retriever:
            return None
        
        try:
            # Get relevant documents for confidence assessment
            docs = self.retriever.invoke(question)
            
            # Generate answer
            result = self.qa_chain.invoke(question)
            
            # Extract answer text
            if hasattr(result, 'content'):
                answer = result.content
            else:
                answer = str(result)
            
            # Determine confidence based on document matches
            confidence = "High" if len(docs) > 0 else "Low"
            
            return {
                "answer": answer,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"Error querying RAG system: {e}")
            return None
    
    def is_initialized(self) -> bool:
        """Check if RAG pipeline is initialized"""
        return self.qa_chain is not None


def create_resume_rag(resume_text: str, api_key: str) -> Optional[ResumeRAG]:
    """
    Factory function to create and initialize ResumeRAG
    
    Args:
        resume_text (str): Resume content
        api_key (str): Groq API key
        
    Returns:
        ResumeRAG: Initialized RAG system or None if failed
    """
    try:
        rag = ResumeRAG(api_key)
        if rag.setup_rag_pipeline(resume_text):
            return rag
        return None
    except Exception as e:
        print(f"Error creating ResumeRAG: {e}")
        return None
