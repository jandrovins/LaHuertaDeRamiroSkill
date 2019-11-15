from mycroft import MycroftSkill, intent_file_handler


class Lahuertaderamiroskill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('lahuertaderamiroskill.intent')
    def handle_lahuertaderamiroskill(self, message):
        self.speak_dialog('lahuertaderamiroskill')


def create_skill():
    return Lahuertaderamiroskill()

