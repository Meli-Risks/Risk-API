from src.application.app import db


class Role(db.Model):
    """
    Represents a user role entity in the database.

    :param id: The unique identifier of the role.
    :param name: The name of the role.
    :param identifier: The unique identifier for the role.
    :param users: The relationship with User entities.
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    identifier = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')
