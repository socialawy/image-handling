# Agent Info: Image Handling Tool

## Project Overview
A versatile Python toolkit for image processing, featuring both a GUI (Tkinter) and a well-defined API. It handles resizing, conversions, social media optimizations, and batch processing operations. Designed to serve creators, developers, and businesses needing professional image manipulation capabilities.

## Important Accounts
- **GitHub Owner**: `socialawy-dev`
- **Primary Contact**: `ahmed.itc@gmail.com`
- **Community Support**: GitHub Issues and Discussions

## Tech Stack
- **Language**: Python 3.8+
- **Core Library**: Pillow (PIL) for image operations
- **GUI Framework**: Tkinter for desktop interface
- **Additional Libraries**: `pillow_heif` (HEIC support), `svglib` (vector support), `numpy` (performance)
- **Testing**: Custom comprehensive test suite

## Key Architecture Components
- `image_handling.py`: Core `ImageHandler` and `ImageToolkit` classes
- `image_editor_ui.py`: Graphical interface implementation with tabbed layout
- `test_comprehensive.py`: Full test suite for validation
- `requirements.txt`: Dependency management
- **Plugin Structure**: Modular design for easy feature addition

## Guidelines for Jules AI Assistant

### 🛠️ Development Tasks
1. **API Consistency**: Ensure functions in `image_handling.py` remain backward compatible
2. **Performance**: Optimize for batch processing using `numpy` where appropriate
3. **Format Support**: When adding new formats, update both GUI and API components
4. **Error Handling**: Provide clear error messages and graceful degradation
5. **Documentation**: Keep the "Python API" section in README.md accurate and comprehensive

### 🧪 Testing and Quality Assurance
1. **Run Test Suite**: Always run `python test_comprehensive.py` before submitting changes
2. **Test Coverage**: Add tests for new functionality in the comprehensive test suite
3. **Cross-Platform**: Ensure compatibility across Windows, macOS, and Linux
4. **Performance Testing**: Test with large images and batch operations
5. **GUI Testing**: Verify both GUI and API work correctly

### 🎨 Feature Development
1. **Social Media Templates**: Follow existing patterns when adding new platform optimizations
2. **Filter Implementation**: Use consistent parameter naming and return formats
3. **Batch Operations**: Ensure memory efficiency for large batch jobs
4. **UI Consistency**: Follow existing Tkinter patterns and naming conventions

### 📚 Documentation Standards
1. **Code Comments**: Add clear comments for complex image processing logic
2. **Function Documentation**: Include parameter types, return values, and usage examples
3. **README Updates**: Update feature lists and usage examples
4. **API Examples**: Provide working code examples in documentation

### 🔧 Maintenance Tasks
1. **Dependency Updates**: Keep Pillow and other dependencies current
2. **Security**: Regularly audit dependencies for vulnerabilities
3. **Performance**: Profile and optimize slow operations
4. **Bug Fixes**: Address community-reported issues promptly

## Current Development Goals

### High Priority
- **AI-powered background removal** using modern ML libraries
- **Web-based interface** (Streamlit/Flask) for remote access
- **Advanced filters** and creative effects (LUT support, color grading)
- **Performance optimizations** for GPU acceleration where possible

### Medium Priority
- **Plugin system** for custom filters and effects
- **Cloud storage integration** (AWS S3, Google Cloud)
- **Advanced batch operations** with progress tracking
- **Vector graphics editing** capabilities

### Future Considerations
- **Real-time collaboration** features
- **Mobile app companion**
- **API service** for cloud-based processing
- **Integration with popular design tools**

## Community Support Guidelines

### Issue Response
1. **Bug Reports**: Respond within 48 hours with reproduction steps
2. **Feature Requests**: Evaluate and provide timeline within 1 week
3. **Pull Requests**: Review and merge within 3-5 business days
4. **Questions**: Provide helpful, detailed responses with code examples

### Code Review Standards
1. **Functionality**: Does the code work as intended?
2. **Performance**: Is it efficient and scalable?
3. **Style**: Does it follow project conventions?
4. **Testing**: Are adequate tests included?
5. **Documentation**: Is the change well-documented?

## Testing Commands for Jules

```bash
# Run comprehensive test suite
python test_comprehensive.py

# Test specific functionality
python -c "
from image_handling import ImageHandler, ImageToolkit
handler = ImageHandler()
toolkit = ImageToolkit()
print('✓ Core components loaded successfully')
"

# Test GUI (requires display)
python image_editor_ui.py

# Test batch processing
python -c "
from image_handling import ImageToolkit
import tempfile
import os
toolkit = ImageToolkit()
# Create test scenario
print('✓ Batch processing test setup complete')
"
```

## Common Tasks for Jules

### Adding New Social Media Platform
1. Add platform constants to ImageToolkit
2. Implement platform-specific sizing logic
3. Add GUI controls for the new platform
4. Update test suite with platform tests
5. Document in README

### Implementing New Filter
1. Add filter function to ImageToolkit
2. Handle edge cases and invalid inputs
3. Add GUI controls for filter parameters
4. Include filter in batch operations
5. Add comprehensive tests

### Performance Optimization
1. Profile current implementation
2. Identify bottlenecks (CPU, memory, I/O)
3. Implement optimizations
4. Benchmark improvements
5. Update documentation

## Security and Best Practices

1. **Input Validation**: Always validate image files and parameters
2. **Memory Management**: Handle large files efficiently
3. **Error Handling**: Provide meaningful error messages
4. **Dependency Security**: Regular security audits
5. **Code Quality**: Maintain high test coverage and documentation

This document serves as a comprehensive guide for Jules AI assistant to effectively maintain, enhance, and support the Image Handling Tool project.
