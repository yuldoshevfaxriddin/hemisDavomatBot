import sqlite3

DB_NAME = "hemisInfo.db"
DB_TABLE_NAME = ' USERS '

data_base_connection = sqlite3.connect(DB_NAME)
cursor = data_base_connection.cursor()

def createTable(db_name=DB_TABLE_NAME):
    TABLE_CREATE_QUERY = '''CREATE TABLE {} (
        id INTEGER PRIMARY KEY  AUTOINCREMENT ,
        hemis_user_id varchar(20),
        hemis_user_password varchar(50),
        hemis_profil varchar(50),
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
def insertData(hemis_user_id,hemis_user_password,hemis_profil,tg_user_id,tg_username,tg_first_name,tg_last_name,hemis_cookies_dict=None,user_disabled = 1):
    
    INSERT_INTO_QUERY = f'''INSERT INTO {DB_TABLE_NAME} (hemis_user_id,hemis_user_password,hemis_profil,hemis_cookies_dict,tg_user_id,tg_username,tg_first_name,tg_last_name,user_disabled)
                                VALUES ('{hemis_user_id}','{hemis_user_password}','{hemis_profil}','{hemis_cookies_dict}','{tg_user_id}','{tg_username}','{tg_first_name}','{tg_last_name}','{user_disabled}'); '''
    respons = cursor.execute(INSERT_INTO_QUERY)
    data_base_connection.commit()
    return respons

def selectAllData():
    SELECT_ALL_DATA_QUERY = '''SELECT * FROM {}'''.format(DB_TABLE_NAME)
    respons = cursor.execute(SELECT_ALL_DATA_QUERY).fetchall()
    return respons

def selectUserId(tg_user_id):
    SELECT_ALL_DATA_QUERY = '''SELECT * FROM {} WHERE {}'''.format(DB_TABLE_NAME,tg_user_id)
    respons = cursor.execute(SELECT_ALL_DATA_QUERY).fetchall()
    return respons

# createTable()

# client1 = insertData(hemis_user_id='390201100297',hemis_user_password='390201100297d',hemis_profil='Yuldoshev Faxriddin',tg_user_id='1742197944',tg_username='yuldoshev_faxriddin',tg_first_name='yuldoshev',tg_last_name='faxriddin')
# client2 = insertData(hemis_user_id='390201100297',hemis_user_password='390201100297d',hemis_profil='Yuldoshev Faxriddin',tg_user_id=1742197944,tg_username='yuldoshev_faxriddin',tg_first_name='yuldoshev',tg_last_name='faxriddin')
# print(client1)
# print(client2)
# client3 = selectUserId(tg_user_id=12)
# print(client3)
# client3 = selectUserId(tg_user_id=1742197944)
# print(len(client3))



# test = selectAllData(cur)

# for i in test:
#     print(i)

cursor.close()
# data_base_connection.commit()
data_base_connection.close()