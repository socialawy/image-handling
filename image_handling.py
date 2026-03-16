import os
import io
from typing import List, Tuple, Optional, Union
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import pillow_heif  # For HEIF support
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import numpy as np

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

class ImageFormat(Enum):
    """Supported image formats"""
    PNG = "PNG"
    JPG = "JPEG"
    JPEG = "JPEG"
    GIF = "GIF"
    BMP = "BMP"
    TIFF = "TIFF"
    WEBP = "WEBP"
    SVG = "SVG"
    HEIF = "HEIF"
    HEIC = "HEIC"

@dataclass
class ResizeTemplate:
    """Standard size templates"""
    name: str
    width: int
    height: int
    
class StandardSizes:
    """Common resize templates"""
    THUMBNAIL = ResizeTemplate("Thumbnail", 150, 150)
    INSTAGRAM_SQUARE = ResizeTemplate("Instagram Square", 1080, 1080)
    INSTAGRAM_PORTRAIT = ResizeTemplate("Instagram Portrait", 1080, 1350)
    INSTAGRAM_LANDSCAPE = ResizeTemplate("Instagram Landscape", 1080, 566)
    FACEBOOK_POST = ResizeTemplate("Facebook Post", 1200, 630)
    TWITTER_POST = ResizeTemplate("Twitter Post", 1024, 512)
    LINKEDIN_POST = ResizeTemplate("LinkedIn Post", 1200, 627)
    YOUTUBE_THUMBNAIL = ResizeTemplate("YouTube Thumbnail", 1280, 720)
    A4_PRINT = ResizeTemplate("A4 Print (300 DPI)", 2480, 3508)
    LETTER_PRINT = ResizeTemplate("Letter Print (300 DPI)", 2550, 3300)

