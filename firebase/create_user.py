import firebase_admin
from firebase_admin import auth

app = firebase_admin.initialize_app()

users = [
    auth.ImportUserRecord(
        uid='some-uid',
        email='user@example.com',
        password_hash=b'password_hash',
        password_salt=b'salt'
    ),
]

hash_alg = auth.UserImportHash.bcrypt()
try:
    result = auth.import_users(users, hash_alg=hash_alg)
    for err in result.errors:
        print('Failed to import user:', err.reason)
except exceptions.FirebaseError as error:
    print('Error importing users:', error)

    app = firebase_admin.initialize_app()
