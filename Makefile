.PHONY: test lint unit clean

test:
	python -m pytest

test_category:
	python -m pytest src/category/

test_shared:
	python -m pytest src/shared/

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
runserver:
	python manage.py runserver
migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations
createuser:
	python manage.py createsuperuser 