from adventurelib import *
from Rooms import living_room_cottage, swimming_pool, basement, vera_house, current_room
from Description import dict_items_description, dict_interrogation, dict_biography, start_time
import time
from Characters import all_characters
import adventurelib
import pymorphy3
from art import tprint

with open('Детектив_начало.txt', encoding='utf-8') as file:
    text_start = file.read()
    print(text_start)


say(current_room)
print('Доступные вещи:')
for equipment in current_room.items:
    print(equipment)

inventory = Bag()
number_of_hints = 5
set_context(None)
morph = pymorphy3.MorphAnalyzer()
@when('север', direction='north')
@when('юг', direction='south')
@when('восток', direction='east')
@when('запад', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        if room == basement and 'фонарик' in inventory: # изменить
            current_room = room
            basement.locked = False
            say("Благодаря фонарику вы смогли войти в подвал. И Вы смогли найти кое-что интересное")
            print('Доступные вещи: список людей')
        elif room == basement and 'фонарик' not in inventory:
            current_room = room
            say(room)
        else:
            current_room = room
            say(room)
            print('Доступные вещи:')
            for equipment in room.items:
                print(equipment)

@when("посмотреть карту")
def map():
    print("""
    Бассейн
        ↑↓ (север)
    Гостиная ⇔ (восток) Подвал
        ↑↓ (юг)
    Дом Веры
    """)

@when('взять THING')
def take(thing):
    #TODO исправить морфологию!
    if thing != 'прощальную записку' and thing != 'список людей' and thing != 'фотографию веры с папой':
        thing_accs = morph.parse(thing)[0].inflect({'accs'}).word
        thing_normal_form = morph.parse(thing)[0].normal_form
    else:
        thing_accs = thing
        if thing == 'прощальную записку':
            thing_normal_form = 'прощальная записка'
        elif thing == 'фотографию веры с папой':
            thing_normal_form = 'фотография веры с папой'
        else:
            thing_normal_form = thing
    obj = ""
    if thing_accs == thing and not current_room.locked:
        obj = current_room.items.take(thing_normal_form)
    if not obj and len(thing.split()) == 1:
        thing_gent = morph.parse(thing)[0].inflect({'gent'}).word
        print(f'Здесь нет {thing_gent}')
    elif not obj:
        print("Этого предмета здесь нет!")
    else:
        print(f'Вы взяли: {thing_normal_form}.')
        inventory.add(obj)

@when('осмотреть THING')
def look(thing):
    if thing != 'прощальную записку' and thing != 'список людей' and thing != 'фотографию веры с папой':
        thing_accs = morph.parse(thing)[0].inflect({'accs'}).word
        thing_normal_form = morph.parse(thing)[0].normal_form
    else:
        thing_accs = thing
        if thing == 'прощальную записку':
            thing_normal_form = 'прощальная записка'
        elif thing == 'фотографию веры с папой':
            thing_normal_form = 'фотография веры с папой'
        else:
            thing_normal_form = thing
    if thing_normal_form in inventory and thing_accs == thing:
        say(dict_items_description[thing_normal_form])
    elif len(thing.split()) == 1:
        thing_gent = morph.parse(thing_normal_form)[0].inflect({'gent'}).word
        print(f"У Вас нет {thing_gent} в инвентаре")
    else:
        print('Этого предмета у вас в инвентаре нет!')

@when('допросить NICKNAME')
def interrogate(nickname):
    if nickname.lower() in dict_interrogation:
        hero = [people for people in all_characters if people.name == nickname.capitalize()][0]
        say(f"{hero.name}:{hero.dialog_with_hero()}")
    else:
        say('Человек с таким именем допросить нельзя')

@when('обвинить NAME')
def accuse(name):
    if name.lower() == 'михаила' or name.lower() == 'михаил':
        say('Поздравляю, детектив! Вы абсолютно верно нашли все улики и сопоставили факты. Вы замечательно поработли и нашли убийцу!')
        say("Время за которое вы прошли игру:")
        elapsed_time = time.time() - start_time
        gmt_time = time.gmtime(elapsed_time)
        tprint(time.strftime("%H:%M:%S", gmt_time))
        if gmt_time.tm_min < 5:
            say(f"Вы показали просто отличное время! Подсказок использовано: {5 - number_of_hints}")
        elif 5 <= gmt_time.tm_min < 10:
            say(f"Вы хорошо себя показали, детектив! Подсказок использовано: {5 - number_of_hints}")
        elif 10 <= gmt_time.tm_min <= 20:
            say(f"Вы показали неплохое время, но можно было и лучше, Вам есть над чем работать! Подсказок использовано: {5 - number_of_hints}")
        else:
            say("Со своей задачей вы действительно справились, но это заняло у вас очень много времени! Подсказок использовано: {5 - number_of_hints}")
        exit()
    else:
        say('К сожалению, вы ошиблись, на самом деле Веру убил Михаил, после чего он скрылся в неизвестном направлении. '
            'Начальство вами очень не довольно, но важно не это, а то, что вы не нашли реального убийцу, может вам стоит '
            'сменить профессию, потому что заниматься расследованиями важных для общества дел определённо не ваше.')
        exit()


@when('команды')
def movies():
    with open('Детектив_описание команд.txt', encoding='utf-8') as file:
        list_of_movies = file.read()
    print(list_of_movies)

@when('инвентарь')
def implement():
    if inventory:
        for elems in inventory:
            say(elems)
    else:
        say('У вас пока нет ничего в инвентаре')

@when('подсказка')
def clue():
    global number_of_hints
    if number_of_hints > 0:
        number_of_hints -= 1
        if not inventory:
            say('В первую очередь попробуйте исследовать локации, может там можно найти улики.')
        elif "фотография веры с папой" not in inventory:
            say('Поробуйте для начала узнать немного о биографии убитой, не помешает и исследовать её дом, может'
                ' там будет что-то важное, например какая-то информация о её родственниках?')
        elif "фотография веры с папой" in inventory and not all_characters[0].dialog:
            say("Попробуйте допросить мужа Веры, Бориса")
        elif all_characters[0].dialog and get_context() is None:
            say("Внимательно прочитайте, что сказал Борис, почему Вера с Борисом хотели поехать на Камчатку,"
                " а в итоге было выбрано совершенно другое направление, может это как-то связано с профессией Веры(бортпроводница)?")
            set_context('Камчатка и Пятигорск')
        elif all_characters[0].dialog and get_context() == 'Камчатка и Пятигорск':
            say("Дело в том, что на Камчатку можно добраться только на самолёте, а в Пятигорск только на поезде. А значит"
                " Инна и Михаил выбрали это направление, потому что не хотели лететь на самолёте!")
            set_context('Последние подсказки')
        elif 'фонарик' not in inventory:
            say('А теперь посмотрите, тщательно ли вы осмотрели гостиную?!')
        elif 'фонарик' in inventory and 'список людей' not in inventory:
            say('У Вас есть фонарик, попробуйте зайти в подвал, может там найдётся что-то интересное?')
        elif 'список людей' in inventory and 'фотография' in inventory:
            say('Осмотрев список людей, погибших в авиакатастрофе и фотографию, становится понятно, '
                'что родители Михаила погибли, потому что Инна на тот момент не была замужем, а следовательно, '
                'Волковы у неё в семье быть не могли')
        elif 'марка' not in inventory:
            say('Разгадка уже совсем близка, осмотрите место преступления, там лежит главная улика')
        else:
            say('У вас есть марка с авиакатастрофой рядом с телом убитой и Михаил, чьи родители в одной из таких катастроф'
                ' погибли, кажется, можно сделать вывод кто убийца?!')

    else:
        say('К сожалению, вы исчерпали весь лимит подсказок, дальше только сами.')


@when('биография NAME')
def biography(name):
    if name in dict_biography:
        say(f"{name}: {dict_biography[name]}")
    else:
        say('Извините, этого человека не было на месте преступления')

def no_command_matches(command):
    say(f"К сожалению, команды: '{command}' не существует")


adventurelib.no_command_matches = no_command_matches
start()
