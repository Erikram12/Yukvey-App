import base64

from flask import Flask, request, session, jsonify
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timezone

import pytz
from flask import render_template, request
from matplotlib import pyplot as plt

from app import app
import io


from models import LandsatSatelite
from services import ConexionN2yo, ConexionGoogleEE
import ee
import geemap
from flask_leaflet import Leaflet

app.secret_key = 'animalitosverdes1236'  # Cambia esto por una clave secreta única para tu aplicación

# Ruta para la página principal (home)
@app.route('/')
def index():
    recursos = [
        {
            "icon": "fire",
            "title": "Prevencion de Incendios forestales",
            "description": "La NASA proporciona muchos recursos para monitorear y rastrear incendios forestales.",
            "color": "green"
        },
        {
            "icon": "code",
            "title": "Ciencia abierta",
            "description": "La ciencia abierta potencia un proceso científico inclusivo y colaborativo a través del intercambio abierto de datos y conocimientos.",
            "color": "orange"
        },
        {
            "icon": "wind",
            "title": "Calidad del aire",
            "description": "La contaminación del aire es una de las mayores amenazas mundiales para el medio ambiente y la salud.",
            "color": "teal"
        }
    ]
    return render_template('index.html', recursos=recursos)

# Ruta para la página "About"
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para la página "Services"
@app.route('/services')
def services():
    return render_template('services.html')

# Ruta para la página "Contact"
@app.route('/contact')
def contact():
    return render_template('contact.html')


#-----------------------------------------------------------------------------------------------------------------------

@app.route('/ecenaLandsat', methods=['GET','POST'])

def ecenaLandsat():

    latitud = request.form.get('lat')  # Obtiene la latitud del formulario
    longitud = request.form.get('lon')  # Obtiene la longitud del formulario


    print(f'Latitud: {latitud} y longitud {longitud}: ' )


    # Imprimir para depuración
    print('Ingresamos a la funcion para generar escena landsat')



    #Crear objeto para usar la coneccion con la api:
    conexion = ConexionGoogleEE.Conexion()
    conexion.conectar()

    longitud = float(longitud)
    latitud = float(latitud)

    # Definir el área de interés (AOI) para San Miguel el Grande, Oax
    aoi = ee.Geometry.Point(longitud,latitud) # Coordenadas ajustadas según el AOI

    # Definir el rango de fechas para agosto de 2024
    start_date = '2024-08-01'
    end_date = '2024-08-31'

    # Seleccionar imágenes de Landsat 5, 7, 8 y 9 de la Collection 2 para el rango de fechas definido
    landsat5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2') \
              .filterDate(start_date, end_date) \
              .filterBounds(aoi)

    landsat7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2') \
              .filterDate(start_date, end_date) \
              .filterBounds(aoi)

    landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
              .filterDate(start_date, end_date) \
              .filterBounds(aoi)

    landsat9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2') \
              .filterDate(start_date, end_date) \
              .filterBounds(aoi)

    # Combinar todas las colecciones en una sola
    all_landsat = landsat5.merge(landsat7).merge(landsat8).merge(landsat9)

    # Función para aplicar la corrección atmosférica
    def apply_atmospheric_correction(image):
        surface_reflectance = image.select(['SR_B4', 'SR_B3', 'SR_B2']).divide(10000)  # Normalizar las bandas
        return surface_reflectance

    # Aplicar la corrección a todas las imágenes
    corrected_landsat = all_landsat.map(apply_atmospheric_correction)

    # Seleccionar la imagen más reciente
    most_recent_image = corrected_landsat.sort('system:time_start', False).first()

    # Mostrar la lista de imágenes (opcional)
    image_list = all_landsat.aggregate_array('system:index').getInfo()
    print("Lista de imágenes Landsat encontradas:", image_list)

    # Visualizar la imagen más reciente usando los valores de min y max proporcionados
    # Crear un mapa interactivo centrado en San Miguel el Grande, Oax
    Map = geemap.Map(center=[16.9464, -97.1443], zoom=10)

    #   Agregar la imagen corregida al mapa en bandas RGB
    rgb_vis_params = {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0.7896480202674866,
    'max': 2.100752031803131,
    'gamma': [1.4, 1.4, 1.4]
    }
    Map.addLayer(most_recent_image, rgb_vis_params, 'Most Recent Corrected RGB')

    # Agregar el área de interés (AOI) al mapa
    Map.addLayer(aoi, {}, 'Área de Interés')

    # Guardar el mapa como archivo HTML
    Map.save(outfile="ecenitaLandsat.html")
    #y leer su contenido
    with open("ecenitaLandsat.html", 'r') as file:
        mapa_html = file.read()

    return render_template('index.html', Mapa=mapa_html, latitudes= latitud, longitudes = longitud)

