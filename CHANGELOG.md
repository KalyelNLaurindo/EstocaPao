# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Self-Healing and Disaster Recovery (DRP) auto-restoration protocol from `.bak` backup files (Task 08).
- `CommandLineInterfaceParser` console routing using standard `argparse` parser (Task 09).
- Log stamp format standardizer (`YYYY-MM-DD HH:MM:SS`) and conditional terminal ANSI colorized styling (Task 10).
- Standard package setup configurations in `pyproject.toml` with the global executable entrypoint `estocapao` (Task 11).
- Comprehensive end-to-end integration and E2E validation test suites for CLI routing, DRP restoration, and global executables.
- Created immutable `BatchValueObject` domain model under `src/estocapao/modules/inventory/domain/value.py` validating quantity boundaries and ISO date strings.
- Custom domain validation exception classes (`DomainValidationError`, `InvalidQuantityError`, and `InvalidDateError`).
- Unit test suite for `BatchValueObject` validation, boundaries, date parsing, equality, and immutability under `tests/unit/test_domain_value.py`.
- Added Pull Request Template (`.github/pull_request_template.md`) to establish professional code-review workflows.
- Added GitHub Actions workflow (`.github/workflows/ci.yml`) for automated unit testing (CI).

## [0.1.0] - 2026-06-12
### Added
- Initial project structure layout and context documents.
- Configuration settings (`config.ini`) and Python packaging definitions (`pyproject.toml`).
- Development guides including `CLAUDE.md` and project `README.md`.
