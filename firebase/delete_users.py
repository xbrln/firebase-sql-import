import time
import firebase_admin
import mysql.connector
from mysql.connector import Error
from firebase_admin import auth

app = firebase_admin.initialize_app()


def delete_users():
    try:
        connection = mysql.connector.connect(
            host='db', database='migrate_users', user='migrate_users', password='migrate_users')
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT id, uid FROM user_migrate WHERE uid IS NOT NULL ORDER BY id ASC LIMIT 1000"
            cursor.execute(query)
            records = cursor.fetchall()
            users = []
            for row in records:
                users.append(row[1])
                update_query = "UPDATE user_migrate SET uid = NULL WHERE id = %s"
                cursor.execute(update_query % row[0])
                connection.commit()
            result = auth.delete_users(users)
            print('Successfully deleted {0} users'.format(result.success_count))
            print('Failed to delete {0} users'.format(result.failure_count))
            for err in result.errors:
                print('error #{0}, reason: {1}'.format(result.index, result.reason))
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


while True:
    delete_users()
    time.sleep(4)
