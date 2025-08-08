# Estudo projeto Django

## Tecnologias utilizadas

- **Django 5.2** — framework web principal (Python)
- **Tailwind CSS 4** — utilitário CSS moderno
- **DaisyUI** — biblioteca de componentes baseada em Tailwind
- **django-compressor** — compressão/otimização de CSS e JS
- **django-browser-reload** — recarregamento automático no desenvolvimento
- **CKEditor** — editor de texto avançado para campos ricos
- **Yarn** — gerenciador de dependências JS
- **uv** — gerenciador de dependências e ambientes Python ultrarrápido
- **Makefile** — automatização de comandos comuns


## Gerenciamento de Ambiente com uv

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências e ambiente virtual. O `uv` é uma alternativa moderna ao pip/pipenv/venv, sendo muito rápido e fácil de usar.

### Principais comandos

#### Instalar dependências

```bash
uv pip install -r requirements.txt
```
Se estiver usando apenas o `pyproject.toml`:
```bash
uv pip install -e .
```

#### Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

#### Rodar comandos Python

```bash
python -m pytest
make test
```
(ou qualquer comando do Makefile)

#### Gerenciar pacotes

```bash
uv pip install <pacote>
uv pip uninstall <pacote>
```

 **Dica:** Certifique-se de que sua IDE está usando o interpretador Python do `.venv` criado pelo uv (`.venv/bin/python`).

---

## Rodando os Testes

Para garantir que os imports funcionem corretamente (já que os módulos estão dentro de `src/`), utilize o runner customizado incluído no projeto:

```bash
python3 run_tests.py
```

Esse script configura automaticamente o PYTHONPATH para incluir o diretório `src`, permitindo que os imports do tipo `from category.domain.entities import Category` funcionem sem problemas.

### Alternativas com unittest

Rodar um teste específico:
```bash
Rodar todos os testes:
```bash
python manage.py test
```

Ou, se preferir usar o Makefile:
```bash
make test
```

---

## Estrutura do Projeto

```
project_root/
├── app/                  # App Django principal (configurações, rotas, views, templates base)
│   ├── __init__.py
│   ├── settings.py       # Configurações globais do projeto
│   ├── urls.py           # Rotas globais
│   ├── views.py          # Views globais
│   └── templates/        # Templates base e globais
│       └── ...
│
├── products/             # Domínio de produtos (exemplo de app)
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py         # Modelos do domínio
│   ├── static/           # Arquivos estáticos do app
│   │   └── ...
│   ├── templates/        # Templates específicos do domínio
│   │   └── ...
│   ├── tests.py
│   └── views.py
│
├── shared/               # Utilitários e infraestrutura compartilhada
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   └── utils/
│       └── ulid_genarate_utils.py
│
├── static/               # Arquivos estáticos globais (CSS, JS, imagens)
│   └── css/
│       ├── input.css
│       └── output.css
│   └── ...
│
├── media/                # Uploads de arquivos de usuários
│   └── ...
│
├── manage.py             # Entrypoint de comandos Django
├── requirements.txt      # Dependências Python
├── package.json          # Dependências JS (Tailwind, DaisyUI, etc)
├── Makefile              # Comandos utilitários
└── README.md             # Documentação
```

---

## Buildando a imagem Docker

Para construir a imagem Docker multi-stage nomeada como `django`, execute:

```bash
docker build -f docker/Dockerfile -t django .
```

Isso irá gerar uma imagem chamada `django` pronta para rodar o projeto.

### Iniciando o container

Para rodar o projeto localmente utilizando a imagem Docker criada:

```bash
docker run --rm -it -p 8000:8000 django
```

Acesse em [http://localhost:8000](http://localhost:8000) para ver o site rodando.

### Rodando as migrations

Antes de acessar o site, rode as migrations do Django para preparar o banco de dados:

```bash
docker run --rm -it django python manage.py migrate
```

Se quiser criar um superusuário:

```bash
docker run --rm -it django python manage.py createsuperuser
```


## Utilizando o Makefile

O projeto possui um arquivo `Makefile` que facilita a execução dos comandos mais comuns. Exemplos:

- **Rodar todos os testes**
  ```bash
  make test
  ```

- **Rodar apenas testes do módulo category**
  ```bash
  make test_category
  ```

- **Limpar arquivos temporários (\_\_pycache\_\_, .pyc)**
  ```bash
  make clean
  ```

> Edite o Makefile conforme a necessidade do seu projeto!

---

## Comandos adicionais do Makefile

O Makefile também inclui comandos úteis para o gerenciamento do projeto Django:

- **runserver**: Inicia o servidor de desenvolvimento do Django.
  ```bash
  make runserver
  # Equivalente a: python manage.py runserver
  ```
- **migrate**: Aplica as migrações do banco de dados.
  ```bash
  make migrate
  # Equivalente a: python manage.py migrate
  ```
- **migrations**: Cria novas migrações a partir das alterações nos modelos.
  ```bash
  make migrations
  # Equivalente a: python manage.py makemigrations
  ```
- **createuser**: Cria um superusuário (administrador) para acessar o painel administrativo do Django.
  ```bash
  make createuser
  # Equivalente a: python manage.py createsuperuser
  ```

Esses comandos facilitam a administração do ambiente de desenvolvimento, permitindo rodar tarefas comuns com apenas uma linha no terminal.

---
