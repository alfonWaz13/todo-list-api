import os
from dataclasses import dataclass


@dataclass
class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todosapp.db")
