<VirtualHost *:49502>
     ServerName 2001:1bb0:e000:1e::421 
     WSGIScriptAlias / /home/dev/crocohost/crocohost/app.wsgi
     <Directory /home/username/ExampleFlask/ExampleFlask/>
     		# set permissions as per apache2.conf file
            Options FollowSymLinks
            AllowOverride None
            Require all granted
     </Directory>
     # ErrorLog ${APACHE_LOG_DIR}/error.log
     # LogLevel warn
     # CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
