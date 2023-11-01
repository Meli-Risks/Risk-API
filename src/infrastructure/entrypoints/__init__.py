from src.infrastructure.adapters.clients.country_client import CountryClient
from src.infrastructure.adapters.databases.auth_repository import AuthRepository
from src.infrastructure.adapters.databases.blacklist_repository import BlackListRepository
from src.infrastructure.adapters.databases.country_repository import CountryRepository
from src.infrastructure.adapters.databases.provider_repository import ProviderRepository
from src.infrastructure.adapters.databases.risk_repository import RiskRepository

country_client = CountryClient()
country_gateway = CountryRepository()
provider_gateway = ProviderRepository()
risk_gateway = RiskRepository()
auth_gateway = AuthRepository()
blacklist_gateway = BlackListRepository()
