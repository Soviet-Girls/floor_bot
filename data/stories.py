import io
from PIL import Image, ImageDraw, ImageFont

# функция генерации изображения
# в папке проекта лежит файл "stories.png"
# на него будем накладывать текст в указанных координатах
def generate_image(floor, volume, owners, tokens) -> io.BytesIO:
    img = Image.open("stories.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("XO_Tahion_Nu.ttf", 85)
    draw.text((458+10, 1153-5), str(floor), (0, 0, 0), font=font)
    draw.text((539+10, 1261-5), str(volume), (0, 0, 0), font=font)
    draw.text((728+10, 1368-5), str(owners), (0, 0, 0), font=font)
    draw.text((563+10, 1475-5), str(tokens), (0, 0, 0), font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

if __name__ == "__main__":
    # пример вызова функции
    generate_image("705 ₽ (+15%)", "210 940 ₽", 102, 300)