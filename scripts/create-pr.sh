#!/bin/bash
# Automated PR creation script
# Usage: bash scripts/create-pr.sh "PR Title" "base-branch" "head-branch"

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arguments
PR_TITLE="${1}"
BASE_BRANCH="${2:-main}"
HEAD_BRANCH="${3:-$(git branch --show-current)}"

# Validation
if [ -z "$PR_TITLE" ]; then
  echo -e "${RED}❌ Error: PR title required${NC}"
  echo "Usage: bash scripts/create-pr.sh \"PR Title\" [base-branch] [head-branch]"
  exit 1
fi

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
  echo -e "${YELLOW}⚠️  GitHub CLI not found${NC}"
  echo "Install from: https://cli.github.com/"
  echo ""
  echo -e "${GREEN}Alternative: Open this URL to create PR manually:${NC}"
  REPO=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
  echo "https://github.com/$REPO/compare/$BASE_BRANCH...$HEAD_BRANCH"
  exit 1
fi

echo -e "${GREEN}🚀 Creating PR...${NC}"
echo "  Title: $PR_TITLE"
echo "  Base: $BASE_BRANCH"
echo "  Head: $HEAD_BRANCH"
echo ""

# Generate PR body
PR_BODY=$(cat << 'TEMPLATE'
## Summary

Brief description of what this PR does.

## Changes

- Change 1
- Change 2
- Change 3

## Testing

- [ ] Build passes (`npm run build`)
- [ ] Tests pass (if applicable)
- [ ] Security audit clean (`npm audit`)
- [ ] Manual testing complete

## Checklist

- [ ] Code follows project conventions
- [ ] Documentation updated (if needed)
- [ ] No secrets or credentials in code
- [ ] Breaking changes documented (if any)

## Related Issues

Closes #
TEMPLATE
)

# Create PR
gh pr create \
  --base "$BASE_BRANCH" \
  --head "$HEAD_BRANCH" \
  --title "$PR_TITLE" \
  --body "$PR_BODY" \
  --draft

echo ""
echo -e "${GREEN}✅ Draft PR created successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. Review the PR description and update as needed"
echo "  2. Mark as ready for review when complete"
echo "  3. Request reviewers if needed"
