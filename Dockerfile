FROM php:8.1-apache

WORKDIR /home/allergens

COPY ./frontend /var/www/html/

COPY ./db /home/db/

COPY ./server /home/server/

# Install necessary packages
RUN docker-php-ext-install mysqli

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

RUN apt-get update ; apt-get install -y python3 default-mysql-server default-mysql-client

# Establish database
RUN 
RUN mysql -u root < /home/db/database-data.sql ; mysql -u root < /home/db/database-data.sql
RUN touch menu.pdf ; python3 /home/db/db-update.py

# Establish https
RUN cp /home/server/ssl.conf /etc/apache2/sites-available/default-ssl.conf
RUN cp /home/server/allergens.crt /etc/ssl/certs
RUN cp /home/server/allergens.key /etc/ssl/private

# Enable Apache SSL module
RUN a2enmod ssl
RUN a2ensite default-ssl.conf
RUN service apache2 restart

EXPOSE 443