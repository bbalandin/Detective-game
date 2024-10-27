from adventurelib import *


# Room.add_direction('living_room', 'swimming_pool')
# Room.add_direction('vera_house', 'basement')


# Описываем гостиную
living_room_cottage = Room("""
Перед Вами гостиная коттеджа, где не так давно было очень весело. Вы можете видите много новогодних подарков,
бросается в глаза и ёлка, стильно и лаконично украшенная.
""")
flashlight = Item('фонарик')
letter = Item('записка', 'поздравление с Новым годом')
photo = Item('фотография')
living_room_cottage.locked = False
living_room_cottage.items = Bag([flashlight, letter, photo])

# Описание бассейка
swimming_pool = living_room_cottage.north = Room("""
Бассейн. Судя по разбросанным вещам, в тот роковой вечер он пользовался большой популярностью. Хотя именно здесь и был
найден труп. Её звали Вера, всё что о ней сообщила полиция, что она работала бортпроводницей и на момент
убийства ей было всего 25 лет. Становится не понятно, кому и как могла навредить столь юная и хрупкая девушка
""")
farewell_note = Item('прощальная записка')
brand = Item('марка', 'старинная марка')
swimming_pool.locked = False
swimming_pool.items = Bag([farewell_note, brand])

# Подвал коттеджа
basement = living_room_cottage.east = Room("""Тёмный подвал, кажется, без фонарика тут не обойтись!""")
basement.locked = True
plane_crash_list = Item('Список людей')
basement.items = Bag([plane_crash_list])

# Дом Веры:
vera_house = living_room_cottage.south = Room("""Вот вы и пришли Вы в дом убитой... Всё навевает тоской, ведь раньше здесь часто собирались друзья.
А сейчас тут совсем пусто, но время работать. Вы видите много фотографий Веры с родителями. Но одна Вас особенно привлекла.
""")
photo_vera_father = Item("фотография Веры с папой")
vera_house.locked = False
vera_house.items = Bag([photo_vera_father])

current_room = living_room_cottage