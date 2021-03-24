# firebase-user-import

This project consists of couple of python scripts, which do the following,
- Import users from a mysql database to firebase
- Delete those migrated users
- Create a new user in firebase
- Login to firebase with the created users email and password

## Installation

- git clone
- Build containers by running
```docker-compose up --build -d```

## Other requirements

- To have a mysql database with a migrate_users table which has username, email, passowrd, uid and id column
- To have a Firebase project set up and add firebase credentials to a newly created file called credentials.json in firebase directory

## How to run the scripts

- ssh into docker web container by running
```docker exec -it migrate-users-web bash```
- cd into firebase directory
``` cd firebase```
- Import users by running
```python migrate.py```
- Delete users by running
```python delete_users.py```
- Create a user by running 
```python create_user.py```
- Login user by running
```python login_user.py --email email --password password```
