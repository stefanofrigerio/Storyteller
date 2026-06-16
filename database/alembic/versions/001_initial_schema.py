"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-06-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('interest_tags', sa.JSON(), nullable=True),
        sa.Column('preferred_content_types', sa.JSON(), nullable=True),
        sa.Column('story_length', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('verbosity_level', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('notifications_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('distance_threshold', sa.Float(), nullable=False, server_default='50.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_preferences_id'), 'user_preferences', ['id'], unique=False)

    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('accuracy', sa.Float(), nullable=True),
        sa.Column('speed', sa.Float(), nullable=True),
        sa.Column('heading', sa.Float(), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('city', sa.String(length=255), nullable=True),
        sa.Column('country', sa.String(length=255), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)
    op.create_index(op.f('ix_locations_timestamp'), 'locations', ['timestamp'], unique=False)
    op.create_index('idx_location_coords', 'locations', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_location_user_time', 'locations', ['user_id', 'timestamp'], unique=False)

    # Create pois table
    op.create_table(
        'pois',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=False),
        sa.Column('poi_type', sa.String(length=100), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('historical_context', sa.Text(), nullable=True),
        sa.Column('fun_facts', sa.Text(), nullable=True),
        sa.Column('source', sa.Enum('OSM', 'GOOGLE', 'MANUAL', 'GENERATED', name='poisource'), nullable=False, server_default='MANUAL'),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source', 'external_id', name='uq_poi_source_external_id')
    )
    op.create_index(op.f('ix_pois_id'), 'pois', ['id'], unique=False)
    op.create_index('idx_poi_coords', 'pois', ['latitude', 'longitude'], unique=False)
    op.create_index('idx_poi_type', 'pois', ['poi_type'], unique=False)

    # Create stories table
    op.create_table(
        'stories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('poi_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('content_type', sa.Enum('HISTORICAL', 'CULTURAL', 'FUNNY', 'RECOMMENDATION', 'NARRATIVE', 'ARCHITECTURAL', name='contenttype'), nullable=False),
        sa.Column('prompt_used', sa.Text(), nullable=True),
        sa.Column('model_version', sa.String(length=100), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('generation_time', sa.Float(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_rating', sa.Integer(), nullable=True),
        sa.Column('is_cached', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('cache_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['poi_id'], ['pois.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stories_id'), 'stories', ['id'], unique=False)
    op.create_index(op.f('ix_stories_generated_at'), 'stories', ['generated_at'], unique=False)
    op.create_index('idx_story_user_generated', 'stories', ['user_id', 'generated_at'], unique=False)
    op.create_index('idx_story_type', 'stories', ['content_type'], unique=False)
    op.create_index('idx_story_favorite', 'stories', ['user_id', 'is_favorite'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index('idx_story_favorite', table_name='stories')
    op.drop_index('idx_story_type', table_name='stories')
    op.drop_index('idx_story_user_generated', table_name='stories')
    op.drop_index(op.f('ix_stories_generated_at'), table_name='stories')
    op.drop_index(op.f('ix_stories_id'), table_name='stories')
    op.drop_table('stories')

    op.drop_index('idx_poi_type', table_name='pois')
    op.drop_index('idx_poi_coords', table_name='pois')
    op.drop_index(op.f('ix_pois_id'), table_name='pois')
    op.drop_table('pois')

    op.drop_index('idx_location_user_time', table_name='locations')
    op.drop_index('idx_location_coords', table_name='locations')
    op.drop_index(op.f('ix_locations_timestamp'), table_name='locations')
    op.drop_index(op.f('ix_locations_id'), table_name='locations')
    op.drop_table('locations')

    op.drop_index(op.f('ix_user_preferences_id'), table_name='user_preferences')
    op.drop_table('user_preferences')

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS contenttype')
    op.execute('DROP TYPE IF EXISTS poisource')
