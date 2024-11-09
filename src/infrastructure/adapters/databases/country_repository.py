from flask import json

from src.application.app import db
from src.domain.gateways.country_gateway import ICountryGateway
from src.infrastructure.entities.country import Country


class CountryRepository(ICountryGateway):
    """
    Implementation of the ICountryGateway interface using a SQL database to manage country-related data.
    """

    def __init__(self):
        """
        Initialize the CountryRepository  with a connection to the database.
        """
        self.db = db

    def set_flag(self, flag_key, ttl=86400):
        """
        Set a flag omitted

        :param flag_key: The key to set.
        :param ttl: Optional time-to-live in seconds (default is 86400 seconds, or 24 hours).
        """

    def check_flag(self, flag_key):
        """
        Check if a flag exists, count if exists countries

        :param flag_key: The key to check.

        :return: True if the flag exists, False otherwise.
        """

        return Country.query.count() > 0

    def set_countries_data(self, country_data_list):
        """
        Set country data in database.

        :param country_data_list: A list of country data objects to store in database.
        """
        list_countries = []
        for country in country_data_list:
            country_dict = country.to_dict()
            new_country = Country(
                cid=country_dict['id'],
                code=country_dict['code'],
                flag=country_dict['flag'],
                name=country_dict['name'],
            )
            list_countries.append(new_country)

        self.db.session.add_all(list_countries)
        self.db.session.commit()

    def get_all_countries_data(self):
        """
        Get all country data stored in dstabase.

        :return: A dictionary of country data where the keys are country codes and values are country data objects.
        """
        country_data = Country.query.all()
        result = {}
        for code, data in country_data.items():
            result[code.decode()] = data.to_dict()
        return result

    def get_countries_data_by_codes(self, country_codes):
        """
        Get country data for specified country codes from database.

        :param country_codes: A list of country codes to retrieve data for.

        :return: A dictionary of country data where the keys are country codes and values are country data objects.
        """
        country_data = Country.query.filter(Country.code.in_(country_codes)).all()
        result = {}
        for code, data in zip(country_codes, country_data):
            if data:
                result[code] = data.to_dict()
        return result

    def delete(self, key):
        """
        Delete all countries.

        :param key: The key to delete, ignore.
        """
        Country.query.delete()
        self.db.session.commit()
