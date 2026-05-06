FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY api ./api
COPY db ./db
COPY docs ./docs
COPY README.md .

EXPOSE 8000

CMD ["uvicorn", "alignment_engine.main:app", "--host", "0.0.0.0", "--port", "8000"]
