import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import group_token
from random import randrange
from VKinder import VKinder


kinder = VKinder()
vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': randrange(10 ** 7)
                                })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()
            user_id = event.user_id
            name = kinder.get_user_info(user_id)[0]['first_name']
            age_list = str(list(range(16, 60)))

            if request == 'привет':
                write_msg(event.user_id, f"Хай, {name}, напиши свой возвраст")

            elif request in age_list:
                age = int(event.text)
                kinder.add_user_to_bd(user_id, age)
                kinder.user_search(user_id)
                photo = kinder.get_photos(user_id)
                for itm in photo[1:]:
                    write_msg(user_id, 'фото:', attachment=itm)
                write_msg(user_id, f'ссылка: {photo[0]}')
                write_msg(user_id, 'напиши дальше, для следующего поиска')

            elif request == 'дальше':
                age = kinder.from_user_bd(user_id)['age']
                kinder.user_search(user_id)
                photo = kinder.get_photos(user_id)
                for itm in photo[1:]:
                    write_msg(user_id, 'фото:', attachment=itm)
                write_msg(user_id, f'ссылка: {photo[0]}')
                write_msg(user_id, 'напиши дальше, для следующего поиска')

            elif request == 'пока':
                write_msg(event.user_id, 'Пока((')

            else:
                write_msg(event.user_id, 'Не поняла вашего ответа...')

