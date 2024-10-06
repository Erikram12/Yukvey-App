# Yukvey app

## Descripción

Yukvey app es una aplicacion web para facilitar  la consulta y comparacion de datos  de reflectancia terrestre utilizando la serie de satelites Landsat.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Descripción](#descripción)
- [Uso](#uso)
- [Características](#características)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Autores](#autores)
- [Agradecimientos](#agradecimientos)

## Instalación


1.- Clonar el repositorio:

git clone https://github.com/Erikram12/Yukvey-App


2.- Acceder al directorio donde se almacena la carpeta del proyecto descargado:

```bash
  cd C:\Users\Ramsi\Documents\Yukvei-App
```
3.-Después usamos el siguiente comando para crear el entorno de flask:
```
py -3 -m venv .venv
```
4.-Despues usamos el siguiente comando para activar el entorno:
```
.venv\Scripts\activate 
```

5.-Ahora Empezamos con la instalación de lasdependencias que necesita el proyecto con los siguientes Comandos:
```
pip install Flask
pip install ee
pip install math
pip install datetime
pip install services
pip install jsonify
pip install requests
```
5.-Una vez terminada la instalacion de dependecias para ejecutar el proyecto con el servidor local usamos el siguiente comando:
```
flask --app run --debug run
```
## Descripcion:

El usuario selecciona una ubicacion de interes para que la aplicacion genere datos de reflectancia terrestre. El usuario puede personalizar sus consultas si asi lo desea y proporcionar predicciones del paso del satelite landsat cercanas a su ubicacion, la obtencion de ecenas landsat en alta resolucion y la generacion de firmas espectrales comparativas de diferentes fechas que tambien pueden ser personalizadas.

![image](https://github.com/user-attachments/assets/48024a2e-06a6-4130-8a5c-194a6e5b0d3e)

## Uso:

Los usuarios sin conocimientos fuertes en ciencias de la tierra y programacion pueden consultar datos de manera sencilla y practica para visualizar los cambios en su entorno, aprender sobre la tecnologia de reflectancia y la utilidad e impacto de los satelites de la serie Landsat de la nasaa.
Del mismo modo las personas con conocimientos avanzados tambien pueden realizar consultas mas avanzadas de acuerdo a sus nececidades modificando los parametros de captura.

## Contribuciones:

Incluir imagenes de otros satelites y herramientas para la captura de ecenas con diferentes tipos de sensores para poder funcionar en condiciones de poca luz como imagenes satelitales nocturnas o diferentes organizaciones aliadas.

## Agradecimientos:

Agradecemos la apertura de eventos que impulsan a todos los interesados  a resolver problematicas que afectan a su entorno, en especial agradecemos a todos los organizadores de la nasa international space apps challege. 
Gracias.




 




