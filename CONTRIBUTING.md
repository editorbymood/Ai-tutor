# Contributing to AI-Powered Personal Tutor

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

Follow the [SETUP_GUIDE.md](SETUP_GUIDE.md) to set up your development environment.

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Maximum line length: 100 characters
- Use type hints where appropriate

```python
def calculate_score(answers: list, correct_answers: list) -> float:
    """
    Calculate quiz score based on answers.
    
    Args:
        answers: List of student answers
        correct_answers: List of correct answers
    
    Returns:
        Score as percentage (0-100)
    """
    # Implementation
```

### JavaScript/React (Frontend)

- Use ES6+ features
- Follow Airbnb style guide
- Use functional components with hooks
- Use meaningful component and variable names
- Add PropTypes or TypeScript types

```javascript
const CourseCard = ({ course, onEnroll }) => {
  // Component implementation
};

CourseCard.propTypes = {
  course: PropTypes.object.isRequired,
  onEnroll: PropTypes.func.isRequired,
};
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_users.py

# Run with coverage
pytest --cov=apps
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Commit Messages

Use clear and descriptive commit messages:

- `feat: Add user authentication`
- `fix: Fix quiz scoring bug`
- `docs: Update README`
- `style: Format code`
- `refactor: Refactor course model`
- `test: Add tests for AI tutor`
- `chore: Update dependencies`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Reporting Bugs

Use GitHub Issues to report bugs. Include:

- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details

## Feature Requests

We welcome feature requests! Please:

- Check if it's already requested
- Provide clear use case
- Explain expected behavior
- Consider implementation approach

## Questions?

Feel free to open an issue for questions or reach out to maintainers.

Thank you for contributing! 🎉