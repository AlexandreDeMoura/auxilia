---
name: maintain-knowledge-base
description: Update the knowledge base in `knowledge-base/` after a code change. Use whenever you have changed the app's code, before you stop.
---

# Maintain the knowledge base

`knowledge-base/` at the repo root describes this app so that the Builder, who does not read the code, can understand it. After a code change it must be true again: every sentence describes what the app now does, and every Anchor points to code that exists.

## Steps

1. **List the code you changed**: every file you added, edited, renamed or deleted in this session (`git status`, `git diff`).
2. **Find the Parts it touches.** Search `knowledge-base/parts/` for the path of each changed file. Add any Part whose capability you changed through a file it has no Anchor in yet.
3. **Make each of those Parts true.** Point every Anchor at the code as it now is, add an Anchor for a new place that carries the capability, remove one whose code is gone, and reword `is` and the labels if the capability changed.
4. **Find the Flows that name those Parts.** Search `knowledge-base/flows/` for each Part's id.
5. **Make each of those Flows true.** Re-read every Step that names the Part, on the main path and in every Variant, against the new code, and rewrite what the Actor does, what they see and what the system does. A Variant repeats the Steps it shares with the main path, so the same edit is often needed in both. Then rewrite the Manual QA Check (`qa`) of every path whose Steps changed, so that following it by hand verifies the new behaviour.
6. **Run the Deterministic Check** with the command the repo's `CLAUDE.md` gives, and fix what it reports until it passes.
7. **Tell the Builder** which knowledge base files you changed and, in plain words, what is different for the Actor.

Done when every Part from step 2 and every Flow from step 4 has been re-read against the new code, and the Deterministic Check passes.

If your change is behaviour that no existing Flow covers, tell the Builder that a Flow is missing and name it. Writing a Flow from zero is outside this skill.

## The files

An id is a file name without `.yaml`, in lower case with dashes.

| File | Holds |
|---|---|
| `actors.yaml` | Each Actor by id: `name`, `is`. |
| `areas.yaml` | Each Area by id: `name`, `is`. |
| `flows/<area>/<flow>.yaml` | One Flow: its main path, its Variants and their Manual QA Checks. |
| `parts/<part>.yaml` | One Part and its Anchors. |

### A Part

```yaml
name: Tool approval
is: Stops the agent before it runs a tool marked "needs approval" and checks the answer.
anchors:
  - label: The tool step and its buttons
    at: web/src/chat/tool-step.tsx#ToolStep
    side: screen
```

- A Part is one capability the Builder would name in conversation, whatever layers of code it spans, so one Part carries Anchors on both sides.
- `at` is `path#Symbol`: the path from the repo root, then a function, class, constant or type defined at the top level of that file, or `Class.member` for a member. The symbol must be defined exactly once in the file. Without `#Symbol` the Anchor points at the whole file.
- `side` is `screen` or `backend`.
- `label` says in the Builder's words what that place in the code is for.

### A Flow

```yaml
name: Approve a tool call
actor: member
goal: Let the agent run a tool after seeing what it is about to do.
trigger: The agent decides to call a tool marked "needs approval".
outcome: The tool has run and the agent has finished its reply.
preconditions:
  - The Member is signed in.
  - flow_to_write: chat/start-a-thread
    so_that: A thread with that agent is open.
steps:
  - id: decide
    does: Clicks Approve.
    sees: Both buttons lock.
    system: The browser sends the decision.
    parts: [tool-approval]
qa:
  setup:
    - Sign in as a Member.
  steps:
    - do: Click Approve.
      expect: Both buttons lock.
variants:
  - id: deny
    name: The Member denies the call
    diverges_at: decide
    when: The Member clicks Deny instead of Approve.
    outcome: The tool was never run.
    steps: []
    qa: { setup: [], steps: [] }
```

- A Step is one moment: `does` (the Actor acts), `sees` (what is on screen), `system` (what the system does). Any may be absent, never all three. A new Step starts whenever the Actor acts or the system does a distinct thing.
- A Step with `system` names at least one Part in `parts`. Steps never point to code; only Anchors do.
- When a Step's `system` describes something no Part covers, add a Part file for it.
- A Variant starts at the Step named by `diverges_at` and lists its own Steps through to its own `outcome`. It never rejoins the main path.
- The main path and every Variant each have exactly one `qa`: `setup` starts from the preconditions, then each step pairs what the Builder does (`do`) with what they should observe (`expect`).
- A precondition is a plain sentence, or `flow_to_write` with `so_that` when it waits for a Flow nobody has written yet.

## The words

Write for the Builder: plain sentences about what happens, naming things as they appear on screen. File names, function names and other code identifiers belong in an Anchor's `at`, nowhere else.
