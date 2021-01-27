"""The Python SDK for Terra."""

# Set default logging to avoid NoHandler warnings
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
