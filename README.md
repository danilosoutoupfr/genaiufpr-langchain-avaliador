# GenAI-LangChain-AgenteAvaliador
Primeiro trabalho: a partir das avaliações obtidas da API, conforme o código do repositório, desenvolver um agente que indique se a avaliação é positiva ou negativa.



git clone https://github.com/danilosoutoupfr/genaiufpr-langchain-avaliador.git

docker build -t genaiufpr-langchain-avaliador . docker run -d -p 8000:8000 --restart always --name genaiufpr-langchain-avaliador genaiufpr-langchain-avaliador

curl -X GET http://localhost:8000



docker build -t agt-ava .
### teste
docker run --rm -d --env-file=.env -p 8002:8000 --name agt-ava agt-ava
### produção
docker run -d --env-file=.env -p 8002:8000 --restart always --name agt-ava agt-ava

curl -X GET http://localhost:8002
curl -X POST http://localhost:8002/avaliar \
  -H "Content-Type: application/json" \
  -d '{"review": "Este produto é incrível! Adorei a qualidade e recomendo a todos."}'

