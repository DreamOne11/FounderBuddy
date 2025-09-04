"""ICP (Ideal Client Persona) section for Value Canvas."""

from .models import ICPData
from .prompts import ICP_PROMPTS, ICP_TEMPLATE

__all__ = ["ICPData", "ICP_TEMPLATE", "ICP_PROMPTS"]