class ImageHandler:
    """Versatile image handling tool with import, export, resize, and conversion capabilities"""
    
    def __init__(self):
        self.supported_formats = list(ImageFormat)
        self.standard_sizes = StandardSizes()
        
    def import_image(self, file_path: Union[str, Path]) -> Image.Image:
        """Import image from file path"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {file_path}")
            
        # Handle SVG separately
        if file_path.suffix.lower() == '.svg':
            return self._import_svg(file_path)
            
        try:
            image = Image.open(file_path)
            # Convert to RGB if necessary (for compatibility)
            if image.mode in ('RGBA', 'LA', 'P'):
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[3])
                else:
                    background.paste(image)
                return background
            return image.convert('RGB')
        except Exception as e:
            raise ValueError(f"Failed to import image: {str(e)}")
    
    def _import_svg(self, file_path: Path) -> Image.Image:
        """Import SVG file and convert to PIL Image"""
        try:
            drawing = svg2rlg(str(file_path))
            img_data = renderPM.drawToString(drawing, fmt='PNG')
            return Image.open(io.BytesIO(img_data))
        except Exception as e:
            raise ValueError(f"Failed to import SVG: {str(e)}")
    
    def export_image(self, image: Image.Image, output_path: Union[str, Path], 
                    format: Optional[ImageFormat] = None, quality: int = 95, 
                    compress_level: int = 6, optimize: bool = True, 
                    lossless: bool = True, reduce_colors: bool = False, 
                    max_colors: int = 256) -> None:
        """Export image to specified path and format with advanced compression options"""
        output_path = Path(output_path)
        
        # Determine format from extension if not specified
        if format is None:
            ext = output_path.suffix.lower()[1:]
            try:
                format = ImageFormat[ext.upper()]
            except KeyError:
                format = ImageFormat.PNG
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save with appropriate settings
        save_kwargs = {}
        
        if format == ImageFormat.PNG:
            # Advanced PNG compression options
            save_kwargs = {
                'optimize': optimize,
                'compress_level': compress_level  # 0-9, where 9 is maximum compression
            }
            
            # Reduce colors for better compression (optional)
            if reduce_colors and image.mode in ('RGBA', 'RGB'):
                if image.mode == 'RGBA':
                    # Convert to P mode with transparency
                    image = image.convert('P', palette=Image.Palette.ADAPTIVE, colors=max_colors)
                    # Create transparency mask
                    alpha = image.split()[-1] if len(image.split()) == 4 else None
                    if alpha:
                        image = image.convert('RGBA')
                        save_kwargs['transparency'] = 0
                else:
                    # Convert RGB to palette mode
                    image = image.convert('P', palette=Image.Palette.ADAPTIVE, colors=max_colors)
                    
        elif format == ImageFormat.JPG or format == ImageFormat.JPEG:
            save_kwargs = {
                'quality': quality,
                'optimize': optimize,
                'progressive': True
            }
        elif format == ImageFormat.GIF:
            save_kwargs = {'optimize': optimize}
        elif format == ImageFormat.WEBP:
            save_kwargs = {
                'quality': quality, 
                'method': 6,
                'lossless': lossless
            }
            
        image.save(output_path, format.value, **save_kwargs)
    
    def batch_process(self, input_dir: Union[str, Path], output_dir: Union[str, Path],
                     operation: callable, **kwargs) -> List[Path]:
        """Process multiple images in a directory"""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        processed_files = []
        
        for file_path in input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', 
                                                                    '.gif', '.bmp', '.tiff', 
                                                                    '.webp', '.heif', '.heic']:
                try:
                    image = self.import_image(file_path)
                    processed_image = operation(self, image, **kwargs)
                    output_path = output_dir / file_path.name
                    self.export_image(processed_image, output_path)
                    processed_files.append(output_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    
        return processed_files
    
    def convert_format(self, image: Image.Image, target_format: ImageFormat) -> Image.Image:
        """Convert image to different format"""
        # For most conversions, the image object remains the same
        # The actual format conversion happens during export
        return image
    
    def resize_fixed(self, image: Image.Image, width: int, height: int) -> Image.Image:
        """Resize image to fixed dimensions"""
        return image.resize((width, height), Image.Resampling.LANCZOS)
    
    def resize_with_aspect_ratio(self, image: Image.Image, width: Optional[int] = None,
                                height: Optional[int] = None) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        if width is None and height is None:
            return image
            
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        
        if width is None:
            width = int(height * aspect_ratio)
        elif height is None:
            height = int(width / aspect_ratio)
        else:
            # Both dimensions specified - fit within bounds
            target_ratio = width / height
            if aspect_ratio > target_ratio:
                height = int(width / aspect_ratio)
            else:
                width = int(height * aspect_ratio)
                
        return image.resize((width, height), Image.Resampling.LANCZOS)
    
    def smart_resize_with_canvas(self, image: Image.Image, width: int, height: int,
                               background_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Resize image to fit within canvas while maintaining aspect ratio"""
        # Calculate the scale factor to fit the image within the target dimensions
        scale = min(width / image.width, height / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        
        # Resize the image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create canvas
        canvas = Image.new('RGB', (width, height), background_color)
        
        # Calculate position to center the image
        x = (width - new_width) // 2
        y = (height - new_height) // 2
        
        # Paste resized image onto canvas
        canvas.paste(resized, (x, y))
        
        return canvas
    
    def smart_crop(self, image: Image.Image, width: int, height: int) -> Image.Image:
        """Smart crop to exact dimensions"""
        original_width, original_height = image.size
        target_ratio = width / height
        original_ratio = original_width / original_height
        
        if original_ratio > target_ratio:
            # Image is wider - crop width
            new_width = int(original_height * target_ratio)
            left = (original_width - new_width) // 2
            right = left + new_width
            top = 0
            bottom = original_height
        else:
            # Image is taller - crop height
            new_height = int(original_width / target_ratio)
            top = (original_height - new_height) // 2
            bottom = top + new_height
            left = 0
            right = original_width
            
        cropped = image.crop((left, top, right, bottom))
        return cropped.resize((width, height), Image.Resampling.LANCZOS)
    
    def apply_template(self, image: Image.Image, template: ResizeTemplate,
                      maintain_aspect: bool = True) -> Image.Image:
        """Apply standard size template"""
        if maintain_aspect:
            return self.smart_resize_with_canvas(image, template.width, template.height)
        else:
            return self.resize_fixed(image, template.width, template.height)
    
    def enhance_brightness(self, image: Image.Image, factor: float) -> Image.Image:
        """Adjust image brightness (factor: 0.0 = black, 1.0 = original, 2.0 = twice as bright)"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def enhance_contrast(self, image: Image.Image, factor: float) -> Image.Image:
        """Adjust image contrast (factor: 0.0 = gray, 1.0 = original, 2.0 = twice the contrast)"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def enhance_saturation(self, image: Image.Image, factor: float) -> Image.Image:
        """Adjust color saturation (factor: 0.0 = grayscale, 1.0 = original, 2.0 = twice as saturated)"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    def apply_filter(self, image: Image.Image, filter_name: str) -> Image.Image:
        """Apply predefined filters"""
        filters = {
            'blur': ImageFilter.BLUR,
            'contour': ImageFilter.CONTOUR,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'emboss': ImageFilter.EMBOSS,
            'sharpen': ImageFilter.SHARPEN,
            'smooth': ImageFilter.SMOOTH,
            'gaussian_blur': ImageFilter.GaussianBlur(radius=2),
        }
        
        if filter_name.lower() in filters:
            return image.filter(filters[filter_name.lower()])
        else:
            raise ValueError(f"Unknown filter: {filter_name}")
    
    def add_text_overlay(self, image: Image.Image, text: str, position: Tuple[int, int],
                        font_size: int = 24, color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Add text overlay to image"""
        img_copy = image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
            
        draw.text(position, text, font=font, fill=color)
        return img_copy
    
    def create_blank_canvas(self, width: int, height: int, 
                          color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Create a blank canvas"""
        return Image.new('RGB', (width, height), color)
    
    def composite_images(self, background: Image.Image, overlay: Image.Image,
                        position: Tuple[int, int], opacity: float = 1.0) -> Image.Image:
        """Composite one image over another"""
        bg_copy = background.copy()
        
        if opacity < 1.0:
            # Adjust overlay opacity
            overlay_copy = overlay.copy()
            if overlay_copy.mode != 'RGBA':
                overlay_copy = overlay_copy.convert('RGBA')
            alpha = overlay_copy.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            overlay_copy.putalpha(alpha)
            overlay = overlay_copy
            
        bg_copy.paste(overlay, position, overlay if overlay.mode == 'RGBA' else None)
        return bg_copy


# Example usage and utility functions
class ImageToolkit:
    """High-level interface for common image operations"""
    
    def __init__(self):
        self.handler = ImageHandler()

    def process_for_social_media(self, input_path: str, platform: str = "instagram") -> dict:
        """Process image for various social media platforms and return paths to the optimized images"""
        image = self.handler.import_image(input_path)
        output_dir = Path(input_path).parent / "processed"
        output_dir.mkdir(exist_ok=True)
        base_name = Path(input_path).stem
        results = {}
        
        if platform.lower() == "instagram":
            # Create square, portrait, and landscape versions
            square = self.handler.apply_template(image, StandardSizes.INSTAGRAM_SQUARE)
            portrait = self.handler.apply_template(image, StandardSizes.INSTAGRAM_PORTRAIT)
            landscape = self.handler.apply_template(image, StandardSizes.INSTAGRAM_LANDSCAPE)
            
            square_path = output_dir / f"{base_name}_instagram_square.jpg"
            portrait_path = output_dir / f"{base_name}_instagram_portrait.jpg"
            landscape_path = output_dir / f"{base_name}_instagram_landscape.jpg"
            
            self.handler.export_image(square, square_path, ImageFormat.JPG)
            self.handler.export_image(portrait, portrait_path, ImageFormat.JPG)
            self.handler.export_image(landscape, landscape_path, ImageFormat.JPG)
            
            results["square"] = square_path
            results["portrait"] = portrait_path
            results["landscape"] = landscape_path
            
        elif platform.lower() == "facebook":
            # Create Facebook post image
            post = self.handler.apply_template(image, StandardSizes.FACEBOOK_POST)
            post_path = output_dir / f"{base_name}_facebook_post.jpg"
            self.handler.export_image(post, post_path, ImageFormat.JPG)
            results["post"] = post_path
            
        elif platform.lower() == "twitter":
            # Create Twitter post image
            post = self.handler.apply_template(image, StandardSizes.TWITTER_POST)
            post_path = output_dir / f"{base_name}_twitter_post.jpg"
            self.handler.export_image(post, post_path, ImageFormat.JPG)
            results["post"] = post_path
            
        elif platform.lower() == "linkedin":
            # Create LinkedIn post image
            post = self.handler.apply_template(image, StandardSizes.LINKEDIN_POST)
            post_path = output_dir / f"{base_name}_linkedin_post.jpg"
            self.handler.export_image(post, post_path, ImageFormat.JPG)
            results["post"] = post_path
            
        elif platform.lower() == "youtube":
            # Create YouTube thumbnail
            thumbnail = self.handler.apply_template(image, StandardSizes.YOUTUBE_THUMBNAIL)
            thumbnail_path = output_dir / f"{base_name}_youtube_thumbnail.jpg"
            self.handler.export_image(thumbnail, thumbnail_path, ImageFormat.JPG)
            results["thumbnail"] = thumbnail_path
            
        elif platform.lower() == "all":
            # Process for all platforms
            instagram_results = self.process_for_social_media(input_path, "instagram")
            facebook_results = self.process_for_social_media(input_path, "facebook")
            twitter_results = self.process_for_social_media(input_path, "twitter")
            linkedin_results = self.process_for_social_media(input_path, "linkedin")
            youtube_results = self.process_for_social_media(input_path, "youtube")
            
            results = {
                "instagram": instagram_results,
                "facebook": facebook_results,
                "twitter": twitter_results,
                "linkedin": linkedin_results,
                "youtube": youtube_results
            }
            
        return results
    
    def batch_resize(self, input_dir: str, output_dir: str, width: int = None, 
                   height: int = None, maintain_aspect: bool = True) -> List[Path]:
        """Batch resize images in a directory"""
        
        def resize_operation(handler, image, **kwargs):
            width = kwargs.get('width')
            height = kwargs.get('height')
            maintain_aspect = kwargs.get('maintain_aspect', True)
            
            if maintain_aspect:
                return handler.resize_with_aspect_ratio(image, width, height)
            else:
                return handler.resize_fixed(image, width, height)
        
        return self.handler.batch_process(
            input_dir, 
            output_dir, 
            resize_operation, 
            width=width, 
            height=height, 
            maintain_aspect=maintain_aspect
        )
    
    def batch_convert(self, input_dir: str, output_dir: str, 
                    target_format: ImageFormat = ImageFormat.JPG) -> List[Path]:
        """Batch convert images to a specific format"""
        
        def convert_operation(handler, image, **kwargs):
            return handler.convert_format(image, kwargs.get('target_format'))
        
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        processed_files = []
        
        for file_path in input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', 
                                                                  '.gif', '.bmp', '.tiff', 
                                                                  '.webp', '.heif', '.heic']:
                try:
                    image = self.handler.import_image(file_path)
                    # Get new filename with target extension
                    new_filename = f"{file_path.stem}.{target_format.value.lower()}"
                    output_path = output_dir / new_filename
                    self.handler.export_image(image, output_path, target_format)
                    processed_files.append(output_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
        
        return processed_files
    
    def batch_compress_png(self, input_dir: str, output_dir: str, 
                          compress_level: int = 6, optimize: bool = True, 
                          reduce_colors: bool = False, max_colors: int = 256) -> List[Path]:
        """Batch compress PNG images with advanced options"""
        
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        processed_files = []
        
        for file_path in input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() == '.png':
                try:
                    image = self.handler.import_image(file_path)
                    output_path = output_dir / file_path.name
                    
                    # Apply PNG compression
                    self.handler.export_image(
                        image, 
                        output_path, 
                        ImageFormat.PNG,
                        compress_level=compress_level,
                        optimize=optimize,
                        reduce_colors=reduce_colors,
                        max_colors=max_colors
                    )
                    processed_files.append(output_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
        
        return processed_files
    
    def create_watermark(self, image: Image.Image, text: str, opacity: float = 0.3) -> Image.Image:
        """Add a watermark to an image"""
        # Create a transparent canvas for the watermark
        width, height = image.size
        watermark = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Try to use a nice font, fall back to default if not available
        try:
            font_size = max(width, height) // 20  # Scale font size to image
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text size and position
        text_width, text_height = draw.textsize(text, font)
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw the watermark text
        draw.text((x, y), text, font=font, fill=(255, 255, 255, int(255 * opacity)))
        
        # Convert original image to RGBA if needed
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Combine the images
        watermarked = Image.alpha_composite(image, watermark)
        return watermarked.convert('RGB')  # Convert back to RGB
    
    def create_collage(self, image_paths: List[str], columns: int = 2, spacing: int = 10, 
                     background_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Create a collage from multiple images"""
        images = [self.handler.import_image(path) for path in image_paths]
        
        # Determine thumbnail size (based on the smallest image)
        min_width = min(img.width for img in images)
        min_height = min(img.height for img in images)
        
        # Create thumbnails
        thumbnails = [img.copy().resize((min_width, min_height), Image.Resampling.LANCZOS) 
                     for img in images]
        
        # Calculate rows and final collage size
        rows = (len(thumbnails) + columns - 1) // columns
        collage_width = columns * min_width + (columns + 1) * spacing
        collage_height = rows * min_height + (rows + 1) * spacing
        
        # Create blank canvas
        collage = Image.new('RGB', (collage_width, collage_height), background_color)
        
        # Paste thumbnails into collage
        for i, thumb in enumerate(thumbnails):
            row = i // columns
            col = i % columns
            x = spacing + col * (min_width + spacing)
            y = spacing + row * (min_height + spacing)
            collage.paste(thumb, (x, y))
        
        return collage
    
    def enhance_image(self, image: Image.Image, brightness: float = 1.0, 
                    contrast: float = 1.0, saturation: float = 1.0) -> Image.Image:
        """Apply multiple enhancements to an image"""
        enhanced = image.copy()
        
        if brightness != 1.0:
            enhanced = self.handler.enhance_brightness(enhanced, brightness)
        
        if contrast != 1.0:
            enhanced = self.handler.enhance_contrast(enhanced, contrast)
        
        if saturation != 1.0:
            enhanced = self.handler.enhance_saturation(enhanced, saturation)
        
        return enhanced


# Command-line interface for the tool
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Versatile Image Handling Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Resize command
    resize_parser = subparsers.add_parser("resize", help="Resize an image")
    resize_parser.add_argument("input", help="Input image path")
    resize_parser.add_argument("output", help="Output image path")
    resize_parser.add_argument("--width", type=int, help="Target width")
    resize_parser.add_argument("--height", type=int, help="Target height")
    resize_parser.add_argument("--maintain-aspect", action="store_true", help="Maintain aspect ratio")
    resize_parser.add_argument("--canvas", action="store_true", help="Use canvas to maintain aspect ratio")
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert image format")
    convert_parser.add_argument("input", help="Input image path")
    convert_parser.add_argument("output", help="Output image path")
    convert_parser.add_argument("--format", choices=[f.name for f in ImageFormat], help="Target format")
    
    # Batch resize command
    batch_resize_parser = subparsers.add_parser("batch-resize", help="Batch resize images")
    batch_resize_parser.add_argument("input_dir", help="Input directory")
    batch_resize_parser.add_argument("output_dir", help="Output directory")
    batch_resize_parser.add_argument("--width", type=int, help="Target width")
    batch_resize_parser.add_argument("--height", type=int, help="Target height")
    batch_resize_parser.add_argument("--maintain-aspect", action="store_true", help="Maintain aspect ratio")
    
    # Batch convert command
    batch_convert_parser = subparsers.add_parser("batch-convert", help="Batch convert image formats")
    batch_convert_parser.add_argument("input_dir", help="Input directory")
    batch_convert_parser.add_argument("output_dir", help="Output directory")
    batch_convert_parser.add_argument("--format", choices=[f.name for f in ImageFormat], 
                                    required=True, help="Target format")
    
    # Batch PNG compression command
    batch_compress_parser = subparsers.add_parser("batch-compress-png", help="Batch compress PNG images")
    batch_compress_parser.add_argument("input_dir", help="Input directory")
    batch_compress_parser.add_argument("output_dir", help="Output directory")
    batch_compress_parser.add_argument("--compress-level", type=int, default=6, choices=range(10), 
                                      help="Compression level (0-9, where 9 is maximum compression)")
    batch_compress_parser.add_argument("--optimize", action="store_true", default=True, 
                                      help="Enable optimization")
    batch_compress_parser.add_argument("--reduce-colors", action="store_true", 
                                      help="Reduce colors for better compression")
    batch_compress_parser.add_argument("--max-colors", type=int, default=256, 
                                      help="Maximum number of colors when reducing colors")
    
    # Social media command
    social_parser = subparsers.add_parser("social", help="Optimize for social media")
    social_parser.add_argument("input", help="Input image path")
    social_parser.add_argument("--platform", choices=["instagram", "facebook", "twitter", 
                                                   "linkedin", "youtube", "all"],
                             default="all", help="Target platform")
    
    # Template command
    template_parser = subparsers.add_parser("template", help="Apply size template")
    template_parser.add_argument("input", help="Input image path")
    template_parser.add_argument("output", help="Output image path")
    template_parser.add_argument("--template", choices=[
        "thumbnail", "instagram_square", "instagram_portrait", "instagram_landscape",
        "facebook_post", "twitter_post", "linkedin_post", "youtube_thumbnail",
        "a4_print", "letter_print"
    ], required=True, help="Template to apply")
    
    # Enhance command
    enhance_parser = subparsers.add_parser("enhance", help="Enhance image")
    enhance_parser.add_argument("input", help="Input image path")
    enhance_parser.add_argument("output", help="Output image path")
    enhance_parser.add_argument("--brightness", type=float, default=1.0, help="Brightness factor")
    enhance_parser.add_argument("--contrast", type=float, default=1.0, help="Contrast factor")
    enhance_parser.add_argument("--saturation", type=float, default=1.0, help="Saturation factor")
    enhance_parser.add_argument("--filter", choices=[
        "blur", "contour", "edge_enhance", "emboss", "sharpen", "smooth", "gaussian_blur"
    ], help="Apply filter")
    
    # Collage command
    collage_parser = subparsers.add_parser("collage", help="Create image collage")
    collage_parser.add_argument("output", help="Output collage path")
    collage_parser.add_argument("--inputs", nargs="+", required=True, help="Input image paths")
    collage_parser.add_argument("--columns", type=int, default=2, help="Number of columns")
    collage_parser.add_argument("--spacing", type=int, default=10, help="Spacing between images")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create toolkit instance
    toolkit = ImageToolkit()
    
    try:
        # Handle commands
        if args.command == "resize":
            image = toolkit.handler.import_image(args.input)
            
            if args.canvas:
                resized = toolkit.handler.smart_resize_with_canvas(image, args.width, args.height)
            elif args.maintain_aspect:
                resized = toolkit.handler.resize_with_aspect_ratio(image, args.width, args.height)
            else:
                resized = toolkit.handler.resize_fixed(image, args.width, args.height)
                
            toolkit.handler.export_image(resized, args.output)
            print(f"Resized image saved to {args.output}")
            
        elif args.command == "convert":
            image = toolkit.handler.import_image(args.input)
            if args.format:
                format = ImageFormat[args.format]
            else:
                # Try to infer from output extension
                ext = Path(args.output).suffix.lower()[1:]
                format = next((f for f in ImageFormat if f.name.lower() == ext), ImageFormat.PNG)
                
            toolkit.handler.export_image(image, args.output, format)
            print(f"Converted image saved to {args.output}")
            
        elif args.command == "batch-resize":
            results = toolkit.batch_resize(
                args.input_dir, 
                args.output_dir,
                args.width,
                args.height,
                args.maintain_aspect
            )
            print(f"Batch resize complete. Processed {len(results)} images.")
            
        elif args.command == "batch-convert":
            format = ImageFormat[args.format]
            results = toolkit.batch_convert(args.input_dir, args.output_dir, format)
            print(f"Batch convert complete. Processed {len(results)} images.")
            
        elif args.command == "batch-compress-png":
            results = toolkit.batch_compress_png(
                args.input_dir,
                args.output_dir,
                compress_level=args.compress_level,
                optimize=args.optimize,
                reduce_colors=args.reduce_colors,
                max_colors=args.max_colors
            )
            print(f"Batch PNG compression complete. Processed {len(results)} images.")
            for file_path in results:
                original_size = os.path.getsize(args.input_dir + "/" + file_path.name) if os.path.exists(args.input_dir + "/" + file_path.name) else 0
                compressed_size = os.path.getsize(file_path)
                if original_size > 0:
                    reduction = ((original_size - compressed_size) / original_size) * 100
                    print(f"  {file_path.name}: {original_size:,} → {compressed_size:,} bytes ({reduction:.1f}% reduction)")
            
        elif args.command == "social":
            results = toolkit.process_for_social_media(args.input, args.platform)
            print(f"Social media optimization complete.")
            for platform, paths in results.items():
                if isinstance(paths, dict):
                    print(f"Platform: {platform}")
                    for variant, path in paths.items():
                        print(f"  - {variant}: {path}")
                else:
                    print(f"  - {platform}: {paths}")
                    
        elif args.command == "template":
            image = toolkit.handler.import_image(args.input)
            template_name = args.template.upper()
            template = getattr(StandardSizes, template_name, None)
            
            if not template:
                print(f"Unknown template: {args.template}")
                return
                
            resized = toolkit.handler.apply_template(image, template)
            toolkit.handler.export_image(resized, args.output)
            print(f"Template applied, image saved to {args.output}")
            
        elif args.command == "enhance":
            image = toolkit.handler.import_image(args.input)
            enhanced = toolkit.enhance_image(
                image,
                args.brightness,
                args.contrast,
                args.saturation
            )
            
            if args.filter:
                enhanced = toolkit.handler.apply_filter(enhanced, args.filter)
                
            toolkit.handler.export_image(enhanced, args.output)
            print(f"Enhanced image saved to {args.output}")
            
        elif args.command == "collage":
            collage = toolkit.create_collage(
                args.inputs,
                args.columns,
                args.spacing
            )
            toolkit.handler.export_image(collage, args.output)
            print(f"Collage saved to {args.output}")
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()