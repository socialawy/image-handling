# Agent Info: Image Handling Tool

## Project Overview
A versatile Python toolkit for image processing, featuring both a GUI (Tkinter) and a well-defined API. It handles resizing, conversions, and social media optimizations.

## Important Accounts
- **GitHub Owner**: `socialawy-dev`
- **Primary Contact**: `ahmed.itc@gmail.com`

## Tech Stack
- **Language**: Python 3.8+
- **Core Library**: Pillow (PIL)
- **GUI**: Tkinter
- **Other Libs**: `pillow_heif`, `svglib`, `numpy`

## Key Modules
- `image_handling.py`: Core `ImageHandler` and `ImageToolkit` classes.
- `image_editor_ui.py`: The graphical interface implementation.

## Guidelines for Jules
1. **API Consistency**: Ensure functions in `image_handling.py` remain backward compatible.
2. **Performance**: Optimize for batch processing using `numpy` where appropriate.
3. **Formats**: When adding support for new formats, ensure both GUI and API are updated.
4. **Documentation**: Keep the "Python API" section in `README.md` accurate.

## Current Goals
- AI-powered background removal.
- Web-based interface (Streamlit).
- More creative filters and LUT support.
