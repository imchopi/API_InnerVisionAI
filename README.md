## 1. Justificación y descripción del proyecto.

## 2. Obtención de datos. Se debe especificar la fuente de los datos. Se indicará por qué medios se han obtenido (encuestas, sensores, scrapping, etc.). Los datos se deben cargar en una estructura que permita su posterior manipulación y uso.

Para conseguir los datos que necesitábamos, decidimos extraer imágenes de internet 🖼️. Como nuestro modelo va a funcionar en tiempo real ⏳, queríamos que reconociera objetos comunes en la empresa, como sillas, armarios y mesas 🪑📦.

Por eso elegimos IKEA 🏠 como fuente de información, ya que es una de las mejores referencias y sabemos que tiene justo lo que estábamos buscando ✅.

Lo primero que hicimos fue instalar las librerías necesarias 🛠️. Al principio, como la web parecía sencilla 🌐, pensamos que con BeautifulSoup 🥣 sería suficiente, pero no fue así ❌.

Si queríamos cargar todas las imágenes 🖼️, nos dimos cuenta de que había un botón de "Mostrar más" 🔘 que era el encargado de cargar las imágenes.

Para solucionar este problema, utilizamos Selenium 🚗💨, que nos permite interactuar con la web como si fuéramos un usuario real.

A continuación, explicaré las librerías que usaremos 📚 para llevar a cabo la extracción de datos 🔍.

### 📌 Librerías utilizadas para la extracción de datos

# Foto 

Para poder extraer información de la web, utilizamos varias librerías 📚 que nos ayudarán en diferentes tareas:

os 📂 → Nos permite interactuar con los archivos y carpetas de nuestro sistema.

time ⏳ → Se usa para pausar el código y esperar antes de realizar ciertas acciones.

requests 🌍 → Nos ayuda a hacer peticiones a sitios web y obtener su contenido.

re 🔍 → Se usa para trabajar con patrones de texto, como encontrar enlaces o filtrar datos.
BeautifulSoup (de bs4) 🥣 → Nos permite extraer información de una página web de forma más sencilla.

🚀 Automatización con Selenium

webdriver 🚗 → Nos permite controlar un navegador web (como Chrome).

Service 🛠️ → Maneja la configuración del navegador para Selenium.

Options ⚙️ → Nos ayuda a establecer preferencias para el navegador (como abrirlo en modo 
invisible).

By 🔎 → Se usa para encontrar elementos dentro de la página web.

WebDriverWait ⏳ → Permite que el código espere hasta que un elemento de la web aparezca.

expected_conditions (EC) ✅ → Nos ayuda a esperar hasta que ciertas condiciones se cumplan, como que un botón sea visible antes de hacer clic.

## 🔍 Estructura del Código  

Lo siguiente que mostraré es un poco cómo he **organizado** este código 📜.  

Voy a explicar **cada parte** para que sea fácil de entender y seguir 📌.  

---

## FOTO 

# 🖥️ Clase IKEA Scraper

Esta clase se encarga de **extraer información** de la web de **IKEA** 🏠, específicamente imágenes de **armarios, mesas y sillas**.  

## 📌 1. Inicialización (`__init__` method)  
Cuando creamos un objeto de esta clase, se ejecuta este código automáticamente.  

### 🔗 `self.category_urls`  
- Es un diccionario que contiene las **categorías de muebles** y los enlaces de IKEA donde están los productos 📦.  
- Por ejemplo, para obtener **armarios**, el código buscará en:  
  - `"https://www.ikea.com/es/es/cat/armarios-19053/"`  

### 🏷️ `self.headers`  
- Sirve para **simular** que el navegador es un usuario real y evitar bloqueos de la web.  
- Aquí se usa un **"User-Agent"** (que le dice a la web que estamos usando un navegador como Chrome o Firefox).  

---

## 🚀 2. Configuración del navegador con Selenium  
Como la web tiene **botones interactivos**, usamos **Selenium** para controlarla automáticamente.  

### ⚙️ `chrome_options = Options()`  
- Nos permite **configurar** cómo se abrirá el navegador.  
- `chrome_options.add_argument("--start-maximized")` 🖥️  
  - Abre el navegador en **pantalla completa** para evitar problemas con elementos ocultos.  

### 🚗 `self.driver = webdriver.Chrome(...)`  
- Aquí estamos **iniciando Chrome** para que Selenium pueda interactuar con la web **como si fuera un usuario real**.  

