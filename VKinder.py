import vk_api
from datetime import date
from models import User, Partner, create_tables
from config import token, DSN, group_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DSN)
Session = sessionmaker(engine)
session = Session()


class VKinder:

    def __init__(self):
        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()
        self.error = vk_api.VkApiError
        self.bot = vk_api.VkApi(token=group_token)

    def get_user_info(self, user_id):
        try:
            data = self.api.users.get(user_ids=user_id, fields='bdate, city, sex, relation')
            age = self.age_calculate(data[0]['bdate'])
            name = data[0]['first_name']
            sex = data[0]['sex']
            city = data[0]['city']['title']
            city_id = data[0]['city']['id']
            self.add_user_to_bd(user_id, name, age, sex, city, city_id)
        except self.error as error:
            result = error
            return result

    @staticmethod
    def age_calculate(bdate):
        age = 0
        if bdate == None:
            age = age
        else:
            date_list = bdate.split('.')
            if len(date_list) == 3:
                year = date_list[2]
                age = date.today().year - int(year)
            else:
                age = age
        return age

    @staticmethod
    def change_user_age(user_id, age):
        session.query(User).filter(User.id == user_id).update({User.age: age})

    @staticmethod
    def add_user_to_bd(user_id, name, age, sex, city, city_id):
        check = session.query(User).get(user_id)
        if check == None:
            user = User(id=user_id,
                        name=name,
                        age=age,
                        sex=sex,
                        city=city,
                        city_id=city_id)
            session.add(user)
            session.commit()
            session.close()

    @staticmethod
    def from_user_bd(user_id):
        user_dict = {}
        for table in session.query(User).filter(User.id == user_id).all():
            data = vars(table)
            dict_1 = {'city': data['city'],
                      'sex': data['sex'],
                      'name': data['name'],
                      'age': data['age'],
                      'city_id': data['city_id'],
                      'user_id': data['id']}
            user_dict.update(dict_1)
        return user_dict

    def sex_change(self, user_id):
        data = self.from_user_bd(user_id)
        sex = data['sex']
        if sex == 2:
            gender = 1
        else:
            gender = 2
        return gender

    def partner_search(self, user_id, offset, count):
        data = self.from_user_bd(user_id)
        age = data['age']
        try:
            request = self.api.users.search(
                city=data['city_id'],
                sex=self.sex_change(user_id),
                age_from=age - 5,
                age_to=age + 5,
                status=1 or 6,
                fields='domain, deactivated',
                offset=offset,
                count=count)
            for user in request['items']:
                if user['is_closed'] == False:
                    partner_id = user['id']
                    self.add_partner_to_bd(partner_id, user_id)
                    offset += count
        except self.error as error:
            result = error
            return result

    @staticmethod
    def add_partner_to_bd(partner_id, user_id):
        check = session.query(Partner).get(partner_id)
        if check == None:
            partner = Partner(id=partner_id,
                              views='нет',
                              user_id=user_id)
            session.add(partner)
            session.commit()
            session.close()

    @staticmethod
    def user_views_partner(partner_id):
        session.query(Partner).filter(Partner.id == partner_id).update({Partner.views: 'да'})
        session.commit()

    def get_photos(self, partner_id):
        try:
            data = self.api.photos.get(owner_id=partner_id, album_id='profile', extended=1)
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
            domain = f'vk.com/id{partner_id}'
            attachment_list.append(domain)
            for photo_ids in photo_ids_list:
                photo = photo_ids
                attachment = f'photo{partner_id}_{photo}'
                attachment_list.append(attachment)
            return attachment_list
        except self.error as error:
            result = error
            print(result)
            return result

    @staticmethod
    def from_partner_bd():
        partner_ids_list = []
        for table in session.query(Partner.id).filter(Partner.views == 'нет').all():
            for data in table:
                partner_ids_list.append(data)
        return partner_ids_list
