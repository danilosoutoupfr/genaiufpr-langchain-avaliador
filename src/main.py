import json
from os import getenv
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
API_KEY = getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=API_KEY,
    model="qwen/qwen3.8-27b",
    temperature=0.7
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

app = FastAPI(
    title="API de Avaliação de Reviews",
    description="API para classificar revisões de produtos em POSITIVA, NEUTRA ou NEGATIVA."
)


class ReviewRequest(BaseModel):
    review: str


class ReviewListRequest(BaseModel):
    reviews: list[str]


class AvaliacaoResponse(BaseModel):
    review: str
    classificacao: str
    nota: int
    confianca: float


def classificar_review(texto_review: str) -> AvaliacaoResponse:
    resposta = chain.invoke({"avaliacao": texto_review})
    try:
        dados = json.loads(resposta.content)
        return AvaliacaoResponse(
            review=texto_review,
            classificacao=dados["classificacao"],
            nota=dados["nota"],
            confianca=dados["confianca"]
        )
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar resposta do modelo: {resposta.content}"
        ) from e


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.post("/avaliar", response_model=AvaliacaoResponse)
def avaliar_review(payload: ReviewRequest):
    """Recebe um único review e retorna a avaliação."""
    return classificar_review(payload.review)


@app.post("/avaliar-lista", response_model=list[AvaliacaoResponse])
def avaliar_lista_reviews(payload: ReviewListRequest):
    """Recebe uma lista de reviews e retorna a lista de classificações."""
    return [classificar_review(review) for review in payload.reviews]

