FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY api.py latency_sentinel.py ./
USER 10001:10001
EXPOSE 8080
CMD ["python", "api.py", "--host", "0.0.0.0"]
