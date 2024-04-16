import os
import sys
import pygame
import requests

clock = pygame.time.Clock()

lon, lat, delta = 0, 0, 0
toponym_to_find = 'Попова 40а/2'


def find(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print("Ну ты и животное, даже ввести правильно не смог!")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    global text_name
    text_name = ((toponym['metaDataProperty'])['GeocoderMetaData'])['text']
    global text_index
    try:
        text_index = (((toponym['metaDataProperty'])['GeocoderMetaData'])['Address'])['postal_code']
    except Exception:
        text_index = ''
    global text_output
    text_output = text_name
    toponym_coodrinates = toponym["Point"]["pos"]
    lon, lat = toponym_coodrinates.split(" ")

    delta = "0.002"
    return lon, lat, delta


color_line = (120, 0, 150)
color1 = (240, 0, 195)
color2 = (120, 0, 150)
color3 = (120, 0, 150)
color_re = (180, 0, 225)
color_in = (180, 0, 225)
w_in = 2
type_m = 'map'


def render(lon, lat, delta):
    api_server = "http://static-maps.yandex.ru/1.x/"
    global type_m

    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": type_m
    }
    response = requests.get(api_server, params=params)
    if not response:
        print("Ну ты и животное, даже с этим не справился!")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    return response


def type_1():
    font = pygame.font.Font(None, 32)
    text = font.render(f'Схема', True, color1)
    screen.blit(text, (90, 60))


def type_2():
    font = pygame.font.Font(None, 32)
    text = font.render(f'Спутник', True, color2)
    screen.blit(text, (90, 120))


def type_3():
    font = pygame.font.Font(None, 32)
    text = font.render(f'Гибрид', True, color3)
    screen.blit(text, (90, 180))


def recent():
    font = pygame.font.Font(None, 60)
    text = font.render(f'Сброс', True, color_re)
    screen.blit(text, (710, 95))


def postal_code():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Почтовый индекс', True, (180, 0, 225))
    screen.blit(text, (15, 260))

    font_e = pygame.font.Font(None, 24)
    text_e0 = font_e.render('Внимание!!!', True, (120, 0, 150))
    text_e1 = font_e.render('Индекс может не уместиться', True, (120, 0, 150))
    text_e2 = font_e.render('на строку с адресом!', True, (120, 0, 150))
    screen.blit(text_e0, (15, 290))
    screen.blit(text_e1, (15, 320))
    screen.blit(text_e2, (15, 345))


pygame.init()
pygame.display.set_caption('Большая задача по Maps API')
screen = pygame.display.set_mode((900, 675))
clock = pygame.time.Clock()
lon, lat, delta = find(toponym_to_find)
lon0, lat0, delta0 = lon, lat, delta
screen.fill((40, 40, 45))
input_box = pygame.Rect(275, 100, 400, 50)
print_box = pygame.Rect(275, 25, 600, 40)
text = ''
text_output = text_name
font = pygame.font.Font(None, 60)
font0 = pygame.font.Font(None, 40)

response = render(lon, lat, delta)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
screen.blit(pygame.image.load(map_file), (275, 200))
pygame.display.flip()
running = True
active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEMOTION:
            if 690 < event.pos[0] < 870 and 75 < event.pos[1] < 175:
                color_re = (240, 0, 225)
            else:
                color_re = (180, 0, 225)

            if 240 < event.pos[0] < 260 and 263 < event.pos[1] < 283:
                color_in = (240, 0, 225)
            else:
                color_in = (180, 0, 225)

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    toponym_to_find = text
                    lon, lat, delta = find(toponym_to_find)
                    response = render(lon, lat, delta)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color_line = (240, 0, 195) if active else (120, 0, 150)

            if 70 < event.pos[0] < 200 and 40 < event.pos[1] < 100:
                color1 = (240, 0, 195)
                color2 = (120, 0, 150)
                color3 = (120, 0, 150)
                type_m = 'map'
                response = render(lon, lat, delta)

            if 70 < event.pos[0] < 200 and 100 < event.pos[1] < 160:
                color1 = (120, 0, 150)
                color2 = (240, 0, 195)
                color3 = (120, 0, 150)
                type_m = 'sat'
                response = render(lon, lat, delta)

            if 70 < event.pos[0] < 200 and 160 < event.pos[1] < 220:
                color1 = (120, 0, 150)
                color2 = (120, 0, 150)
                color3 = (240, 0, 195)
                type_m = 'sat,skl'
                response = render(lon, lat, delta)

            #  Сброс запроса
            if 690 < event.pos[0] < 870 and 75 < event.pos[1] < 175:
                text_output = 'Россия, Смоленск, улица Попова, 40А'
                lon, lat, delta = lon0, lat0, delta0
                response = render(lon, lat, delta)

            if 240 < event.pos[0] < 260 and 263 < event.pos[1] < 283:
                if w_in == 0:
                    w_in = 2
                    text_output = text_name
                else:
                    w_in = 0
                    text_output = f'{text_name}, {text_index}'

        if pygame.key.get_pressed()[pygame.K_PAGEUP]:
            if float(delta) < 50:
                delta = float(delta) * 2
                response = render(lon, lat, delta)

        if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
            if float(delta) > 0.00002:
                delta = float(delta) / 2
                response = render(lon, lat, delta)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if float(lat) > -85 + float(delta) * 3:
                lat = float(lat) - float(delta) * 1.4
                response = render(str(lon), str(lat), delta)

        if pygame.key.get_pressed()[pygame.K_UP]:
            if float(lat) < 85 - float(delta) * 3:
                lat = float(lat) + float(delta) * 1.4
                response = render(str(lon), str(lat), delta)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if float(lon) > -180 + float(delta) * 3:
                lon = float(lon) - float(delta) * 3
                response = render(str(lon), str(lat), delta)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if float(lon) < 180 - float(delta) * 3:
                lon = float(lon) + float(delta) * 3
                response = render(str(lon), str(lat), delta)

        screen.fill((40, 40, 45))
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (275, 200))
        txt_surface = font.render(text, True, color_line)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color_line, input_box, 2, 5)

        txt0_surface = font0.render(text_output[:40], True, (120, 0, 150))
        screen.blit(txt0_surface, (print_box.x + 5, print_box.y + 5))
        pygame.draw.rect(screen, (120, 0, 150), print_box, 2, 5)
        pygame.draw.rect(screen, color_in, pygame.Rect(240, 263, 20, 20), w_in, 5)
        type_1()
        type_2()
        type_3()
        recent()
        postal_code()
        pygame.display.flip()
    clock.tick(100)
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
