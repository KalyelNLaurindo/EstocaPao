## 📝 Description

Brief summary of the changes made and the business/technical problem they resolve. Please link relevant task IDs (e.g., `TSK-01`).

## 🚀 Impact & Changes

Detail what has changed in the system layers:
- **Domain**: (e.g., New business entities, value objects, invariants)
- **Application**: (e.g., New use cases, orchestrators)
- **Infrastructure**: (e.g., File operations, CLI router, database adapters)
- **Tests**: (e.g., Unit tests, integration tests)

## 🧪 Verification Plan

### Manual Verification
Describe steps taken to verify the changes:
```bash
# Set path and execute unit tests
$env:PYTHONPATH="src"
python -m unittest discover -s tests/unit
```

## 🏁 Quality Checklist (Definition of Done)
- [ ] Code is PEP 8 compliant.
- [ ] Comprehensive unit tests cover all edge cases, exceptions, and boundaries.
- [ ] Zero third-party external dependencies imported.
- [ ] Docstrings and inline code comments are written clearly in English.
