from datetime import datetime

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    created_at: datetime | None = Field(default_factory=datetime.now)
    created_by: int | None = Field(default=None, foreign_key="User.id")
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
    updated_by: int | None = Field(default=None, foreign_key="User.id")


class MetadataMixin(SQLModel):
    page: int
    total: int
    per_page: int
    total_pages: int
    search: str
