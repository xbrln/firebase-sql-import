import secrets
import firebase_admin
import mysql.connector
from mysql.connector import Error
from firebase_admin import auth
import time

app = firebase_admin.initialize_app()


def migrate_users():
    try:
        connection = mysql.connector.connect(
            host='db', database='migrate_users', user='migrate_users', password='migrate_users')
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT username, email, password, id FROM user_migrate WHERE uid IS NULL ORDER BY id ASC LIMIT 1000"
            cursor.execute(query)
            records = cursor.fetchall()
            users = []
            for row in records:
                uid = secrets.token_hex(16)
                users.append(
                    auth.ImportUserRecord(
                        uid=uid,
                        display_name=row[0],
                        email=row[1],
                        password_hash=bytes(row[2], encoding='utf-8'),
                        password_salt=bytes(row[2][:28], encoding='utf-8')
                    )
                )
                update_query = "UPDATE user_migrate SET uid = %s WHERE id = %s"
                cursor.execute(update_query, (uid, row[3]))
                connection.commit()
            hash_alg = auth.UserImportHash.bcrypt()
            try:
                result = auth.import_users(users, hash_alg=hash_alg)
                for err in result.errors:
                    print('Failed to import user:', err.reason)
                print('user migrated !')
            except exceptions.FirebaseError as error:
                print('Error importing users:', error)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


while True:
    migrate_users()
    time.sleep(8)
