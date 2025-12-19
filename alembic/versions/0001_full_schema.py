"""full schema"""
from alembic import op
import sqlalchemy as sa

revision = "0001_full_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tg_id", sa.BigInteger, unique=True, nullable=False),
        sa.Column("username", sa.String),
        sa.Column("full_name", sa.String),
        sa.Column("role", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("last_seen_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "operator_shifts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("operator_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("pickup_address", sa.Text, nullable=False),
        sa.Column("started_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime),
        sa.Column("auto_closed", sa.Boolean, server_default="false"),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("min_qty", sa.Integer, server_default="5"),
    )

    op.create_table(
        "bank_accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("bank_id", sa.Integer, nullable=False),
        sa.Column("bank_name", sa.String, nullable=False),
        sa.Column("sbp_phone", sa.String),
        sa.Column("card_number", sa.String),
        sa.Column("card_masked", sa.String),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("load", sa.Integer, server_default="0"),
        sa.Column("weight", sa.Integer, server_default="100"),
        sa.Column("disabled_until", sa.DateTime),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("client_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("operator_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("shift_id", sa.Integer, sa.ForeignKey("operator_shifts.id"), nullable=True),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("delivery_method", sa.String, nullable=False),
        sa.Column("pickup_address_snapshot", sa.Text),
        sa.Column("bank_id", sa.Integer),
        sa.Column("bank_account_id", sa.Integer, sa.ForeignKey("bank_accounts.id")),
        sa.Column("delivery_fee", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id"), unique=True),
        sa.Column("proof_file_id", sa.Text),
        sa.Column("is_confirmed", sa.Boolean, server_default="false"),
        sa.Column("confirmed_by_operator_id", sa.Integer),
        sa.Column("confirmed_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "chats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("client_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("operator_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("admin_requested_at", sa.DateTime),
        sa.Column("admin_joined_at", sa.DateTime),
        sa.Column("admin_id", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "warehouses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("owner_id", sa.Integer),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default="true"),
    )

    op.create_table(
        "warehouse_products",
        sa.Column("warehouse_id", sa.Integer, sa.ForeignKey("warehouses.id"), primary_key=True),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id"), primary_key=True),
        sa.Column("qty_available", sa.Integer, server_default="0"),
        sa.Column("low_notified", sa.Boolean, server_default="false"),
    )

    op.create_table(
        "stock_reservations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id")),
        sa.Column("warehouse_id", sa.Integer, sa.ForeignKey("warehouses.id")),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id")),
        sa.Column("qty", sa.Integer, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "bank_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("bank_id", sa.Integer, nullable=False),
        sa.Column("bank_account_id", sa.Integer),
        sa.Column("order_id", sa.Integer),
        sa.Column("event_type", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "restock_orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("product_id", sa.Integer, nullable=False),
        sa.Column("warehouse_id", sa.Integer, nullable=False),
        sa.Column("qty", sa.Integer, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "operator_sla_stats",
        sa.Column("operator_id", sa.Integer, primary_key=True),
        sa.Column("date", sa.Date, primary_key=True),
        sa.Column("orders_done", sa.Integer, server_default="0"),
        sa.Column("auto_closed_shifts", sa.Integer, server_default="0"),
        sa.Column("reassignments", sa.Integer, server_default="0"),
        sa.Column("avg_response_sec", sa.Float, server_default="0"),
        sa.Column("warnings_count", sa.Integer, server_default="0"),
    )

def downgrade():
    op.drop_table("operator_sla_stats")
    op.drop_table("restock_orders")
    op.drop_table("bank_events")
    op.drop_table("stock_reservations")
    op.drop_table("warehouse_products")
    op.drop_table("warehouses")
    op.drop_table("chats")
    op.drop_table("payments")
    op.drop_table("orders")
    op.drop_table("bank_accounts")
    op.drop_table("products")
    op.drop_table("operator_shifts")
    op.drop_table("users")
