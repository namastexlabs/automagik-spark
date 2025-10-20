# AutoMagik Spark Release Guide

This guide explains how to release new versions of AutoMagik Spark to PyPI and GitHub.

## Table of Contents

- [Version Numbering](#version-numbering)
- [Release Types](#release-types)
- [Release Process](#release-process)
- [Pre-Release Process (RC/Beta)](#pre-release-process-rcbeta)
- [Stable Release Process](#stable-release-process)
- [Troubleshooting](#troubleshooting)

---

## Version Numbering

AutoMagik Spark follows [Semantic Versioning](https://semver.org/) (SemVer):

```
MAJOR.MINOR.PATCH[-PRERELEASE]

Examples:
- 0.3.7        (stable release)
- 0.3.8rc1     (release candidate 1)
- 0.3.8rc2     (release candidate 2)
- 0.4.0b1      (beta 1)
- 1.0.0        (major stable release)
```

### Version Components

- **MAJOR**: Breaking changes or significant new features
- **MINOR**: New features, backwards-compatible
- **PATCH**: Bug fixes and small improvements
- **PRERELEASE**: Optional suffix for testing versions
  - `rc1`, `rc2`, etc. - Release candidates (feature-complete, testing phase)
  - `b1`, `b2`, etc. - Beta versions (feature-complete but may have bugs)
  - `a1`, `a2`, etc. - Alpha versions (early testing, incomplete features)

---

## Release Types

### 1. Release Candidate (RC)

Use for **feature-complete** versions that need testing before stable release.

**When to use:**
- All planned features for the version are implemented
- Code is believed to be stable
- Need community testing before marking as stable

**Example flow:**
```
0.3.7 (stable) → 0.3.8rc1 → 0.3.8rc2 → 0.3.8 (stable)
```

### 2. Beta Release

Use for **feature-complete** versions with known bugs or incomplete polish.

**When to use:**
- Major features are complete but need more testing
- Known issues exist but are being addressed
- Want early adopter feedback

**Example flow:**
```
0.3.7 (stable) → 0.4.0b1 → 0.4.0b2 → 0.4.0rc1 → 0.4.0 (stable)
```

### 3. Stable Release

Use for **production-ready** versions.

**When to use:**
- All features are tested and working
- No known critical bugs
- Documentation is complete
- Ready for production use

---

## Release Process

### Prerequisites

1. **Clean working directory**
   ```bash
   git status
   # Should show no uncommitted changes
   ```

2. **Up-to-date main branch**
   ```bash
   git checkout main
   git pull origin main
   ```

3. **All tests passing**
   ```bash
   pytest
   ruff check .
   mypy .
   ```

4. **PyPI Trusted Publishing configured**
   - Go to https://pypi.org/manage/account/publishing/
   - Add publisher for `namastexlabs/automagik-spark`
   - Environment name: `production`

---

## Pre-Release Process (RC/Beta)

Use this process for testing versions before stable release.

### Step 1: Update Version in pyproject.toml

Edit `pyproject.toml`:

```toml
[project]
name = "automagik-spark"
version = "0.3.8rc1"  # Change this line
```

### Step 2: Commit Version Change

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.3.8rc1

Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"
git push origin main
```

### Step 3: Create and Push Git Tag

```bash
# Create annotated tag (important: use 'v' prefix)
git tag -a v0.3.8rc1 -m "Release v0.3.8rc1 - Release Candidate 1

This is a release candidate for testing before stable release.

Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"

# Push the tag to trigger workflows
git push origin v0.3.8rc1
```

### Step 4: Monitor GitHub Actions

1. Go to https://github.com/namastexlabs/automagik-spark/actions
2. Watch for two workflows to start:
   - **"Publish to PyPI"** - Builds and publishes package
   - **"Auto Release Generation"** - Creates GitHub release with AI-generated notes

### Step 5: Verify Release

```bash
# Wait 5-10 minutes, then test installation
pip install automagik-spark==0.3.8rc1

# Verify version
automagik-spark --version
# Should output: automagik-spark 0.3.8rc1

# Test basic functionality
automagik-spark db upgrade
automagik-spark api start --help
```

### Step 6: Announce Pre-Release

Share with team for testing:
```
🔖 New release candidate available for testing!

Version: 0.3.8rc1
Install: pip install automagik-spark==0.3.8rc1
Release: https://github.com/namastexlabs/automagik-spark/releases/tag/v0.3.8rc1

Please test and report any issues before stable release.
```

---

## Stable Release Process

Use this process for production-ready versions.

### Step 1: Update Version in pyproject.toml

Edit `pyproject.toml`:

```toml
[project]
name = "automagik-spark"
version = "0.3.8"  # Remove rc/beta suffix
```

### Step 2: Update CHANGELOG (Optional but Recommended)

Create or update `CHANGELOG.md` with release notes:

```markdown
## [0.3.8] - 2025-10-20

### Added
- New workflow scheduling feature with cron support
- MCP server integration for Spark workflows

### Fixed
- Fixed input_value handling in scheduled tasks
- Resolved Hive v2 API compatibility issues

### Changed
- Improved error handling in workflow execution
- Updated dependencies to latest versions
```

### Step 3: Commit Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release version 0.3.8

- Update version to 0.3.8
- Add CHANGELOG entries for this release

Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"
git push origin main
```

### Step 4: Create and Push Git Tag

```bash
# Create annotated tag
git tag -a v0.3.8 -m "Release v0.3.8 - Stable Release

New Features:
- Workflow scheduling with cron support
- MCP server integration
- Enhanced error handling

Bug Fixes:
- Fixed scheduled task execution
- Resolved Hive API compatibility

Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"

# Push the tag
git push origin v0.3.8
```

### Step 5: Monitor and Verify

Follow steps 4-5 from the Pre-Release Process above.

### Step 6: Announce Stable Release

Share with team and users:
```
🎉 New stable release available!

Version: 0.3.8
Install: pip install --upgrade automagik-spark
Release: https://github.com/namastexlabs/automagik-spark/releases/tag/v0.3.8
PyPI: https://pypi.org/project/automagik-spark/0.3.8/

What's new:
- Workflow scheduling with cron support
- MCP server integration
- Improved error handling and stability

Upgrade now: pip install --upgrade automagik-spark
```

---

## Troubleshooting

### Version Mismatch Error

**Error:** "Version mismatch! pyproject.toml: X.X.X, Git tag: Y.Y.Y"

**Solution:**
1. Check `pyproject.toml` version matches your git tag (without 'v' prefix)
2. Delete the incorrect tag: `git tag -d vX.X.X && git push origin :refs/tags/vX.X.X`
3. Fix version in `pyproject.toml`
4. Commit and create new tag

### PyPI Upload Fails

**Error:** "File already exists" or "403 Forbidden"

**Solutions:**

1. **Version already exists on PyPI:**
   - You cannot overwrite PyPI packages
   - Bump to a new version (e.g., 0.3.8rc2 instead of 0.3.8rc1)
   - Create new tag with bumped version

2. **PyPI Trusted Publishing not configured:**
   - Go to https://pypi.org/manage/account/publishing/
   - Add publisher:
     - Owner: `namastexlabs`
     - Repository: `automagik-spark`
     - Workflow: `publish-pypi.yml`
     - Environment: `production`

3. **Token issues:**
   - Check GitHub repository secrets
   - Verify `PYPI_API_TOKEN` is set (if not using Trusted Publishing)

### Build Fails

**Error:** Build artifacts not found or build fails

**Solutions:**

1. **Check build backend:**
   ```bash
   # Verify pyproject.toml has build-system section
   grep -A3 "\[build-system\]" pyproject.toml
   ```

2. **Test build locally:**
   ```bash
   python -m pip install build hatchling
   python -m build
   ls -lh dist/
   ```

3. **Check package structure:**
   ```bash
   # Verify automagik_spark/ directory exists
   ls -la automagik_spark/
   ```

### GitHub Release Not Created

**Error:** Auto-release workflow completes but no GitHub release

**Solutions:**

1. **Check ANTHROPIC_API_KEY:**
   - Workflow needs this secret for AI-generated notes
   - Without it, fallback template is used
   - Add to GitHub repository secrets if missing

2. **Manual release creation:**
   ```bash
   # Create release manually via GitHub CLI
   gh release create v0.3.8 \
     --title "automagik-spark 0.3.8" \
     --notes "See CHANGELOG.md for details" \
     dist/*
   ```

### Tag Already Exists

**Error:** "tag already exists" when pushing

**Solution:**
```bash
# Delete local tag
git tag -d v0.3.8

# Delete remote tag
git push origin :refs/tags/v0.3.8

# Recreate tag
git tag -a v0.3.8 -m "Release message"
git push origin v0.3.8
```

---

## Quick Reference

### Common Release Commands

```bash
# Check current version
grep '^version = ' pyproject.toml

# Create RC release
# 1. Update pyproject.toml to "0.3.8rc1"
git commit -am "chore: bump to 0.3.8rc1

Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"
git push
git tag -a v0.3.8rc1 -m "Release Candidate 1"
git push origin v0.3.8rc1

# Create stable release
# 1. Update pyproject.toml to "0.3.8"
git commit -am "chore: release 0.3.8

Co-authored-by: Automagik Genie 🧞 <genie@namastex.ai>"
git push
git tag -a v0.3.8 -m "Stable Release"
git push origin v0.3.8

# Test installation
pip install automagik-spark==0.3.8rc1  # or 0.3.8
automagik-spark --version

# Verify on PyPI
open https://pypi.org/project/automagik-spark/

# View release
open https://github.com/namastexlabs/automagik-spark/releases
```

---

## Best Practices

1. **Always test locally before releasing**
   ```bash
   pytest && ruff check . && mypy .
   ```

2. **Use RC versions for major changes**
   - Get community feedback
   - Catch bugs before stable release

3. **Write clear commit messages**
   - Follow conventional commits format
   - Always include co-author credit

4. **Document breaking changes**
   - Update CHANGELOG.md
   - Add migration guides if needed

5. **Announce releases**
   - Post in team channels
   - Update documentation
   - Share on social media (for major releases)

---

## Support

- **Issues**: https://github.com/namastexlabs/automagik-spark/issues
- **Discussions**: https://github.com/namastexlabs/automagik-spark/discussions
- **Documentation**: https://github.com/namastexlabs/automagik-spark/blob/main/README.md

---

**Co-Authored-By**: Automagik Genie 🧞 <genie@namastex.ai>