---

## 📁 Función `create_directories`

Esta función se encarga de **crear carpetas** en el sistema para almacenar las imágenes de cada categoría 🗂️.

### 🛠️ ¿Cómo funciona?

1. **Obtiene las categorías** 🏷️  
   - Usa `self.category_urls.keys()` para obtener la lista de categorías disponibles (ejemplo: "sillas", "mesas", "armarios").  

2. **Crea una carpeta para cada categoría** 📂  
   - Recorre la lista de categorías y construye la ruta donde se guardarán los datos.  
   - Usa `os.path.join(base_path, category)` para combinar la ruta base con el nombre de la categoría.  

3. **Verifica si la carpeta existe** ✅  
   - Si la carpeta **no existe**, se crea con `os.makedirs(path)`.  

4. **Devuelve la lista de categorías** 🔄  
   - Retorna la lista de categorías que se crearon.  

--- 

## FOTO 

## 🖼️ Función `download_image`

Esta función **descarga una imagen desde una URL y la guarda en el sistema** 📥📂.

### 🛠️ ¿Cómo funciona?

1. **Hace una solicitud a la URL** 🌍  
   - Utiliza `requests.get(url, headers=self.headers)` para obtener la imagen desde el enlace.  
   - Usa **`self.headers`** para simular una petición desde un navegador y evitar bloqueos.  

2. **Verifica que la imagen se haya descargado correctamente** ✅  
   - Si el código de respuesta (`response.status_code`) es `200`, significa que la imagen se descargó sin problemas.  

3. **Guarda la imagen en el archivo especificado** 💾  
   - Abre el archivo en modo escritura binaria (`'wb'`).  
   - Escribe el contenido de la imagen en el archivo.  
   - Imprime un mensaje confirmando que la imagen se guardó correctamente.  

4. **Manejo de errores** ⚠️  
   - Si ocurre un error en la descarga, se captura con `except Exception as e`.  
   - Se imprime un mensaje indicando el problema y la función devuelve `False`.  

---

# Foto 

## 🔄 Función `load_all_products`

Esta función **carga todos los productos de la página web** haciendo clic en el botón `"Mostrar más"` hasta que ya no haya más productos disponibles 🛍️.

### 🛠️ ¿Cómo funciona?

1. **Abre la página web** 🌐  
   - Utiliza `self.driver.get(url)` para acceder a la URL proporcionada.  

2. **Espera a que la página cargue** ⏳  
   - Crea una espera con `WebDriverWait` para asegurarse de que los elementos estén listos antes de interactuar con ellos.  

3. **Bucle para cargar más productos** 🔄  
   - Se usa un `while True` para hacer clic en `"Mostrar más"` varias veces.  
   - **Busca el botón** con `wait.until(...)` y verifica que sea **clickeable**.  
   - **Ejecuta un clic** en el botón con `execute_script("arguments[0].click();", load_more_button)`.  
   - Muestra el mensaje `"Cargando más productos..."` en la terminal.  
   - Espera `2 segundos` (`time.sleep(2)`) antes de intentar hacer clic nuevamente.  

4. **Manejo de errores** ⚠️  
   - Si el botón `"Mostrar más"` ya no está disponible, significa que **no hay más productos**.  
   - En ese caso, se muestra el mensaje `"No hay más productos para cargar."` y el bucle se detiene con `break`.

---

# Foto 

## 🔍 Función `scrape_category`

Esta función **extrae imágenes de productos** de una **categoría específica** en IKEA 🏠 y las guarda en una carpeta 📂.

### 🛠️ ¿Cómo funciona?

1. **Carga la página de la categoría** 🌐  
   - Obtiene la URL de la categoría desde `self.category_urls[category]`.  
   - Llama a `self.load_all_products(url)`, que se encarga de hacer clic en `"Mostrar más"` hasta que todos los productos estén cargados.  

2. **Extrae los productos con `BeautifulSoup`** 🥣  
   - Obtiene el código HTML de la página con `self.driver.page_source`.  
   - Busca todos los productos en la web usando `soup.find_all('div', class_='plp-fragment-wrapper')`.  

3. **Recorre cada producto y extrae su información** 🔄  
   - Para cada producto, intenta encontrar:  
     - La **imagen** (`<img>`) y su URL.  
     - El **nombre del producto** dentro de un `<span>`.  

