import os
from logfire import configure
from logfire import instrument_sqlalchemy
import logging

logger = logging.getLogger("app")
def init_logfire(sync_engine):
    """
    Enables Logfire only in development when ENABLE_LOGFIRE=true and ENVIRONMENT is development
    # for production setup logging -pending
    """
    enable = os.getenv("ENABLE_LOGFIRE", "false").lower() == "true"
    environment = os.getenv("ENVIRONMENT", "production").lower()

 
    if enable and environment == "development":
        token = os.getenv("LOGFIRE_TOKEN")
        base_url = os.getenv("LOGFIRE_BASE_URL", "https://logfire-us.pydantic.dev")
        configure(service_name="fitness-app", environment=environment, token=token, base_url=base_url)
        instrument_sqlalchemy(sync_engine)
            # Standard Python logging for production or if Logfire disabled
        
    else:  
       
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        
        logger.info("Standard logging enabled (production mode)")


    