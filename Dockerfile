FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN groupadd --system storylens \
    && useradd --system --gid storylens --home-dir /app storylens

COPY requirements.txt ./
RUN pip install --no-cache-dir --requirement requirements.txt

COPY start.py README.md ./
COPY storylens ./storylens

RUN chown -R storylens:storylens /app
USER storylens

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/health', timeout=3)" || exit 1

CMD ["python", "start.py"]
