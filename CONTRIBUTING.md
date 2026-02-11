# Contributing to OpenLiveCaption

Thank you for your interest in contributing to OpenLiveCaption! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, education, socio-economic status
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated promptly and fairly.

## Getting Started

### Prerequisites

- **Python 3.8 or later**
- **Git** for version control
- **Basic knowledge** of Python, PyQt6, and audio processing
- **Familiarity** with the project (read README.md and try the application)

### First-Time Contributors

If you're new to open source:
1. Read the [README.md](README.md) to understand the project
2. Browse [existing issues](https://github.com/yourusername/OpenLiveCaption/issues) labeled `good first issue`
3. Join [GitHub Discussions](https://github.com/yourusername/OpenLiveCaption/discussions) to ask questions
4. Start with documentation improvements or bug fixes

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/OpenLiveCaption.git
cd OpenLiveCaption

# Add upstream remote
git remote add upstream https://github.com/yourusername/OpenLiveCaption.git
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov hypothesis black flake8 mypy
```

### 4. Verify Setup

```bash
# Run tests to verify setup
pytest

# Run the application
python Main.py
```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes** - Fix issues reported in GitHub Issues
2. **New Features** - Implement features from the roadmap or propose new ones
3. **Documentation** - Improve README, guides, or code comments
4. **Testing** - Add unit tests, property-based tests, or integration tests
5. **Performance** - Optimize code for speed or memory usage
6. **Accessibility** - Improve accessibility features
7. **Translations** - Add support for new languages
8. **Platform Support** - Improve platform-specific implementations

### Contribution Workflow

1. **Find or Create an Issue**
   - Check [existing issues](https://github.com/yourusername/OpenLiveCaption/issues)
   - Create a new issue if needed
   - Comment on the issue to claim it

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

3. **Make Changes**
   - Write code following our [coding standards](#coding-standards)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   # Run all tests
   pytest
   
   # Run specific test file
   pytest tests/test_audio/test_audio_capture.py
   
   # Run with coverage
   pytest --cov=src --cov-report=html
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   # or
   git commit -m "fix: resolve issue #123"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings (except when single quotes avoid escaping)
- **Imports**: Grouped and sorted (standard library, third-party, local)

### Code Formatting

We use **Black** for automatic code formatting:

```bash
# Format all Python files
black src/ tests/

# Check formatting without modifying
black --check src/ tests/
```

### Linting

We use **flake8** for linting:

```bash
# Run flake8
flake8 src/ tests/

# Configuration in .flake8 or setup.cfg
```

### Type Hints

We use **type hints** for all function signatures:

```python
def add_subtitle(self, text: str, start_time: float, end_time: float) -> None:
    """Add a subtitle entry"""
    pass
```

Check types with **mypy**:

```bash
mypy src/
```

### Docstrings

Use **Google-style docstrings**:

```python
def transcribe(self, audio: np.ndarray, language: Optional[str] = None) -> TranscriptionResult:
    """
    Transcribe audio chunk and return text with metadata.
    
    Args:
        audio: Audio data as numpy array (float32, 16kHz)
        language: Optional language code (e.g., 'en', 'es'). None for auto-detect.
    
    Returns:
        TranscriptionResult containing text, language, confidence, and timestamps.
    
    Raises:
        TranscriptionError: If transcription fails.
    """
    pass
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `AudioCaptureEngine`)
- **Functions/Methods**: `snake_case` (e.g., `start_capture`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_SAMPLE_RATE`)
- **Private members**: Prefix with `_` (e.g., `_internal_method`)

### File Organization

```
src/
├── audio/              # Audio capture module
│   ├── __init__.py
│   └── audio_capture.py
├── transcription/      # Transcription module
│   ├── __init__.py
│   └── transcription_engine.py
└── ...

tests/
├── test_audio/         # Audio tests
│   ├── __init__.py
│   └── test_audio_capture.py
└── ...
```

## Testing Guidelines

### Test Requirements

- **All new features** must include tests
- **Bug fixes** should include regression tests
- **Aim for 80%+ code coverage**
- **Property-based tests** for critical functionality

### Test Types

1. **Unit Tests** - Test individual functions/classes
   ```python
   def test_audio_device_enumeration():
       """Test that audio devices can be enumerated"""
       engine = AudioCaptureEngine()
       devices = engine.list_devices()
       assert isinstance(devices, list)
   ```

2. **Property-Based Tests** - Test universal properties
   ```python
   from hypothesis import given, strategies as st
   
   @given(opacity=st.floats(min_value=0.0, max_value=1.0))
   def test_overlay_opacity_configuration(opacity):
       """For any opacity value, setting it should result in that exact value"""
       overlay = CaptionOverlay()
       overlay.set_opacity(opacity)
       assert overlay.get_opacity() == opacity
   ```

3. **Integration Tests** - Test component interactions
   ```python
   def test_end_to_end_transcription():
       """Test complete audio capture to transcription flow"""
       # Setup components
       # Capture audio
       # Transcribe
       # Verify results
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_audio/test_audio_capture.py

# Run specific test
pytest tests/test_audio/test_audio_capture.py::test_audio_device_enumeration

# Run with coverage
pytest --cov=src --cov-report=html

# Run property-based tests with more examples
pytest --hypothesis-seed=0 -v
```

### Test Naming

- Test files: `test_<module_name>.py`
- Test functions: `test_<what_is_being_tested>`
- Property tests: `test_property_<number>_<property_name>`

## Submitting Changes

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(audio): add support for multi-source capture

Implement simultaneous capture from multiple audio sources with mixing.

Closes #123
```

```
fix(export): correct timestamp precision in SRT export

Use rounding instead of truncation to avoid millisecond precision loss.

Fixes #456
```

### Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update CHANGELOG.md

2. **Ensure Tests Pass**
   - All existing tests pass
   - New tests added for new functionality
   - Code coverage maintained or improved

3. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference related issues
   - Describe changes in detail
   - Include screenshots for UI changes

4. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Keep discussion professional and constructive

5. **Merge**
   - Maintainers will merge when approved
   - Delete your branch after merge

### Pull Request Template

```markdown
## Description
Brief description of changes

## Related Issues
Closes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
```

## Reporting Bugs

### Before Reporting

1. **Check existing issues** - Your bug may already be reported
2. **Try latest version** - Bug may be fixed in newer version
3. **Read troubleshooting guide** - See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.10.5]
- OpenLiveCaption version: [e.g., 2.0.0]

**Additional context**
Any other relevant information
```

## Requesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of what you want to happen

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other relevant information
```

## Documentation

### Documentation Standards

- **Clear and concise** - Use simple language
- **Examples** - Include code examples
- **Screenshots** - Add screenshots for UI features
- **Up-to-date** - Keep documentation synchronized with code

### Documentation Types

1. **README.md** - User guide and quick start
2. **Code comments** - Explain complex logic
3. **Docstrings** - Document all public APIs
4. **Guides** - Platform-specific setup guides
5. **Troubleshooting** - Common issues and solutions

## Community

### Communication Channels

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and general discussion
- **Pull Requests** - Code review and collaboration

### Getting Help

- Read the [README.md](README.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Search [existing issues](https://github.com/yourusername/OpenLiveCaption/issues)
- Ask in [GitHub Discussions](https://github.com/yourusername/OpenLiveCaption/discussions)
- Be patient and respectful

### Recognition

Contributors are recognized in:
- GitHub contributors page
- CHANGELOG.md for significant contributions
- README.md acknowledgments section

## License

By contributing to OpenLiveCaption, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to OpenLiveCaption!** 🎉

Your contributions help make this project better for everyone. We appreciate your time and effort!

