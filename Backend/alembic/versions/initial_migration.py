"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'staff', 'customer'), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'suspended'), nullable=False),
        sa.Column('avatar', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_role', 'users', ['role'])
    op.create_index('idx_user_status', 'users', ['status'])
    op.create_index('idx_user_deleted_at', 'users', ['deleted_at'])

    # Create refresh_tokens table
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_revoked', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index('idx_refresh_token_user', 'refresh_tokens', ['user_id'])
    op.create_index('idx_refresh_token_revoked', 'refresh_tokens', ['is_revoked'])
    op.create_index('idx_refresh_token_expires', 'refresh_tokens', ['expires_at'])

    # Create complaints table
    op.create_table(
        'complaints',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('complaint_id', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.Enum('Technical Issue', 'Billing', 'Service Outage', 'Account Management', 'Product Quality', 'Customer Service', 'Other'), nullable=False),
        sa.Column('status', sa.Enum('open', 'inprogress', 'resolved', 'closed'), nullable=False),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', 'urgent'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('attachments', sa.JSON(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('complaint_id')
    )
    op.create_index('idx_complaint_user', 'complaints', ['user_id'])
    op.create_index('idx_complaint_assigned', 'complaints', ['assigned_to'])
    op.create_index('idx_complaint_status', 'complaints', ['status'])
    op.create_index('idx_complaint_priority', 'complaints', ['priority'])
    op.create_index('idx_complaint_created', 'complaints', ['created_at'])
    op.create_index('idx_complaint_updated', 'complaints', ['updated_at'])

    # Create service_requests table
    op.create_table(
        'service_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('request_id', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.Enum('Installation', 'New Service', 'Upgrade', 'Repair', 'Maintenance', 'Other'), nullable=False),
        sa.Column('status', sa.Enum('open', 'inprogress', 'resolved', 'closed'), nullable=False),
        sa.Column('priority', sa.Enum('low', 'medium', 'high'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('preferred_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferred_time', sa.String(length=50), nullable=True),
        sa.Column('attachments', sa.JSON(), nullable=True),
        sa.Column('technician_name', sa.String(length=255), nullable=True),
        sa.Column('completion_notes', sa.Text(), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id')
    )
    op.create_index('idx_request_user', 'service_requests', ['user_id'])
    op.create_index('idx_request_assigned', 'service_requests', ['assigned_to'])
    op.create_index('idx_request_status', 'service_requests', ['status'])
    op.create_index('idx_request_created', 'service_requests', ['created_at'])

    # Create responses table
    op.create_table(
        'responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('complaint_id', sa.Integer(), nullable=True),
        sa.Column('request_id', sa.Integer(), nullable=True),
        sa.Column('is_staff_response', sa.Boolean(), nullable=False),
        sa.Column('is_system_response', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['request_id'], ['service_requests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_response_complaint', 'responses', ['complaint_id'])
    op.create_index('idx_response_request', 'responses', ['request_id'])
    op.create_index('idx_response_user', 'responses', ['user_id'])
    op.create_index('idx_response_created', 'responses', ['created_at'])

    # Create feedbacks table
    op.create_table(
        'feedbacks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('category', sa.Enum('Overall Experience', 'Service Quality', 'Staff Professionalism', 'Resolution Time', 'Communication', 'Website/App Usability'), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('suggestion', sa.Text(), nullable=True),
        sa.Column('would_recommend', sa.Boolean(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_feedback_user', 'feedbacks', ['user_id'])
    op.create_index('idx_feedback_rating', 'feedbacks', ['rating'])
    op.create_index('idx_feedback_created', 'feedbacks', ['created_at'])

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('type', sa.Enum('complaint_update', 'request_update', 'response', 'status_change', 'assignment', 'reminder', 'system'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_notification_user', 'notifications', ['user_id'])
    op.create_index('idx_notification_read', 'notifications', ['is_read'])
    op.create_index('idx_notification_type', 'notifications', ['type'])
    op.create_index('idx_notification_created', 'notifications', ['created_at'])

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.Enum('login', 'logout', 'create', 'update', 'delete', 'soft_delete', 'restore', 'role_change', 'permission_change', 'status_change', 'assign', 'resolve', 'close'), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=True),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_user', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_created', 'audit_logs', ['created_at'])

    # Create system_settings table
    op.create_table(
        'system_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setting_key', sa.String(length=100), nullable=False),
        sa.Column('setting_value', sa.Text(), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('setting_key')
    )
    op.create_index('idx_setting_key', 'system_settings', ['setting_key'], unique=True)

def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('system_settings')
    op.drop_table('audit_logs')
    op.drop_table('notifications')
    op.drop_table('feedbacks')
    op.drop_table('responses')
    op.drop_table('service_requests')
    op.drop_table('complaints')
    op.drop_table('refresh_tokens')
    op.drop_table('users')