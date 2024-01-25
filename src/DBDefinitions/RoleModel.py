import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .UUID import UUIDColumn, UUIDFKey
from .Base import BaseModel


class RoleModel(BaseModel):
    """Spojuje uzivatele a skupinu, ve ktere uzivatel "hraje" roli"""

    __tablename__ = "roles"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), index=True)
    group_id = Column(ForeignKey("groups.id"), index=True)
    roletype_id = Column(ForeignKey("roletypes.id"), index=True)

    startdate = Column(DateTime, comment="when the role begins")
    enddate = Column(DateTime, comment="when the role ends")
    valid = Column(Boolean, default=True, comment="if the role is still active")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when record has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    createdby = UUIDFKey(nullable=True, comment="who has created this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who has changed this record")#Column(ForeignKey("users.id"), index=True, nullable=True)

    roletype = relationship("RoleTypeModel", back_populates="roles")
    user = relationship("UserModel", back_populates="roles", foreign_keys=[user_id])
    group = relationship("GroupModel", back_populates="roles")
