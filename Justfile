
su:
   ./manage.py createsuperuser --email karsten.kroesch@ag.ch --username karsten

serve:
   ./manage.py runserver

migrate:
   ./manage.py makemigrations
   ./manage.py migrate
   
