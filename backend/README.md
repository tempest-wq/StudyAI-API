# StudyAI - Backend API

Este repositório contém o backend para o aplicativo de aprendizado do projeto IA Inclusiva. A infraestrutura utiliza 
uma 
arquitetura 
baseada em API Gateway para garantir segurança, isolamento e escalabilidade.

## Como a Arquitetura Funciona

O tráfego de requisições segue um fluxo de isolamento através de três camadas:

1. **NGINX (Proxy de Borda - Porta 80):** É o único serviço exposto para a internet. Ele recebe as conexões, lida com a segurança básica e repassa o tráfego para a rede interna.
2. **Kong Gateway (Roteador Interno):** Recebe as requisições limpas do NGINX, lê as regras declaradas no arquivo `kong.yaml` e decide para qual serviço enviar (ex: autenticação, rate limiting, roteamento de rotas `/api`).
3. **FastAPI (Aplicação Python):** O servidor web principal que processa a lógica de negócio, conectando-se ao banco 
   de dados e a aplicação de IA com chatbot que será implementada futuramente.

## Pré-requisitos

Para rodar este projeto na sua máquina, você precisa ter instalado:
* **[Docker e Docker Compose](https://docs.docker.com/get-docker/)**
* **[uv](https://github.com/astral-sh/uv)** (Gerenciador de pacotes e dependências Python ultrarrápido)

## Como Iniciar o Ambiente Local

1. **Clone o repositório e acesse a pasta do backend:**
   ```bash
   git clone https://github.com/pelican-program/pia.git
   cd backend
2. **Suba os containers da aplicação:**
   ```bash
   docker compose up -d --build
3. **Verifique se a rota Health Check está funcionando:**
   - Acesse no seu browser:
   ```browser
    http://localhost/api/health

## Como parar os serviços e limpar resquícios
```bash
docker compose down
docker system prune

   