install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

freeze:
	python -m pip freeze > requirements.txt

sdist:
	python setup.py sdist

upload:
	twine upload dist/*

clean:
	rm -rf *.egg-info
	rm -rf dist/

test: FORCE
	python -m pytest

deploy: clean sdist upload

FORCE: 
