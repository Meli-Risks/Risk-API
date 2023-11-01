from src.application.app import db
from src.infrastructure.entities.role import Role


class User(db.Model):
    """
    Represents a user entity in the database.

    :param id: The unique identifier of the user.
    :type id: int
    :param username: The username of the user.
    :type username: str
    :param password: The hashed password of the user.
    :type password: str
    :param email: The email address of the user.
    :type email: str
    :param active: A flag indicating if the user is active.
    :type active: bool
    :param roles: The roles associated with the user.
    :type roles: list of Role
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    roles = db.relationship(Role, secondary='user_roles', back_populates='users')


class UserRoles(db.Model):
    """
    Represents the association between users and roles.

    :param user_id: The user's identifier.
    :type user_id: int
    :param role_id: The role's identifier.
    :type role_id: int
    """

    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
