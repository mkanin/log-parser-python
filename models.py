"""The module for model classes."""

import sqlalchemy as db
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class Report(Base):
    """The Report class."""

    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    report_number = db.Column(db.Integer, nullable=False)
    logs = relationship("Log", back_populates="report")


class Log(Base):
    """The Log class."""

    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    response_header_size = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    response_code = db.Column(db.String(32), nullable=False)
    response_size = db.Column(mysql.INTEGER(64), nullable=False)
    request_method = db.Column(db.String(32), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))
    report = relationship("Report", back_populates="logs")
