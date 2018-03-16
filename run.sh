#!/bin/bash
python manage.py runserver & python bot.py &
#sudo sysctl fs.inotify.max_user_watches=16384