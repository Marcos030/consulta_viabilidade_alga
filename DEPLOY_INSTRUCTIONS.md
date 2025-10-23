# 📦 Instruções para Deploy com Banco Pré-Populado

## 🎯 Objetivo

Fazer deploy no Render.com com o banco SQLite já populado com os dados da planilha, evitando problemas de timeout no upload.

---

## 📋 Passo a Passo

### **1. Preparar o Banco de Dados Localmente**

Execute o script para criar o banco populado:

```bash
python scripts/create_db_for_deploy.py
```

**O que o script faz:**
- ✅ Lê a planilha `data/uploads/enderecos_nordeste.xlsx`
- ✅ Cria o arquivo `data/enderecos.db`
- ✅ Popula com todos os registros (~365 mil)
- ✅ Demora ~2-3 minutos (roda localmente, sem problemas)

**Resultado esperado:**
```
✅ SUCESSO!
📊 Registros inseridos: 365,151
⏱️  Tempo: 120.45s
💾 Banco gerado: D:\Alga\endereco_alga\data\enderecos.db
📏 Tamanho: 45.23 MB
```

---

### **2. Adicionar o Banco ao Repositório**

```bash
git add data/enderecos.db
git commit -m "Add: banco SQLite populado para deploy"
git push
```

**⚠️ Importante:**
- O arquivo `.gitignore` já está configurado para permitir `enderecos.db`
- GitHub aceita arquivos até 100 MB
- O banco tem ~45 MB (OK para GitHub)

---

### **3. Deploy no Render**

O Render vai:
1. ✅ Fazer pull do repositório (com o banco)
2. ✅ Instalar dependências
3. ✅ Iniciar o uvicorn
4. ✅ **Backend já inicia com dados prontos!**

**Nada mais precisa fazer!** 🎉

---

## 🔄 Atualizando os Dados

Quando precisar atualizar a planilha:

```bash
# 1. Substitua a planilha em data/uploads/
# 2. Rode o script novamente
python scripts/create_db_for_deploy.py

# 3. Commit e push
git add data/enderecos.db
git commit -m "Update: atualizar dados da planilha"
git push
```

O Render redesenha automaticamente com os novos dados.

---

## 📊 Como Funciona o Upload no Frontend

O botão de upload **continua funcionando** no frontend:

**Comportamento:**
1. Usuário faz upload de uma planilha
2. Backend **limpa o banco atual**
3. Backend **processa a nova planilha**
4. Dados são atualizados

**⚠️ Limitação no Render Free:**
- Upload pode dar timeout (9+ minutos)
- Se der timeout, dados são perdidos
- **Recomendação:** Usar apenas para demonstração local
- **Para produção:** Atualizar via script + redeploy

---

## ✅ Vantagens desta Abordagem

- ✅ **Sem timeout**: Banco criado localmente
- ✅ **Sem CORS issues**: Não depende de upload HTTP
- ✅ **Deploy rápido**: Backend inicia pronto
- ✅ **Dados garantidos**: Sempre terá registros para consultar
- ✅ **Demonstração funcional**: Site pronto para uso imediato

---

## 🎯 Resultado Final

**Backend no Render:**
- ✅ Inicia em ~30 segundos
- ✅ Já tem 365 mil registros
- ✅ Consultas funcionam imediatamente
- ✅ Frontend pode consultar dados sem fazer upload

**Demonstração perfeita!** 🚀
