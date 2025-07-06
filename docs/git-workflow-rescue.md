# Git Workflow Rescue Guide

When you start "small edits" on main branch but realize it deserves a proper ticket for traceability.

## Common Scenario: Work Sprawl Recovery

You're on `main` branch, made several commits or changes, and realize this should be a proper issue/PR for client awareness.

### Step 1: Stash Your Changes
```bash
# Save all current work with descriptive message
git add -A
git stash push -m "Brief description of what you've done"

# Verify stash was created
git stash list
```

### Step 2: Create Design Document
```bash
# Create design document explaining the work
# This goes in analysis/0000/DESIGN.md
```

### Step 3: Create GitHub Issue
```bash
# Use your /issue command or manually create issue
/issue "Brief description matching your stash message"
# This creates issue with number (e.g., #25)
```

### Step 4: Create Work Branch
```bash
# Create branch following convention: type/issue#-description
git checkout -b docs/25-brief-description
# or: feat/25-description, fix/25-description, chore/25-description
```

### Step 5: Apply Stashed Changes
```bash
# Apply your completed work to the new branch
git stash pop

# Verify everything looks correct
git status
```

### Step 6: Commit and Close
```bash
# Commit with proper message
git add -A
git commit -m "docs: implement brief description

- List key changes made
- Note any validation performed
- Reference completion of requirements

Closes #25"

# Push and create PR
git push -u origin docs/25-brief-description
gh pr create --title "docs: Brief description" --body "Implements #25"
```

## Design-Issue-Work Cycle (Preferred)

### Proper Workflow
```bash
# 1. Design Phase
/design "Detailed description of what needs to be done"
# Creates analysis/0000/DESIGN.md

# 2. Issue Phase  
/issue "Brief title for GitHub issue"
# Creates GitHub issue, gets number assignment

# 3. Work Phase
/work [issue-number]
# Creates branch, references design, implements solution
```

### Quick Reference Commands

```bash
# Check current branch
git branch --show-current

# List recent stashes
git stash list

# See what's in a stash without applying
git stash show -p stash@{0}

# Apply specific stash
git stash apply stash@{1}

# Delete a stash after applying
git stash drop stash@{0}

# Create branch from current state
git checkout -b feature/description

# Push new branch to remote
git push -u origin branch-name
```

## Prevention Tips

### Before Starting Work
1. **Ask**: "Does this deserve a ticket?"
2. **If yes**: Use design-issue-work cycle
3. **If unsure**: Start small, use rescue workflow if it grows

### Signs Work Deserves a Ticket
- Multiple files being changed
- Client-visible improvements
- More than 30 minutes of work
- Need for testing/validation
- Documentation updates
- Performance improvements

### When to Stay on Main
- Typo fixes
- Single-line documentation corrections
- Emergency hotfixes (rare)
- Temporary debugging (remember to clean up)

## Emergency Situations

### Accidentally Committed to Main
```bash
# Move last commit to new branch
git branch emergency-fix
git reset --hard HEAD~1
git checkout emergency-fix
# Now create proper issue and PR
```

### Multiple Commits to Clean Up
```bash
# Interactive rebase to squash commits
git rebase -i HEAD~3  # Last 3 commits
# Follow prompts to squash into single commit
```

### Lost in Complex Git State
```bash
# See what happened recently
git reflog

# Nuclear option: start fresh (loses uncommitted work)
git reset --hard origin/main
git clean -fd
```

## Best Practices

1. **Commit frequently** on feature branches
2. **Use descriptive commit messages** 
3. **Keep branches focused** - one issue per branch
4. **Test before pushing** - run tests, check formatting
5. **Reference issues** in commit messages (Closes #123)

## Integration with Project Automation

This project uses automation commands:
- `/design` - Creates analysis/0000/DESIGN.md
- `/issue` - Creates GitHub issue with proper formatting
- `/work` - Creates branch and implements from design

The rescue workflow bridges the gap when you start work without using these commands.

---

*"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."* - Follow this principle for both code and git workflow.