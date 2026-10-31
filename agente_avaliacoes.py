import requests
import json
from dotenv import load_dotenv
from os import getenv 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

http_reviews = requests.get("https://apis.codante.io/api/reviews-api/reviews")
dict_reviews = json.loads(http_reviews.content.decode("utf-8"))
list_review = []

for review in dict_reviews["data"]:
  list_review.append(review["description"])

#Desenvolva, a partir daqui, um chain para um agente que avalia 
# se as revisões recebidas são positivas ou negativas.
#Utilize todos os componentes do LangChain que trabalhamos 
# até este momento para isso.

load_dotenv()
API_KEY = getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key = API_KEY,
    model        = "qwen/qwen3.8-27b",
    temperature  = 0.7
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Você é um avaliador de revisões de produtos. 
        
        Sua tarefa é classificar se a revisão é POSITIVA, NEUTRA ou NEGATIVA. 
        
        De uma nota de 0 a 10 sendo de 0 a 3 NEGATIVA, de 4 a 6 NEUTRA e de 7 a 10 POSITIVA.

        Restrições:
        - Responda em português brasileiro.
        - Não faça introduções ou conclusões.
        - Não faça saudações.
        - Responda apenas com "POSITIVA", "NEUTRA" ou "NEGATIVA".
        - Sempre responda com a avaliação e a nota
        - Sempre obedeça o formato JSON na resposta
        - Sempre calcule a confiança baseada na sua confiança na avaliação


        Exemplos de saída:
        - {{"classificacao": "POSITIVA", "nota": 10, "confianca": 0.95}}
        - {{"classificacao": "NEUTRA", "nota": 5, "confianca": 0.85}}
        - {{"classificacao": "NEGATIVA", "nota": 2, "confianca": 0.7}}

        """),

        ("human", "{avaliacao}")
    ]
)

chain = prompt | llm
resposta = chain.invoke({"avaliacao": "Eu odiei o produto!"})

print(resposta)
print(resposta.content)


for review in list_review:
    resposta = chain.invoke({"avaliacao": review})
    print(review + ":\n " + resposta.content)