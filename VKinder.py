import random
import vk_api
from models import User
from config import token, DSN
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DSN)
Session = sessionmaker(engine)
session = Session()


class VKinder:

    def __init__(self):
        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()
        self.upload = vk_api.VkUpload(self.vk)

    def get_user_info(self, user_id):
        return self.api.users.get(user_ids=user_id, fields='city, sex, relation')

    def add_user_to_bd(self, user_id, age):
        check = session.query(User).get(user_id)
        if check == None:
            data = self.get_user_info(user_id)
            city = data[0]['city']
            user = User(id=data[0]['id'],
                        name=data[0]['first_name'],
                        surname=data[0]['last_name'],
                        age=age,
                        sex=data[0]['sex'],
                        city=city['title'],
                        city_id=city['id']
                        )
            session.add(user)
            session.commit()
            session.close()

    def from_user_bd(self, user_id):
        dict = {}
        for table in session.query(User).filter(User.id == user_id).all():
            data = vars(table)
            dict_1 = {'city': data['city'],
                      'sex': data['sex'],
                      'age': data['age'],
                      'city_id': data['city_id'],
                      'user_id': data['id'],
                      'name': data['name'],
                      'surname': data['surname']
                      }
            dict.update(dict_1)
        return dict

    def sex_change(self, user_id):
        data = self.from_user_bd(user_id)
        gender = 0
        sex = data['sex']
        if sex == 2:
            gender = 1
        elif sex == 1:
            gender = 2
        return gender

    def user_search(self, user_id):
        data = self.from_user_bd(user_id)
        age = data['age']
        sex = self.sex_change(user_id)
        request = self.api.users.search(
            city=data['city_id'],
            sex=sex,
            age_from=age-5,
            age_to=age+5,
            status=1 or 6,
            fields='domain, deactivated',
            offset=0,
            count=100
        )
        partners_list = []
        for user in request['items']:
            if user['is_closed'] == False:
                partners_list.append(user['id'])
        return partners_list

    def get_photos(self, user_id):
        list_id = self.user_search(user_id)
        owner_id = random.choice(list_id)
        data = self.api.photos.get(owner_id=owner_id, album_id='profile', extended=1)
        top_dict = {}
        photo_ids_list = []
        attachment_list = []
        for files in data['items']:
            photo_id = files['id']
            likes_count = files['likes']['count']
            comment_count = files['comments']['count']
            dict_1 = {likes_count + comment_count: photo_id}
            top_dict.update(dict_1)
        top3 = sorted(top_dict.items())[-3:]
        for ids in top3:
            photo_ids_list.append(ids[1])
        domain = f'vk.com/id{owner_id}'
        attachment_list.append(domain)
        for photo_ids in photo_ids_list:
            photo = photo_ids
            attachment = f'photo{owner_id}_{photo}'
            attachment_list.append(attachment)
        return attachment_list







