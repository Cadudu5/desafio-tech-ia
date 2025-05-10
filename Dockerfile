# Usa uma imagem Python enxuta
FROM python:3.12-slim

# Evita mensagens interativas e define encoding padrão
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Define diretório de trabalho
WORKDIR /app

# Atualiza pacotes e instala dependências do sistema, se necessário (ex: para numpy, pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements.txt primeiro para usar cache do Docker
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do projeto
COPY . .

# Expõe a porta do Uvicorn
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.api.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
