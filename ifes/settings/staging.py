from .production import Production
from configurations import values


class Staging(Production):

    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
