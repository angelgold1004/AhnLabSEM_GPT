from PyPDF2 import PdfReader

import threading
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import uuid
import asyncio

import os
import sys
import openai
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("ORGANIZATION")
sys.path.append(os.getenv("PYTHONPATH"))
llm_model = "gpt-3.5-turbo"


# PDF 파일에서 텍스트 추출
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# OpenAI 챗봇을 사용하여 질문에 답변하는 함수
def answer_question_with_chatbot(text, question):
    prompt = f"{text}\n\n질문: {question}\n답변:"
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

# 챗봇 메인 함수
def pdf_chatbot_main():
    pdf_path = "./data/프리랜서 가이드라인 (출판본).pdf"
    extracted_text = extract_text_from_pdf(pdf_path)

    while True:
        question = input("질문을 입력하세요 (종료하려면 '종료'를 입력하세요): ")
        if question.lower() == '종료':
            break
        answer = answer_question_with_chatbot(extracted_text, question)
        print("답변:", answer)

# 챗봇 실행
pdf_chatbot_main()
