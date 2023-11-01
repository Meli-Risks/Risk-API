from src.application.app import db


class Provider(db.Model):
    """
    Represents a provider entity in the database.

    :param id: The unique identifier of the provider.
    :param name: The name of the provider.
    :param country_codes: An array of country codes associated with the provider.
    """

    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_codes = db.Column(db.ARRAY(db.String(2)))
