# Mapping record

Inventory taken at commit `1fbb8505bf45e10df927859538e75753aed6e7eb`: 22 pages, 134 endpoints, 3 scheduled jobs, 5 incoming events.
Pilot: waiting for the Builder

## Areas

| Area | Is | Flows, roughly | Such as | State |
|---|---|---|---|---|
| Sign-in | Getting into the workspace: first-admin setup, password or Google sign-in, accepting an invite. | 5 | Set up the first admin; Accept an invite; Sign in with Google | not gone into |
| People | An admin managing who is in the workspace: users, roles, teams, invites. | 6 | Invite a user; Change a user's role; Put a user in a team | not gone into |
| MCP servers | An admin adding MCP servers to the workspace, and users connecting their own credentials to them. | 8 | Add a server from the catalog; Add a custom server; Connect to a server with OAuth | not gone into |
| Agents | Setting up an agent: instructions, MCP tools, skills, subagents, sandbox, who can use it, archive. | 13 | Create an agent; Give an agent MCP tools; Share an agent | in progress |
| Chat | Talking to an agent in a thread, and the durable runs behind it, including artifacts and MCP apps. | 12 | Start a thread; Approve a tool call; Stop a run | not gone into |
| Skills | The workspace skill library: writing skills, importing them from GitHub/GitLab sources, syncing and adopting versions. | 6 | Write a skill; Import skills from a GitHub repo; Adopt a new version of a skill | not gone into |
| Triggers | Scheduled agent runs: a cron schedule that starts a thread on its own. | 5 | Schedule a trigger; Run a trigger now; Pause a trigger | not gone into |
| Settings | Personal access tokens, and admin settings for workspace models and sandboxes. | 6 | Create a personal access token; Choose the workspace's default model; Add a sandbox | not gone into |
| Slack | Talking to workspace agents from Slack. | 4 | Ask an agent from Slack; Approve a tool call from Slack | not gone into |

## Entry points