if __name__ == '__main__':
    app.run(debug=True)



#-----------------------------------------------------------------------------------------------------------------------

@app.route('/cuadriculaLandsat', methods=['GET','POST'])

def cuadriculaLandsat():

    # Inicializa la API de Google Earth Engine
    #Crear objeto para usar la coneccion con la api:
    conexion = ConexionGoogleEE.Conexion()
    conexion.conectar()



    # Capturamos las coordenadas que vienen en la URL
    latitud = request.args.get('lat')
    longitud = request.args.get('lon')

    longitud = float(longitud)
    latitud = float(latitud)

    print(latitud, longitud)

    # Definir el área de interés (AOI) para San Miguel el Grande, Oax
    aoi = ee.Geometry.Point(longitud,latitud) # Coordenadas ajustadas según el AOI
    # Definir el rango de fechas para agosto de 2024
    start_date = '2024-08-01'
    end_date = '2024-08-31'

    # Seleccionar imágenes de Landsat 5, 7, 8 y 9 de la Collection 2 para el rango de fechas definido
    landsat5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi)

    landsat7 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi)

    landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi)

    landsat9 = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi)

    # Combinar todas las colecciones en una sola
    all_landsat = landsat5.merge(landsat7).merge(landsat8).merge(landsat9)

    # Función para aplicar la corrección atmosférica
    def apply_atmospheric_correction(image):
        surface_reflectance = image.select(['SR_B4', 'SR_B3', 'SR_B2']).divide(10000)  # Normalizar las bandas
        return surface_reflectance

    # Aplicar la corrección a todas las imágenes
    corrected_landsat = all_landsat.map(apply_atmospheric_correction)

    # Seleccionar la imagen más reciente
    most_recent_image = corrected_landsat.sort('system:time_start', False).first()

    # Mostrar la lista de imágenes (opcional)
    image_list = all_landsat.aggregate_array('system:index').getInfo()
    print("Lista de imágenes Landsat encontradas:", image_list)

    # Crear un mapa interactivo centrado en San Miguel el Grande, Oax
    Map = geemap.Map(center=[16.9464, -97.1443], zoom=10)

    # Definir la ubicación del AOI como punto de referencia (San Miguel el Grande)
    aoi_center = ee.Geometry.Point([-97.1087, 16.9690])  # Coordenadas para el centro del AOI

    # Definir el tamaño del píxel de Landsat
    pixel_size = 30  # 30 metros por píxel

    # Definir la cuadrícula de 3x3 píxeles centrada en el punto `aoi_center`
    x_offsets = [-pixel_size, 0, pixel_size]
    y_offsets = [-pixel_size, 0, pixel_size]

    # Función para mover un punto a nuevas coordenadas relativas a su posición original
    def move(geometry, dx, dy):
        """Desplaza una geometría en dirección x e y según los metros indicados."""
        lon, lat = geometry.getInfo()['coordinates']
        new_lon = lon + dx / 111320  # Aproximación de metros a grados en longitud
        new_lat = lat + dy / 110540  # Aproximación de metros a grados en latitud
        return ee.Geometry.Point([new_lon, new_lat])

    # Crear la lista de píxeles desplazados y cuadrículas
    grid_coordinates = []
    for x_offset in x_offsets:
        for y_offset in y_offsets:
            pixel_center = move(aoi_center, x_offset, y_offset)
            pixel_square = pixel_center.buffer(pixel_size / 2).bounds()
            grid_coordinates.append(pixel_square)

    # Crear una colección de geometrías para la cuadrícula 3x3
    grid_collection = ee.FeatureCollection(grid_coordinates)

    # Recortar la imagen más reciente a la geometría de la cuadrícula
    clipped_image = most_recent_image.clip(grid_collection)

    # Visualizar la imagen recortada usando los valores de min y max proporcionados
    rgb_vis_params = {
        'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
        'min': 0.7896480202674866,
        'max': 2.100752031803131,
        'gamma': [1.4, 1.4, 1.4]
    }

    # Agregar la imagen recortada al mapa en bandas RGB
    Map.addLayer(clipped_image, rgb_vis_params, 'Imagen Recortada RGB')

    # Añadir el centro del AOI al mapa
    Map.addLayer(aoi_center, {'color': 'blue'}, 'Píxel de Destino')

    # Añadir la cuadrícula de 3x3 píxeles al mapa
    Map.addLayer(grid_collection, {'color': 'red'}, 'Cuadrícula 3x3')

    # Mostrar el mapa interactivo
    Map.addLayerControl()  # Añadir control de capas
    Map

    # Guardar el mapa como archivo HTML
    Map.save(outfile="cuadricula_recortada.html")
    #y leer su contenido
    with open("cuadricula_recortada.html", 'r') as file:
        cuadricula_html = file.read()

    return render_template('index.html', Cuadricula=cuadricula_html,cordenada1=latitud,cordenada2=longitud)
