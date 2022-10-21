powershell -Command "(Get-Content .\abresani\settings.py) -Replace 'DEBUG = True', 'DEBUG = False' | Set-Content .\abresani\settings.py"

git pull origin master

docker rm abresani-abresani-1 --force
docker rm abresani_postgresql --force
docker rmi abresani_abresani --force


docker rmi nginx_nginx --force
docker rm nginx --force
docker volume rm abresani_static_volume


docker volume create abresani_files_volume
docker volume create abresani_static_volume
docker volume create abresani_postgresql
docker network create abresani_network

docker-compose up -d


powershell -Command "(Get-Content .\abresani\settings.py) -Replace 'DEBUG = False', 'DEBUG = True' | Set-Content .\abresani\settings.py"

python .\manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

cd config\nginx\
docker-compose up -d


@REM docker system prune -a -f
