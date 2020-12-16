install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

freeze:
	python -m pip freeze > requirements.txt

test:
	python -m pytest