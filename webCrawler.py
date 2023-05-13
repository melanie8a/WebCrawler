from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

def filtrar_equipos(df, criterio, valor):
    if criterio == 'puntos':
        return df[df['Puntos'] == valor]
    elif criterio == 'inicio_letra':
        return df[df['Nombre'].str.startswith(valor, na=False)]
    # Agrega aquí otros criterios de filtrado según tus necesidades
    else:
        return df

url = "https://mexico.as.com/resultados/futbol/mexico_clausura/clasificacion/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# EQUIPOS
eq = soup.find_all('span', class_="nombre-equipo")
img = soup.find_all('span', class_="cont-img-escudo")

# LISTA DE EQUIPOS Y IMÁGENES
equipos = []
imagenes = []
for i, equipo in enumerate(eq[:19]):
    equipos.append(equipo.text)
    if i < len(img):
        img_url = img[i].find('img')['data-src']
        imagenes.append(img_url)
    else:
        imagenes.append('Sin imagen')

# PUNTOS
pt = soup.find_all('td', class_="destacado")

# LISTA DE PUNTOS
puntos = []
for i in pt[:19]:
    puntos.append(i.text)

df = pd.DataFrame({'Nombre': equipos, 'Puntos': puntos, 'Imagen': imagenes}, index=list(range(1, 20)))

print(df)

# Solicitar al usuario el criterio de filtrado y el valor a filtrar
criterio_filtrado = input("Ingrese el criterio de filtrado ('puntos', 'inicio_letra', etc.): ")
valor_filtrado = input("Ingrese el valor de filtrado: ")

# Filtrar los equipos según el criterio seleccionado por el usuario
equipos_filtrados = filtrar_equipos(df, criterio_filtrado, valor_filtrado)

print("\nEquipos filtrados:")
print(equipos_filtrados)

equipos_filtrados.to_csv('Equipos_filtrados.csv', index=False)

# Crear una carpeta para guardar las imágenes
carpeta_imagenes = 'Imagenes_equipos'
os.makedirs(carpeta_imagenes, exist_ok=True)

# Descargar las imágenes de los equipos filtrados
for i, imagen_url in enumerate(equipos_filtrados['Imagen']):
    if imagen_url != 'Sin imagen':
        response = requests.get(imagen_url)
        if response.status_code == 200:
            nombre_imagen = f"{i+1}.png"
            ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
            with open(ruta_imagen, 'wb') as file:
                file.write(response.content)
                print(f"Imagen {nombre_imagen} descargada correctamente.")
        else:
            print(f"No se pudo descargar la imagen {i+1}.")
