---
description: Acting as a codebase Gatekeeper, this configures Ruff to enforce strict standards. It instantly flags AI hallucinations or insecure code, forcing self-correction before you see errors—essential for a clean "vibe coding" workflow.
---

[tool.ruff]
# The "Rabbit" settings: Optimized for speed and security
line-length = 88
target-version = "py311"

[tool.ruff.lint]
# Enable specific rule sets to catch bugs and security issues:
# E: pycodestyle errors (Standard Python style)
# F: Pyflakes (Catch unused imports, undefined variables - crucial for AI)
# I: isort (Sorts imports automatically to prevent spaghetti dependencies)
# B: flake8-bugbear (Catches subtle bugs and security risks)
select = ["E", "F", "I", "B"]

# Avoid ignoring rules to ensure maximum strictness
ignore = []

# Allow the AI to fix these issues automatically (Self-Correction)
fixable = ["ALL"]

[tool.ruff.lint.isort]
# Tells Ruff which modules are part of your local application
known-first-party = ["app"]

[tool.ruff.format]
# Enforce standard quoting for consistency
quote-style = "double"
indent-style = "space"
