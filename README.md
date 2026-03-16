# Image Handling Tool

A powerful Python-based image processing tool that provides a wide range of image manipulation capabilities through both a graphical user interface (GUI) and Python API.

## Features

### Core Features
- **Multiple Format Support**: Read and write various image formats including PNG, JPG, GIF, BMP, TIFF, WEBP, SVG, HEIF, and more
- **Resizing & Scaling**: 
  - Fixed-size resizing
  - Aspect ratio-preserving resizing
  - Smart crop with subject detection
  - Canvas resizing with background options
- **Batch Processing**: 
  - Batch resize multiple images
  - Batch convert between formats
  - Process entire directories at once
- **Social Media Optimization**: Pre-configured templates for popular platforms:
  - Instagram (Square, Portrait, Landscape, Story)
  - Facebook (Post, Cover, Story)
  - Twitter (Post, Header)
  - LinkedIn (Post, Cover)
  - YouTube (Thumbnail, Cover)
- **Image Enhancement**: 
  - Brightness adjustment
  - Contrast adjustment
  - Saturation adjustment
- **Advanced Features**: 
  - Apply various filters (blur, sharpen, emboss, contour)
  - Add watermarks with customizable text and opacity
  - Create collages with customizable layout
  - Smart cropping with subject detection
  - Format conversion with quality settings

### Image Editor UI
- **Intuitive Interface**: 
  - Tabbed interface for organized functionality
  - Real-time preview of changes
  - Status bar for operation feedback
- **File Operations**:
  - Open multiple image formats
  - Save with format options
  - Batch processing interface
- **Image Adjustments**:
  - Interactive sliders for brightness, contrast, and saturation
  - Reset to original functionality
- **Filters & Effects**:
  - Basic filters (blur, sharpen, emboss, contour)
  - Advanced effects (grayscale, sepia)
- **Transform Tools**:
  - Rotation (90° left/right)
  - Flipping (horizontal/vertical)
  - Smart cropping
  - Canvas resizing
- **Social Media Tools**:
  - One-click optimization for different platforms
  - Preview of social media templates
- **Advanced Tools**:
  - Interactive crop with visual guides
  - Watermarking with customizable text, font size, opacity, and position
  - Text overlay with customizable text, font size, and position
  - Blank canvas creation with customizable dimensions and color
  - Image compositing for combining images with position and opacity control
  - Collage creation with layout options
  - Format conversion with quality settings
  - **PNG Compression**: Advanced PNG compression with multiple options

## Installation

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

## Usage

### Image Editor UI

To launch the Image Editor with a graphical interface, run:

```bash
python image_editor_ui.py
```

#### UI Controls

- **File Tab**:
  - Open Image: Load images in various formats
  - Save Image: Save current changes
  - Save As: Save with new name/format
  - Batch Operations:
    - Batch Resize: Process multiple images
    - Batch Convert: Convert multiple images

- **Edit Tab**:
  - Image Adjustments:
    - Brightness slider
    - Contrast slider
    - Saturation slider
  - Transform:
    - Rotate 90° left/right
    - Flip horizontal/vertical
  - Resize Options:
    - Fixed Size resize
    - Aspect Ratio resize
    - Smart Crop

- **Filters Tab**:
  - Basic Filters:
    - Blur
    - Sharpen
    - Emboss
    - Contour
  - Advanced Filters:
    - Grayscale
    - Sepia

- **Social Media Tab**:
  - Platform-specific optimization:
    - Instagram
    - Facebook
    - Twitter
    - LinkedIn
    - YouTube

- **Tools Tab**:
  - Add Watermark (with customizable font size, opacity, and position)
  - Add Text Overlay
  - Crop Image
  - Resize Canvas
  - Convert Format
  - Create Collage
  - Create Blank Canvas
  - Composite Images
  - PNG Compression (with advanced compression options)

#### Quick Start

1. Launch the application:
   ```bash
   python image_editor_ui.py
   ```

2. Basic Image Editing:
   - Click "Open Image" to load an image
   - Use the sliders to adjust brightness, contrast, and saturation
   - Apply filters or effects as needed
   - Use the crop tool if you need to trim the image
   - Save your work with "Save" or "Save As..."

3. Batch Processing:
   - Go to File tab
   - Select "Batch Resize", "Batch Convert", or "Batch Compress PNG"
   - Choose input and output directories
   - Configure processing options
   - Click "Process" to start

#### PNG Compression

The application offers advanced PNG compression with multiple options:

**UI Features:**
- **Batch Compress PNG**: Process multiple PNG files at once
- **Save with Compression**: When saving PNG files, choose compression settings
- **Compression Options**:
  - Compression Level (0-9): Balance between speed and compression ratio
  - Optimization: Enable additional optimization algorithms
  - Color Reduction: Reduce color palette for smaller file sizes
  - Max Colors: Set maximum number of colors (2-256)

**Command Line Usage:**
```bash
# Basic PNG compression
python image_handling.py batch-compress-png input_dir output_dir

# Advanced compression with options
python image_handling.py batch-compress-png input_dir output_dir \
  --compress-level 9 \
  --optimize \
  --reduce-colors \
  --max-colors 128
```

**Compression Levels:**
- **0**: Fastest compression (larger files)
- **6**: Balanced compression (default)
- **9**: Maximum compression (smallest files, slower)

**Tips:**
- Use color reduction for images with limited color palettes
- Higher compression levels are slower but produce smaller files
- Optimization is recommended for web images

4. Social Media Optimization:
   - Go to Social Media tab
   - Select target platform
   - Click the platform button to optimize

### Python API

```python
from image_handling import ImageHandler, ImageToolkit

# Initialize handlers
handler = ImageHandler()
toolkit = ImageToolkit()

# Basic image operations
image = handler.import_image("input.jpg")
resized = handler.resize_with_aspect_ratio(image, width=800)
handler.export_image(resized, "output.jpg")

# Social media optimization
results = toolkit.process_for_social_media("photo.jpg", "instagram")

# Create a collage
image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
collage = toolkit.create_collage(image_paths, columns=2)
handler.export_image(collage, "collage.jpg")

# Batch processing
toolkit.batch_resize("input_folder/", "output_folder/", width=800)
toolkit.batch_convert("input_folder/", "output_folder/", ImageFormat.PNG)

# Add text overlay
image_with_text = handler.add_text_overlay(image, "Hello World!", (50, 50), font_size=48, color=(255, 0, 0))
handler.export_image(image_with_text, "text_overlay_output.png")

# Create a blank canvas
blank_canvas = handler.create_blank_canvas(1024, 768, (0, 0, 0)) # Black canvas
handler.export_image(blank_canvas, "blank_canvas.png")

# Composite images
background_image = handler.import_image("background.jpg")
overlay_image = handler.import_image("overlay.png")
composited_image = handler.composite_images(background_image, overlay_image, (100, 100), opacity=0.7)
handler.export_image(composited_image, "composited_image.png")
```

## Dependencies

The tool relies on several well-maintained Python packages:

- **Pillow (PIL fork)**: Core image processing and GUI support
- **pillow_heif**: HEIF/HEIC image format support
- **svglib**: SVG vector image handling
- **numpy**: Advanced image processing operations
- **tkinter**: Default Python GUI toolkit (included in standard library)

## Extension Possibilities

The modular design allows for easy extension:

- Add new image formats as they become available
- Create custom filters and effects
- Add new social media templates
- Extend the UI with new tools and panels
- Implement additional batch processing features
- Add support for more export options
- Create custom keyboard shortcuts
- Implement plugin system for third-party extensions

## Contributing
...

## License
...
