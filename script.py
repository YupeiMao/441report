# import csv
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','ratemyjob.settings')
# import django
# django.setup()
#
# '''
# dir: RMJ/
# '''
# '''
# Company and Position import
# Author: Yupei Mao
# '''
# path =  "/Users/Neil/Desktop/ratemyjob"
# os.chdir(path)
# from basic_app.models import Images
# # p = Images()
# # p.save()
# q = Images()
# q.save()
# r = Images()
# r.save()
# with open('csvs/Company_Final.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         p = Company(cid=row['CID'], name=row['name'],
#         country=row['country'], state=row['state'],city=row['city'])
#         p.save()
# path =  "/Users/Neil/Desktop/ratemyjob"
# os.chdir(path)
# from basic_app.models import Position
# count = 0
# with open('csvs/Position_Final.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         count+=1
#         if count%100==0:
#             print(count)
#         p = Position(pid=row['PID'], title=row['title'])
#         p.save()

# '''
# Fake User creation and import
# Author: Yupei Mao
# '''
# path =  "/Users/Neil/Desktop/ratemyjob"
# os.chdir(path)
# import random
# from django.contrib.auth.models import User
# from basic_app.models import UserProfileInfo
# from faker import Faker
# from faker.providers import person
# from faker.providers import internet
# from faker.providers import misc
# from faker.providers import lorem
#
# fake = Faker()
# fake.add_provider(person)
# fake.add_provider(internet)
# fake.add_provider(misc)
# fake.add_provider(lorem)
#
# def populate(N=5):
#     user_count = 0
#
#     w = open('user.py','w') #write into UID for reviews references
#     w.write('UIDs = [')
#
#     for n in range(N):
#         print('user_count: --------' + str(user_count))
#         user_count+=1
#         f_uid = fake.md5(raw_output=False)
#
#         # profile = models.ImageField(width_field = 'picture_width',height_field = 'picture_height', max_length = 255,upload_to='', blank=True, null=True)
#
#         f_lastName = fake.last_name()
#         f_firstName = fake.first_name()
#         if len(f_firstName)%2 == 0:
#             f_email = fake.company_email()
#             f_email = f_firstName + str(random.randint(0,50)) + '@' + f_email.split('@')[1]
#         elif len(f_lastName)%2 == 0:
#             f_email = fake.free_email()
#             f_email = f_lastName + str(random.randint(0,50)) + '@' + f_email.split('@')[1]
#         else:
#             f_email = fake.email()
#             f_email = f_lastName +'_'+ f_firstName+ '@' + f_email.split('@')[1]
#         f_email = f_email.lower()
#         f_userName = f_firstName+'-'+f_lastName
#         f_userName = f_userName.lower()
#         if len(f_userName) <=12:
#             f_userName = f_userName + str(random.randint(171,999))
#         else:
#             f_userName = f_userName[:10:] + str(f_uid)[5:8:]
#         while len(f_userName) < 8:
#             f_userName = f_userName + str(random.randint(71,170))
#
#         print('f_userName: --------' + str(f_userName))
#         f_password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
#         # w.write('user: '+f_userName + 'pw: ' + f_password + '\n')
#         fake_user = User(username=f_userName,
#                         first_name=f_firstName,last_name=f_lastName,
#                         email=f_email)
#         fake_user.set_password(f_password)
#         fake_user.save()
#         #UserProfileInfo
#
#         f_bio = fake.paragraph(nb_sentences=random.randint(0,7), variable_nb_sentences=True, ext_word_list=None)
#         f_portfolio_site = f_firstName + str(random.randint(0,50)) + '@' + 'portfolio.info'
#         profile = UserProfileInfo(user=fake_user,bio=f_bio,portfolio_site=f_portfolio_site)
#         profile.save()
#     w.write(']')
# if __name__ == '__main__':
#     populate(985)
# def defaultPassword():
#     user_count = 0
#     f_password = 'Neil1995'
#     users = User.objects.all()
#     for u in users:
#         user_count+=1
#         print('user_count: --------' + str(user_count))
#         u.set_password(f_password)
#         u.save()
# if __name__ == '__main__':
#     defaultPassword()
####test review adds

# path =  "/Users/Neil/Desktop/RMJ"
# os.chdir(path)
# from first_app.models import Review
# p = Review(2,1,1,"cad70a7ec6b2c34f71a5d4e4038f405c","2012-11-11",
#             "summary","pro","con","mgm","1","1","1","1","1","1",1)
# p.save()
#
# import random
#
# path =  "/Users/Neil/Desktop/ratemyjob"
# os.chdir(path)
# from basic_app.models import Review
# review_count = 0
# with open('csvs/Review_Final.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         review_count+=1
#         if review_count==25264:
#             print("review generated ---> " + row['RID'])
#             rand_UID = random.randint(3993,13992)
#             p = Review(int(row['RID']),int(row['CID']),int(row['PID']),rand_UID,
#             date=row['date'], summary=row['summary'],pros=row['pros'],cons=row['cons'],
#             advices_to_management=row['advices-to-management'], overall_ratings=row['overall-ratings'],
#             work_balance_stars=row['work-balance-stars'],culture_values_stars=row['culture-values-stars'],
#             career_opportunities_stars=row['career-opportunities-stars'], company_benefit_stars=row['company-benefit-stars'],
#             senior_management_stars=row['senior-management-stars'],helpful_count=row['helpful-count'])
#             p.save()


#user property
import os
path =  "/Users/Neil/Downloads/411final-upload-master"
os.chdir(path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ratemyjob.settings')
import django
django.setup()
from basic_app.models import UserProperties,UserProfileInfo
us = UserProfileInfo.objects.all()
for u in us:
    p = UserProperties(uid=u,overall_ratings=-1,work_balance_stars=-1,culture_values_stars=-1,career_opportunities_stars=-1,
company_benefit_stars=-1,senior_management_stars=-1)
    p.save()
