# Imagen de la API "Tienda Online" (Práctica 2)
# Autora: Paula Boado Ferreira
# a. Imagen base ligera de Python
FROM python:3.12-slim
# Sin ficheros .pyc, logs al momento y puerto por defecto
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
WORKDIR /app
# b. Copiar primero las dependencias (Docker reutiliza la caché)
COPY requirements.txt .
# c. Instalar las dependencias sin guardar la caché de pip
RUN pip install --no-cache-dir -r requirements.txt
# d. Copiar el código fuente
COPY src/ ./src/
# e. Usuario sin privilegios con permisos sobre el código
RUN useradd -m -s /usr/sbin/nologin appuser
RUN chown -R appuser:appuser /app && chmod -R 755 /app
USER appuser
WORKDIR /app/src
EXPOSE 8000
# f. Comando de inicio: Uvicorn escuchando en 0.0.0.0
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port $PORT"]
