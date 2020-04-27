"""empty message

Revision ID: 34a8b3a88a74
Revises: 
Create Date: 2020-04-27 18:21:19.383506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34a8b3a88a74'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('security',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(length=64), nullable=True),
    sa.Column('sector', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('website', sa.String(length=64), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_security_name'), 'security', ['name'], unique=False)
    op.create_index(op.f('ix_security_sector'), 'security', ['sector'], unique=False)
    op.create_index(op.f('ix_security_summary'), 'security', ['summary'], unique=False)
    op.create_index(op.f('ix_security_ticker'), 'security', ['ticker'], unique=False)
    op.create_index(op.f('ix_security_website'), 'security', ['website'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('followed_securities',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['security.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('security_id', sa.Integer(), nullable=True),
    sa.Column('long', sa.Boolean(), nullable=True),
    sa.Column('unit_price', sa.Integer(), nullable=True),
    sa.Column('total_cost', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['security.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_timestamp'), 'transaction', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_timestamp'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_table('followed_securities')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_security_website'), table_name='security')
    op.drop_index(op.f('ix_security_ticker'), table_name='security')
    op.drop_index(op.f('ix_security_summary'), table_name='security')
    op.drop_index(op.f('ix_security_sector'), table_name='security')
    op.drop_index(op.f('ix_security_name'), table_name='security')
    op.drop_table('security')
    # ### end Alembic commands ###
