from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StatusEnum(str, Enum):
	pending = "pending"
	in_progress = "in_progress"
	done = "done"


class PriorityEnum(str, Enum):
	low = "low"
	medium = "medium"
	high = "high"


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
	hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

	tasks: Mapped[list["Task"]] = relationship(
		"Task", back_populates="owner", cascade="all, delete-orphan"
	)


class Task(Base):
	__tablename__ = "tasks"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	title: Mapped[str] = mapped_column(String(255), nullable=False)
	description: Mapped[str | None] = mapped_column(Text, nullable=True)
	status: Mapped[StatusEnum] = mapped_column(
		SQLEnum(StatusEnum), default=StatusEnum.pending, nullable=False
	)
	priority: Mapped[PriorityEnum] = mapped_column(
		SQLEnum(PriorityEnum), default=PriorityEnum.medium, nullable=False
	)
	due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
	tag: Mapped[str | None] = mapped_column(String(100), nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

	owner: Mapped[User] = relationship("User", back_populates="tasks")
