# OpenAI API 키 설정
import os
import openai

import time
import json

from dotenv import load_dotenv

load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("ORGANIZATION")
# 또는
# openai.api_key = 'your-api-key'


# PDF 문서 읽기 및 텍스트 추출
import PyPDF2

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


# 문서 요약
def summarize_text(text):
    response = openai.Completion.create(
      engine="text-davinci-003", # 엔진 버전에 따라 변경 가능
      prompt="Summarize the following text:\n\n" + text,
      max_tokens=150  # 토큰 수에 따라 조정 가능
    )
    return response.choices[0].text.strip()

# 추천 질문 생성
def generate_questions(text):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Create questions about the following text:\n\n" + text,
      max_tokens=100
    )
    return response.choices[0].text.strip()

# 메인 함수
def main(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    summary = summarize_text(text)
    questions = generate_questions(summary)

    print("Summary:\n", summary)
    print("\nQuestions:\n", questions)

# 실행 예시
def main(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    summary = summarize_text(text)
    questions = generate_questions(summary)

    print("Summary:\n", summary)
    print("\nQuestions:\n", questions)

# 실행 예시
def main(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    summary = summarize_text(text)
    questions = generate_questions(summary)

    print("Summary:\n", summary)
    print("\nQuestions:\n", questions)

main("./data/프리랜서 가이드라인 (출판본).pdf")
