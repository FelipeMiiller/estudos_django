.PHONY: test lint unit clean

test:
	python -m pytest

test_category:
	python -m pytest products/



clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
runserver:
	python manage.py runserver

migrations:
	python manage.py makemigrations	
migrate:
	python manage.py migrate


createuser:
	python manage.py createsuperuser 

