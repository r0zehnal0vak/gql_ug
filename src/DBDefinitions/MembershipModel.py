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

class MembershipModel(BaseModel):
    """Spojuje User s Group jestlize User je clen Group
    Umoznuje udrzovat historii spojeni
    """

    __tablename__ = "memberships"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), index=True)
    group_id = Column(ForeignKey("groups.id"), index=True)

    startdate = Column(DateTime, comment="first date of membership")
    enddate = Column(DateTime, comment="last date of membership")
    valid = Column(Boolean, default=True, comment="if the membership is still active")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when record has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp")
    createdby = UUIDFKey(nullable=True, comment="who has created this record")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who has changed this record")#Column(ForeignKey("users.id"), index=True, nullable=True)

    user = relationship("UserModel", back_populates="memberships", foreign_keys=[user_id])
    group = relationship("GroupModel", back_populates="memberships")

    rbacobject = UUIDFKey(nullable=True, comment="holds object for role resolution")#Column(ForeignKey("users.id"), index=True, nullable=True)    