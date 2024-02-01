import sqlite3

DB_NAME = "hemisInfo.db"
DB_TABLE_NAME = ' USERS '

data_base_connection = sqlite3.connect(DB_NAME,check_same_thread=False,)
cursor = data_base_connection.cursor()

def createTable(db_name=DB_TABLE_NAME):
    TABLE_CREATE_QUERY = '''CREATE TABLE {} (
        id INTEGER PRIMARY KEY  AUTOINCREMENT ,
        hemis_user_id varchar(20),
        hemis_user_password varchar(50),
        hemis_profil varchar(50),
        hemis_profil_image varchar(100),
        hemis_cookies_dict varchar(250),
        tg_user_id varchar(15),
        tg_username varchar(50),
        tg_first_name varchar(50),
        tg_last_name varchar(50),
        user_disabled INTEGER 
    );'''.format(db_name)
  
    respons = cursor.execute(TABLE_CREATE_QUERY)
    # cursor.close()
    return respons

# user_disabled = 1  user malumotlarini olib biladi, user_disabled = 0 user malumotlarini olib bilmaydi
# malumotlarni qo'shish uchun
def insertData(hemis_user_id,hemis_user_password,hemis_profil,hemis_img,tg_user_id,tg_username,tg_first_name,tg_last_name,hemis_cookies_dict='',user_disabled = 1):
    # hemis_img = ''
    # hemis_cookies_dict = ''
    INSERT_INTO_QUERY = f'''INSERT INTO {DB_TABLE_NAME} (hemis_user_id,hemis_user_password,hemis_profil,hemis_profil_image,hemis_cookies_dict,tg_user_id,tg_username,tg_first_name,tg_last_name,user_disabled) VALUES ('{hemis_user_id}','{hemis_user_password}','{hemis_profil}','{hemis_img}','{hemis_cookies_dict}','{tg_user_id}','{tg_username}','{tg_first_name}','{tg_last_name}','{user_disabled}'); '''
    print(INSERT_INTO_QUERY)
    respons = cursor.execute(INSERT_INTO_QUERY)
    data_base_connection.commit()
    return respons
# barcha malumotlarni olish uchun
def selectAllData():
    SELECT_ALL_DATA_QUERY = '''SELECT * FROM {}'''.format(DB_TABLE_NAME)
    respons = cursor.execute(SELECT_ALL_DATA_QUERY).fetchall()
    return respons
# telegram user borlgini tekshirish
def selectUserId(tg_user_id):
    # telegram user borligini tekshirish
    SELECT_ALL_DATA_QUERY = '''SELECT * FROM {} WHERE tg_user_id={}'''.format(DB_TABLE_NAME,tg_user_id)
    respons = cursor.execute(SELECT_ALL_DATA_QUERY).fetchall()
    return respons

def deleteUser(id,db_name = DB_TABLE_NAME):
    DELETE_QUERY = '''DELETE FROM {} WHERE id='{}';'''.format(db_name,id)
    respons = cursor.execute(DELETE_QUERY)
    data_base_connection.commit()
    return respons

def updateUserDisabled(id,disabled = 1,db_name = DB_TABLE_NAME):
    UPDATE_QUERY = f'''UPDATE {db_name} SET user_disabled = {disabled} WHERE id = {id} ;'''
    respons = cursor.execute(UPDATE_QUERY)
    data_base_connection.commit()
    return respons
def updateCookies(tg_id,cookies,db_name = DB_TABLE_NAME):
    UPDATE_QUERY = f'''UPDATE {db_name} SET hemis_cookies_dict = '{cookies}' WHERE id = {tg_id} ;'''
    respons = cursor.execute(UPDATE_QUERY)
    data_base_connection.commit()
    return respons


# createTable()

# client1 = insertData(hemis_user_id='390201100297',hemis_user_password='390201100297d',hemis_profil='Yuldoshev Faxriddin',tg_user_id='sacs1742197944',tg_username='yuldoshev_faxriddin',tg_first_name='yuldoshev',tg_last_name='faxriddin')
# client2 = insertData(hemis_user_id='390201100297',hemis_user_password='390201100297d',hemis_profil='Yuldoshev Faxriddin',tg_user_id=1742197944,tg_username='yuldoshev_faxriddin',tg_first_name='yuldoshev',tg_last_name='faxriddin')
# print(client1)
# print(client2)
# client3 = selectUserId(tg_user_id=12)
# print(client3)
# client3 = selectUserId(tg_user_id=1742197944)
# print(client3)

if __name__ == '__main__':
    test = selectAllData()
    print(len(test))
    for i in test:
        print(i)

# # print(updateUserDisabled(8,0).fetchall())

# test = selectAllData()
# for i in test:
#     print(i)

# cursor.close()
# # data_base_connection.commit()
# data_base_connection.close()




# INSERT INTO  USERS  (hemis_user_id,hemis_user_password,hemis_profil,hemis_profil_image,hemis_cookies_dict,tg_user_id,tg_username,tg_first_name,tg_last_name,user_disabled)  
#                                 VALUES ('390201100297','390201100297d','YO‘LDOSHOV F. U.  941-20DIo'','https://hemis.ubtuit.uz/static/crop/3/3/120_120_90_3343658253.jpg','{"_frontendUser": "e65d589ae348dcb1cbdfaae24486c23040114a27b01dd93da24890ddd609bf34a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_frontendUser%22%3Bi%3A1%3Bs%3A46%3A%22%5B%2218%22%2C%22tG3FjTMA1yF6uNcm2Wx7O3KVRIU2ETxP%22%2C3600%5D%22%3B%7D"}','1742197944','Faxriddin_yuldoshev','Faxriddin Yuldoshev','Faxriddin Yuldoshev','1');