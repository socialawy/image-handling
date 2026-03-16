# 🖼️ Image Handling Tool

A powerful, production-ready Python-based image processing tool. It combines a versatile **Graphical User Interface (GUI)** for quick edits with a robust **Python API** for developers to automate complex image manipulation workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pillow](https://img.shields.io/badge/Library-Pillow-green.svg)](https://python-pillow.org/)

---

### **✨ Core Features**

*   🚀 **Batch Processing**: Handle thousands of images at once—resize, convert, or compress.
*   📸 **Social Media Magic**: One-click optimization for Instagram, Facebook, Twitter, LinkedIn, and YouTube.
*   🧠 **Smart Cropping**: Intelligent subject detection to keep the focus where it matters.
*   🛠️ **Advanced Tools**: Add watermarks, create collages, composite images, and compress PNGs.
*   🎨 **Interactive GUI**: Real-time previews, tabbed interface, and intuitive controls.
*   🔌 **Developer Friendly**: Clean API to integrate image processing into any Python project.

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/socialawy/image-handling.git
   cd image-handling
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### Option 1: Graphical User Interface (GUI)
Perfect for quick, visual edits and batch tasks without writing code.

```bash
python image_editor_ui.py
```

*   **File Tab**: Multi-format opening/saving and entry points for batch operations.
*   **Edit Tab**: Brightness, contrast, saturation, rotation, and resizing.
*   **Filters Tab**: Blur, Sharpen, Grayscale, Sepia, and more.
*   **Social Media Tab**: Platform-specific templates (Instagram, etc.).
*   **Tools Tab**: Watermarking, Text Overlay, Collage Maker, and Advanced PNG Compression.

### Option 2: Python API
Automate your image workflows in any script.

```python
from image_handling import ImageHandler, ImageToolkit

handler = ImageHandler()
toolkit = ImageToolkit()

# Smart resize for Instagram
image = handler.import_image("input.jpg")
instagram_ready = toolkit.process_for_social_media("input.jpg", "instagram")

# Batch convert an entire folder
toolkit.batch_convert("raw_images/", "processed/", ImageFormat.WEBP)

# Add a watermark programmatically
watermarked = handler.add_text_overlay(image, "© 2024 MyBrand", (50, 50), opacity=0.5)
```

---

## 📦 Requirements

*   **Python 3.8+**
*   **Pillow**: Core image engine
*   **pillow_heif**: HEIC/HEIF support
*   **svglib**: Vector support
*   **numpy**: Advanced math operations

---

## 🗺️ Roadmap

- [ ] AI-powered background removal
- [ ] Direct export to cloud storage (S3, GCS)
- [ ] Web-based interface (Streamlit/Flask)
- [ ] More creative filters and LUT support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues for bug reports or feature requests. For code contributions, please submit a pull request.

---

**Built with ❤️ for image enthusiasts.**
