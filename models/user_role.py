from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db
from models.mixins import CreatedUpgradeTimeMixin
from utils.decorators import param_error_handler


class UserRole(CreatedUpgradeTimeMixin):
    __tablename__ = "user_role"
    __table_args__ = (UniqueConstraint("user_id", "role_id"),)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("role.id"))

    @classmethod
    @param_error_handler()
    def get_row_by_ids(cls, user_id: str, role_id: str) -> bool:
        return cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).first()

    @classmethod
    @param_error_handler()
    def is_row_exist(cls, user_id: str, role_id: str) -> bool:
        return db.session.query(
            cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).exists()
        ).scalar()
