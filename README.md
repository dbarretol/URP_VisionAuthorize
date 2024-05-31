# **Script: authorize.py**
En este script se sintetiza la rutina para hacer la prueba del reconocimiento facial.
Al iniciar el script se abrirá una ventana, se debe apretar la tecla 's' para tomar una foto y que el script verifique si el rostro capturado esta en la base de datos 'my_db'.
Si la confirmación es positiva, saldrá el mensaje "Bienvenido, {nombre}", y si no es positivo el reconocimiento se mostrará "Usuario no autorizado"

# **Notebook: main.ipynb**
Contiene diversas pruebas que se hicieron para llegar al código final recogido en authorize.py

# **Carpeta: my_db**
Contiene a los usuarios registrados y autorizados, cada uno tiene 8 fotos, pero pueden tener mas o menos, ya que la función 'IdentifyFace' buscará la imagen con el 'distance' mas pequeño (imagen mas similar a la tomada por la cámara web.

# Carpeta: tmp
En esta carpeta se guardaran todas las fotos que se tomen con la cámara web durante tiempo de ejecución.

# Carpeta: my_ref_db
En el notebook main.ipynb, existe una funcion que toma las imagenes en my_db, las procesa y guarda solo las caras en la carpeta my_ref_db.
