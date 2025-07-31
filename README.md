# Estudo  projeto Django

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
PYTHONPATH=src python3 -m unittest category.test.test_entities
```

Rodar todos os testes:
```bash
PYTHONPATH=src python3 -m unittest discover -s category/test
```

---

## Estrutura do Projeto

```
project-root/
  src/
    category/
      domain/
        entities.py
      test/
        test_entities.py
    shared/
      domain/
        default_entity.py
        test/
          deafault_entity_test.py
  run_tests.py
  requirements.txt
  Makefile
```

---

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
