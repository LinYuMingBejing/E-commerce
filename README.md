#  Cart Project
#### Enviroment:
* Ubuntu: 18.04 
* Python: 3.7
* Fronend: Bootstrap
* Backend: Django Framework
* Database: Redis, MySQL
* Cronjob: Celery

#### Web Url:  http://127.0.0.1/index/
![pages](https://img.onl/a1QWMG)

#### Deploy Applications:
```
$ cd docker
$ sudo docker-compose up --build -d
```

#### Operate Docker Container:
```
# restart container
$ sudo docker restart <container-name>

# stop container
$ sudo docker stop <container-name>

# show container log
$ sudo docker-compose logs -tail 20 -f <container-name>

# enter container
$ sudo docker exec -it <container-name> /bin/bash
```

#### Django Admin
```
# enter web container
$ sudo docker exec -it <container-name> /bin/bash

# create user
$ python manage.py createsuperuser
```

* admin url: http://127.0.0.1/admin
![admin](https://img.onl/1HvJZ6)


#### Cronjob (Celery beat)
```
$ celery beat -A Urmart.tasks -l info
$ celery worker -A Urmart.tasks -l info
```

#### Monitor Celery (Celery Flower)
* flower url: http://127.0.0.1:5001/tasks



#### CSRF Protection
* 以POST方式建立form表單，必須以{% csrf_token %}啟動CSRF防護，保護伺服器避免被攻擊。 CSRF防護方式是在伺服器產生隨機亂數的token，夾帶在表單中傳送給客戶端，當客戶端將表單送回給伺服器時，伺服器會檢查這個token是否是自己發出。
