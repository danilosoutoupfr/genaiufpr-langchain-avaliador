# GenAI-LangChain-AgenteAvaliador
Primeiro trabalho: a partir das avaliações obtidas da API, conforme o código do repositório, desenvolver um agente que indique se a avaliação é positiva ou negativa.



git clone https://github.com/danilosoutoupfr/genaiufpr-langchain-avaliador.git

docker build -t genaiufpr-langchain-avaliador . docker run -d -p 8000:8000 --restart always --name genaiufpr-langchain-avaliador genaiufpr-langchain-avaliador

curl -X GET http://localhost:8000