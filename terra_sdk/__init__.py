"""The Python SDK for Terra."""

# Set default logging to avoid NoHandler warnings
import logging

from .__version__ import *

logging.getLogger(__name__).addHandler(logging.NullHandler())
