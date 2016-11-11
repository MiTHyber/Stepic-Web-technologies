sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo gunicorn -c /home/box/web/etc/gunicorn.conf hello&
sudo gunicorn -c /home/box/web/etc/gunicorn2.conf wsgi&
sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/mysql start
mysql -u root -e "CREATE USER 'saya'@'localhost'"
mysql -u root -e "SET PASSWORD FOR 'saya'@'localhost' = PASSWORD('sayanouta')"
mysql -u root -e "CREATE DATABASE ask"
mysql -u root -e "GRANT ALL ON ask.* TO 'saya'@'localhost'"
sudo ./ask/manage.py makemigrations
sudo ./ask/manage.py migrate

