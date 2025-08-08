# Dockerfile multi-stage otimizado para Django + Tailwind + Yarn

# Stage 1: Build frontend (Tailwind, DaisyUI, etc)
FROM node:20-alpine AS frontend-build
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY static/ ./static/
COPY app/templates/ ./app/templates/
COPY products/templates/ ./products/templates/
# Gera o CSS otimizado
RUN yarn run tailwind:build

# Stage 2: Build backend Python (uv/pyproject.toml)
FROM python:3.10-slim AS python-build
WORKDIR /app

RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system -r pyproject.toml

# Stage 3: Final image
FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=app.settings

# Copia dependências já instaladas
COPY --from=python-build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=python-build /usr/local/bin/uv /usr/local/bin/uv

# Copia projeto
COPY . .

# Copia CSS final gerado
COPY --from=frontend-build /app/static/css/output.css ./static/css/output.css

# Coleta arquivos estáticos para produção
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
