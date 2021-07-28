prestart-test:
	PYTHONPATH=./app python app/app/tests_pre_start.py

prestart-db-init:
	cd app && PYTHONPATH=. ./prestart.sh

run:
	PYTHONPATH=./app uvicorn app.main:app --reload
