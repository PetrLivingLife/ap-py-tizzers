# See
#  https://code-maven.com/create-images-with-python-pil-pillow
#  https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
# TODO just an example of methods that could create simple image with text for testing purposes
# TODO verify function
from PIL import Image, ImageDraw2 as Draw, ImageFont as Font


default_text = "Hello"


def load_cfg(filepath):
    text = "text from config"


def create_new_image(text=None , width=1080, height=1920, aspect_ratio=(16, 9)):
    text = text or default_text
    image = Image.new(mode="RGB", size=(width, height), color="white")
    draw_text(image, text)
    image.save("*.png")
    pass


def calc_center_coords(image_size, font, text):
    """

    :param image_size: tuple(width, height)
    :param font:
    :param text:
    :return: coordinates tuple(horizontal, vertical)
    """
    font_width, font_height = font.getsize(text)
    return image_size[0]/2 - font_width/2, image_size[1]/2 - font_height/2


def draw_text(image, text):
    """
    Creates font as ~70% of the image size
    :param image: image object
    :param text: text to be drawn on image
    :return: font
    """
    draw = Draw.Draw(image)
    image_size = image.size
    fontsize = 1

    def create_font(size):
        return Font.truetype(size=size)

    font = create_font(fontsize)
    # Try to make font readable with every resolution
    # Enlarge it until the text occupies roughly 70% of either image dimension
    while font.getsize(text)[0] < image_size[0] * 0.7 and font.getsize(text)[1] < image_size[1] * 0.7:
        fontsize += 1
        font = create_font(size=fontsize)

    draw.text(calc_center_coords(image_size, font, text), text, font)