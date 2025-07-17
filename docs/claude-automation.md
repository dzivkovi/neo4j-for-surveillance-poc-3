# Claude PR Automation Setup Guide

A comprehensive guide to setting up Claude AI for automated PR reviews with GitHub Projects integration.

## Overview

This guide documents the complete setup process for Claude GitHub Actions, expanding on [Anthropic's official documentation](https://docs.anthropic.com/en/docs/claude-code/github-actions#manual-setup) with real-world implementation details, GitHub Projects integration, and workflow automation best practices.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [GitHub Projects Integration](#github-projects-integration)
4. [Workflow Options](#workflow-options)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

## Prerequisites

- GitHub repository with admin access
- Anthropic API key (from [console.anthropic.com](https://console.anthropic.com))
- Claude Code installed locally
- GitHub Projects board (optional but recommended)

## Initial Setup

### Step 1: Install Claude GitHub App

1. In Claude Code, run the command:
   ```
   /install-github-app
   ```

2. This will automatically:
   - Create a new branch: `add-claude-github-actions-[timestamp]`
   - Add two workflow files:
     - `.github/workflows/claude.yml` (PR Assistant)
     - `.github/workflows/claude-code-review.yml` (Code Review)
   - Set up `ANTHROPIC_API_KEY` as a repository secret
   - Switch you to the new branch

### Step 2: Verify API Key Setup

The API key should already be configured, but you can verify:

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Confirm `ANTHROPIC_API_KEY` is listed

## GitHub Projects Integration

### Why Projects Integration?

Integrating with GitHub Projects provides:
- Automatic PR tracking on your Kanban board
- Visual workflow management
- Team visibility into PR status
- Automated status transitions

### Configuration Steps

#### 1. Enable Workflow Automations

Navigate to your project's Workflows settings:

1. Go to your GitHub Project board
2. Click ⚙️ → Workflows
3. Enable these workflows:

   **For PR Status Tracking:**
   - ✅ **Item closed** → Set Status: Done
   - ✅ **Pull request merged** → Set Status: Done

#### 2. Configure Auto-Add

This automatically adds new PRs to your board:

1. In Workflows, find "Auto-add to project"
2. Toggle it ON
3. Configure:
   - Repository: Select your repo
   - Filter: `is:pr is:open`
   - Action: Add the item to the project

**Important**: Remove any label filters (like `label:bug`) unless you want to restrict which PRs are added.

### Filter Options Explained

| Filter | Purpose | Use When |
|--------|---------|----------|
| `is:pr is:open` | All open PRs | You want to track every PR |
| `is:issue,pr is:open` | All open items | You track both issues and PRs |
| `is:pr is:open label:bug` | Only bug PRs | You have specific workflow for bugs |
| `is:pr is:open author:@me` | Your PRs only | Personal tracking board |

We chose `is:pr is:open` for comprehensive PR tracking.

## Workflow Options

### Option 1: Direct Merge (Infrastructure)
Best for configuration changes like this:
```bash
git checkout main
git merge add-claude-github-actions-[timestamp]
git push origin main
```

### Option 2: PR Review (Standard)
Best for feature development:
```bash
gh pr create --title "feat: Add Claude AI GitHub Actions" \
  --body "Automated code review setup"
```

We chose Option 2 to:
- Test the Claude review process
- Follow standard development workflow
- Create documentation for the team
- See Claude in action before team-wide deployment

## Testing & Verification

### 1. Create Test PR
```bash
gh pr create --title "feat: Add Claude AI GitHub Actions for automated code review" \
  --body "See PR description for details"
```

### 2. Verify Project Board
- Check if PR appears in your project's "Todo" column
- Should happen within seconds of PR creation

### 3. Watch Claude Review
- Claude will comment within ~30 seconds
- Look for constructive feedback and suggestions

### 4. Test Merge Automation
- When PR is merged, it should move to "Done" automatically

## What Claude Does

### On Every PR:
1. **Code Review** - Analyzes changes for:
   - Best practices
   - Security issues
   - Performance improvements
   - Code clarity

2. **Suggestions** - Provides:
   - Specific improvement recommendations
   - Alternative implementations
   - Documentation suggestions

3. **Q&A Support** - Responds to:
   - `@claude` commands in PR comments
   - Questions about the code
   - Clarification requests

### What Claude Doesn't Do:
- ❌ Modify code directly
- ❌ Block PR merging
- ❌ Make automated commits
- ❌ Access external services

## Troubleshooting

### Claude Not Responding to Commands
- **Issue**: Claude not responding to `@claude` commands
- **Solutions**:
  1. Verify the GitHub App is installed correctly
  2. Check that workflows are enabled
  3. Ensure ANTHROPIC_API_KEY is set in repository secrets
  4. Confirm the comment contains `@claude` (not `/claude`)

### PR Not Appearing in Project Board
1. Check Auto-add is enabled
2. Verify filter matches your PR
3. Ensure repository is connected to project

### Claude Not Reviewing Automatically
1. Verify ANTHROPIC_API_KEY is set
2. Check workflow files are on main branch
3. Look at Actions tab for errors

### Workflows Not Moving Items
1. Confirm "Pull request merged" is enabled
2. Check it's set to Status: Done
3. Verify item type matches filter

## Best Practices

### 1. Gradual Rollout
- Test with non-critical PRs first
- Gather team feedback
- Adjust Claude's role based on needs

### 2. Clear PR Descriptions
- Claude reviews better with context
- Include "why" not just "what"
- Reference related issues

### 3. Interact with Claude
- Ask clarifying questions with `@claude`
- Request specific reviews: `@claude please review this for security issues`
- Use Claude as a learning tool: `@claude explain why this approach is better`

### 4. Monitor Usage
- Track API usage in Anthropic Console
- Adjust frequency if needed
- Consider PR size limits

## Example PR Description

```markdown
## Summary
This PR adds Claude AI automation to improve our development workflow by providing:
- 🤖 Automated code review on all PRs
- 💡 Intelligent suggestions for improvements  
- 🔍 Security and best practice checks

## Benefits
- **Faster Reviews**: Instant feedback, 24/7
- **Consistent Quality**: Same high standards on every PR
- **Learning Tool**: Junior devs learn from Claude's suggestions

## Testing
1. Create a test PR after merging
2. Watch Claude review it
3. Try asking Claude questions with `@claude`
```

## Example Claude Commands

In PR comments, you can use:
- `@claude implement this feature based on the issue description`
- `@claude how should I implement user authentication for this endpoint?`
- `@claude fix the TypeError in the user dashboard component`
- `@claude please review this code for security vulnerabilities`
- `@claude explain why this solution is better than alternatives`

## Additional Resources

- [Official Anthropic Documentation](https://docs.anthropic.com/en/docs/claude-code/github-actions)
- [Manual Setup Guide](https://docs.anthropic.com/en/docs/claude-code/github-actions#manual-setup)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Contributing

Found an issue or have an improvement? Please submit a PR! Claude will review it 😊

---

*Last updated: June 18, 2025*
*Based on real implementation experience with Claude Code v1.0*