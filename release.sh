#!/bin/bash
# Quick release script for django-user-starter
# Usage: ./release.sh [patch|minor|major|dev]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TYPE=${1:-patch}
CURRENT_BRANCH=$(git branch --show-current)

echo -e "${YELLOW}🚀 Django User Starter Release Script${NC}"
echo "Current branch: $CURRENT_BRANCH"
echo "Release type: $TYPE"

# Function to create semantic commit
create_commit() {
    local type=$1
    local version=$2
    
    case $type in
        "major")
            prefix="feat!:"
            ;;
        "minor") 
            prefix="feat:"
            ;;
        "patch")
            prefix="fix:"
            ;;
        "dev")
            prefix="chore:"
            ;;
    esac
    
    echo "$prefix prepare release v$version"
}

# Get current version
CURRENT_VERSION=$(python -c "from django_user_starter import __version__; print(__version__)")
echo "Current version: $CURRENT_VERSION"

# Calculate next version
IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"

case $TYPE in
    "major")
        NEW_VERSION="$((major + 1)).0.0"
        ;;
    "minor")
        NEW_VERSION="$major.$((minor + 1)).0"
        ;;
    "patch")
        NEW_VERSION="$major.$minor.$((patch + 1))"
        ;;
    "dev")
        NEW_VERSION="$CURRENT_VERSION"
        ;;
esac

echo "Target version: $NEW_VERSION"

# Confirm release
if [ "$TYPE" != "dev" ]; then
    read -p "Do you want to release v$NEW_VERSION? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Release cancelled${NC}"
        exit 1
    fi
fi

# Check if we're on the right branch
if [ "$TYPE" = "dev" ]; then
    TARGET_BRANCH="dev"
else
    TARGET_BRANCH="main"
fi

echo -e "${YELLOW}📋 Preparing release...${NC}"

# Run tests first
echo "Running tests..."
make test PYTHON=python || {
    echo -e "${RED}❌ Tests failed! Fix tests before releasing.${NC}"
    exit 1
}

# Run quality checks
echo "Running quality checks..."
make lint PYTHON=python || {
    echo -e "${RED}❌ Quality checks failed! Fix linting issues before releasing.${NC}"
    exit 1
}

# Switch to target branch if needed
if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
    echo "Switching to $TARGET_BRANCH branch..."
    git checkout "$TARGET_BRANCH"
    git pull origin "$TARGET_BRANCH"
    
    # Merge current branch if it's not main/dev
    if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "dev" ]; then
        echo "Merging $CURRENT_BRANCH into $TARGET_BRANCH..."
        git merge "$CURRENT_BRANCH" --no-ff -m "Merge branch '$CURRENT_BRANCH' into $TARGET_BRANCH"
    fi
fi

# Create semantic commit
COMMIT_MSG=$(create_commit "$TYPE" "$NEW_VERSION")
echo "Creating commit: $COMMIT_MSG"

# Stage all changes
git add .
git commit -m "$COMMIT_MSG" || echo "No changes to commit"

# Push to trigger CI/CD
echo "Pushing to origin/$TARGET_BRANCH..."
git push origin "$TARGET_BRANCH"

echo -e "${GREEN}✅ Release process initiated!${NC}"
echo -e "${GREEN}🔗 Check GitHub Actions: https://github.com/yaninsanity/django-user-starter/actions${NC}"

if [ "$TYPE" = "dev" ]; then
    echo -e "${GREEN}📦 Dev version will be published to TestPyPI${NC}"
else
    echo -e "${GREEN}🎉 Release v$NEW_VERSION will be published to PyPI${NC}"
fi
