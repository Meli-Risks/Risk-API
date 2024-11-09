from src.application.app import db


class Country(db.Model):
    """
    Represents a user entity in the database.

    :param id: The unique identifier of the user.
    :type id: int
    """

    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, unique=True, nullable=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    flag = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """
        Convert the Country object to a dictionary.

        :return: A dictionary representation of the Country object.
        """
        return {
            "code": self.code,
            "id": self.cid,
            "name": self.name,
            "flag": self.flag
        }