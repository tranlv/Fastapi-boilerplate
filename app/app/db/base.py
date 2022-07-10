# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.auth import User, UserBan, SocialAccount  # noqa


__author__ = ""
__maintainer__ = ""
__email__ = ""
__copyright__ = ""
