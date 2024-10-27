from adventurelib import *
from Description import dict_interrogation, dict_biography

class Character(Item):
    def interrogation(self, answer):
        # Ответ персонажа при допросе
        self.dialog = False
        self.ask_biography = False
        self.answer = answer

    def dialog_with_hero(self):
        self.dialog = True
        return self.answer

    def biography(self, text_of_biography):
        self.biography_of_hero = text_of_biography

    def ask_biography(self):
        self.ank_biography = True
        return self.biography_of_hero


boris = Character('Борис')
boris.biography(dict_biography['борис'])
boris.interrogation(dict_interrogation['борис'])
vera = Character('Вера')
vera.biography(dict_biography['вера'])
michael = Character('Михаил')
michael.biography(dict_biography['михаил'])
michael.interrogation(dict_interrogation['михаил'])
inna = Character('Инна')
inna.biography(dict_biography['инна'])
inna.interrogation(dict_interrogation['инна'])
all_characters = [boris, vera, michael, inna]