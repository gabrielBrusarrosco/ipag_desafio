# Desafio Técnico iPag - API de Pedidos

**Autor:** Gabriel César Brusarrosco
**Status:** Concluído ✅

---

## 📝 Descrição do Projeto

Este projeto consiste em uma API REST para gerenciamento de pedidos e um Worker para processamento assíncrono de notificações, desenvolvido como parte do desafio técnico para a vaga de Desenvolvedor(a) de Software na iPag.

A solução foi construída seguindo as melhores práticas de arquitetura de software, com foco em clareza, manutenibilidade e robustez.

---

## ✨ Funcionalidades

- ✅ Criação de Pedidos (`POST /v1/orders/`)
- ✅ Listagem de Pedidos com filtro por status (`GET /v1/orders/`)
- ✅ Consulta de Pedido específico por ID (`GET /v1/orders/{order_id}`)
- ✅ Atualização de Status de Pedido (`PUT /v1/orders/{order_id}/status`)
- ✅ Resumo Estatístico de Pedidos (`GET /v1/orders/summary/`)
- ✅ Publicação assíncrona de eventos de mudança de status via RabbitMQ.
- ✅ Worker para consumir eventos e registrar logs de notificação.
- ✅ Validação de dados de entrada, incluindo formato de CPF.
- ✅ Lógica de transição de status de pedidos.

---

## 🏛️ Arquitetura e Decisões Técnicas

A aplicação foi desenvolvida em **Python** utilizando o micro-framework **FastAPI**, com foco em uma arquitetura limpa e desacoplada.

* **Arquitetura em Camadas (Layered Architecture):** O código foi organizado nas seguintes camadas para garantir a separação de responsabilidades:
    * **Endpoints (API):** Responsável por lidar com requisições e respostas HTTP.
    * **Serviços (Services):** Contém a lógica de negócio e orquestra as operações.
    * **Repositórios (Repositories):** Abstrai toda a comunicação com o banco de dados.

* **Banco de Dados (PostgreSQL):** Optei pelo PostgreSQL por sua robustez e recursos avançados. As chaves primárias de todas as tabelas foram implementadas com **UUIDs** para garantir identificadores únicos e não sequenciais, uma prática recomendada para microsserviços.

* **Migrations (Alembic):** O versionamento do schema do banco de dados é gerenciado pelo Alembic, permitindo a evolução segura e controlada da estrutura das tabelas.

* **Processamento Assíncrono (RabbitMQ):** Para operações que podem ser demoradas, como o envio de notificações, foi implementado um fluxo assíncrono. O `OrderService` publica uma mensagem na fila do RabbitMQ, e um **Worker** separado consome essa mensagem, processa e salva o log, garantindo que a API permaneça rápida e responsiva. O worker também implementa uma **lógica de retentativa com limite** para lidar com falhas temporárias.

* **Containerização (Docker):** Todo o ambiente (API, Worker, PostgreSQL, RabbitMQ) é orquestrado com **Docker Compose**, garantindo um ambiente de desenvolvimento e produção consistente, portátil e fácil de configurar.

---

## 🚀 Como Executar o Projeto

**Pré-requisitos:**
* [Docker](https://www.docker.com/get-started/)
* [Docker Compose](https://docs.docker.com/compose/install/)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/gabrielBrusarrosco/ipag_desafio.git
    cd ipag-desafio
    ```

2.  **Construa e inicie os contêineres:**
    O comando a seguir irá construir as imagens, baixar as dependências e iniciar todos os serviços em segundo plano.
    ```bash
    docker-compose up --build -d
    ```

3.  **Acesse a Aplicação:**
    * A API estará disponível em `http://localhost:8000`.
    * A documentação interativa (Swagger UI) está em `http://localhost:8000/docs`.
    * A interface de gerenciamento do RabbitMQ está em `http://localhost:15672` (login: `guest` / senha: `guest`).

4.  **Execute as Migrations (se necessário):**
    As tabelas são criadas pela primeira vez através das migrations. Para rodar manualmente:
    ```bash
    docker-compose exec api alembic upgrade head
    ```
    
---

## 📖 Documentação da API

A documentação completa e interativa de todos os endpoints está disponível via Swagger UI. Através dela, é possível testar todas as funcionalidades da API diretamente pelo navegador.

**URL:** `http://localhost:8000/docs`

---