# Como Executar no Windows

## 1. Instalar Python

1. Vá para https://www.python.org/downloads/
2. Baixe a versão mais recente do Python (3.11 ou superior)
3. **IMPORTANTE**: Durante a instalação, marque a opção "Add Python to PATH"
4. Complete a instalação

## 2. Verificar Instalação

Abra o Prompt de Comando (cmd) e digite:
```
python --version
```

Se aparecer algo como "Python 3.11.x", está funcionando.

## 3. Instalar Dependências

No Prompt de Comando, navegue até a pasta do projeto:
```
cd "caminho\para\sua\pasta"
```

Instale as bibliotecas:
```
python -m pip install streamlit numpy pandas scipy
```

## 4. Executar a Aplicação

```
python -m streamlit run app.py
```

## 5. Solução Alternativa (Mais Fácil)

Crie um arquivo chamado `executar.bat` na mesma pasta do app.py com este conteúdo:

```batch
@echo off
echo Instalando dependencias...
python -m pip install streamlit numpy pandas scipy
echo.
echo Iniciando aplicacao...
python -m streamlit run app.py
pause
```

Depois é só clicar duas vezes no arquivo `executar.bat`.

## Problemas Comuns

- **"python não é reconhecido"**: Python não foi instalado ou não está no PATH
- **"Access denied"**: Execute o cmd como Administrador
- **Pasta com espaços**: Use aspas no caminho: cd "C:\Minha Pasta\Projeto"

## Testando sem Instalar Python

Se quiser testar rapidamente, use este site:
https://streamlit.io/cloud

Faça upload dos arquivos lá e execute online.