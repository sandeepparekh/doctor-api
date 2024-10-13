from sqlalchemy import Table, Column, Integer, String, Boolean
from app.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(100)),
    Column("date_of_birth", String(50)),
    Column("gender", String(10)),
    Column("email", String(100), unique=True),
    Column("phone_number", String(15), unique=True),
    Column("mailing_address", String(255)),
    Column("medical_registration_number", String(100), unique=True),
    Column("specialty", String(100)),
    Column("reason_for_participation", String(255)),
    Column("agreement_to_terms", Boolean, nullable=False),
    Column("consent_for_data_use", Boolean, nullable=False),
    Column("privacy_agreement", Boolean, nullable=False),
    Column("password", String(255)),  # New column for password
    Column("otp", String(6)),
    Column("verified", Boolean, default=False),
)
