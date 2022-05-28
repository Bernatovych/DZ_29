""" models.py """
from sqlalchemy.engine import Engine
from sqlalchemy import event
from book import db


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Phone(db.Model):
    """ Phone """
    __tablename__ = "phones"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    records_id = db.Column(db.Integer, db.ForeignKey('records.id', ondelete='CASCADE'))
    records = db.relationship("Record", back_populates="phones")


class Note(db.Model):
    """ Note """
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    records_id = db.Column(db.Integer, db.ForeignKey('records.id', ondelete='CASCADE'))
    records = db.relationship("Record", back_populates="notes")
    tags = db.relationship("Tag", back_populates="notes", passive_deletes='all')


class Tag(db.Model):
    """ Tag """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='CASCADE'))
    notes = db.relationship("Note", back_populates="tags")


class Address(db.Model):
    """ Address """
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    records_id = db.Column(db.Integer, db.ForeignKey('records.id', ondelete='CASCADE'))
    records = db.relationship("Record", back_populates="addresses")


class Email(db.Model):
    """ Email """
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    records_id = db.Column(db.Integer, db.ForeignKey('records.id', ondelete='CASCADE'))
    records = db.relationship("Record", back_populates="emails")


class Record(db.Model):
    """ Record """
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthday = db.Column(db.Date)
    phones = db.relationship("Phone", back_populates="records", passive_deletes='all')
    notes = db.relationship("Note", back_populates="records", passive_deletes='all')
    addresses = db.relationship("Address", back_populates="records", passive_deletes='all')
    emails = db.relationship("Email", back_populates="records", passive_deletes='all')