if __name__ == '__main__':
    app.run(debug=True)

#-----------------------------------------------------------------------------------------------------------------------

@app.route('/FirmaEspectral', methods = ['POST','GET'])
def firmaEspectral():
    # Inicializa la API de Google Earth Engine
    # Crear objeto para usar la coneccion con la api:
    conexion = ConexionGoogleEE.Conexion()
    conexion.conectar()

    # Capturamos las coordenadas que vienen en la URL
    latitud = request.args.get('lat')
    longitud = request.args.get('lon')

    longitud = float(longitud)
    latitud = float(latitud)

    print(latitud, longitud)

    # Definir el área de interés (AOI) - San Miguel el Grande, Oaxaca
    aoi = ee.Geometry.Point([-97.1087, 16.9690])  # Centro del AOI como un punto

    # Seleccionar una imagen de Landsat 8 para el área de interés y un rango de fechas
    landsat_image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(aoi) \
        .filterDate('2024-08-01', '2024-08-31') \
        .first()

    # Obtener los valores de las bandas SR (Surface Reflectance)
    bands = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7']  # Bandas Landsat 8 visibles e infrarrojo cercano
    band_names = ['Blue', 'Green', 'Red', 'NIR', 'SWIR1', 'SWIR2']  # Nombres de las bandas para el gráfico

    # Reducir el área al valor promedio de cada banda en el punto de interés (AOI)
    mean_dict = landsat_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=30,  # Escala de píxel para Landsat 8
        maxPixels=1e9
    )

    # Obtener los valores de reflectancia de las bandas
    mean_values = mean_dict.getInfo()  # Convertir a diccionario Python

    # Extraer valores de reflectancia en cada banda
    reflectance_values = [mean_values[band] for band in bands]

    # Mostrar los metadatos principales de la escena
    satellite = landsat_image.get('SPACECRAFT_ID').getInfo()
    date = landsat_image.date().format('YYYY-MM-dd').getInfo()
    cloud_coverage = landsat_image.get('CLOUD_COVER').getInfo()
    print(f"Satélite: {satellite}")
    print(f"Fecha de adquisición: {date}")
    print(f"Porcentaje de nubosidad: {cloud_coverage}%")

    # Crear el gráfico de la firma espectral
    plt.figure(figsize=(10, 6))
    plt.plot(band_names, reflectance_values, marker='o', linestyle='-', color='b')
    plt.title(f'Firma Espectral para el AOI - {date}')
    plt.xlabel('Bandas Espectrales')
    plt.ylabel('Reflectancia')
    plt.grid(True)

    # Guardar la imagen como archivo PNG
    plt.savefig('firma_espectral.png', format='png')

    # Leer la imagen en modo binario y codificarla a base64
    with open("firma_espectral.png", 'rb') as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')

    # Renderizar la plantilla y pasar la cadena base64
    return render_template('index.html', firma=encoded_image, latitudfirma1 = latitud, latitudfirma2= longitud)



