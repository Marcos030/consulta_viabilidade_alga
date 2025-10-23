# 🏠 Sistema de Consulta de Viabilidade de Endereços

Sistema completo (Frontend + Backend) para consultar a viabilidade de endereços do Nordeste do Brasil através de CEP e código do logradouro.

## 📋 Sobre

Este sistema permite consultar rapidamente se um endereço específico é viável para operações, baseado em dados de planilhas Excel. Inclui uma interface web moderna e responsiva.

### Características

- ✅ **Frontend React**: Interface moderna e responsiva
- ✅ **Backend FastAPI**: API REST rápida e documentada
- ✅ **Simples e rápida**: Consultas em menos de 10ms
- ✅ **Gratuita**: Usa SQLite local, sem custos de banco de dados
- ✅ **Escalável**: Suporta centenas de milhares de registros
- ✅ **Deploy fácil**: Configurado para Render.com
- ✅ **Documentação automática**: Interface Swagger/OpenAPI

## 🚀 Instalação Local

### Pré-requisitos

- **Python 3.10 ou superior**
- **Node.js 18 ou superior**
- **npm** ou **yarn**

### 1. Instalar dependências do Backend

```bash
# Na raiz do projeto
pip install -r requirements.txt
```

### 2. Instalar dependências do Frontend

```bash
# Entre na pasta frontend
cd frontend
npm install
```

## 📊 Como usar localmente

### 1. Iniciar o Backend

```bash
# Na raiz do projeto
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

### 2. Iniciar o Frontend

Em outro terminal:

```bash
# Entre na pasta frontend
cd frontend
npm run dev
```

O frontend estará disponível em: **http://localhost:3000**

### 3. Usar a aplicação

1. Acesse http://localhost:3000 no navegador
2. **Upload da planilha**: Clique em "Selecionar Arquivo" e envie o arquivo `enderecos_nordeste.xlsx`
   - O upload pode demorar até 9 minutos
   - Um timer mostrará o tempo decorrido
3. **Consultar endereço**: Digite o CEP e Código do Logradouro e clique em "Pesquisar"
4. **Limpar base**: Use o botão "Limpar Base de Dados" para resetar (pede confirmação)

### Opção alternativa: Carregar dados via script

Para carregar os dados sem usar a interface:

```bash
python scripts/load_excel.py "caminho/para/enderecos_nordeste.xlsx"
```

## 🔍 Endpoints da API

### 1. Health Check

Verifica o status da API e retorna estatísticas.

```bash
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "banco_de_dados": "conectado",
  "total_registros": 365151,
  "estatisticas": {
    "total_registros": 365151,
    "por_viabilidade": {
      "Viável": 320000,
      "Não viável": 45151
    },
    "por_municipio": {
      "FORTALEZA": 150000,
      "RECIFE": 80000,
      "SALVADOR": 70000
    }
  }
}
```

### 2. Consultar Viabilidade

Consulta a viabilidade de um endereço pelo CEP e código do logradouro.

```bash
GET /consultar?cep=60876672&cod_logradouro=13784
```

**Parâmetros:**
- `cep`: CEP do endereço (com ou sem hífen)
- `cod_logradouro`: Código do logradouro

**Resposta - Endereço encontrado:**
```json
{
  "encontrado": true,
  "viabilidade": "Viável",
  "detalhes": {
    "uf": "CE",
    "municipio": "FORTALEZA",
    "localidade": "FORTALEZA",
    "bairro": "JANGURUSSU",
    "logradouro": "RUA SAO BERNARDO",
    "cod_logradouro": "13784",
    "n_fachada": "144",
    "comp_1": null,
    "comp_2": null,
    "comp_3": null,
    "regiao": "NORDESTE",
    "cep": "60876672",
    "total_hps": 1
  },
  "mensagem": "Endereço encontrado com sucesso"
}
```

**Resposta - Endereço não encontrado:**
```json
{
  "encontrado": false,
  "viabilidade": null,
  "detalhes": null,
  "mensagem": "Endereço não encontrado para CEP 60876672 e Código 99999"
}
```

### 3. Upload de Planilha

Faz upload de uma nova planilha Excel.

```bash
POST /upload
Content-Type: multipart/form-data
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Planilha processada com sucesso! 365151 registros inseridos.",
  "registros_inseridos": 365151,
  "tempo_processamento": 45.32
}
```

### 4. Limpar Banco

Remove todos os dados do banco de dados.

```bash
DELETE /limpar
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Banco de dados limpo com sucesso"
}
```

## 💻 Exemplos de Integração

### Python

```python
import requests

