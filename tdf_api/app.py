from fastapi import FastAPI
# from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")

app = FastAPI(
    title="TDF API",
    description="Simple API Server for TDF",
    version="0.1.0",
)

# add_routes(
#     app,
#     ChatDeepSeek(model="deepseek-chat"),
#     path="/deepseek"
# )

# model_deepseek = ChatDeepSeek(model="deepseek-chat", temperature=0, max_tokens=250) #gpt-3.5-turbo, gpt-4o-deepseek
model_gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_tokens=250) #gemini-1.5-turbo
model_llama = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=250)

prompt1 = ChatPromptTemplate.from_template("Write a concise summary about {company_ticker} with not more than 50 words. Also include recent stock performance and key financial metrics below the summary with bullet points.")
prompt2 = ChatPromptTemplate.from_template("Write a concise summary about the sector, {company_ticker} belongs to and summary should be within 50 words. Also include the pros and cons about the sector with bullet points.")

add_routes(
    app,
    prompt1|model_gemini,
    path="/company_summary"
)

add_routes(
    app,
    prompt2|model_llama,
    path="/sector_summary"
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)