def build_country_dto(country):
    """
    Build a CountryDTO object from the provided country data.

    :param country: A dictionary containing country data.

    :return: A CountryDTO object containing transformed country data.
    """
    country_code = country.get('cca2', None)
    flag = country.get('flag', None)
    country_id_str = country.get('ccn3', None)
    country_id = int(country_id_str) if country_id_str is not None and country_id_str.isdigit() else None

    common_name = country.get('name', {}).get('common', None)

    spa_translations = country.get('translations', {}).get('spa', {})
    common_sp_name = spa_translations.get('common', common_name)

    transformed_data = CountryDTO(
        country_code=country_code,
        country_id=country_id,
        common_name=common_name,
        common_sp_name=common_sp_name,
        flag=flag
    )

    return transformed_data


class CountryDTO:
    """
    Data Transfer Object (DTO) for country information.
    """

    def __init__(self, country_code, country_id, common_name, common_sp_name, flag):
        """
        Initialize a CountryDTO object.

        :param country_code: The country code.
        :param country_id: The country identifier.
        :param common_name: The common name of the country.
        :param common_sp_name: The common name in Spanish.
        :param flag: The icon flag
        """
        self.country_code = country_code
        self.country_id = country_id
        self.common_name = common_name
        self.common_sp_name = common_sp_name
        self.flag = flag

    def to_dict(self):
        """
        Convert the CountryDTO object to a dictionary.

        :return: A dictionary representation of the CountryDTO object.
        """
        return {
            "code": self.country_code,
            "id": self.country_id,
            "name": self.common_sp_name,
            "flag": self.flag
        }
