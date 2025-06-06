"""baskets

Revision ID: 3da61204ae1b
Revises: 83db7aa3d9d9
Create Date: 2025-05-28 18:52:03.651537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3da61204ae1b'
down_revision: Union[str, None] = '83db7aa3d9d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('book_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('book_name', sa.String(), nullable=False),
    sa.Column('book_author', sa.String(), nullable=False),
    sa.Column('book_description', sa.String(), nullable=False),
    sa.Column('book_price', sa.Float(), nullable=False),
    sa.Column('supply', sa.Integer(), nullable=True),
    sa.Column('book_cover_path', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('supply >= 0', name='check_supply_non_negative'),
    sa.PrimaryKeyConstraint('book_id'),
    sa.UniqueConstraint('book_name')
    )
    op.create_table('genres',
    sa.Column('genre_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('genre_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('genre_id'),
    sa.UniqueConstraint('genre_name')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('baskets',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'book_id')
    )
    op.create_table('book_genres',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], ),
    sa.PrimaryKeyConstraint('book_id', 'genre_id')
    )
    op.create_table('user_books',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('book_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_books')
    op.drop_table('book_genres')
    op.drop_table('baskets')
    op.drop_table('users')
    op.drop_table('genres')
    op.drop_table('books')
    # ### end Alembic commands ###
