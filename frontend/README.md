# Frontend - Sistema de Consulta de Viabilidade de Endereços

Frontend React + Vite para o sistema de consulta de endereços.

## 🚀 Tecnologias

- **React 18** - Framework JavaScript
- **Vite** - Build tool e dev server
- **CSS puro** - Estilização sem frameworks
- **Fetch API** - Requisições HTTP

## 📦 Instalação

```bash
cd frontend
npm install
```

## 🛠️ Desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em: [http://localhost:3000](http://localhost:3000)

**Importante**: Certifique-se de que o backend está rodando em `http://localhost:8000`

## 🏗️ Build para Produção

```bash
npm run build
```

Os arquivos buildados estarão na pasta `dist/`

## 📋 Pré-visualização do Build

```bash
npm run preview
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do frontend:

```env
VITE_API_URL=http://localhost:8000
```

Para produção, altere para a URL do seu backend no Render.com:

```env
VITE_API_URL=https://seu-backend.onrender.com
```

## 📱 Funcionalidades

### 1. Consulta de CEP
- Campo CEP com máscara automática (00000-000)
- Campo Código do Logradouro (apenas números)
- Validação de campos obrigatórios
- Tabela de resultados com: Viabilidade, Município, Bairro, Logradouro

### 2. Upload de Planilha
- Aceita apenas arquivos `.xlsx` com nome `enderecos_nordeste.xlsx`
- Timer mostrando tempo decorrido
- Barra de progresso animada
- Suporte para uploads longos (até 9 minutos)

### 3. Limpar Base de Dados
- Modal de confirmação antes de executar
- Mensagem de aviso sobre ação irreversível

## 🎨 Design

- **Responsivo**: Funciona em mobile, tablet e desktop
- **Mobile-first**: Layout otimizado para dispositivos móveis
- **Acessível**: Labels e feedbacks visuais claros
- **Moderno**: UI limpa e minimalista

## 📂 Estrutura de Arquivos

```
frontend/
├── public/              # Arquivos estáticos
├── src/
│   ├── App.jsx         # Componente principal
│   ├── App.css         # Estilos da aplicação
│   ├── main.jsx        # Entry point
│   ├── index.css       # Estilos globais
│   └── api.js          # Funções de comunicação com API
├── index.html          # HTML principal
├── package.json        # Dependências
├── vite.config.js      # Configuração do Vite
└── .env                # Variáveis de ambiente
```

## 🐛 Troubleshooting

### Erro: "Failed to fetch"
- Verifique se o backend está rodando
- Verifique se a URL da API no `.env` está correta
- Verifique se o CORS está configurado no backend

### Erro: "Cannot find module"
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build não funciona
```bash
npm run build -- --debug
```

## 📝 Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run preview` - Pré-visualiza build de produção

## 🌐 Deploy

Este frontend está configurado para deploy automático no **Render.com** através do arquivo `render.yaml` na raiz do projeto.

Veja o [README principal](../README.md) para instruções completas de deploy.
