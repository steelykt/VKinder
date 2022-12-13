import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import group_token
from random import randrange
from VKinder import VKinder


class Bot:

    def __init__(self):
        self.vk = vk_api.VkApi(token=group_token)
        self.longpoll = VkLongPoll(self.vk)
        self.kinder = VKinder()
        self.offset = 0
        self.count = 35

    def write_msg(self, user_id, message, attachment=None):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'attachment': attachment,
                                         'random_id': randrange(10 ** 7)})

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text.lower()
                    user_id = event.user_id
                    data = self.kinder.get_user_info(user_id)
                    name = self.kinder.from_user_bd(user_id)['name']
                    age = self.kinder.from_user_bd(user_id)['age']
                    age_list = str(list(range(16, 60)))

                    if request == 'привет':
                        if age == 0:
                            self.write_msg(user_id, f"Хай, {name}, укажите свой возвраст")
                        else:
                            try:
                                self.write_msg(user_id, 'Ищу Вам пару...')
                                self.kinder.partner_search(user_id, self.offset, self.count)
                                partners_list = self.kinder.from_partner_bd()
                                owner_id = str(random.choice(partners_list))
                                self.kinder.user_views_partner(owner_id)
                                photo = self.kinder.get_photos(owner_id)
                                for itm in photo[1:]:
                                    self.write_msg(user_id, 'фото:', attachment=itm)
                                self.write_msg(user_id, f'ссылка: {photo[0]}')
                                self.write_msg(user_id, 'напиши дальше, для следующего поиска')
                                self.offset += self.count
                            except:
                                self.write_msg(user_id, f'что-то пошло не так: {data}')

                    elif request in age_list:
                        age = int(event.text)
                        self.kinder.change_user_age(user_id, age)
                        try:
                            self.write_msg(user_id, 'Ищу Вам пару...')
                            self.kinder.partner_search(user_id, self.offset, self.count)
                            partners_list = self.kinder.from_partner_bd()
                            owner_id = str(random.choice(partners_list))
                            self.kinder.user_views_partner(owner_id)
                            photo = self.kinder.get_photos(owner_id)
                            for itm in photo[1:]:
                                self.write_msg(user_id, 'фото:', attachment=itm)
                            self.write_msg(user_id, f'ссылка: {photo[0]}')
                            self.write_msg(user_id, 'напиши дальше, для следующего поиска')
                            self.offset += self.count
                        except:
                            self.write_msg(user_id, f'что-то пошло не так: {data}')


                    elif request == 'дальше':
                        try:
                            self.write_msg(user_id, 'Ищу Вам пару...')
                            self.kinder.partner_search(user_id, self.offset, self.count)
                            partners_list = self.kinder.from_partner_bd()
                            owner_id = str(random.choice(partners_list))
                            self.kinder.user_views_partner(owner_id)
                            photo = self.kinder.get_photos(owner_id)
                            for itm in photo[1:]:
                                self.write_msg(user_id, 'фото:', attachment=itm)
                            self.write_msg(user_id, f'ссылка: {photo[0]}')
                            self.write_msg(user_id, 'напиши дальше, для следующего поиска')
                            self.offset += self.count
                        except:
                            self.write_msg(user_id, f'что-то пошло не так: {data}')

                    elif request == 'пока':
                        self.write_msg(event.user_id, 'Пока((')

                    else:
                        self.write_msg(event.user_id, 'Не поняла вашего ответа...')


bot = Bot()
bot.listen()