| Kind | Entry point | In | Area | Belongs to |
|---|---|---|---|---|
| page | /auth | web/src/app/auth/page.tsx | Sign-in | Flow to write: sign-in |
| page | /setup | web/src/app/setup/page.tsx | Sign-in | not looked at yet |
| page | /invite/[token] | web/src/app/invite/[token]/page.tsx | Sign-in | not looked at yet |
| page | /users | web/src/app/(protected)/users/page.tsx | People | not looked at yet |
| page | /mcp-servers | web/src/app/(protected)/mcp-servers/page.tsx | MCP servers | not looked at yet |
| page | /mcp-servers/add | web/src/app/(protected)/mcp-servers/add/page.tsx | MCP servers | not looked at yet |
| page | /mcp-servers/add/custom | web/src/app/(protected)/mcp-servers/add/custom/page.tsx | MCP servers | not looked at yet |
| page | /mcp-servers/[id] | web/src/app/(protected)/mcp-servers/[id]/page.tsx | MCP servers | not looked at yet |
| page | /agents | web/src/app/(protected)/agents/page.tsx | Agents | Flow: find-an-agent |
| page | /agents/new | web/src/app/(protected)/agents/new/page.tsx | Agents | Flow: create-an-agent |
| page | /agents/[id] | web/src/app/(protected)/agents/[id]/page.tsx | Agents | Flow to write: edit-an-agent, Flow to write: give-an-agent-mcp-tools, Flow to write: connect-a-server-from-an-agent, Flow to write: give-an-agent-code-execution, Flow to write: enable-skills-on-an-agent, Flow to write: add-a-subagent, Flow to write: share-an-agent, Flow to write: tag-an-agent, Flow to write: manage-agent-tags, Flow to write: archive-an-agent |
| page | /agents/[id]/threads | web/src/app/(protected)/agents/[id]/threads/page.tsx | Chat | not looked at yet |
| page | /agents/[id]/chat | web/src/app/(protected)/agents/[id]/chat/page.tsx | Chat | not looked at yet |
| page | /agents/[id]/chat/[threadId] | web/src/app/(protected)/agents/[id]/chat/[threadId]/page.tsx | Chat | not looked at yet |
| page | /skills | web/src/app/(protected)/skills/page.tsx | Skills | not looked at yet |
| page | /skills/new | web/src/app/(protected)/skills/new/page.tsx | Skills | not looked at yet |
| page | /skills/[id] | web/src/app/(protected)/skills/[id]/page.tsx | Skills | not looked at yet |
| page | /skills/sources/new | web/src/app/(protected)/skills/sources/new/page.tsx | Skills | not looked at yet |
| page | /triggers | web/src/app/(protected)/triggers/page.tsx | Triggers | not looked at yet |
| page | /triggers/new | web/src/app/(protected)/triggers/new/page.tsx | Triggers | not looked at yet |
| page | /triggers/[id] | web/src/app/(protected)/triggers/[id]/page.tsx | Triggers | not looked at yet |
| page | /settings | web/src/app/(protected)/settings/page.tsx | Settings | not looked at yet |
| endpoint | GET /auth/providers | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | GET /auth/setup/status | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | POST /auth/setup | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | POST /auth/signin | backend/app/auth/router.py | Sign-in | Flow to write: sign-in |
| endpoint | POST /auth/signout | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | GET /auth/invite/{token} | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | POST /auth/invite/accept | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | GET /auth/google | backend/app/auth/router.py | Sign-in | Flow to write: sign-in |
| endpoint | GET /auth/google/callback | backend/app/auth/router.py | Sign-in | Flow to write: sign-in |
| endpoint | GET /auth/me | backend/app/auth/router.py | Sign-in | not looked at yet |
| endpoint | POST /users | backend/app/users/router.py | People | not looked at yet |
| endpoint | GET /users | backend/app/users/router.py | People | not looked at yet |
| endpoint | GET /users/role-counts | backend/app/users/router.py | People | not looked at yet |
| endpoint | GET /users/{user_id} | backend/app/users/router.py | People | not looked at yet |
| endpoint | GET /users/email/{email} | backend/app/users/router.py | People | not looked at yet |
| endpoint | PATCH /users/{user_id} | backend/app/users/router.py | People | not looked at yet |
| endpoint | PATCH /users/{user_id}/role | backend/app/users/router.py | People | not looked at yet |
| endpoint | PATCH /users/{user_id}/team | backend/app/users/router.py | People | not looked at yet |
| endpoint | DELETE /users/{user_id} | backend/app/users/router.py | People | not looked at yet |
| endpoint | GET /teams | backend/app/teams/router.py | People | not looked at yet |
| endpoint | POST /teams | backend/app/teams/router.py | People | not looked at yet |
| endpoint | PATCH /teams/{team_id} | backend/app/teams/router.py | People | not looked at yet |
| endpoint | DELETE /teams/{team_id} | backend/app/teams/router.py | People | not looked at yet |
| endpoint | POST /invites | backend/app/invites/router.py | People | not looked at yet |
| endpoint | GET /invites | backend/app/invites/router.py | People | not looked at yet |
| endpoint | DELETE /invites/{invite_id} | backend/app/invites/router.py | People | not looked at yet |
| endpoint | POST /mcp-servers | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/official | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | POST /mcp-servers/catalog/sync | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/{server_id} | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | PATCH /mcp-servers/{server_id} | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/{server_id}/oauth-secret-hint | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/{server_id}/agents | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | DELETE /mcp-servers/{server_id} | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | POST /mcp-servers/{server_id}/reset | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/{server_id}/connections | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | DELETE /mcp-servers/{server_id}/connections/{user_id} | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/oauth/callback | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/{server_id}/list-tools | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | GET /mcp-servers/{server_id}/is-connected | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | POST /mcp-servers/test-connection | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | POST /mcp-servers/{server_id}/test-connection | backend/app/mcp/servers/router.py | MCP servers | not looked at yet |
| endpoint | POST /agents | backend/app/agents/router.py | Agents | Flow: create-an-agent |
| endpoint | GET /agents | backend/app/agents/router.py | Agents | Flow: find-an-agent, Flow to write: handle-an-archived-agent |
| endpoint | GET /agents/{agent_id} | backend/app/agents/router.py | Agents | Flow to write: edit-an-agent |
| endpoint | PATCH /agents/{agent_id} | backend/app/agents/router.py | Agents | Flow to write: tag-an-agent |
| endpoint | PUT /agents/{agent_id}/config | backend/app/agents/router.py | Agents | Flow to write: edit-an-agent, Flow to write: give-an-agent-mcp-tools, Flow to write: give-an-agent-code-execution, Flow to write: enable-skills-on-an-agent, Flow to write: add-a-subagent |
| endpoint | DELETE /agents/{agent_id} | backend/app/agents/router.py | Agents | Flow to write: archive-an-agent |
| endpoint | POST /agents/{agent_id}/restore | backend/app/agents/router.py | Agents | Flow to write: handle-an-archived-agent |
| endpoint | DELETE /agents/{agent_id}/permanent | backend/app/agents/router.py | Agents | Flow to write: handle-an-archived-agent |
| endpoint | GET /agents/{agent_id}/permissions | backend/app/agents/router.py | Agents | Flow to write: share-an-agent |
| endpoint | PUT /agents/{agent_id}/permissions | backend/app/agents/router.py | Agents | Flow to write: share-an-agent |
| endpoint | GET /agents/{agent_id}/teams | backend/app/agents/router.py | Agents | Flow to write: share-an-agent |
| endpoint | PUT /agents/{agent_id}/teams | backend/app/agents/router.py | Agents | Flow to write: share-an-agent |
| endpoint | POST /agents/{agent_id}/mcp-servers/{server_id} | backend/app/agents/router.py | Agents | Flow to write: give-an-agent-mcp-tools |
| endpoint | PATCH /agents/{agent_id}/mcp-servers/{server_id} | backend/app/agents/router.py | Agents | Flow to write: give-an-agent-mcp-tools |
| endpoint | DELETE /agents/{agent_id}/mcp-servers/{server_id} | backend/app/agents/router.py | Agents | Flow to write: give-an-agent-mcp-tools |
| endpoint | POST /agents/{agent_id}/mcp-servers/{server_id}/sync-tools | backend/app/agents/router.py | Agents | Flow to write: connect-a-server-from-an-agent |
| endpoint | POST /agents/{agent_id}/subagents/{subagent_id} | backend/app/agents/router.py | Agents | Flow to write: add-a-subagent |
| endpoint | DELETE /agents/{agent_id}/subagents/{subagent_id} | backend/app/agents/router.py | Agents | Flow to write: add-a-subagent |
| endpoint | GET /agents/{agent_id}/is-ready | backend/app/agents/router.py | Chat | not looked at yet |
| endpoint | GET /agents/{agent_id}/threads | backend/app/agents/router.py | Chat | not looked at yet |
| endpoint | GET /tags | backend/app/tags/router.py | Agents | Flow to write: tag-an-agent, Flow to write: manage-agent-tags |
| endpoint | POST /tags | backend/app/tags/router.py | Agents | Flow to write: manage-agent-tags |
| endpoint | PATCH /tags/{tag_id} | backend/app/tags/router.py | Agents | Flow to write: manage-agent-tags |
| endpoint | DELETE /tags/{tag_id} | backend/app/tags/router.py | Agents | Flow to write: manage-agent-tags |
| endpoint | GET /threads/{thread_id}/artifacts | backend/app/artifacts/router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/artifacts/{artifact_id}/content | backend/app/artifacts/router.py | Chat | not looked at yet |
| endpoint | GET /artifacts/viewer | backend/app/artifacts/router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/artifacts/{artifact_id}/export/slides | backend/app/artifacts/router.py | Chat | not looked at yet |
| endpoint | GET /artifacts/google-slides/callback | backend/app/artifacts/router.py | Chat | not looked at yet |
| endpoint | POST /threads/{thread_id}/commands | backend/app/runtime/api/protocol_router.py | Chat | not looked at yet |
| endpoint | POST /threads/{thread_id}/stream/events | backend/app/runtime/api/protocol_router.py | Chat | not looked at yet |
| endpoint | POST /threads/{thread_id}/history | backend/app/runtime/api/protocol_router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/state | backend/app/runtime/api/protocol_router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/messages/{message_id} | backend/app/runtime/api/protocol_router.py | Chat | not looked at yet |
| endpoint | GET /runs/active | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | POST /threads/{thread_id}/runs/invoke | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | POST /threads/{thread_id}/runs | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/runs | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/runs/active | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id}/runs/{run_id} | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | POST /threads/{thread_id}/runs/{run_id}/cancel | backend/app/runtime/api/runs_router.py | Chat | not looked at yet |
| endpoint | POST /mcp-servers/{server_id}/app/read-resource | backend/app/mcp/apps/router.py | Chat | not looked at yet |
| endpoint | POST /mcp-servers/{server_id}/app/call-tool | backend/app/mcp/apps/router.py | Chat | not looked at yet |
| endpoint | GET /threads/{thread_id} | backend/app/threads/router.py | Chat | not looked at yet |
| endpoint | GET /threads | backend/app/threads/router.py | Chat | not looked at yet |
| endpoint | POST /threads | backend/app/threads/router.py | Chat | not looked at yet |
| endpoint | PATCH /threads/{thread_id} | backend/app/threads/router.py | Chat | not looked at yet |
| endpoint | DELETE /threads/{thread_id} | backend/app/threads/router.py | Chat | not looked at yet |
| endpoint | GET /skills | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | POST /skills | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | GET /skills/{skill_id} | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | PUT /skills/{skill_id} | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | DELETE /skills/{skill_id} | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | GET /skills/{skill_id}/diff | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | POST /skills/{skill_id}/adopt | backend/app/skills/router.py | Skills | not looked at yet |
| endpoint | GET /skills/sources | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | POST /skills/sources/preview | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | POST /skills/sources | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | GET /skills/sources/{source_id} | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | PATCH /skills/sources/{source_id} | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | DELETE /skills/sources/{source_id} | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | GET /skills/sources/{source_id}/plan | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | POST /skills/sources/{source_id}/sync | backend/app/skills/sources/router.py | Skills | not looked at yet |
| endpoint | GET /triggers | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | POST /triggers | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | GET /triggers/schedule/preview | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | GET /triggers/{trigger_id}/threads | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | GET /triggers/{trigger_id} | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | PATCH /triggers/{trigger_id} | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | POST /triggers/{trigger_id}/run | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | DELETE /triggers/{trigger_id} | backend/app/triggers/router.py | Triggers | not looked at yet |
| endpoint | POST /auth/tokens | backend/app/auth/tokens/router.py | Settings | not looked at yet |
| endpoint | GET /auth/tokens | backend/app/auth/tokens/router.py | Settings | not looked at yet |
| endpoint | DELETE /auth/tokens/{token_id} | backend/app/auth/tokens/router.py | Settings | not looked at yet |
| endpoint | GET /model-providers | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | GET /model-providers/models | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | GET /model-providers/models/manage | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | PUT /model-providers/models/default | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | DELETE /model-providers/models/default | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | PUT /model-providers/models/{provider}/{model_id:path} | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | POST /model-providers/whitelist/sync | backend/app/model_providers/router.py | Settings | not looked at yet |
| endpoint | GET /sandboxes | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | POST /sandboxes | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | GET /sandboxes/{sandbox_id} | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | GET /sandboxes/{sandbox_id}/agents | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | GET /sandboxes/{sandbox_id}/secret-hint | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | PATCH /sandboxes/{sandbox_id} | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | DELETE /sandboxes/{sandbox_id} | backend/app/sandbox/router.py | Settings | not looked at yet |
| endpoint | GET /health | backend/app/main.py |  | no Flow: the host's uptime probe; it reports the background loops' liveness, no Actor observes it |
| endpoint | /* (auxilia's own MCP server, streamable HTTP) | backend/app/main.py | | no Flow: mounted but advertises no tools, so no client can do anything with it yet |
| endpoint | ANY /api/backend/[...path] | web/src/app/api/backend/[...path]/route.ts | | no Flow: the web app's proxy to the backend, the plumbing every page's calls go through |
| job | Run dispatcher, claims queued runs every 0.5 s | backend/app/runtime/runs/worker.py | Chat | not looked at yet |
| job | Run reaper, every 15 s (plus a daily prune of old runs) | backend/app/runtime/runs/reaper.py | Chat | not looked at yet |
| job | Trigger scanner, every 20 s | backend/app/triggers/scanner.py | Triggers | not looked at yet |
| event | Slack: assistant thread started (POST /integrations/slack/events) | backend/app/integrations/slack/router.py | Slack | not looked at yet |
| event | Slack: message from a user (POST /integrations/slack/events) | backend/app/integrations/slack/router.py | Slack | not looked at yet |
| event | Slack: "select agent" button (POST /integrations/slack/interactions) | backend/app/integrations/slack/router.py | Slack | not looked at yet |
| event | Slack: tool approve / reject button (POST /integrations/slack/interactions) | backend/app/integrations/slack/router.py | Slack | not looked at yet |
| event | Slack: url_verification (POST /integrations/slack/events) | backend/app/integrations/slack/router.py | | no Flow: Slack's one-off handshake when the app's events URL is configured |

## Hesitations

To settle when the Area is gone into.

- POST /threads/{thread_id}/runs/invoke: no page calls it; it is the blocking run for scripts using a personal access token. In Chat for now; it could be its own "API access" Area along with tokens from Settings.
- POST /users, GET /users/{user_id}, GET /users/email/{email}, PATCH /users/{user_id}: no page calls them. Left in People.
- /agents/[id]/threads: an agent's thread list. In Chat, because that is where a user finds a thread again; it could go in Agents.
- Run dispatcher and run reaper: they serve every Chat, Trigger and Slack Flow; placed in Chat, where a stuck or reaped run is seen.
- GET /agents/{agent_id}/is-ready and GET /agents/{agent_id}/threads: moved from Agents to Chat; only the chat pages and the thread history page call them.
- MCP-app endpoints (/mcp-servers/{server_id}/app/*) sit under the MCP servers path but are called from inside a chat; placed in Chat.