# Consultar viabilidade
response = requests.get(
    "http://localhost:8000/consultar",
    params={
        "cep": "60876672",
        "cod_logradouro": "13784"
    }
)

data = response.json()

if data["encontrado"]:
    print(f"Viabilidade: {data['viabilidade']}")
    print(f"Município: {data['detalhes']['municipio']}")
    print(f"Bairro: {data['detalhes']['bairro']}")
else:
    print("Endereço não encontrado")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function consultarViabilidade(cep, codLogradouro) {
  try {
    const response = await axios.get('http://localhost:8000/consultar', {
      params: {
        cep: cep,
        cod_logradouro: codLogradouro
      }
    });

    if (response.data.encontrado) {
      console.log(`Viabilidade: ${response.data.viabilidade}`);
      console.log(`Município: ${response.data.detalhes.municipio}`);
    } else {
      console.log('Endereço não encontrado');
    }
  } catch (error) {
    console.error('Erro:', error.message);
  }
}

consultarViabilidade('60876672', '13784');
```

### cURL

```bash
# Consultar endereço
curl "http://localhost:8000/consultar?cep=60876672&cod_logradouro=13784"

# Upload de planilha
curl -X POST "http://localhost:8000/upload" \
  -F "file=@planilha.xlsx"

# Health check
curl "http://localhost:8000/health"
```

### OpenAI Function Calling

```python
import openai

functions = [
    {
        "name": "consultar_viabilidade_endereco",
        "description": "Consulta se um endereço é viável para operação",
        "parameters": {
            "type": "object",
            "properties": {
                "cep": {
                    "type": "string",
                    "description": "CEP do endereço (com ou sem hífen)"
                },
                "cod_logradouro": {
                    "type": "string",
                    "description": "Código do logradouro"
                }
            },
            "required": ["cep", "cod_logradouro"]
        }
    }
]

# Usar em uma conversa com GPT-4
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "O endereço com CEP 60876672 e código 13784 é viável?"}
    ],
    functions=functions,
    function_call="auto"
)
```

## 📁 Estrutura do Projeto

```
endereco_alga/
├── app/
│   ├── __init__.py          # Inicialização do pacote
│   ├── main.py              # API FastAPI e endpoints
│   ├── database.py          # Conexão SQLite e queries
│   ├── models.py            # Schemas Pydantic
│   ├── services.py          # Lógica de negócio
│   └── utils.py             # Funções auxiliares
├── data/
│   ├── enderecos.db         # Banco SQLite (gerado)
│   └── uploads/             # Planilhas temporárias
├── scripts/
│   └── load_excel.py        # Script de carga inicial
├── tests/
│   └── test_api.py          # Testes (a implementar)
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🗄️ Estrutura do Banco de Dados

### Tabela: `enderecos`

| Coluna            | Tipo    | Descrição                    |
|-------------------|---------|------------------------------|
| id                | INTEGER | Chave primária (auto)        |
| viabilidade_atual | TEXT    | Status de viabilidade        |
| uf                | TEXT    | Unidade Federativa           |
| municipio         | TEXT    | Município                    |
| localidade        | TEXT    | Localidade                   |
| bairro            | TEXT    | Bairro                       |
| logradouro        | TEXT    | Nome do logradouro           |
| cod_logradouro    | TEXT    | Código do logradouro (índice)|
| n_fachada         | TEXT    | Número da fachada            |
| comp_1            | TEXT    | Complemento 1                |
| comp_2            | TEXT    | Complemento 2                |
| comp_3            | TEXT    | Complemento 3                |
| regiao            | TEXT    | Região                       |
| cep               | TEXT    | CEP (índice)                 |
| total_hps         | INTEGER | Total de HPs                 |

### Índices

