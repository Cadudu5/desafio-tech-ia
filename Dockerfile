# Usa a mesma versão do seu ambiente local
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta usada pelo Uvicorn
EXPOSE 8000

# Comando padrão para rodar a aplicação FastAPI
CMD ["uvicorn", "app.api.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
