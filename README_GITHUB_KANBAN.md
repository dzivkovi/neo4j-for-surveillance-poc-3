# GitHub Projects Kanban Setup for Development Teams

A practical guide to setting up lean Kanban workflow with GitHub Projects, based on real implementation experience.

## Overview

This guide shows how to set up a minimal, effective Kanban board using GitHub Projects that integrates seamlessly with your development workflow. Perfect for teams wanting visual project management without complexity.

## Table of Contents

1. [Why GitHub Projects + Kanban](#why-github-projects--kanban)
2. [Quick Setup (2 Minutes)](#quick-setup-2-minutes)
3. [Column Configuration](#column-configuration)
4. [Automation Setup](#automation-setup)
5. [Security & Permissions](#security--permissions)
6. [Common Pitfalls](#common-pitfalls)
7. [Best Practices](#best-practices)

## Why GitHub Projects + Kanban

### Repository vs Projects - They Work Together

- **Repository**: Code, issues, PRs (unchanged)
- **Project**: Visual board view of your workflow
- **Result**: Same issues, better organization

### What You Get

- Visual workflow tracking (Backlog → Todo → In Progress → Review → Done)
- Automated PR/issue lifecycle management
- Team visibility into work status
- Integration with existing GitHub workflow

### What You DON'T Get (And Don't Need)

- Complex project management overhead
- Separate tools to maintain
- Learning curve for team members

## Quick Setup (2 Minutes)

### Step 1: Create Project

1. Go to your repository
2. Click **"Projects"** tab
3. Click **"Create a project"**
4. Choose **"Kanban"** template (not "Start from scratch")
5. Name it: `[Repository Name] - Kanban`

### Step 2: Link Repository

**Important**: The "Link repository" option isn't obvious in GitHub's UI.

**Method 1 - Automatic Linking:**

1. In your project, click **"+ Add item"**
2. Type `#` to see repository issues
3. Adding any issue automatically links the repository

**Method 2 - Manual Linking:**

1. Create an issue in your repository first
2. Return to project and add that issue
3. Repository is now linked

### Step 3: Customize Columns

Default Kanban template gives you too many columns. Simplify to:

- **Backlog** (rename "Todo")
- **In Progress**
- **Review** (add this)
- **Done**

**Delete unnecessary columns:**

1. Click column "..." menu
2. Select "Delete column"
3. Move any items to appropriate columns first

## Column Configuration

### Recommended Minimal Setup

| Column | Purpose | Items Move Here |
|--------|---------|-----------------|
| **Backlog** | Ideas, future work | New issues created |
| **In Progress** | Active development | When you start coding |
| **Review** | Awaiting code review | When PR is created |
| **Done** | Completed work | When PR is merged |

### Why This Works

- **4 columns max** - Simple visual scan
- **Clear ownership** - Know who does what
- **Logical flow** - Matches development process

## Automation Setup

### What to Automate

```code
✅ New issues → Backlog
✅ Merged PRs → Done
❌ Everything else (keep manual control)
```

### Configuration Steps

**1. Auto-Add New Items:**

- Project Settings → Workflows → "Auto-add to project"
- Filter: `is:issue,pr is:open`
- Action: Add to Backlog

**2. Auto-Complete:**

- Project Settings → Workflows → "Pull request merged"
- Action: Move to Done

**3. What NOT to Automate:**

- Backlog → In Progress (you decide priority)
- In Progress → Review (you decide when ready)
- Review → In Progress (manual feedback loop)

### Why Minimal Automation

- **You control workflow** - Automation serves you, not vice versa
- **Context matters** - Humans make better priority decisions
- **Debugging is easier** - Less moving parts

## Security & Permissions

### Common Scenario: Public Repository, Controlled Project

**Your Situation:**

- Repository is public (code visible to world)
- Want project visible but not editable by strangers

**Solution:**

1. **Project Visibility**: Set to Public
   - Settings → Visibility → Public
2. **Access Control**: Don't add external collaborators
   - Only invited users can edit
   - Public users have read-only access
3. **Result**: Transparency without chaos

### Permission Levels

- **Read**: Can view project (public users)
- **Write**: Can move items, edit (invited collaborators)
- **Admin**: Can change settings (repository owners)

## Common Pitfalls

### 1. "My Project Isn't Connected to My Repository"

**Symptoms:**

- Issues don't appear in project
- Can't reference repository items

**Fix:**

- Add any issue using `#[issue-number]`
- Repository automatically links

### 2. "Items Stay in Wrong Columns"

**Reality Check:** This is normal! GitHub only automates:

- Creation (→ Backlog)
- Completion (→ Done)

**Manual Steps (Expected):**

- Backlog → In Progress (when you start)
- In Progress → Review (when you create PR)

### 3. "Too Many Columns"

**Problem:** Kanban template creates excessive columns
**Solution:** Delete extras, keep 4 maximum

### 4. "Items Have 'No Status'"

**Cause:** Auto-add didn't set default column
**Fix:**

- Set default status in project settings
- Or manually drag items to Backlog

## Best Practices

### 1. Column Limits

- **Backlog**: No limit (idea parking)
- **In Progress**: 3-5 items max (prevent context switching)
- **Review**: 2-3 items max (encourage fast reviews)
- **Done**: No limit (celebration zone)

- **Weekly**: Clean up Backlog, close stale items
- **After each PR**: Verify automation moved item to Done
- **Monthly**: Review column limits and workflow

### 3. Team Adoption

- **Start small**: Use with just issues first
- **Add PRs gradually**: Once team is comfortable
- **Don't force**: Some team members prefer lists

### 4. Integration with Claude

If using Claude Code automation:

- PRs auto-reviewed by Claude
- Manual workflow progression still required
- Use `@claude` commands for complex questions

## Workflow Example

```code
1. Create issue → Auto-appears in Backlog
2. Ready to work → Drag to In Progress  
3. Start coding → (stay in In Progress)
4. Create PR → Drag to Review
5. Code review happens → (stay in Review)
6. Merge PR → Auto-moves to Done ✅
```

## Troubleshooting

### Project Not Showing Repository Issues

1. Check filter: Should be `is:issue,pr is:open`
2. Create test issue in repository
3. Try adding with `#[issue-number]`

### Automation Not Working

1. Verify workflows are enabled in project settings
2. Check filter syntax (common error: extra labels)
3. Test with simple issue creation

### Performance Issues

- Limit to 100 items per view
- Archive completed items monthly
- Use labels for filtering, not separate projects

## Useful GitHub CLI Commands

```bash
# Ensure GitHub token has project scope
gh auth refresh -s project

# Get full user info
gh api user

# Gets current authenticated user
gh project list --owner $(gh api user | jq -r '.login')

# List all Kanban column statuses, assuming projectid=1 and userid=dzivkovi
gh project field-list 1 --owner dzivkovi --format json | \
   jq -r '.fields[] | select(.name=="Status") | .options[].name'
# Backlog
# In progress
# In review
# Done

# Create a purple 'epic' label (skip if it already exists)
gh label create epic --description "Large, cross-cutting work item" --color B60205 \
  --repo dzivkovi/neo4j-for-surveillance-poc-3

# Create a new GitHub Issue
gh issue create \
  --repo dzivkovi/neo4j-for-surveillance-poc-3 \
  --title "Data reload & Lucene indexes (MVP)" \
  --body-file data/issue_body.md \
  --label "enhancement,epic"
# The command prints the new issue number
# e.g. https://github.com/dzivkovi/neo4j-for-surveillance-poc-3/issues/7.

# Add the issue to the project board
gh project item-add 1 --owner dzivkovi \
  --url https://github.com/dzivkovi/neo4j-for-surveillance-poc-3/issues/7

# Close the obsolete Issue #6
# - List all labels in the repository
gh label list
# - Add the 'invalid' label, or 'wontfix' or 'duplicate'
gh issue edit 6 --add-label invalid --repo dzivkovi/neo4j-for-surveillance-poc-3
# - Close the issue with a comment
gh issue close 6 \
  --comment "Closing: generated from incomplete docs; superseded by #7." \
  --repo dzivkovi/neo4j-for-surveillance-poc-3

# Add a comment to an existing issue
gh issue comment 7 --body "Design Complete

After detailed analysis, complete implementation specification is ready:

**Design Document**: \`analysis/7/DESIGN.md\`

Validated against current Neo4j schema via MCP. Maps to 25+ of 77 evaluation questions.
Ready for implementation (manual or automated via \`/work 7\`).

Key insight: Reuse existing \`durationinseconds\` property, change location index from RANGE to POINT type."
```

## Additional Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Kanban Methodology Basics](https://www.atlassian.com/agile/kanban)
- [GitHub Projects API](https://docs.github.com/en/rest/projects)
- [GitHub Command Line](https://cli.github.com/)

---

*This guide is based on real implementation experience with GitHub Projects for software development teams. Last updated: June 22, 2025*