- `idx_cep_cod`: Índice composto em (cep, cod_logradouro) - usado nas consultas principais
- `idx_cep`: Índice em cep
- `idx_cod_logradouro`: Índice em cod_logradouro

## 🔧 Configuração Avançada

### Variáveis de Ambiente (opcional)

Crie um arquivo `.env`:

```env
DATABASE_PATH=data/enderecos.db
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Rodar em Produção

```bash
# Instalar gunicorn para produção
pip install gunicorn

# Iniciar com gunicorn (Linux/Mac)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Windows - use uvicorn diretamente
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Performance

- **Consulta**: < 10ms por endereço (com índices)
- **Upload**: ~30-60 segundos para 365.000 registros
- **Memória**: ~100-200MB em execução
- **Banco de dados**: ~50MB para 365.000 registros

## 🌐 Deploy no Render.com

Este projeto está configurado para deploy automático no Render.com usando o arquivo `render.yaml`.

### Passos para Deploy

#### 1. Preparar o Repositório

```bash
# Inicializar git (se ainda não tiver)
git init
git add .
git commit -m "Initial commit"

# Criar repositório no GitHub e fazer push
git remote add origin https://github.com/seu-usuario/seu-repo.git
git push -u origin main
```

#### 2. Criar conta no Render.com

1. Acesse [render.com](https://render.com)
2. Crie uma conta ou faça login
3. Conecte sua conta do GitHub

#### 3. Deploy usando render.yaml

1. No dashboard do Render, clique em **"New +"** → **"Blueprint"**
2. Conecte seu repositório do GitHub
3. O Render detectará automaticamente o arquivo `render.yaml`
4. Clique em **"Apply"**

O Render criará automaticamente:
- **Backend**: Web Service rodando FastAPI
- **Frontend**: Static Site com o React buildado

#### 4. Atualizar URL do Backend no Frontend

Após o deploy do backend:

1. Copie a URL do backend (ex: `https://endereco-alga-backend.onrender.com`)
2. No Render, vá em **Settings** do serviço frontend
3. Adicione/edite a variável de ambiente:
   ```
   VITE_API_URL=https://endereco-alga-backend.onrender.com
   ```
4. Salve e o frontend será automaticamente redeployado

#### 5. Testar a aplicação

Acesse a URL do frontend fornecida pelo Render (ex: `https://endereco-alga-frontend.onrender.com`)

### ⚠️ Importante

**Plano Free do Render:**
- Services são desligados após 15 minutos de inatividade
- Primeira requisição após inatividade pode demorar 30-60 segundos (cold start)
- Banco SQLite persiste, mas pode ser perdido ao redesenhar
- **Recomendação**: Fazer upload da planilha após cada deploy

**Banco de Dados:**
- O SQLite será recriado a cada deploy
- Para persistência permanente, considere usar:
  - PostgreSQL no Render (pago)
  - Persistir arquivo SQLite em disco permanente (pago)

### 📊 Monitoramento

No dashboard do Render você pode:
- Ver logs em tempo real
- Monitorar uso de recursos
- Configurar alertas
- Ver métricas de requisições

## 🐛 Troubleshooting

### Backend

**Erro: "Arquivo não encontrado"**
```bash
python scripts/load_excel.py "caminho/completo/enderecos_nordeste.xlsx"
```

**Erro: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Erro: "Port already in use"**
```bash
uvicorn app.main:app --port 8001
```

### Frontend

**Erro: "Failed to fetch"**
- Verifique se o backend está rodando
- Verifique a URL da API no `.env`
- Verifique se CORS está habilitado no backend

**Erro de build**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Deploy no Render

**Backend não inicia**
- Verifique logs no dashboard do Render
- Confirme que `requirements.txt` está correto
- Verifique se o comando de start está correto

**Frontend com página em branco**
- Verifique se a variável `VITE_API_URL` está configurada
- Verifique o console do navegador para erros
- Confirme que o build foi concluído com sucesso

**Erro 502/503**
- Service pode estar em cold start (aguarde 1 minuto)
- Verifique se o service está ativo no dashboard

## 📝 Licença

Este projeto é de uso interno da Alga.

## 👥 Suporte

Para dúvidas ou problemas, entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com ❤️ usando React + FastAPI + SQLite**
