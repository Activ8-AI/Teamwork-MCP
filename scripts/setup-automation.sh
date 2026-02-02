#!/bin/bash
# Master automation setup script for Teamwork-MCP
# Run this once to set up all automation: bash scripts/setup-automation.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║   Teamwork-MCP Automation Setup                          ║
║   Configuring workflows, hooks, and CI/CD                ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

MISSING=()

if ! command -v node &> /dev/null; then MISSING+=("Node.js"); fi
if ! command -v npm &> /dev/null; then MISSING+=("npm"); fi
if ! command -v git &> /dev/null; then MISSING+=("git"); fi

if [ ${#MISSING[@]} -gt 0 ]; then
  echo -e "${RED}❌ Missing required tools: ${MISSING[*]}${NC}"
  exit 1
fi

echo -e "${GREEN}✅ All prerequisites installed${NC}"
echo ""

# Setup Git hooks
echo -e "${BLUE}🪝 Setting up Git hooks...${NC}"
bash scripts/setup-hooks.sh

# Install pre-commit (optional Python-based hooks)
echo ""
echo -e "${YELLOW}📦 Optional: Install pre-commit framework? (Python-based) [y/N]${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    pip install pre-commit || pip3 install pre-commit
    pre-commit install
    echo -e "${GREEN}✅ Pre-commit hooks installed${NC}"
  else
    echo -e "${YELLOW}⚠️  Python/pip not found. Skipping pre-commit framework.${NC}"
  fi
fi

# Make scripts executable
echo ""
echo -e "${BLUE}🔧 Making scripts executable...${NC}"
chmod +x scripts/*.sh
echo -e "${GREEN}✅ Scripts are executable${NC}"

# Configure Git settings
echo ""
echo -e "${BLUE}⚙️  Configuring Git settings...${NC}"

# Set pull strategy
git config pull.rebase false 2>/dev/null || true

# Enable automatic branch cleanup on merge
git config fetch.prune true

# Set default branch to main
git config init.defaultBranch main 2>/dev/null || true

echo -e "${GREEN}✅ Git configured${NC}"

# GitHub CLI setup
echo ""
if command -v gh &> /dev/null; then
  echo -e "${GREEN}✅ GitHub CLI installed${NC}"

  if gh auth status &> /dev/null; then
    echo -e "${GREEN}✅ GitHub CLI authenticated${NC}"
  else
    echo -e "${YELLOW}⚠️  GitHub CLI not authenticated${NC}"
    echo "Run: gh auth login"
  fi
else
  echo -e "${YELLOW}⚠️  GitHub CLI not installed${NC}"
  echo "Install from: https://cli.github.com/"
  echo "Required for automated PR creation and management"
fi

# Verify GitHub Actions
echo ""
echo -e "${BLUE}🔍 Checking GitHub Actions workflows...${NC}"
WORKFLOW_COUNT=$(find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l)
echo -e "${GREEN}✅ Found $WORKFLOW_COUNT workflow files${NC}"

# List workflows
echo ""
echo -e "${BLUE}📋 Available workflows:${NC}"
find .github/workflows -type f \( -name "*.yml" -o -name "*.yaml" \) -exec basename {} \; | sort

# Create secrets baseline for detect-secrets
if [ -f ".pre-commit-config.yaml" ]; then
  echo ""
  echo -e "${BLUE}🔒 Creating secrets baseline...${NC}"
  if command -v detect-secrets &> /dev/null; then
    detect-secrets scan > .secrets.baseline
    echo -e "${GREEN}✅ Secrets baseline created${NC}"
  else
    echo -e "${YELLOW}⚠️  detect-secrets not installed (optional)${NC}"
  fi
fi

# Summary
echo ""
echo -e "${GREEN}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║   ✅ Automation Setup Complete!                          ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}📊 Setup Summary:${NC}"
echo ""
echo "Git Hooks:"
echo "  ✅ pre-commit (TypeScript check, secret detection)"
echo "  ✅ commit-msg (conventional commits)"
echo "  ✅ pre-push (tests, security audit)"
echo ""
echo "GitHub Actions:"
echo "  ✅ CI/CD pipeline"
echo "  ✅ Security scanning"
echo "  ✅ Branch cleanup"
echo "  ✅ PR validation"
echo "  ✅ Auto-close superseded PRs"
echo "  ✅ Changelog updates"
echo "  ✅ Release automation"
echo ""
echo "Dependabot:"
echo "  ✅ Weekly dependency updates"
echo "  ✅ Security alerts"
echo "  ✅ Grouped updates"
echo ""
echo -e "${YELLOW}📚 Next Steps:${NC}"
echo ""
echo "1. Review automation documentation:"
echo "   docs/automation.md"
echo ""
echo "2. Configure repository settings:"
echo "   • Enable GitHub Secret Scanning"
echo "   • Enable Dependabot alerts"
echo "   • Set up branch protection rules"
echo ""
echo "3. Test the setup:"
echo "   git commit -m 'test: verify automation'"
echo ""
echo "4. For PR automation:"
echo "   bash scripts/create-pr.sh 'Your PR title'"
echo ""
echo "5. For releases:"
echo "   bash scripts/release.sh patch"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
