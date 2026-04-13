# Brainstorm Phase Design

## Goal

Add a brainstorming phase to SKILL.md that helps users clarify **what to draw** before entering style configuration. The skill collects context, reads data files, proposes a structured plan, and gets user confirmation before proceeding.

## Current Flow

```
User request → HARD GATE (6 config questions) → Generate diagram → Builder functions
```

## New Flow

```
User request → Step 0: Brainstorm → HARD GATE (6 config questions) → Generate diagram → Builder functions
```

## Step 0: Brainstorm Phase

### Three Questions (asked together)

| # | Question | Purpose | Example |
|---|----------|---------|---------|
| Q1 | What diagram do you want? Describe your scenario and purpose. | Understand domain and intent | "K8s microservice architecture, for onboarding new engineers" |
| Q2 | Any reference files or data? (file paths or "none") | Acquire data sources | `data/metrics.csv`, screenshots, existing `.excalidraw` files |
| Q3 | What key information and relationships should the diagram show? | Define core elements and structure | "Pod → Service → Ingress three layers, plus monitoring sidecar" |

### Rules

- Ask all three questions in a single message.
- If the user's original request already answers some questions, skip those.
- For Q2: if the user provides file paths, read the files before proposing the plan. Supported formats: CSV, JSON, images (PNG/JPG), existing `.excalidraw` files.
- If the user says "none" to Q2, skip data integration.

### AI Proposal

After collecting answers (and reading any provided files), output a structured plan:

```
## Diagram Plan

**Type**: [flowchart / architecture / comparison table / timeline / bar chart / ...]
**Content**: [list main elements]
**Structure**: [hierarchy, groups, relationships]
**Layout**: [top-down / left-right / radial / grid, brief description]
**Data**: [if files were provided, describe how they integrate into the diagram]

Confirm this plan? Or tell me what to adjust.
```

### Transition

Once the user confirms (or adjusts and confirms), proceed to HARD GATE configuration questions (Step 1 in current SKILL.md).

## Changes Required

### SKILL.md

- Rename current "Step 1: Configuration Questions" heading to "Step 1: Configuration Questions" (no change, but renumber context)
- Insert new section "Step 0: Brainstorm" before HARD GATE
- Update HARD GATE text: "You MUST complete Step 0 (Brainstorm) before asking configuration questions."

No code changes required. This is purely a SKILL.md workflow modification.

## Scope

- Single change target: `SKILL.md`
- No new files, no code changes
- The brainstorm logic lives entirely in the SKILL.md prompt instructions
