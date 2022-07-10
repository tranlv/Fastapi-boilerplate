from celery import Celery

__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""


celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
