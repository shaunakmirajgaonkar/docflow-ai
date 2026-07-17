# Contributing to DocFlow AI

Thanks for your interest in contributing! This project is a 100% local,
privacy-first Intelligent Document Processing platform, and contributions of
all kinds are welcome — bug fixes, new features, documentation, and tests.

## Getting started

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/docflow-ai.git
   cd docflow-ai
   ```

2. Set up your local environment (see `run instructions.md` for full details):
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. Create a new branch for your change:
   ```bash
   git checkout -b feature/my-improvement
   ```

## Making changes

- Keep changes focused — one feature or fix per pull request.
- Follow existing code style and structure (FastAPI routers in `app/routers/`,
  business logic in `app/services/`, schemas in `app/models/`).
- Test your changes locally end-to-end (upload → process → Q&A → search)
  before submitting.
- Update `README.md` or `CHANGELOG.md` if your change affects setup,
  behavior, or dependencies.

## Submitting a pull request

1. Commit your changes with a clear message:
   ```bash
   git commit -m "Add: short description of the change"
   ```
2. Push to your fork and open a pull request against `main`.
3. Describe what the change does and why, and include steps to test it.

## Reporting bugs

Open an issue with:
- Steps to reproduce
- Expected vs. actual behavior
- Your OS, Python version, and relevant logs (redact any personal data)

## Code of Conduct

By participating in this project, you agree to abide by our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Questions

Open an issue or reach out via the contact info in `README.md`.
