import os
import openai
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain, AnalyzeDocumentChain
#import FinanceDataReader as fdr
from langchain.callbacks import get_openai_callback
import time

# 환경 변수 설정 (이 부분은 환경 설정 파일 또는 OS 환경 변수에서 설정하는 것이 좋습니다)
# os.environ["OPENAI_API_KEY"] = "your_actual_open_ai_api_key"

# PDF 파일에서 텍스트 추출
path = "./data/프리랜서 가이드라인 (출판본).pdf"
reader = PdfReader(path)
house_law_raw_text = ""
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        house_law_raw_text += (text + " ")

# 환율 정보 가져오기
#exchange_rate = fdr.DataReader('USD/KRW', '2023').iloc[-1]['Close']

# 질문-답변 챗봇 함수
def qa_bot(source, question, model='gpt-4', temperature=0, chain_type="map_reduce"):
    model = ChatOpenAI(model=model, temperature=temperature)
    qa_chain = load_qa_chain(model, chain_type=chain_type)
    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

    with get_openai_callback() as cb:
        start = time.time()
        print(qa_document_chain.run(input_document=source, question=question))
        end = time.time()

        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): {cb.total_cost:.2f}$, Total Cost (Won): {cb.total_cost*exchange_rate:.2f}₩")
        print(f"걸린 시간: {end-start:.2f}초")

# 예시 질문 실행
qa_bot(house_law_raw_text, "이 문서의 주요 내용은 무엇입니까?")
