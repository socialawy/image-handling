import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkinter.font import Font
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageOps
import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Dict, Any

from image_handling import (
    ImageHandler, ImageToolkit, ImageFormat, StandardSizes,
    ResizeTemplate
)

# Standard size templates for social media
@dataclass
class SizeTemplate:
    width: int
    height: int
    name: str = ""
    description: str = ""

class StandardSizes(Enum):
    # Social Media
    INSTAGRAM_SQUARE = SizeTemplate(1080, 1080, "Instagram Square", "1:1 aspect ratio")
    INSTAGRAM_PORTRAIT = SizeTemplate(1080, 1350, "Instagram Portrait", "4:5 aspect ratio")
    INSTAGRAM_LANDSCAPE = SizeTemplate(1080, 566, "Instagram Landscape", "1.91:1 aspect ratio")
    INSTAGRAM_STORY = SizeTemplate(1080, 1920, "Instagram Story", "9:16 aspect ratio")
    
    FACEBOOK_POST = SizeTemplate(1200, 630, "Facebook Post", "1.91:1 aspect ratio")
    FACEBOOK_COVER = SizeTemplate(820, 312, "Facebook Cover", "2.63:1 aspect ratio")
    FACEBOOK_STORY = SizeTemplate(1080, 1920, "Facebook Story", "9:16 aspect ratio")
    
    TWITTER_POST = SizeTemplate(1200, 675, "Twitter Post", "16:9 aspect ratio")
    TWITTER_HEADER = SizeTemplate(1500, 500, "Twitter Header", "3:1 aspect ratio")
    
    LINKEDIN_POST = SizeTemplate(1200, 627, "LinkedIn Post", "1.91:1 aspect ratio")
    LINKEDIN_COVER = SizeTemplate(1584, 396, "LinkedIn Cover", "4:1 aspect ratio")
    
    YOUTUBE_THUMBNAIL = SizeTemplate(1280, 720, "YouTube Thumbnail", "16:9 aspect ratio")
    YOUTUBE_COVER = SizeTemplate(2560, 1440, "YouTube Cover", "16:9 aspect ratio")
    
    # Print Sizes (in pixels at 300 DPI)
    WALLET = SizeTemplate(900, 600, "Wallet", "2x3 inches")
    CREDIT_CARD = SizeTemplate(1050, 600, "Credit Card", "3.5x2 inches")
    POSTCARD = SizeTemplate(1500, 1050, "Postcard", "5x3.5 inches")
    A5 = SizeTemplate(1748, 2480, "A5", "5.83x8.27 inches")
    A4 = SizeTemplate(2480, 3508, "A4", "8.27x11.69 inches")
    A3 = SizeTemplate(3508, 4961, "A3", "11.69x16.54 inches")
    
    # Common Photo Sizes (in pixels at 300 DPI)
    FOUR_BY_SIX = SizeTemplate(1800, 1200, "4x6", "4x6 inches")
    FIVE_BY_SEVEN = SizeTemplate(2100, 1500, "5x7", "5x7 inches")
    EIGHT_BY_TEN = SizeTemplate(3000, 2400, "8x10", "8x10 inches")
    
    # Screen Resolutions
    HD = SizeTemplate(1280, 720, "HD", "720p")
    FULL_HD = SizeTemplate(1920, 1080, "Full HD", "1080p")
    QHD = SizeTemplate(2560, 1440, "QHD", "1440p")
    UHD_4K = SizeTemplate(3840, 2160, "4K UHD", "2160p")
    
    # Device Screens
    IPHONE_13 = SizeTemplate(1170, 2532, "iPhone 13", "iPhone 13 display")
    IPAD_PRO = SizeTemplate(2048, 2732, "iPad Pro", "12.9-inch iPad Pro")
    MACBOOK_PRO_14 = SizeTemplate(3024, 1964, "MacBook Pro 14")
    
    @classmethod
    def get_all_templates(cls):
        """Return a list of all available size templates"""
        return [t.value for t in cls]

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x800")
        
        self.current_image = None
        self.original_image = None
        self.display_image = None
        self.filename = ""
        
        # Initialize backend handlers
        self.handler = ImageHandler()
        self.toolkit = ImageToolkit()
        
        # Configure styles
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TScale', padding=5)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls with notebook for tabs
        control_frame = ttk.LabelFrame(main_frame, text="Image Controls", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(control_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # File Tab
        file_tab = ttk.Frame(notebook)
        notebook.add(file_tab, text="File")
        
        # File operations
        ttk.Button(file_tab, text="Open Image", command=self.open_image).pack(fill=tk.X, pady=5)
        ttk.Button(file_tab, text="Save Image", command=self.save_image).pack(fill=tk.X, pady=5)
        ttk.Button(file_tab, text="Save As...", command=self.save_as_image).pack(fill=tk.X, pady=5)
        
        # Batch operations
        ttk.Separator(file_tab, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(file_tab, text="Batch Operations").pack(anchor=tk.W)
        ttk.Button(file_tab, text="Batch Resize...", command=self.batch_resize_ui).pack(fill=tk.X, pady=2)
        ttk.Button(file_tab, text="Batch Convert...", command=self.batch_convert_ui).pack(fill=tk.X, pady=2)
        ttk.Button(file_tab, text="Batch Compress PNG...", command=self.batch_compress_png_ui).pack(fill=tk.X, pady=2)
        
        # Edit Tab
        edit_tab = ttk.Frame(notebook)
        notebook.add(edit_tab, text="Edit")
        
        # Adjustments
        ttk.Label(edit_tab, text="Brightness").pack(anchor=tk.W)
        self.brightness = ttk.Scale(edit_tab, from_=0.1, to=2.0, value=1.0, 
                                  command=lambda v: self.adjust_image('brightness', float(v)))
        self.brightness.pack(fill=tk.X, pady=5)
        
        ttk.Label(edit_tab, text="Contrast").pack(anchor=tk.W)
        self.contrast = ttk.Scale(edit_tab, from_=0.1, to=2.0, value=1.0,
                                command=lambda v: self.adjust_image('contrast', float(v)))
        self.contrast.pack(fill=tk.X, pady=5)
        
        ttk.Label(edit_tab, text="Saturation").pack(anchor=tk.W)
        self.saturation = ttk.Scale(edit_tab, from_=0.0, to=2.0, value=1.0,
                                   command=lambda v: self.adjust_image('saturation', float(v)))
        self.saturation.pack(fill=tk.X, pady=5)
        
        # Rotate/Flip
        ttk.Separator(edit_tab, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(edit_tab, text="Rotate/Flip").pack(anchor=tk.W)
        
        rotate_frame = ttk.Frame(edit_tab)
        rotate_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(rotate_frame, text="↺ 90°", command=lambda: self.rotate_image(90)).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(rotate_frame, text="↻ 90°", command=lambda: self.rotate_image(-90)).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(rotate_frame, text="↕ Flip", command=lambda: self.flip_image(Image.FLIP_TOP_BOTTOM)).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(rotate_frame, text="↔ Flip", command=lambda: self.flip_image(Image.FLIP_LEFT_RIGHT)).pack(side=tk.LEFT, padx=2, expand=True)
        
        # Resize options
        ttk.Separator(edit_tab, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(edit_tab, text="Resize").pack(anchor=tk.W)
        
        resize_frame = ttk.Frame(edit_tab)
        resize_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(resize_frame, text="Fixed Size...", command=self.resize_fixed_ui).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(resize_frame, text="Aspect Ratio...", command=self.resize_aspect_ui).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(resize_frame, text="Smart Crop...", command=self.smart_crop_ui).pack(side=tk.LEFT, padx=2, expand=True)
        
        # Filters Tab
        filter_tab = ttk.Frame(notebook)
        notebook.add(filter_tab, text="Filters")
        
        # Basic Filters
        ttk.Label(filter_tab, text="Basic Filters").pack(anchor=tk.W)
        
        filter_frame1 = ttk.Frame(filter_tab)
        filter_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame1, text="Blur", command=lambda: self.apply_filter(ImageFilter.BLUR)).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(filter_frame1, text="Sharpen", command=lambda: self.apply_filter(ImageFilter.SHARPEN)).pack(side=tk.LEFT, padx=2, expand=True)
        
        filter_frame2 = ttk.Frame(filter_tab)
        filter_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame2, text="Emboss", command=lambda: self.apply_filter(ImageFilter.EMBOSS)).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(filter_frame2, text="Contour", command=lambda: self.apply_filter(ImageFilter.CONTOUR)).pack(side=tk.LEFT, padx=2, expand=True)
        
        # Advanced Filters
        ttk.Separator(filter_tab, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(filter_tab, text="Advanced Filters").pack(anchor=tk.W)
        
        filter_frame3 = ttk.Frame(filter_tab)
        filter_frame3.pack(fill=tk.X, pady=5)
        
        ttk.Button(filter_frame3, text="Grayscale", command=self.apply_grayscale).pack(side=tk.LEFT, padx=2, expand=True)
        ttk.Button(filter_frame3, text="Sepia", command=self.apply_sepia).pack(side=tk.LEFT, padx=2, expand=True)
        
        # Social Media Tab
        social_tab = ttk.Frame(notebook)
        notebook.add(social_tab, text="Social Media")
        
        ttk.Label(social_tab, text="Optimize for:").pack(anchor=tk.W, pady=(5, 0))
        
        social_frame = ttk.Frame(social_tab)
        social_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(social_frame, text="Instagram", 
                  command=lambda: self.optimize_for_social("instagram")).pack(fill=tk.X, pady=2)
        ttk.Button(social_frame, text="Facebook", 
                  command=lambda: self.optimize_for_social("facebook")).pack(fill=tk.X, pady=2)
        ttk.Button(social_frame, text="Twitter", 
                  command=lambda: self.optimize_for_social("twitter")).pack(fill=tk.X, pady=2)
        ttk.Button(social_frame, text="LinkedIn", 
                  command=lambda: self.optimize_for_social("linkedin")).pack(fill=tk.X, pady=2)
        ttk.Button(social_frame, text="YouTube", 
                  command=lambda: self.optimize_for_social("youtube")).pack(fill=tk.X, pady=2)
        
        # Tools Tab
        tools_tab = ttk.Frame(notebook)
        notebook.add(tools_tab, text="Tools")
        
        ttk.Button(tools_tab, text="Add Watermark", command=self.add_watermark_ui).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Add Text Overlay", command=self.add_text_overlay_ui).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Crop Image", command=self.start_crop).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Resize Canvas", command=self.resize_canvas_ui).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Convert Format", command=self.convert_format_ui).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Create Collage...", command=self.create_collage_ui).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Create Blank Canvas...", command=self.create_blank_canvas_ui).pack(fill=tk.X, pady=2)
        ttk.Button(tools_tab, text="Composite Images...", command=self.composite_images_ui).pack(fill=tk.X, pady=2)
        
        # Reset button at the bottom
        ttk.Button(control_frame, text="Reset All Changes", command=self.reset_image, style='Accent.TButton').pack(fill=tk.X, pady=10)
        
        # Right panel - Image display
        self.image_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, width=800, height=600)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.image_frame.pack_propagate(False)
        
        # Canvas for image display
        self.canvas = tk.Canvas(self.image_frame, bg='#f0f0f0', cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initialize crop rectangle
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        # Bind mouse events for cropping
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_image(self):
        filetypes = [
            ('Image files', '*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.heif *.heic *.svg'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            try:
                self.filename = filename
                self.original_image = self.handler.import_image(filename)
                self.current_image = self.original_image.copy()
                self.display_image_on_canvas()
                self.status_var.set(f"Opened: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def save_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save!")
            return
            
        if not self.filename:
            self.save_as_image()
            return
            
        try:
            self.handler.export_image(self.current_image, self.filename)
            self.status_var.set(f"Saved: {os.path.basename(self.filename)}")
            messagebox.showinfo("Success", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def display_image_on_canvas(self):
        if not self.current_image:
            return
            
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:  # Canvas not yet rendered
            canvas_width = 800
            canvas_height = 600
        
        # Calculate aspect ratio
        img_width, img_height = self.current_image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio * 0.9)  # 90% of available space
        new_height = int(img_height * ratio * 0.9)
        
        # Resize image
        resized_img = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.display_image = ImageTk.PhotoImage(resized_img)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.display_image)
        
        # Store canvas position and scale for cropping
        self.canvas_x = x
        self.canvas_y = y
        self.canvas_scale = ratio * 0.9  # Same scale factor used for resizing
    
    def adjust_image(self, adjustment, value):
        if not self.current_image or not self.original_image:
            return
            
        # Start from original image
        self.current_image = self.original_image.copy()
        
        # Apply adjustments using backend handlers
        if adjustment == 'brightness' and value != 1.0:
            self.current_image = self.handler.enhance_brightness(self.current_image, value)
        elif adjustment == 'contrast' and value != 1.0:
            self.current_image = self.handler.enhance_contrast(self.current_image, value)
        elif adjustment == 'saturation' and value != 1.0:
            self.current_image = self.handler.enhance_saturation(self.current_image, value)
        
        self.display_image_on_canvas()
    
    def apply_filter(self, filter_type):
        if not self.current_image:
            return
            
        try:
            filter_name = filter_type.__name__.lower()
            self.current_image = self.handler.apply_filter(self.current_image, filter_name)
            self.display_image_on_canvas()
            self.status_var.set(f"Applied filter: {filter_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.brightness.set(1.0)
            self.contrast.set(1.0)
            self.saturation.set(1.0)
            self.display_image_on_canvas()
            self.status_var.set("Image reset to original")
            
    def rotate_image(self, degrees):
        if self.current_image:
            self.current_image = self.current_image.rotate(degrees, expand=True)
            self.display_image_on_canvas()
            self.status_var.set(f"Rotated image by {degrees}°")
    
    def flip_image(self, mode):
        if self.current_image:
            self.current_image = self.current_image.transpose(mode)
            self.display_image_on_canvas()
            flip_text = "Flipped vertically" if mode == Image.FLIP_TOP_BOTTOM else "Flipped horizontally"
            self.status_var.set(flip_text)
    
    def apply_grayscale(self):
        if self.current_image:
            self.current_image = self.current_image.convert('L').convert('RGB')
            self.display_image_on_canvas()
            self.status_var.set("Applied grayscale filter")
    
    def apply_sepia(self):
        if self.current_image:
            # Convert to grayscale first
            grayscale = self.current_image.convert('L')
            # Create sepia palette
            sepia = Image.new('RGB', grayscale.size)
            width, height = grayscale.size
            
            # Apply sepia tone
            for x in range(width):
                for y in range(height):
                    r, g, b = grayscale.getpixel((x, y)), grayscale.getpixel((x, y)), grayscale.getpixel((x, y))
                    tr = int(r * 0.393 + g * 0.769 + b * 0.189)
                    tg = int(r * 0.349 + g * 0.686 + b * 0.168)
                    tb = int(r * 0.272 + g * 0.534 + b * 0.131)
                    sepia.putpixel((x, y), (min(255, tr), min(255, tg), min(255, tb)))
            
            self.current_image = sepia
            self.display_image_on_canvas()
            self.status_var.set("Applied sepia filter")
    
    def optimize_for_social(self, platform):
        if not self.current_image:
            return
            
        try:
            results = self.toolkit.process_for_social_media(self.filename, platform)
            
            # Update current image with the first result
            if results:
                first_result = next(iter(results.values()))
                if isinstance(first_result, dict):
                    first_result = next(iter(first_result.values()))
                self.current_image = self.handler.import_image(first_result)
                self.display_image_on_canvas()
                self.status_var.set(f"Optimized for {platform.capitalize()}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def add_watermark_ui(self):
        if not self.current_image:
            return
            
        try:
            # Create a dialog to get watermark text, font size, and opacity
            watermark_dialog = tk.Toplevel(self.root)
            watermark_dialog.title("Add Watermark")
            watermark_dialog.transient(self.root)
            watermark_dialog.grab_set()

            ttk.Label(watermark_dialog, text="Watermark Text:").pack(padx=10, pady=5)
            text_entry = ttk.Entry(watermark_dialog, width=40)
            text_entry.pack(padx=10, pady=2)

            ttk.Label(watermark_dialog, text="Font Size:").pack(padx=10, pady=5)
            font_size_var = tk.StringVar(value="36")
            font_size_entry = ttk.Entry(watermark_dialog, textvariable=font_size_var, width=10)
            font_size_entry.pack(padx=10, pady=2)

            ttk.Label(watermark_dialog, text="Opacity (0.0 - 1.0):").pack(padx=10, pady=5)
            opacity_var = tk.StringVar(value="0.5") # Default to 50% opacity
            opacity_entry = ttk.Entry(watermark_dialog, textvariable=opacity_var, width=10)
            opacity_entry.pack(padx=10, pady=2)

            # Position inputs
            ttk.Label(watermark_dialog, text="Position (X, Y):").pack(padx=10, pady=5)
            pos_frame = ttk.Frame(watermark_dialog)
            pos_frame.pack(fill=tk.X, padx=10)

            x_var = tk.StringVar(value="10")
            y_var = tk.StringVar(value="10")
            ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
            ttk.Entry(pos_frame, textvariable=x_var, width=5).pack(side=tk.LEFT, padx=5)
            ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
            ttk.Entry(pos_frame, textvariable=y_var, width=5).pack(side=tk.LEFT, padx=5)

            def apply_watermark():
                try:
                    text = text_entry.get()
                    if not text:
                        messagebox.showerror("Error", "Watermark text cannot be empty.")
                        return

                    font_size = int(font_size_var.get())
                    opacity = float(opacity_var.get())
                    pos_x = int(x_var.get())
                    pos_y = int(y_var.get())

                    if not (0.0 <= opacity <= 1.0):
                        messagebox.showerror("Error", "Opacity must be between 0.0 and 1.0.")
                        return

                    # Convert current image to RGBA to support transparency if it's not already
                    original_mode = self.current_image.mode
                    if original_mode != 'RGBA':
                        temp_image = self.current_image.convert('RGBA')
                    else:
                        temp_image = self.current_image.copy()

                    # Create a drawing context on the temporary RGBA image
                    draw = ImageDraw.Draw(temp_image)
                    
                    # Use a default font (you might want to provide a font file for better results)
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    
                    # Add text with semi-transparent white, using user-defined opacity
                    fill_color = (255, 255, 255, int(255 * opacity))
                    draw.text((pos_x, pos_y), text, font=font, fill=fill_color)
                    
                    # Convert back to original mode if it was not RGBA
                    if original_mode != 'RGBA':
                        self.current_image = temp_image.convert(original_mode)
                    else:
                        self.current_image = temp_image

                    self.display_image_on_canvas()
                    self.status_var.set("Watermark added")
                    watermark_dialog.destroy()
                    
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid numbers for Font Size, Opacity, X, and Y.")
                except Exception as e:
                    self.status_var.set(f"Error adding watermark: {str(e)}")
                    messagebox.showerror("Error", f"Failed to add watermark: {str(e)}")

            ttk.Button(watermark_dialog, text="Apply Watermark", command=apply_watermark).pack(pady=10)
            
        except Exception as e:
            self.status_var.set(f"Error adding watermark: {str(e)}")
            messagebox.showerror("Error", f"Failed to add watermark: {str(e)}")
    
    def start_crop(self):
        if not self.current_image:
            return
        self.cropping = True
        self.status_var.set("Drag to select area to crop. Right-click to cancel.")
    
    def on_mouse_down(self, event):
        if hasattr(self, 'cropping') and self.cropping:
            self.start_x = event.x
            self.start_y = event.y
            
            # Delete previous rectangle if exists
            if self.rect:
                self.canvas.delete(self.rect)
            
            # Create new rectangle
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, 
                self.start_x, self.start_y,
                outline='red', width=2, dash=(5, 5)
            )
    
    def on_mouse_drag(self, event):
        if hasattr(self, 'cropping') and self.cropping and self.rect:
            # Update rectangle coordinates
            self.canvas.coords(
                self.rect, 
                self.start_x, self.start_y, 
                event.x, event.y
            )
    
    def on_mouse_up(self, event):
        if hasattr(self, 'cropping') and self.cropping and self.rect:
            # Get final coordinates
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            
            # Ensure x1,y1 is top-left and x2,y2 is bottom-right
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            
            # Convert to image coordinates (accounting for canvas padding)
            img_x1 = int((x1 - self.canvas_x) / self.canvas_scale)
            img_y1 = int((y1 - self.canvas_y) / self.canvas_scale)
            img_x2 = int((x2 - self.canvas_x) / self.canvas_scale)
            img_y2 = int((y2 - self.canvas_y) / self.canvas_scale)
            
            # Ensure coordinates are within image bounds
            img_x1 = max(0, min(img_x1, self.current_image.width))
            img_y1 = max(0, min(img_y1, self.current_image.height))
            img_x2 = max(0, min(img_x2, self.current_image.width))
            img_y2 = max(0, min(img_y2, self.current_image.height))
            
            # Only crop if we have a valid selection
            if abs(img_x2 - img_x1) > 10 and abs(img_y2 - img_y1) > 10:
                try:
                    self.current_image = self.current_image.crop((img_x1, img_y1, img_x2, img_y2))
                    self.display_image_on_canvas()
                    self.status_var.set("Image cropped")
                except Exception as e:
                    self.status_var.set(f"Error cropping: {str(e)}")
            
            # Clean up
            self.canvas.delete(self.rect)
            self.rect = None
            self.cropping = False
    
    def resize_canvas_ui(self):
        if not self.current_image:
            return
            
        # Create a dialog to get new dimensions
        width = simpledialog.askinteger("Resize Canvas", "New width:", 
                                      initialvalue=self.current_image.width)
        if not width:
            return
            
        height = simpledialog.askinteger("Resize Canvas", "New height:", 
                                       initialvalue=self.current_image.height)
        if not height:
            return
            
        try:
            self.current_image = self.handler.smart_resize_with_canvas(
                self.current_image, width, height
            )
            self.display_image_on_canvas()
            self.status_var.set(f"Canvas resized to {width}x{height}")
            
        except Exception as e:
            self.status_var.set(f"Error resizing canvas: {str(e)}")
    
    def convert_format_ui(self):
        if not self.current_image:
            return
            
        # Create a dialog to select format
        format_win = tk.Toplevel(self.root)
        format_win.title("Convert Format")
        format_win.transient(self.root)
        format_win.grab_set()
        
        ttk.Label(format_win, text="Select output format:").pack(padx=10, pady=5)
        
        format_var = tk.StringVar(value="JPEG")
        formats = [(f.name, f.name) for f in ImageFormat]
        
        for text, value in formats:
            ttk.Radiobutton(format_win, text=text, variable=format_var, value=value).pack(anchor=tk.W, padx=20)
        
        def convert():
            try:
                format = ImageFormat[format_var.get()]
                self.current_image = self.handler.convert_format(self.current_image, format)
                self.status_var.set(f"Converted to {format.name}")
                format_win.destroy()
                self.display_image_on_canvas()
                
            except Exception as e:
                self.status_var.set(f"Error converting format: {str(e)}")
        
        ttk.Button(format_win, text="Convert", command=convert).pack(pady=10)
    
    def save_as_image(self):
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save!")
            return
            
        filetypes = [
            ('JPEG', '*.jpg;*.jpeg'),
            ('PNG', '*.png'),
            ('BMP', '*.bmp'),
            ('GIF', '*.gif'),
            ('TIFF', '*.tif;*.tiff'),
            ('WEBP', '*.webp'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=filetypes,
            initialfile=os.path.splitext(os.path.basename(getattr(self, 'filename', 'untitled')))[0] + "_edited"
        )
        
        if filename:
            try:
                # Get format from extension
                ext = os.path.splitext(filename)[1].lower()
                format = ImageFormat[ext[1:].upper()] if ext[1:].upper() in ImageFormat.__members__ else ImageFormat.JPG
                
                # If PNG, show compression options dialog
                if format == ImageFormat.PNG:
                    if not self.show_png_compression_dialog():
                        return  # User cancelled compression dialog
                    
                    # Use compression settings
                    settings = self.png_compress_settings
                    self.handler.export_image(
                        self.current_image, 
                        filename, 
                        format,
                        compress_level=settings['compress_level'].get(),
                        optimize=settings['optimize'].get(),
                        reduce_colors=settings['reduce_colors'].get(),
                        max_colors=settings['max_colors'].get()
                    )
                    # Clear settings after use
                    self.png_compress_settings = None
                else:
                    self.handler.export_image(self.current_image, filename, format)
                self.filename = filename
                self.status_var.set(f"Saved: {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Image saved successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                self.status_var.set(f"Error saving image: {str(e)}")

    def show_png_compression_dialog(self):
        """Show PNG compression options dialog"""
        compress_win = tk.Toplevel(self.root)
        compress_win.title("PNG Compression Options")
        compress_win.transient(self.root)
        compress_win.grab_set()
        
        # Compression options frame
        options_frame = ttk.Frame(compress_win)
        options_frame.pack(padx=20, pady=20)
        
        # Compression level
        ttk.Label(options_frame, text="Compression Level (0-9):").grid(row=0, column=0, sticky=tk.W, pady=5)
        compress_level_var = tk.IntVar(value=6)
        compress_level_scale = ttk.Scale(options_frame, from_=0, to=9, variable=compress_level_var, 
                                       orient=tk.HORIZONTAL, length=200)
        compress_level_scale.grid(row=0, column=1, padx=10)
        compress_level_label = ttk.Label(options_frame, text="6 (Medium)")
        compress_level_label.grid(row=0, column=2)
        
        def update_compress_label(value):
            compress_level_label.config(text=f"{int(float(value))} ({'Fastest' if int(float(value)) == 0 else 'Best' if int(float(value)) == 9 else 'Medium'})")
        
        compress_level_scale.config(command=update_compress_label)
        
        # Optimization checkbox
        optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enable optimization", variable=optimize_var).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Color reduction options
        reduce_colors_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Reduce colors for better compression", 
                       variable=reduce_colors_var).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Max colors (disabled by default)
        colors_frame = ttk.Frame(options_frame)
        colors_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Label(colors_frame, text="Max colors:").pack(side=tk.LEFT)
        max_colors_var = tk.IntVar(value=256)
        max_colors_spin = ttk.Spinbox(colors_frame, from_=2, to=256, textvariable=max_colors_var, width=10)
        max_colors_spin.pack(side=tk.LEFT, padx=5)
        
        def toggle_colors_options():
            if reduce_colors_var.get():
                max_colors_spin.config(state='normal')
            else:
                max_colors_spin.config(state='disabled')
        
        reduce_colors_var.trace('w', lambda *args: toggle_colors_options())
        toggle_colors_options()  # Set initial state
        
        # Store compression settings for later use
        self.png_compress_settings = {
            'compress_level': compress_level_var,
            'optimize': optimize_var,
            'reduce_colors': reduce_colors_var,
            'max_colors': max_colors_var
        }
        
        # Buttons
        button_frame = ttk.Frame(compress_win)
        button_frame.pack(pady=10)
        
        def on_save():
            compress_win.destroy()
        
        def on_cancel():
            compress_win.destroy()
            self.png_compress_settings = None
        
        ttk.Button(button_frame, text="Save", command=on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Wait for dialog to close
        compress_win.wait_window()
        
        # Return True if user wants to save, False if cancelled
        return hasattr(self, 'png_compress_settings') and self.png_compress_settings is not None

    def batch_resize_ui(self):
        # Create a dialog for batch resize
        resize_win = tk.Toplevel(self.root)
        resize_win.title("Batch Resize")
        resize_win.transient(self.root)
        resize_win.grab_set()
        
        # Input directory
        ttk.Label(resize_win, text="Input Directory:").pack(padx=10, pady=5)
        input_dir_var = tk.StringVar()
        ttk.Entry(resize_win, textvariable=input_dir_var, width=40).pack(padx=10)
        ttk.Button(resize_win, text="Browse...", 
                  command=lambda: input_dir_var.set(filedialog.askdirectory())).pack(pady=5)
        
        # Output directory
        ttk.Label(resize_win, text="Output Directory:").pack(padx=10, pady=5)
        output_dir_var = tk.StringVar()
        ttk.Entry(resize_win, textvariable=output_dir_var, width=40).pack(padx=10)
        ttk.Button(resize_win, text="Browse...", 
                  command=lambda: output_dir_var.set(filedialog.askdirectory())).pack(pady=5)
        
        # Dimensions
        ttk.Label(resize_win, text="Dimensions:").pack(padx=10, pady=5)
        dim_frame = ttk.Frame(resize_win)
        dim_frame.pack(fill=tk.X, padx=10)
        
        width_var = tk.StringVar()
        height_var = tk.StringVar()
        ttk.Label(dim_frame, text="Width:").pack(side=tk.LEFT)
        ttk.Entry(dim_frame, textvariable=width_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(dim_frame, text="Height:").pack(side=tk.LEFT)
        ttk.Entry(dim_frame, textvariable=height_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Options
        maintain_aspect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(resize_win, text="Maintain Aspect Ratio", 
                       variable=maintain_aspect_var).pack(padx=10, pady=5)
        
        def process():
            try:
                input_dir = input_dir_var.get()
                output_dir = output_dir_var.get()
                width = int(width_var.get()) if width_var.get() else None
                height = int(height_var.get()) if height_var.get() else None
                
                if not input_dir or not output_dir:
                    messagebox.showerror("Error", "Please select input and output directories")
                    return
                
                results = self.toolkit.batch_resize(
                    input_dir, output_dir, width, height, maintain_aspect_var.get()
                )
                
                messagebox.showinfo("Success", f"Processed {len(results)} images")
                resize_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(resize_win, text="Process", command=process).pack(pady=10)

    def batch_convert_ui(self):
        # Create a dialog for batch convert
        convert_win = tk.Toplevel(self.root)
        convert_win.title("Batch Convert")
        convert_win.transient(self.root)
        convert_win.grab_set()
        
        # Input directory
        ttk.Label(convert_win, text="Input Directory:").pack(padx=10, pady=5)
        input_dir_var = tk.StringVar()
        ttk.Entry(convert_win, textvariable=input_dir_var, width=40).pack(padx=10)
        ttk.Button(convert_win, text="Browse...", 
                  command=lambda: input_dir_var.set(filedialog.askdirectory())).pack(pady=5)
        
        # Output directory
        ttk.Label(convert_win, text="Output Directory:").pack(padx=10, pady=5)
        output_dir_var = tk.StringVar()
        ttk.Entry(convert_win, textvariable=output_dir_var, width=40).pack(padx=10)
        ttk.Button(convert_win, text="Browse...", 
                  command=lambda: output_dir_var.set(filedialog.askdirectory())).pack(pady=5)
        
        # Format selection
        ttk.Label(convert_win, text="Target Format:").pack(padx=10, pady=5)
        format_var = tk.StringVar(value="JPEG")
        for format in ImageFormat:
            ttk.Radiobutton(convert_win, text=format.name, variable=format_var, 
                           value=format.name).pack(anchor=tk.W, padx=20)
        
        def process():
            try:
                input_dir = input_dir_var.get()
                output_dir = output_dir_var.get()
                format = ImageFormat[format_var.get()]
                
                if not input_dir or not output_dir:
                    messagebox.showerror("Error", "Please select input and output directories")
                    return
                
                results = self.toolkit.batch_convert(input_dir, output_dir, format)
                
                messagebox.showinfo("Success", f"Processed {len(results)} images")
                convert_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(convert_win, text="Process", command=process).pack(pady=10)

    def batch_compress_png_ui(self):
        # Create a dialog for batch PNG compression
        compress_win = tk.Toplevel(self.root)
        compress_win.title("Batch Compress PNG")
        compress_win.transient(self.root)
        compress_win.grab_set()
        
        # Input directory
        ttk.Label(compress_win, text="Input Directory:").pack(padx=10, pady=5)
        input_dir_var = tk.StringVar()
        ttk.Entry(compress_win, textvariable=input_dir_var, width=40).pack(padx=10)
        ttk.Button(compress_win, text="Browse...", 
                  command=lambda: input_dir_var.set(filedialog.askdirectory())).pack(pady=5)
        
        # Output directory
        ttk.Label(compress_win, text="Output Directory:").pack(padx=10, pady=5)
        output_dir_var = tk.StringVar()
        ttk.Entry(compress_win, textvariable=output_dir_var, width=40).pack(padx=10)
        ttk.Button(compress_win, text="Browse...", 
                  command=lambda: output_dir_var.set(filedialog.askdirectory())).pack(pady=5)
        
        # Compression options frame
        options_frame = ttk.LabelFrame(compress_win, text="Compression Options")
        options_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Compression level
        ttk.Label(options_frame, text="Compression Level (0-9):").pack(anchor=tk.W, padx=10, pady=2)
        compress_level_var = tk.IntVar(value=6)
        compress_level_scale = ttk.Scale(options_frame, from_=0, to=9, variable=compress_level_var, 
                                       orient=tk.HORIZONTAL)
        compress_level_scale.pack(padx=10, fill=tk.X)
        compress_level_label = ttk.Label(options_frame, text="6 (Medium)")
        compress_level_label.pack(padx=10)
        
        def update_compress_label(value):
            compress_level_label.config(text=f"{int(float(value))} ({'Fastest' if int(float(value)) == 0 else 'Best' if int(float(value)) == 9 else 'Medium'})")
        
        compress_level_scale.config(command=update_compress_label)
        
        # Optimization checkbox
        optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enable optimization", variable=optimize_var).pack(anchor=tk.W, padx=10, pady=5)
        
        # Color reduction options
        reduce_colors_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Reduce colors for better compression", 
                       variable=reduce_colors_var).pack(anchor=tk.W, padx=10, pady=5)
        
        # Max colors (disabled by default)
        colors_frame = ttk.Frame(options_frame)
        colors_frame.pack(padx=10, fill=tk.X)
        ttk.Label(colors_frame, text="Max colors:").pack(side=tk.LEFT)
        max_colors_var = tk.IntVar(value=256)
        max_colors_spin = ttk.Spinbox(colors_frame, from_=2, to=256, textvariable=max_colors_var, width=10)
        max_colors_spin.pack(side=tk.LEFT, padx=5)
        
        def toggle_colors_options():
            if reduce_colors_var.get():
                max_colors_spin.config(state='normal')
            else:
                max_colors_spin.config(state='disabled')
        
        reduce_colors_var.trace('w', lambda *args: toggle_colors_options())
        toggle_colors_options()  # Set initial state
        
        def process():
            try:
                input_dir = input_dir_var.get()
                output_dir = output_dir_var.get()
                
                if not input_dir or not output_dir:
                    messagebox.showerror("Error", "Please select input and output directories")
                    return
                
                results = self.toolkit.batch_compress_png(
                    input_dir,
                    output_dir,
                    compress_level=compress_level_var.get(),
                    optimize=optimize_var.get(),
                    reduce_colors=reduce_colors_var.get(),
                    max_colors=max_colors_var.get()
                )
                
                # Show compression results
                result_msg = f"Processed {len(results)} PNG images\n\n"
                total_original = 0
                total_compressed = 0
                
                for file_path in results:
                    original_path = os.path.join(input_dir, file_path.name)
                    if os.path.exists(original_path):
                        original_size = os.path.getsize(original_path)
                        compressed_size = os.path.getsize(file_path)
                        reduction = ((original_size - compressed_size) / original_size) * 100
                        result_msg += f"{file_path.name}: {original_size:,} → {compressed_size:,} bytes ({reduction:.1f}% reduction)\n"
                        total_original += original_size
                        total_compressed += compressed_size
                
                if total_original > 0:
                    total_reduction = ((total_original - total_compressed) / total_original) * 100
                    result_msg += f"\nTotal: {total_original:,} → {total_compressed:,} bytes ({total_reduction:.1f}% reduction)"
                
                messagebox.showinfo("Compression Complete", result_msg)
                compress_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(compress_win, text="Compress", command=process).pack(pady=10)

    def resize_fixed_ui(self):
        if not self.current_image:
            return
            
        # Create a dialog to get new dimensions
        width = simpledialog.askinteger("Resize", "New width:", 
                                      initialvalue=self.current_image.width)
        if not width:
            return
            
        height = simpledialog.askinteger("Resize", "New height:", 
                                       initialvalue=self.current_image.height)
        if not height:
            return
            
        try:
            self.current_image = self.handler.resize_fixed(self.current_image, width, height)
            self.display_image_on_canvas()
            self.status_var.set(f"Resized to {width}x{height}")
            
        except Exception as e:
            self.status_var.set(f"Error resizing: {str(e)}")

    def resize_aspect_ui(self):
        if not self.current_image:
            return
            
        # Create a dialog to get new dimensions
        width = simpledialog.askinteger("Resize with Aspect Ratio", "New width (0 to maintain):", 
                                      initialvalue=self.current_image.width)
        if width is None:
            return
            
        height = simpledialog.askinteger("Resize with Aspect Ratio", "New height (0 to maintain):", 
                                       initialvalue=self.current_image.height)
        if height is None:
            return
            
        try:
            width = width if width > 0 else None
            height = height if height > 0 else None
            self.current_image = self.handler.resize_with_aspect_ratio(self.current_image, width, height)
            self.display_image_on_canvas()
            self.status_var.set("Resized while maintaining aspect ratio")
            
        except Exception as e:
            self.status_var.set(f"Error resizing: {str(e)}")

    def smart_crop_ui(self):
        if not self.current_image:
            return
            
        # Create a dialog to get new dimensions
        width = simpledialog.askinteger("Smart Crop", "Target width:", 
                                      initialvalue=self.current_image.width)
        if not width:
            return
            
        height = simpledialog.askinteger("Smart Crop", "Target height:", 
                                       initialvalue=self.current_image.height)
        if not height:
            return
            
        try:
            self.current_image = self.handler.smart_crop(self.current_image, width, height)
            self.display_image_on_canvas()
            self.status_var.set(f"Smart cropped to {width}x{height}")
            
        except Exception as e:
            self.status_var.set(f"Error cropping: {str(e)}")

    def create_collage_ui(self):
        # Create a dialog for collage creation
        collage_win = tk.Toplevel(self.root)
        collage_win.title("Create Collage")
        collage_win.transient(self.root)
        collage_win.grab_set()
        
        # Image selection
        ttk.Label(collage_win, text="Select Images:").pack(padx=10, pady=5)
        image_list = []
        
        def add_images():
            files = filedialog.askopenfilenames(
                filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp')]
            )
            if files:
                image_list.extend(files)
                update_list()
        
        def update_list():
            listbox.delete(0, tk.END)
            for img in image_list:
                listbox.insert(tk.END, os.path.basename(img))
        
        ttk.Button(collage_win, text="Add Images...", command=add_images).pack(pady=5)
        
        listbox = tk.Listbox(collage_win, height=6)
        listbox.pack(fill=tk.X, padx=10, pady=5)
        
        # Options
        ttk.Label(collage_win, text="Options:").pack(padx=10, pady=5)
        
        columns_var = tk.StringVar(value="2")
        ttk.Label(collage_win, text="Columns:").pack(anchor=tk.W, padx=20)
        ttk.Entry(collage_win, textvariable=columns_var, width=10).pack(anchor=tk.W, padx=20)
        
        spacing_var = tk.StringVar(value="10")
        ttk.Label(collage_win, text="Spacing:").pack(anchor=tk.W, padx=20)
        ttk.Entry(collage_win, textvariable=spacing_var, width=10).pack(anchor=tk.W, padx=20)
        
        def process():
            try:
                if not image_list:
                    messagebox.showerror("Error", "Please add images first")
                    return
                
                columns = int(columns_var.get())
                spacing = int(spacing_var.get())
                
                # Create collage
                collage = self.toolkit.create_collage(image_list, columns, spacing)
                
                # Save collage
                filename = filedialog.asksaveasfilename(
                    defaultextension=".jpg",
                    filetypes=[('JPEG', '*.jpg'), ('PNG', '*.png')],
                    initialfile="collage.jpg"
                )
                
                if filename:
                    self.handler.export_image(collage, filename)
                    messagebox.showinfo("Success", "Collage created successfully!")
                    collage_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(collage_win, text="Create Collage", command=process).pack(pady=10)

    def add_text_overlay_ui(self):
        if not self.current_image:
            return
            
        # Create a dialog for text overlay
        text_win = tk.Toplevel(self.root)
        text_win.title("Add Text Overlay")
        text_win.transient(self.root)
        text_win.grab_set()
        
        # Text input
        ttk.Label(text_win, text="Text:").pack(padx=10, pady=5)
        text_var = tk.StringVar()
        ttk.Entry(text_win, textvariable=text_var, width=40).pack(padx=10)
        
        # Font size
        ttk.Label(text_win, text="Font Size:").pack(padx=10, pady=5)
        size_var = tk.StringVar(value="24")
        ttk.Entry(text_win, textvariable=size_var, width=10).pack(padx=10)
        
        # Position
        ttk.Label(text_win, text="Position:").pack(padx=10, pady=5)
        pos_frame = ttk.Frame(text_win)
        pos_frame.pack(fill=tk.X, padx=10)
        
        x_var = tk.StringVar(value="10")
        y_var = tk.StringVar(value="10")
        ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
        ttk.Entry(pos_frame, textvariable=x_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
        ttk.Entry(pos_frame, textvariable=y_var, width=5).pack(side=tk.LEFT, padx=5)
        
        def add_text():
            try:
                text = text_var.get()
                font_size = int(size_var.get())
                x = int(x_var.get())
                y = int(y_var.get())
                
                self.current_image = self.handler.add_text_overlay(
                    self.current_image, text, (x, y), font_size
                )
                self.display_image_on_canvas()
                self.status_var.set("Text overlay added")
                text_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(text_win, text="Add Text", command=add_text).pack(pady=10)

    def create_blank_canvas_ui(self):
        # Create a dialog for blank canvas
        canvas_win = tk.Toplevel(self.root)
        canvas_win.title("Create Blank Canvas")
        canvas_win.transient(self.root)
        canvas_win.grab_set()
        
        # Dimensions
        ttk.Label(canvas_win, text="Dimensions:").pack(padx=10, pady=5)
        dim_frame = ttk.Frame(canvas_win)
        dim_frame.pack(fill=tk.X, padx=10)
        
        width_var = tk.StringVar(value="800")
        height_var = tk.StringVar(value="600")
        ttk.Label(dim_frame, text="Width:").pack(side=tk.LEFT)
        ttk.Entry(dim_frame, textvariable=width_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(dim_frame, text="Height:").pack(side=tk.LEFT)
        ttk.Entry(dim_frame, textvariable=height_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Color
        ttk.Label(canvas_win, text="Background Color (RGB):").pack(padx=10, pady=5)
        color_frame = ttk.Frame(canvas_win)
        color_frame.pack(fill=tk.X, padx=10)
        
        r_var = tk.StringVar(value="255")
        g_var = tk.StringVar(value="255")
        b_var = tk.StringVar(value="255")
        ttk.Label(color_frame, text="R:").pack(side=tk.LEFT)
        ttk.Entry(color_frame, textvariable=r_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(color_frame, text="G:").pack(side=tk.LEFT)
        ttk.Entry(color_frame, textvariable=g_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(color_frame, text="B:").pack(side=tk.LEFT)
        ttk.Entry(color_frame, textvariable=b_var, width=5).pack(side=tk.LEFT, padx=5)
        
        def create_canvas():
            try:
                width = int(width_var.get())
                height = int(height_var.get())
                r = int(r_var.get())
                g = int(g_var.get())
                b = int(b_var.get())
                
                self.current_image = self.handler.create_blank_canvas(width, height, (r, g, b))
                self.original_image = self.current_image.copy()
                self.display_image_on_canvas()
                self.status_var.set("Blank canvas created")
                canvas_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(canvas_win, text="Create Canvas", command=create_canvas).pack(pady=10)

    def composite_images_ui(self):
        # Create a dialog for image compositing
        comp_win = tk.Toplevel(self.root)
        comp_win.title("Composite Images")
        comp_win.transient(self.root)
        comp_win.grab_set()
        
        # Overlay image selection
        ttk.Label(comp_win, text="Select Overlay Image:").pack(padx=10, pady=5)
        overlay_path_var = tk.StringVar()
        ttk.Entry(comp_win, textvariable=overlay_path_var, width=40).pack(padx=10)
        ttk.Button(comp_win, text="Browse...", 
                  command=lambda: overlay_path_var.set(filedialog.askopenfilename(
                      filetypes=[('Image files', '*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp')]
                  ))).pack(pady=5)
        
        # Position
        ttk.Label(comp_win, text="Position:").pack(padx=10, pady=5)
        pos_frame = ttk.Frame(comp_win)
        pos_frame.pack(fill=tk.X, padx=10)
        
        x_var = tk.StringVar(value="0")
        y_var = tk.StringVar(value="0")
        ttk.Label(pos_frame, text="X:").pack(side=tk.LEFT)
        ttk.Entry(pos_frame, textvariable=x_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(pos_frame, text="Y:").pack(side=tk.LEFT)
        ttk.Entry(pos_frame, textvariable=y_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Opacity
        ttk.Label(comp_win, text="Opacity (0.0-1.0):").pack(padx=10, pady=5)
        opacity_var = tk.StringVar(value="1.0")
        ttk.Entry(comp_win, textvariable=opacity_var, width=10).pack(padx=10)
        
        def composite():
            try:
                if not self.current_image:
                    messagebox.showerror("Error", "No base image selected")
                    return
                    
                overlay_path = overlay_path_var.get()
                if not overlay_path:
                    messagebox.showerror("Error", "Please select an overlay image")
                    return
                
                x = int(x_var.get())
                y = int(y_var.get())
                opacity = float(opacity_var.get())
                
                overlay_image = self.handler.import_image(overlay_path)
                self.current_image = self.handler.composite_images(
                    self.current_image, overlay_image, (x, y), opacity
                )
                self.display_image_on_canvas()
                self.status_var.set("Images composited")
                comp_win.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(comp_win, text="Composite", command=composite).pack(pady=10)

def main():
    root = tk.Tk()
    app = ImageEditor(root)
    
    # Handle window resize
    def on_resize(event):
        if hasattr(app, 'current_image') and app.current_image:
            app.display_image_on_canvas()
    
    root.bind('<Configure>', on_resize)
    
    # Center the window
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
