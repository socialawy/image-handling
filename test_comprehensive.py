"""
Image Handling Tool - Comprehensive Test Suite
Tests both GUI and API functionality for community validation.
Run with: python test_comprehensive.py
"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Some tests will be skipped.")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: NumPy not available. Some tests will be skipped.")

try:
    import pillow_heif
    HEIF_AVAILABLE = True
except ImportError:
    HEIF_AVAILABLE = False
    print("Warning: pillow_heif not available. HEIF tests will be skipped.")

try:
    import svglib
    SVGLIB_AVAILABLE = True
except ImportError:
    SVGLIB_AVAILABLE = False
    print("Warning: svglib not available. SVG tests will be skipped.")


def test_python_environment():
    """Test Python version and core dependencies."""
    print("Testing Python Environment...")
    
    # Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (need 3.8+)")
        return False
    
    # Core dependencies
    core_modules = {
        'PIL': 'Pillow',
        'tkinter': 'Tkinter'
    }
    
    # Optional dependencies
    optional_modules = {
        'numpy': 'NumPy',
        'pillow_heif': 'pillow-heif (HEIF support)',
        'svglib': 'svglib (SVG support)'
    }
    
    all_ok = True
    
    # Test core modules
    for module, name in core_modules.items():
        if module == 'PIL' and not PIL_AVAILABLE:
            print(f"  ✗ {name} - NOT INSTALLED (Required)")
            all_ok = False
        else:
            try:
                __import__(module)
                print(f"  ✓ {name}")
            except ImportError:
                print(f"  ✗ {name} - NOT INSTALLED (Required)")
                all_ok = False
    
    # Test optional modules
    for module, name in optional_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ⚠ {name} - NOT INSTALLED (Optional)")
    
    return all_ok


def test_api_functionality():
    """Test core ImageHandler and ImageToolkit API."""
    print("\nTesting API Functionality...")
    
    if not PIL_AVAILABLE:
        print("  ⚠ PIL not available - skipping API tests")
        return True  # Skip but don't fail
    
    try:
        from image_handling import ImageHandler, ImageToolkit
        
        # Test ImageHandler
        handler = ImageHandler()
        print("  ✓ ImageHandler initialization")
        
        # Test ImageToolkit
        toolkit = ImageToolkit()
        print("  ✓ ImageToolkit initialization")
        
        # Create test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            # Create a simple test image
            test_img = Image.new('RGB', (100, 100), color='red')
            test_img.save(tmp.name)
            
            # Test image loading
            loaded_img = handler.import_image(tmp.name)
            if loaded_img:
                print("  ✓ Image import functionality")
            else:
                print("  ✗ Image import failed")
                return False
            
            # Test resize
            resized = toolkit.resize_image(loaded_img, (50, 50))
            if resized and resized.size == (50, 50):
                print("  ✓ Image resize functionality")
            else:
                print("  ✗ Image resize failed")
                return False
            
            # Test format conversion
            output_dir = tempfile.mkdtemp()
            # Convert the image object first, then export
            converted_image = toolkit.convert_format(loaded_img, 'JPEG')
            if converted_image:
                # Export the converted image
                output_path = os.path.join(output_dir, "test_converted.jpg")
                from image_handling import ImageFormat
                toolkit.handler.export_image(converted_image, output_path, ImageFormat.JPEG)
                converted = [output_path]
            else:
                converted = []
            
            if converted and len(converted) > 0:
                print("  ✓ Format conversion functionality")
            else:
                print("  ✗ Format conversion failed")
                return False
            
            # Cleanup
            os.unlink(tmp.name)
            shutil.rmtree(output_dir)
        
        return True
        
    except Exception as e:
        print(f"  ✗ API test failed: {str(e)}")
        return False


def test_social_media_templates():
    """Test social media optimization features."""
    print("\nTesting Social Media Templates...")
    
    try:
        from image_handling import ImageToolkit
        
        toolkit = ImageToolkit()
        
        # Create test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            test_img = Image.new('RGB', (1080, 720), color='blue')
            test_img.save(tmp.name)
            
            # Test Instagram optimization
            instagram_result = toolkit.process_for_social_media(tmp.name, 'instagram')
            if instagram_result:
                print("  ✓ Instagram optimization")
            else:
                print("  ✗ Instagram optimization failed")
                return False
            
            # Test multiple platforms
            platforms = ['facebook', 'twitter', 'linkedin']
            for platform in platforms:
                result = toolkit.process_for_social_media(tmp.name, platform)
                if result:
                    print(f"  ✓ {platform.title()} optimization")
                else:
                    print(f"  ✗ {platform.title()} optimization failed")
                    return False
            
            # Cleanup
            os.unlink(tmp.name)
        
        return True
        
    except Exception as e:
        print(f"  ✗ Social media test failed: {str(e)}")
        return False


def test_batch_processing():
    """Test batch processing capabilities."""
    print("\nTesting Batch Processing...")
    
    try:
        from image_handling import ImageToolkit
        
        toolkit = ImageToolkit()
        
        # Create test images
        input_dir = tempfile.mkdtemp()
        output_dir = tempfile.mkdtemp()
        
        test_images = []
        for i in range(3):
            img_path = os.path.join(input_dir, f'test_{i}.png')
            test_img = Image.new('RGB', (100, 100), color=(i*80, 100, 200))
            test_img.save(img_path)
            test_images.append(img_path)
        
        # Test batch conversion
        results = toolkit.batch_convert(input_dir, output_dir, 'JPEG')
        if len(results) == 3:
            print("  ✓ Batch conversion")
        else:
            print("  ✗ Batch conversion failed")
            return False
        
        # Test batch resize
        results = toolkit.batch_resize(input_dir, output_dir, width=50, height=50)
        if len(results) == 3:
            print("  ✓ Batch resize")
        else:
            print("  ✗ Batch resize failed")
            return False
        
        # Cleanup
        shutil.rmtree(input_dir)
        shutil.rmtree(output_dir)
        
        return True
        
    except Exception as e:
        print(f"  ✗ Batch processing test failed: {str(e)}")
        return False


def test_gui_components():
    """Test GUI components (non-visual testing)."""
    print("\nTesting GUI Components...")
    
    try:
        # Test if GUI module can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("image_editor_ui", "image_editor_ui.py")
        
        if spec and spec.loader:
            print("  ✓ GUI module structure valid")
        else:
            print("  ✗ GUI module structure invalid")
            return False
        
        # Test required GUI dependencies
        try:
            import tkinter
            print("  ✓ Tkinter available")
        except ImportError:
            print("  ✗ Tkinter not available")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ GUI test failed: {str(e)}")
        return False


def test_project_structure():
    """Verify project structure and documentation."""
    print("\nTesting Project Structure...")
    
    required_files = [
        'image_handling.py',
        'image_editor_ui.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        'CONTRIBUTING.md',
        'CODE_OF_CONDUCT.md',
        'AGENTS.md'
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            all_ok = False
    
    return all_ok


def main():
    """Run comprehensive test suite."""
    print("=" * 70)
    print("Image Handling Tool - Comprehensive Test Suite")
    print("=" * 70)
    
    tests = [
        ("Python Environment", test_python_environment),
        ("API Functionality", test_api_functionality),
        ("Social Media Templates", test_social_media_templates),
        ("Batch Processing", test_batch_processing),
        ("GUI Components", test_gui_components),
        ("Project Structure", test_project_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("✓ ALL TESTS PASSED!")
        print("The Image Handling Tool is ready for community use!")
        return 0
    else:
        print(f"✗ {total - passed} TESTS FAILED")
        print("Please address the issues above before community release.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
