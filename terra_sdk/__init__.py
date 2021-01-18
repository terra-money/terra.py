"""terra_sdk 지구, the Python SDK for Terra."""

# Set default logging to avoid NoHandler warnings
import logging

from .__version__ import *
from .client.terra import Terra

logging.getLogger(__name__).addHandler(logging.NullHandler())
