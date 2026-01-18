# -*- coding: utf-8 -*-
"""
add sku to products

Revision ID: cf560864011c
Revises: 0001_full_schema
Create Date: 2025-12-19
"""

from alembic import op
import sqlalchemy as sa


# ===============================
# Alembic identifiers
# ===============================
revision = "cf560864011c"
down_revision = "0001_full_schema"
branch_labels = None
depends_on = None


# ===============================
# Upgrade
# ===============================
def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("sku", sa.String(length=50), nullable=False, server_default="")
    )

    # делаем sku уникальным
    op.create_unique_constraint(
        "uq_products_sku",
        "products",
        ["sku"]
    )


# ===============================
# Downgrade
# ===============================
def downgrade() -> None:
    op.drop_constraint("uq_products_sku", "products", type_="unique")
    op.drop_column("products", "sku")

