# Pagina-Web-Practica
Pagina web de la practica realizada durante los meses de enero y febrero
## Instalacion en Ubuntu (recomendada para servidor AWS)

Para una guia mas detallada puedes seguir los tutoriales de digital ocean
  - <a href="https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04">Apache, MySQL y PHP</a>
  - <a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-phpmyadmin-on-ubuntu-18-04">phpMyAdmin</a>

### Install Apache HTTP Server
```
sudo apt update
sudo apt install apache2
```
### Install MySQL Database
```
sudo apt install mysql-server
sudo mysql
```
- Esto configurara la clave del usuario de mysql para ajustarla al de nuestro proyecto
- Se recomienda copiar linea por linea para ejecutar por separado
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Unab.2019';
FLUSH PRIVILEGES;
exit
```
### Install PHP Engine
```
sudo apt install php libapache2-mod-php php-mysql
sudo systemctl restart apache2
```
### Install phpMyAdmin Tool

<b>ADVERTENCIA:</b> Durante la instalacion nos preguntará varias cosas que debemos tener en mente previo a instalar.

- La primera cosa que nos preguntará es que motor web utilizaremos. En la lista veremos que <b>Apache 2</b> aparece <b>destacado</b> pero aun asi este no esta <b>seleccionado</b> por lo que debes apretar la <b>barra espaciadora</b> para marcarlo (aparecera un asterisco) luego presiona <b>TAB</b> y <b>ENTER</b> para continuar la instalacion.
- La segunda seleccion es para las crenciales simplemente selecciona <b>YES</b> y presiona <b>ENTER</b>
- En la tercera nos pedira ingresar manualmente una clave, escribimos <b>Unab.2019</b> y le damos <b>ENTER</b>
```
sudo apt install phpmyadmin php-mbstring php-gettext
sudo phpenmod mbstring
sudo systemctl restart apache2
```
### Configurar la base de datos
- Crear base de datos con el nombre <b>CyberAware</b>
- Importar el archivo <b>CrearTablas.sql</b>
### Install Miniconda
- Descargar miniconda desde <a href="https://docs.conda.io/en/latest/miniconda.html">aqui. </a>
- Una vez descargado dirigirse a la ubicación del archivo y correr el siguiente comando
```
bash Miniconda3-latest-Linux-x86_64.sh
```
### Levantar Página Web
- Tenemos que clonar este repositorio en nuestra maquina
- Tenemos que mover el directorio a <b>/var/www/html/..</b>
- Ahora tenemos que instalar las librerias necesarias para el proyecto, por lo que hay que dirigirse a la carpeta script y correr el siguiente comando:
 ```
 pip install requsitos.txt
 ```
Tambien se deben descargar las stopwords para que no tengamos problemas:
```
import nltk
nltk.download('stopwords')
```

- Una vez instaladas las librerias tenemos que levantar el servicio:
```
nohup python Servicio.py &
```
- Por ultimo solo queda correr el archivo auto.py para ello tenemos que hacer:
```
python auto.py
```
o si queremos que corra en background
```
nohup python auto.py &
```


