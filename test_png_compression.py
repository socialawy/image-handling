#!/usr/bin/env python3
"""
Test script for PNG compression functionality
"""

import os
import tempfile
from PIL import Image
from image_handling import ImageHandler, ImageToolkit

def create_test_image():
    """Create a test PNG image"""
    # Create a simple test image
    img = Image.new('RGB', (800, 600), color='red')
    # Add some pattern to make it compressible
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    for i in range(0, 800, 20):
        for j in range(0, 600, 20):
            draw.rectangle([i, j, i+15, j+15], fill='blue' if (i+j) % 40 == 0 else 'green')
    
    return img

def test_png_compression():
    """Test PNG compression functionality"""
    print("Testing PNG compression functionality...")
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(input_dir)
        os.makedirs(output_dir)
        
        # Create test images
        test_img = create_test_image()
        test_path = os.path.join(input_dir, "test.png")
        test_img.save(test_path, "PNG")
        
        original_size = os.path.getsize(test_path)
        print(f"Original image size: {original_size:,} bytes")
        
        # Test compression with different settings
        toolkit = ImageToolkit()
        
        # Test 1: Basic compression
        print("\n1. Testing basic compression...")
        results = toolkit.batch_compress_png(input_dir, output_dir, compress_level=6)
        compressed_size = os.path.getsize(results[0])
        reduction = ((original_size - compressed_size) / original_size) * 100
        print(f"Compressed size: {compressed_size:,} bytes ({reduction:.1f}% reduction)")
        
        # Test 2: Maximum compression
        print("\n2. Testing maximum compression...")
        results = toolkit.batch_compress_png(input_dir, output_dir, compress_level=9, optimize=True)
        max_compressed_size = os.path.getsize(results[0])
        max_reduction = ((original_size - max_compressed_size) / original_size) * 100
        print(f"Max compressed size: {max_compressed_size:,} bytes ({max_reduction:.1f}% reduction)")
        
        # Test 3: Color reduction
        print("\n3. Testing color reduction...")
        results = toolkit.batch_compress_png(input_dir, output_dir, compress_level=9, 
                                            optimize=True, reduce_colors=True, max_colors=128)
        color_reduced_size = os.path.getsize(results[0])
        color_reduction = ((original_size - color_reduced_size) / original_size) * 100
        print(f"Color reduced size: {color_reduced_size:,} bytes ({color_reduction:.1f}% reduction)")
        
        print("\n✅ PNG compression tests completed successfully!")
        print(f"Best compression achieved: {color_reduction:.1f}% size reduction")

if __name__ == "__main__":
    test_png_compression()
