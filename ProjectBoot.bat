
git pull origin master

docker rm abresani-abresani-1 --force
docker rm abresani_postgresql --force

docker rmi abresani_abresani --force

docker volume create abresani_files_volume
docker volume create abresani_static_volume
docker volume create abresani_postgresql
docker network create abresani_network

docker-compose up -d
@REM (Get-Content .\abresani\settings.py) -Replace 'DEBUG = True', 'DEBUG = False' | Set-Content .\abresani\settings.py

@REM (Get-Content .\abresani\settings.py) -Replace 'DEBUG = False', 'DEBUG = True' | Set-Content .\abresani\settings.py

python manage.py makemigrations
python manage.py migrate

@REM docker system prune -a -f
