# GenAI-LangChain-AgenteAvaliador
Primeiro trabalho: a partir das avaliações obtidas da API, conforme o código do repositório, desenvolver um agente que indique se a avaliação é positiva ou negativa.



git clone https://github.com/danilosoutoupfr/genaiufpr-langchain-avaliador.git

docker build -t genaiufpr-langchain-avaliador . docker run -d -p 8000:8000 --restart always --name genaiufpr-langchain-avaliador genaiufpr-langchain-avaliador

curl -X GET http://localhost:8000



docker build -t agt-ava .
docker run --rm -d --env-file=.env -p 8777:8000 --name agt-ava agt-ava


curl -X GET http://localhost:8777
curl -X POST http://localhost:8777/avaliar \
  -H "Content-Type: application/json" \
  -d '{"review": "Este produto é incrível! Adorei a qualidade e recomendo a todos."}'

