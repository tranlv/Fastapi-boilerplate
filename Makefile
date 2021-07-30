CURRENT_TIMESTAMP:=`date +'%Y%m%d_%H:%M:%S'`

prestart-test:
	PYTHONPATH=./app python app/app/tests_pre_start.py

prestart-db-init:
	cd app && PYTHONPATH=. ./prestart.sh

run:
	PYTHONPATH=./app uvicorn app.main:app --reload

make-migration:
	cd app && PYTHONPATH=. alembic revision --autogenerate -m "${CURRENT_TIMESTAMP} migration"

migrate:
	cd app && PYTHONPATH=. alembic upgrade head