# Ruta de API N2Y0(Prediccion de paso de satelite)
@app.route('/api-data', methods=['POST','GET'])
def api_data():

    latitud = (request.form.get('lat')) # Obtiene la latitud del formulario
    longitud = (request.form.get('lon'))  # Obtiene la longitud del formulario


    print(f"Latitud: {session['latitud']}, Longitud: {session['longitud']}")

    conexion = ConexionN2yo.Conexion()
    json_data = conexion.conectar(latitud,longitud)  # Llama al método con las coordenadas


    if json_data:  # Verifica que la conexión fue exitosa y se obtuvieron datos
        data = json_data
        info = LandsatSatelite.Info(**data['info'])
        positions = [LandsatSatelite.Position(**pos) for pos in data['positions']]
        satellite_data = LandsatSatelite.SatelliteData(info, positions)

        # Imprimir los resultados para verificar
        # print(satellite_data)

        # Extraer longitud y latitud del primer punto
        usuarioPoint = conexion.datosGeograf(latitud, longitud)
        longitudFirst = positions[0].satlongitude
        latitudFirst = positions[0].satlatitude

        # Extraer longitud y latitud de las posiciones para el trazado
        longitudes = [position.satlongitude for position in positions]
        latitudes = [position.satlatitude for position in positions]



        def haversineFormula(lat1, lon1, lat2, lon2):
            # Convertir grados a radianes
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

            # Diferencias
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            # Fórmula de Haversine
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            # Radio de la Tierra en kilómetros (aproximadamente 6371 km)
            r = 6371

            return r * c

        min_distance = float('inf')  # Inicializar con un valor muy alto
        closest_time = None
        closest_position = None

        for position in positions:
            # Convertir todas las coordenadas a float antes de pasar a la fórmula Haversine
            distance = haversineFormula(float(position.satlatitude), float(position.satlongitude),
                                        float(usuarioPoint[0]),
                                        float(usuarioPoint[1]))

            if distance < min_distance:
                min_distance = distance
                closest_time = position.timestamp  # timestamp

                closest_position = position  # posicion de satelite mas corta

        # Convertir el timestamp a una fecha y hora legible
        fecha_legible = datetime.fromtimestamp(closest_time, tz=timezone.utc)

        # Convertir a zona horaria de México (CDT)
        zona_mexico = pytz.timezone('America/Mexico_City')
        fecha_mexico = fecha_legible.astimezone(zona_mexico)

        print(f"La posición más cercana es a {min_distance} km y ocurre en {fecha_mexico}")
        print(closest_position)

        prediccioncita = f"La posición más cercana es a {min_distance} km y ocurre en {fecha_mexico}"


    return render_template('index.html', prediccion= prediccioncita)


# Ruta /ecenaLandsat sigue igual
@app.route('/ecenaLandsat', methods=['POST'])
def ecena_landsat():
    # Aquí procesas la funcionalidad de /ecenaLandsat como lo tienes
    # ...
    return render_template('index.html')

# Nueva ruta para obtener metadatos de Landsat
@app.route('/get_metadata', methods=['POST'])
def get_metadata():
    # Obtener latitud y longitud desde la solicitud del cliente
    latitude = request.form['lat']
    longitude = request.form['lon']

    # Definir el área de interés (AOI) usando latitud y longitud proporcionadas
    aoi = ee.Geometry.Point([float(longitude), float(latitude)])

    # Seleccionar una imagen de Landsat 8 en el rango de fechas especificado
    landsat_image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(aoi) \
        .filterDate('2024-08-01', '2024-08-31') \
        .first()

    # Obtener metadatos de la imagen
    try:
        satellite = landsat_image.get('SPACECRAFT_ID').getInfo()  # Satélite de adquisición
        date = landsat_image.date().format('YYYY-MM-dd').getInfo()  # Fecha de adquisición
        time = landsat_image.date().format('HH:mm:ss').getInfo()  # Hora de adquisición
        sensor_latitude = landsat_image.get('SENSOR_LATITUDE').getInfo()  # Latitud del sensor
        sensor_longitude = landsat_image.get('SENSOR_LONGITUDE').getInfo()  # Longitud del sensor
        wrs_path = landsat_image.get('WRS_PATH').getInfo()  # Ruta WRS
        wrs_row = landsat_image.get('WRS_ROW').getInfo()  # Fila WRS
        cloud_coverage = landsat_image.get('CLOUD_COVER').getInfo()  # Porcentaje de nubosidad
        image_quality = landsat_image.get('IMAGE_QUALITY').getInfo()  # Calidad de la imagen

        # Renderizar los datos a la plantilla HTML
        return render_template('index.html',
                               satellite=satellite,
                               date=date,
                               time=time,
                               sensor_latitude=sensor_latitude,
                               sensor_longitude=sensor_longitude,
                               wrs_path=wrs_path,
                               wrs_row=wrs_row,
                               cloud_coverage=cloud_coverage,
                               image_quality=image_quality,
                               lat=latitude, lon=longitude)

    except Exception as e:
        return render_template('index.html', error=str(e), lat=latitude, lon=longitude)

if __name__ == '__main__':
    app.run(debug=True)


