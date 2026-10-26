FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY . .
RUN python -m pip install --no-cache-dir nodeenv && nodeenv -p --node=20.18.0 && /opt/venv/bin/npm --prefix frontend install && /opt/venv/bin/npm --prefix frontend run build
ENV PORT=3000
EXPOSE 3000
CMD ["python", "-m", "backend.app"]
