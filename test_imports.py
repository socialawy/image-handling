from image_handling import ImageHandler, ImageToolkit, StandardSizes
try:
    handler = ImageHandler()
    print("ImageHandler initialized")
    toolkit = ImageToolkit()
    print("ImageToolkit initialized")
    print(f"StandardSizes: {StandardSizes}")
    print(f"StandardSizes.INSTAGRAM_SQUARE: {StandardSizes.INSTAGRAM_SQUARE}")
except Exception as e:
    print(f"Error: {e}")
