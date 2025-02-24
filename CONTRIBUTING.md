# Contributing to Apyrat

Thanks for considering contributing to Apyrat! Here's how you can help.

## Ways to Contribute

### 🐛 Report Bugs

Report bugs by [opening an issue](https://github.com/codewithemad/apyrat/issues).
Include:

- Your OS and Python version
- Steps to reproduce
- Error messages
- Expected vs actual behavior

### 🛠️ Fix Bugs or Add Features

Check our [GitHub issues](https://github.com/codewithemad/apyrat/issues) for bugs and features tagged with "help wanted".

### 📝 Improve Documentation

Help improve:

- Code docstrings
- README and other docs
- Code comments

## Development Setup

1. Fork and clone:

   ```bash
   git clone git@github.com:your_username/apyrat.git
   cd apyrat
   ```

2. Install dependencies using [uv](https://github.com/astral-sh/uv):

   ```bash
   make install
   ```

3. Create a branch:

   ```bash
   git checkout -b feature-name
   ```

## Development Guidelines

### Code Quality

We use:

- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [Pytest](https://docs.pytest.org/) for testing

Run checks:

```bash
# Format and lint
make format
make lint

# Run tests
make test
```

### Testing

- Write tests for new features
- Ensure all tests pass
- Test edge cases

## Pull Request Process

1. Update docs if needed
2. Add tests
3. Run checks:

   ```bash
   make format
   make lint
   make test
   ```

4. Push changes:

   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature-name
   ```

5. Open a PR with:
   - Clear description
   - Issue numbers if relevant
   - Breaking change notes if any

## Release Process (Maintainers)

```bash
# Build and publish
make build
make publish
```

## Questions?

[Open an issue](https://github.com/codewithemad/apyrat/issues) for support.
