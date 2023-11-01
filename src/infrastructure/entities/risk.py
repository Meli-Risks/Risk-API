from src.application.app import db
from src.infrastructure.entities.provider import Provider


class Risk(db.Model):
    """
    Represents a risk entity in the database.

    :param id: The unique identifier of the risk.
    :param title: The title or name of the risk.
    :param description: The description of the risk.
    :param impact: The impact level of the risk.
    :param probability: The probability level of the risk.
    :param user_id: The user ID associated with the risk.
    :param country_code: The country code associated with the risk.
    :param provider_id: The provider ID associated with the risk.
    :param provider: The relationship with the Provider entity.
    """

    __tablename__ = 'risks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    impact = db.Column(db.Integer)
    probability = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    country_code = db.Column(db.String(2), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    provider = db.relationship(Provider, backref=db.backref('risks', lazy='dynamic'))
