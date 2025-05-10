from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_report(query: str):
    llm = OpenAI(model="gpt-3.5-turbo")
    return llm(f"Genera un reporte sobre: {query}")