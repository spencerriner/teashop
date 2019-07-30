"""empty message

Revision ID: b0e4e8b840c6
Revises: bd0bf54348cd
Create Date: 2019-07-30 16:35:31.375357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b0e4e8b840c6'
down_revision = 'bd0bf54348cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_item', 'employee_id',
               existing_type=mysql.INTEGER(display_width=10),
               nullable=False)
    op.create_foreign_key(None, 'order_item', 'add_on_item', ['food_description'], ['food_description'])
    op.drop_column('order_item', 'add_on_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_item', sa.Column('add_on_number', mysql.INTEGER(display_width=10), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'order_item', type_='foreignkey')
    op.create_foreign_key('order_item_ibfk_3', 'order_item', 'add_on_item', ['add_on_number'], ['add_on_number'])
    op.alter_column('order_item', 'employee_id',
               existing_type=mysql.INTEGER(display_width=10),
               nullable=True)
    op.drop_column('order_item', 'food_description')
    # ### end Alembic commands ###
