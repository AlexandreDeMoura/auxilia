"""create_official_mcp_servers_and_add_description

Revision ID: ee903a5e6aa0
Revises: 09bb4fe47733
Create Date: 2025-12-18 15:12:53.326581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'ee903a5e6aa0'
down_revision: Union[str, Sequence[str], None] = '09bb4fe47733'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Seed data for official MCP servers
OFFICIAL_MCP_SERVERS = [
    {
        "name": "Notion",
        "url": "https://mcp.notion.com/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/notion.png",
        "description": "Connect your AI tools to Notion using the Model Context Protocol (MCP), an open standard that lets AI assistants interact with your Notion workspace.",
    },
    {
        "name": "Atlassian",
        "url": "https://mcp.atlassian.com/v1/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/atlassian.png",
        "description": "The Atlassian Rovo MCP Server is a cloud-based bridge between your Atlassian Cloud site and compatible external tools. Once configured, it enables those tools to interact with Jira, Compass, and Confluence data in real-time. This functionality is powered by secure OAuth 2.1 authorization, which ensures all actions respect the user’s existing access controls.",
    },
    {
        "name": "Linear",
        "url": "https://mcp.linear.app/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/linear.png",
        "description": "Linear's MCP server follows the authenticated remote MCP spec, so the server is centrally hosted and managed. The Linear MCP server has tools available for finding, creating, and updating objects in Linear like issues, projects, and comments.",
    },
    {
        "name": "Sentry",
        "url": "https://mcp.sentry.dev/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/sentry.png",
        "description": "The Sentry MCP Server provides a secure way of bringing Sentry's full issue context into systems that are able to leverage the Model Context Protocol (MCP). Sentry hosts and manages a remote MCP server, which you can connect to and leverage centrally.",
    },
    {
        "name": "Stripe",
        "url": "https://mcp.stripe.com",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/stripe.png",
        "description": "The Stripe Model Context Protocol (MCP) server defines a set of tools that AI agents can use to interact with the Stripe API and search our knowledge base (including documentation and support articles).",
    },
    {
        "name": "Canva",
        "url": "https://mcp.canva.com/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/canva.png",
        "description": "Once set up, your AI can create new empty designs, autofill templates with your content, find your existing designs, and export them as PDFs or images. It's an easy way to speed up creative tasks—no coding required.",
    },
    {
        "name": "Intercom",
        "url": "https://mcp.intercom.com/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/intercom.png",
        "description": "Intercom's MCP is a secure, standardized protocol that allows AI models to access, interact with, and maintain context around Intercom data and tools like conversations, contacts, and workspace-specific functionality.",
    },
    {
        "name": "DeepWiki",
        "url": "https://mcp.deepwiki.com/mcp",
        "auth_type": "none",
        "icon_url": "https://storage.googleapis.com/choose-assets/deepwiki.png",
        "description": "DeepWiki provides up-to-date documentation you can talk to, for every repo in the world. Think Deep Research for GitHub.",
    },
    {
        "name": "Supabase",
        "url": "https://mcp.supabase.com/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/supabase.png",
        "description": "The Model Context Protocol (MCP) is a standard for connecting Large Language Models (LLMs) to platforms like Supabase. Once connected, your AI assistants can interact with and query your Supabase projects on your behalf.",
    },
    {
        "name": "Amplitude",
        "url": "https://mcp.amplitude.com/mcp",
        "auth_type": "oauth2",
        "icon_url": "https://storage.googleapis.com/choose-assets/amplitude.png",
        "description": "The Amplitude Model Context Protocol (MCP) server enables teams to analyze product data, experiments, and user behavior using conversational AI. Query and create Amplitude content including charts, dashboards, experiments, and cohorts directly through AI interfaces using natural language.",
    },
]


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # Create official_mcp_servers table with same structure as mcp_servers
    official_mcp_servers_table = op.create_table('official_mcp_servers',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('auth_type', postgresql.ENUM('none', 'api_key', 'oauth2', name='mcp_auth_type', create_type=False), nullable=False),
    sa.Column('icon_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # Seed official MCP servers data
    op.bulk_insert(official_mcp_servers_table, OFFICIAL_MCP_SERVERS)

    # Add description column to mcp_servers table
    op.add_column('mcp_servers', sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # Remove description column from mcp_servers table
    op.drop_column('mcp_servers', 'description')

    # Drop official_mcp_servers table
    op.drop_table('official_mcp_servers')
    # ### end Alembic commands ###