4. **Limpia el nombre del producto** 🏷️  
   - Si el nombre contiene caracteres especiales, los reemplaza con `_` usando `re.sub()`.  
   - Si no se encuentra un nombre, usa un nombre genérico basado en la categoría y el índice (`category_idx`).  

5. **Descarga la imagen** 📥  
   - Guarda la imagen en la ruta `save_path`, nombrándola con el nombre limpio.  
   - Llama a `self.download_image(img_url, image_path)`, que descarga y guarda la imagen.  
   - Muestra un mensaje en la terminal confirmando la descarga.  

6. **Manejo de errores** ⚠️  
   - Si hay un problema al procesar un producto, muestra un mensaje de error y pasa al siguiente.  

---

# Foto 

## 🚀 Función `run`

Esta función **ejecuta el scraping completo** en todas las categorías definidas 🏠🔄.

### 🛠️ ¿Cómo funciona?

1. **Muestra un mensaje de inicio** 📢  
   - Se imprime `"Iniciando proceso de scraping..."` para indicar que el proceso ha comenzado.  

2. **Crea los directorios para cada categoría** 📂  
   - Llama a `self.create_directories(base_path)`, que se encarga de crear carpetas donde se guardarán las imágenes.  
   - Muestra en la terminal las categorías para las cuales se han creado carpetas.  

3. **Realiza el scraping de cada categoría** 🔄  
   - **Recorre todas las categorías disponibles** usando un `for`.  
   - **Imprime un mensaje indicando que está iniciando el scraping** de esa categoría.  
   - Genera la ruta donde se guardarán las imágenes (`category_path`).  
   - Llama a `self.scrape_category(category, category_path)`, que extrae las imágenes de la web.  
   - Muestra un mensaje indicando que el scraping de esa categoría ha finalizado.  
   - **Espera 3 segundos (`time.sleep(3)`)** antes de pasar a la siguiente categoría.  

4. **Cierra el navegador** 🔚  
   - Llama a `self.driver.quit()`, lo que finaliza el uso de Selenium y cierra el navegador.  

--- 

# Foto 

## 🏁 Ejecución del scraper en local

Este bloque de código **inicia el proceso de scraping** cuando ejecutamos el script en nuestro ordenador 🖥️.

### 🛠️ ¿Cómo funciona?

1. **Verifica si el script se está ejecutando directamente** 🏗️  
   - La condición `if __name__ == "__main__":` se asegura de que el código **solo se ejecute** cuando ejecutamos el archivo directamente y no si se importa como módulo en otro script.  

2. **Crea una instancia del scraper** 🏠  
   - Se inicializa un objeto `IKEAScraper`, indicando la ruta del **ChromeDriver** (`chromedriver.exe`).  
   - `ChromeDriver` es necesario para que **Selenium** pueda controlar el navegador.  

3. **Ejecuta el proceso completo de scraping** 🚀  
   - Se llama a `scraper.run()`, que se encargará de:
     - Abrir el navegador.
     - Extraer los productos de todas las categorías.
     - Descargar las imágenes.
     - Guardarlas en carpetas organizadas.


## 3. Limpieza de datos (eliminación de nulos y datos erróneos, etc.). Descripción de los datos. Se debe dar una descripción completa de los datos indicando qué significa cada uno de los atributos.

## 4. Exploración y visualización de los datos. Se realizará un estudio de los datos buscando correlaciones, mostrando gráficas de diferente tipología, observando si hay valores nulos, etc.

## 5. Preparación de los datos para los algoritmos de Machine Learning. Se deben tratar los datos (limpiando, escalando, separando y todo lo que sea necesario) de tal forma que queden listos para entrenar el modelo.

## 6. Entrenamiento del modelo y comprobación del rendimiento. Se entrenarán uno o varios modelos, comprobando en cada caso el rendimiento que ofrecen mediante las apropiadas medidas de error y/o acierto.

## 7. Se tiene que incluir alguna de las técnicas estudiadas en el tema de Procesamiento de Lenguaje Natural: expresiones regulares, tokenización, generación de texto, análisis de sentimientos, etc.

## 8. Se debe realizar también una aplicación web que haga uso del modelo entrenado.

## 9. Conclusiones. Se expondrán las conclusiones que se han obtenido en la realización del TFM.
