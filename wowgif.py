from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype("times.ttf", 1000)
x,y = font.getsize('world')
image = Image.new('RGB',(x,y))
draw = ImageDraw.Draw(image)
draw.text((0, 0), "world", font=font)
image.save('test/x.png', "PNG")