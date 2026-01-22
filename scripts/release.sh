#!/bin/bash
# Automated release script
# Usage: bash scripts/release.sh [patch|minor|major|<version>]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

VERSION_TYPE="${1:-patch}"

echo -e "${BLUE}🚀 Starting release process...${NC}"
echo ""

# Ensure we're on main and up to date
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo -e "${YELLOW}⚠️  Switching to main branch...${NC}"
  git checkout main
fi

echo -e "${BLUE}📥 Pulling latest changes...${NC}"
git pull origin main

# Ensure working directory is clean
if ! git diff-index --quiet HEAD --; then
  echo -e "${RED}❌ Working directory not clean. Commit or stash changes first.${NC}"
  exit 1
fi

# Run security audit
echo -e "${BLUE}🔒 Running security audit...${NC}"
if ! npm audit --audit-level=high; then
  echo -e "${RED}❌ Security vulnerabilities found. Fix before releasing.${NC}"
  exit 1
fi

# Run build
echo -e "${BLUE}🔨 Building project...${NC}"
if ! npm run build; then
  echo -e "${RED}❌ Build failed. Fix errors before releasing.${NC}"
  exit 1
fi

# Run tests if available
if [ -f "pytest.ini" ] || [ -d "tests" ]; then
  echo -e "${BLUE}🧪 Running tests...${NC}"
  if ! pytest tests/; then
    echo -e "${RED}❌ Tests failed. Fix before releasing.${NC}"
    exit 1
  fi
fi

# Get current version
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo -e "${BLUE}📌 Current version: ${CURRENT_VERSION}${NC}"

# Calculate new version
if [[ "$VERSION_TYPE" =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
  NEW_VERSION="$VERSION_TYPE"
else
  # Use npm version to calculate
  NEW_VERSION=$(npm version "$VERSION_TYPE" --no-git-tag-version | sed 's/v//')
fi

echo -e "${GREEN}📌 New version: ${NEW_VERSION}${NC}"
echo ""

# Confirm
read -p "Continue with release v${NEW_VERSION}? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo -e "${YELLOW}Release cancelled.${NC}"
  git checkout package.json package-lock.json 2>/dev/null || true
  exit 0
fi

# Update CHANGELOG
echo -e "${BLUE}📝 Updating CHANGELOG...${NC}"
DATE=$(date +%Y-%m-%d)

if [ -f "CHANGELOG.md" ]; then
  # Replace [Unreleased] with version and date
  sed -i "s/## \[Unreleased\]/## [${NEW_VERSION}] - ${DATE}\n\n## [Unreleased]/" CHANGELOG.md
else
  echo -e "${YELLOW}⚠️  CHANGELOG.md not found${NC}"
fi

# Commit version bump
echo -e "${BLUE}💾 Committing version bump...${NC}"
git add package.json package-lock.json CHANGELOG.md 2>/dev/null || true
git commit -m "chore(release): ${NEW_VERSION}"

# Create git tag
echo -e "${BLUE}🏷️  Creating tag v${NEW_VERSION}...${NC}"
git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}"

# Push
echo -e "${BLUE}📤 Pushing to remote...${NC}"
git push origin main
git push origin "v${NEW_VERSION}"

echo ""
echo -e "${GREEN}✅ Release v${NEW_VERSION} complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. GitHub Actions will automatically:"
echo "     • Build and publish Docker image"
echo "     • Create GitHub Release"
echo "     • Publish to NPM (if configured)"
echo ""
echo "  2. Monitor workflow at:"
echo "     https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
