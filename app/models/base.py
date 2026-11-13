from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, MetaData, func


class Base(DeclarativeBase):
    metadata = MetaData()


class DateTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # 插入时由 PG 生成，采用服务器时间
        insert_sentinel=False,  # 禁止 ORM 隐式写入
        nullable=False,  # 不允许为空
        index=True,  # 可通过创建时间索引
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # 插入时由 PG 生成，采用服务器时间
        onupdate=func.now(),  # 更新时由 PG 刷新，采用服务器时间
        insert_sentinel=False,  # 禁止 ORM 隐式写入
        nullable=False,
    )
