# 🚀 Guia Rápido de Início

## Para rodar localmente (2 comandos)

### Terminal 1 - Backend
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend em: http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend em: http://localhost:3000

## Usar a aplicação

1. **Abra**: http://localhost:3000
2. **Upload**: Clique em "Selecionar Arquivo" e envie `enderecos_nordeste.xlsx` (demora ~9 min)
3. **Consultar**: Digite CEP (ex: 49097-050) e Código (ex: 21331) → Pesquisar
4. **Limpar**: Use o botão vermelho para resetar a base

## Estrutura do Projeto

```
endereco_alga/
├── app/                    # Backend FastAPI
│   ├── main.py            # Endpoints da API
│   ├── database.py        # Conexão SQLite
│   ├── models.py          # Schemas
│   └── services.py        # Lógica de negócio
├── frontend/              # Frontend React
│   └── src/
│       ├── App.jsx        # Componente principal
│       ├── App.css        # Estilos
│       └── api.js         # Chamadas à API
└── render.yaml            # Config para deploy
```

## Deploy no Render.com

1. **Criar repositório Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/seu-usuario/repo.git
   git push -u origin main
   ```

2. **No Render.com**
   - New + → Blueprint
   - Conectar repositório
   - Apply

3. **Configurar variável de ambiente**
   - Copie a URL do backend
   - No frontend: Settings → Environment
   - Adicione: `VITE_API_URL=https://seu-backend.onrender.com`

Pronto! 🎉

## Dúvidas?

Leia o [README.md](README.md) completo para mais detalhes.
