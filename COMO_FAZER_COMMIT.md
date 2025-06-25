# Como Fazer Commit para o GitHub

## Método 1 - Interface Web (Recomendado)

1. **Baixar projeto do Replit:**
   - Clique nos 3 pontos (...) ao lado do nome do projeto
   - Selecione "Download as zip"
   - Extraia os arquivos

2. **Ir para o repositório GitHub:**
   - Acesse: https://github.com/RebecaToda/fabrica
   - Clique em "Upload files" ou "Add file" → "Upload files"

3. **Fazer upload:**
   - Arraste todos os arquivos ou clique "choose your files"
   - Adicione mensagem: "Sistema de otimização de produção implementado"
   - Clique "Commit changes"

## Método 2 - Git no seu computador

Se tiver Git instalado no Windows:

```bash
git clone https://github.com/RebecaToda/fabrica.git
cd fabrica
# Copie os arquivos baixados do Replit para esta pasta
git add .
git commit -m "Sistema de otimização de produção implementado"
git push origin main
```

## Arquivos importantes para incluir:

- app.py (aplicação principal)
- pyproject.toml (dependências)
- .streamlit/config.toml (configuração)
- executar.bat (para Windows)
- otimizacao_simples.html (versão HTML)
- INSTALACAO_WINDOWS.md (guia)
- README.md (documentação)
- replit.md (arquitetura)

## Resultado final:

Seu repositório terá um sistema completo de otimização de produção com:
- Interface web em Streamlit
- Cálculos de programação linear
- Versão HTML estática
- Guias de instalação completos