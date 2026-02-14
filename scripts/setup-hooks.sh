#!/bin/bash
# Setup Git hooks for Teamwork-MCP
# Run this once after cloning: bash scripts/setup-hooks.sh

set -e

echo "🔧 Setting up Git hooks..."

# Install Husky if not already installed
if ! npm list husky &>/dev/null; then
  echo "📦 Installing Husky..."
  npm install --save-dev husky
fi

# Initialize Husky
npx husky install

# Create pre-commit hook
cat > .husky/pre-commit << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🔍 Running pre-commit checks..."

# TypeScript type check
echo "📝 TypeScript check..."
npm run build || {
  echo "❌ TypeScript errors found. Fix before committing."
  exit 1
}

# Secret detection
echo "🔒 Checking for secrets..."
if git diff --cached --name-only | xargs grep -iE '(password|secret|key|token).*=.*["'\'']' 2>/dev/null | grep -v 'process.env' | grep -v '.example'; then
  echo "❌ Potential secrets found in staged files!"
  exit 1
fi

# Check .gitignore coverage
echo "🔍 Checking .gitignore..."
if git diff --cached --name-only | grep -E '\.env$|\.pem$|\.key$|\.p12$|\.pfx$|secrets\.json$'; then
  echo "❌ Attempting to commit files that should be in .gitignore!"
  exit 1
fi

echo "✅ Pre-commit checks passed!"
EOF

chmod +x .husky/pre-commit

# Create commit-msg hook for conventional commits
cat > .husky/commit-msg << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "📝 Validating commit message..."

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Conventional commit pattern
PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|security)(\(.+\))?: .{1,}"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
  echo "❌ Invalid commit message format!"
  echo ""
  echo "Commit message must follow conventional commits:"
  echo "  type(scope): description"
  echo ""
  echo "Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, security"
  echo ""
  echo "Examples:"
  echo "  feat(api): add new endpoint for user data"
  echo "  fix(auth): resolve token expiration bug"
  echo "  docs: update README with setup instructions"
  exit 1
fi

echo "✅ Commit message valid!"
EOF

chmod +x .husky/commit-msg

# Create pre-push hook
cat > .husky/pre-push << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🚀 Running pre-push checks..."

# Run tests if they exist
if [ -f "pytest.ini" ] || [ -d "tests" ]; then
  echo "🧪 Running tests..."
  pytest tests/ || {
    echo "❌ Tests failed. Fix before pushing."
    exit 1
  }
fi

# Security audit
echo "🔒 Running security audit..."
npm audit --audit-level=high || {
  echo "⚠️  Security vulnerabilities found!"
  echo "Run 'npm audit fix' to resolve"
  exit 1
}

echo "✅ Pre-push checks passed!"
EOF

chmod +x .husky/pre-push

# Update package.json to run husky install on npm install
if ! grep -q '"prepare": "husky install"' package.json; then
  echo "📝 Adding prepare script to package.json..."
  npm pkg set scripts.prepare="husky install"
fi

echo ""
echo "✅ Git hooks setup complete!"
echo ""
echo "Hooks installed:"
echo "  • pre-commit: Type check, secret detection"
echo "  • commit-msg: Conventional commits validation"
echo "  • pre-push: Tests and security audit"
echo ""
echo "To bypass hooks (use sparingly): git commit --no-verify"
