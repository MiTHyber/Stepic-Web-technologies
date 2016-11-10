sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo gunicorn -c /home/box/web/etc/gunicorn.conf hello --daemon
sudo gunicorn -c /home/box/web/etc/gunicorn2.conf wsgi --daemon
sudo /etc/init.d/gunicorn restart
