from src.application.app import db
from src.infrastructure.entities.risk import Risk


class RiskTreatment(db.Model):
    """
    SQLAlchemy Model for the risk_treatment table.
    This table stores information about the treatment of cybersecurity risks.
    """

    __tablename__ = 'risk_treatments'

    id = db.Column(db.Integer, primary_key=True)  # Unique risk treatment ID
    name = db.Column(db.String(100), nullable=False)  # Name of the risk treatment
    description = db.Column(db.Text, nullable=False)  # Detailed description of the risk treatment
    constraints = db.Column(db.Text)  # Constraints or limitations associated with the risk treatment
    start_date = db.Column(db.TIMESTAMP)  # Start date of the risk treatment implementation
    final_date = db.Column(db.TIMESTAMP)  # End date of the risk treatment implementation
    risk_id = db.Column(db.Integer, db.ForeignKey('risks.id'),
                        nullable=False)  # ID of the associated risk in the risks table
    risk = db.relationship(Risk,
                           backref=db.backref('risk_treatments', lazy='dynamic'))  # Relationship with the Risk model
