from datetime import datetime
from dataclasses import dataclass
from typing import Optional


from shared.domain.default_entity import DefaultEntity


@dataclass(frozen=True)
class Category():

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
 
