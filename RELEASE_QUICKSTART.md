# AutoMagik Spark - Quick Release Guide

This is a quick reference for releasing AutoMagik Spark. For detailed documentation, see [VERSION_BUMP.md](VERSION_BUMP.md).

## 🚀 Quick Release Commands

### Release Candidate (RC) - Recommended for testing

```bash
# Create first RC (0.3.7 → 0.3.8rc1)
make release-rc

# Deploy RC to PyPI and GitHub
make deploy-release

# Test the RC
pip install automagik-spark==0.3.8rc1
automagik-spark --version

# Need another RC? (0.3.8rc1 → 0.3.8rc2)
make bump-rc    # Choose [n]ext
make commit-version
make tag-current
make deploy-release

# Ready for stable? (0.3.8rc2 → 0.3.8)
make bump-rc    # Choose [s]table
make commit-version
make tag-current
make deploy-release
```

### Patch Release (0.3.7 → 0.3.8)

```bash
make release-patch
make deploy-release
```

### Minor Release (0.3.7 → 0.4.0)

```bash
make release-minor
make deploy-release
```

### Major Release (0.3.7 → 1.0.0)

```bash
make release-major
make deploy-release
```

### Dev/Pre-release (for testing on Test PyPI)

```bash
make release-dev
make deploy-dev
```

## 📋 What Each Command Does

### `make release-rc`
1. Prompts for version bump strategy
2. Updates `pyproject.toml`
3. Commits with co-author credit
4. Creates git tag
5. Runs quality checks and tests
6. Builds package

### `make deploy-release`
1. Pushes tags to GitHub
2. Publishes to PyPI
3. Creates GitHub release (auto-generated via workflow)

## 🔖 RC Release Workflow Example

```bash
# Current version: 0.3.7

# Step 1: Create first RC
make release-rc
# → Bumps to 0.3.8rc1
# → Commits, tags, tests, builds

# Step 2: Deploy RC
make deploy-release
# → Pushes tag v0.3.8rc1
# → Publishes to PyPI
# → GitHub workflow creates release

# Step 3: Test RC
pip install automagik-spark==0.3.8rc1
# ... test your features ...

# Step 4a: Need fixes? Create RC2
make bump-rc
# Choose: [n]ext RC
# → Bumps to 0.3.8rc2

make commit-version
make tag-current
make deploy-release

# Step 4b: Ready for stable? Finalize
make bump-rc
# Choose: [s]table
# → Bumps to 0.3.8

make commit-version
make tag-current
make deploy-release
```

## 🎯 Interactive `bump-rc` Options

When you run `make bump-rc` on an RC version, you'll be prompted:

```
Current version is RC: 0.3.8rc1
Action: [n]ext RC, [s]table, or [c]ancel? [n/s/c]:
```

- **[n]** - Create next RC (rc1 → rc2 → rc3...)
- **[s]** - Finalize to stable version (rc1 → 0.3.8)
- **[c]** - Cancel operation

## ✅ Pre-release Checklist

Before running `make deploy-release`:

- [ ] All tests passing (`make test`)
- [ ] Code quality checks passed (`make quality`)
- [ ] Changes committed and pushed
- [ ] CHANGELOG.md updated (optional)
- [ ] Documentation updated if needed

## 🔗 Useful Commands

```bash
# Check current version
grep '^version' pyproject.toml

# View all available make commands
make help

# Run quality checks
make quality

# Run tests
make test

# Build locally (without publishing)
make build

# Check what will be published
make check-dist
```

## 📚 Documentation

- **Detailed Guide**: [VERSION_BUMP.md](VERSION_BUMP.md)
- **Release Notes Template**: [.github/RELEASE_NOTES_TEMPLATE.md](.github/RELEASE_NOTES_TEMPLATE.md)
- **PyPI Publishing Workflow**: [.github/workflows/publish-pypi.yml](.github/workflows/publish-pypi.yml)
- **Auto-Release Workflow**: [.github/workflows/auto-release.yml](.github/workflows/auto-release.yml)

## 🆘 Troubleshooting

### "Version mismatch" error
- Ensure `pyproject.toml` version matches your git tag (without 'v' prefix)

### PyPI upload fails
- Check if version already exists on PyPI
- Verify PyPI Trusted Publishing is configured

### GitHub release not created
- Check that tag was pushed: `git push origin --tags`
- Verify ANTHROPIC_API_KEY secret (optional, for AI-generated notes)

### Need to delete a tag
```bash
git tag -d v0.3.8rc1              # Delete local
git push origin :refs/tags/v0.3.8rc1  # Delete remote
```

---

**Quick tip**: Always test with RC releases before stable releases! 🔖

**Co-Authored-By**: Automagik Genie 🧞 <genie@namastex.ai>
