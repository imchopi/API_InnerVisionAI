## 1. Justificación y descripción del proyecto.

## 2. Obtención de datos. Se debe especificar la fuente de los datos. Se indicará por qué medios se han obtenido (encuestas, sensores, scrapping, etc.). Los datos se deben cargar en una estructura que permita su posterior manipulación y uso.

Para conseguir los datos que necesitábamos, decidimos extraer imágenes de internet 🖼️. Como nuestro modelo va a funcionar en tiempo real ⏳, queríamos que reconociera objetos comunes en la empresa, como sillas, armarios y mesas 🪑📦.

Por eso elegimos IKEA 🏠 como fuente de información, ya que es una de las mejores referencias y sabemos que tiene justo lo que estábamos buscando ✅.

Lo primero que hicimos fue instalar las librerías necesarias 🛠️. Al principio, como la web parecía sencilla 🌐, pensamos que con BeautifulSoup 🥣 sería suficiente, pero no fue así ❌.

Si queríamos cargar todas las imágenes 🖼️, nos dimos cuenta de que había un botón de "Mostrar más", que era el encargado de cargar las imágenes.

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

---

## 🖥️ Ampliando el scraping: objetos más pequeños  

Después de extraer información sobre **muebles**, decidimos también obtener datos de **objetos más pequeños** que se pueden encontrar dentro de la empresa, como **teclados, portátiles y ratones** ⌨️💻🖱️.  

### 🔍 Cambio de fuente: PCComponentes  
Para estos productos, optamos por **extraer la información de PCComponentes** 🛒.  

Sin embargo, pronto nos dimos cuenta de una **diferencia clave** con la web de IKEA:  
🔹 **No tenía un botón de "Cargar más"** como IKEA.  
🔹 En su lugar, había un **botón para pasar a la siguiente página** 📄➡️.  

### 🚧 Problema encontrado: Bloqueo de bots  
Cuando intentamos **pasar a la siguiente página**, la web nos detectaba como **un bot** 🚫🤖, impidiendo que siguiéramos navegando.  

### 💡 Solución ingeniosa  
Para **evitar el bloqueo**, encontramos una solución **sencilla pero efectiva**:  

🔄 En lugar de hacer clic en **"Siguiente página"**, usamos un **bucle** que:  
1. **Scrapea** la información de la página actual.  
2. **Cierra el navegador** completamente.  
3. **Vuelve a abrirlo** en la siguiente página con la nueva URL.  

📌 **Resultado:** La web no detectaba que éramos un bot, permitiéndonos extraer la información sin problemas 🎯.  

---

## 🖥️ Código para extraer datos de PCComponentes  

En esta situación, utilizaremos **tres códigos similares** 🔄, pero con algunos **detalles específicos** cambiados para que cada uno **interactúe con su categoría correspondiente**.  

📌 **Las tres categorías a scrapear son:**  
- **Teclados** ⌨️  
- **Portátiles** 💻  
- **Ratones** 🖱️  

Dado que los códigos son casi **idénticos**, solo mostraré el código correspondiente a **los ratones** 🖱️, ya que la lógica es la misma para los otros dos casos, con pequeños ajustes.  

---

📌 **A continuación, el código para extraer información de los ratones en PCComponentes** 🚀.

# Foto 

## 📚 Librerías utilizadas para el scraping de PCComponentes  

Para poder extraer los datos de **PCComponentes**, utilizamos varias **librerías** 📦 que nos ayudarán en diferentes tareas:  

### 🔹 **Librerías básicas**
- **`requests`** 🌍 → Se usa para hacer peticiones a la web y obtener su contenido.  
- **`os`** 📂 → Permite interactuar con los archivos y carpetas del sistema.  
- **`time`** ⏳ → Se usa para hacer pausas en el código y evitar bloqueos por sobrecarga de peticiones.  

### 🥣 **BeautifulSoup: Análisis del HTML**
- **`BeautifulSoup (bs4)`** 🏗️ → Se encarga de **extraer información del código HTML** de la web.  

### 🚀 **Selenium: Automatización del navegador**  
Dado que la web de **PCComponentes** requiere **interacción con la paginación**, usamos **Selenium** para controlarla:  

- **`webdriver`** 🚗 → Controla el navegador (Chrome en este caso).  
- **`Service`** 🛠️ → Configura la ejecución del navegador de forma automática.  
- **`Options`** ⚙️ → Permite configurar cómo se abre el navegador (ejemplo: en modo sin interfaz).  
- **`By`** 🔎 → Se usa para buscar elementos dentro de la web (ejemplo: botones o imágenes).  
- **`WebDriverWait`** ⏳ → Permite que el código **espere** hasta que un elemento de la web se cargue correctamente.  
- **`expected_conditions (EC)`** ✅ → Se usa para definir condiciones antes de interactuar con elementos de la web (como esperar a que un botón sea clickeable).  

---

# FOTO

## 🖱️ Clase `PCscrapper`

Esta clase se encarga de **extraer información de los ratones en PCComponentes** 🛒.  

### 🛠️ **Inicialización de la clase (`__init__` method)**  

Cuando creamos un objeto de esta clase, se ejecuta el código de inicialización que:  

### 🔗 **Define las URLs de las páginas a scrapear**  
- **`self.category_urls`** almacena un **diccionario de URLs**, donde cada clave es el nombre de la página y el valor es la URL correspondiente.  
- Se usa un **bucle con `range(1, 29)`**, lo que indica que se van a recorrer **28 páginas** (de la 1 a la 28).  
- La URL cambia dinámicamente con `?page={page}`, lo que permite navegar por las diferentes páginas sin hacer clic en "Siguiente".  

### 🏷️ **Define las cabeceras (`headers`)**  
- **`self.headers`** almacena un **"User-Agent"**, que hace que la petición parezca de un navegador real.  
- Esto ayuda a **evitar bloqueos** por parte de la web al detectar actividad sospechosa de bots 🤖🚫.  

---

# Foto 

## 📂 Función `create_directories`

Esta función se encarga de **crear carpetas** en el sistema para almacenar las imágenes de cada categoría 🗂️.

### 🛠️ ¿Cómo funciona?

1. **Obtiene las categorías** 🏷️  
   - Usa `self.category_urls.keys()` para obtener la lista de categorías disponibles (ejemplo: `"ratones1"`, `"ratones2"`, `"ratones3"`, etc.).  

2. **Crea una carpeta para cada categoría** 📂  
   - Recorre la lista de categorías y **construye la ruta** donde se guardarán los datos.  
   - Usa `os.path.join(base_path, category)` para combinar la ruta base con el nombre de la categoría.  

3. **Verifica si la carpeta existe** ✅  
   - Si la carpeta **no existe**, se crea con `os.makedirs(path)`.  

4. **Devuelve la lista de categorías** 🔄  
   - Retorna la lista de categorías que se crearon.  

---

# Foto 

## 🖼️ Función `download_image`

Esta función **descarga una imagen desde una URL y la guarda en el sistema** 📥📂.

### 🛠️ **¿Cómo funciona?**

1. **Hace una solicitud a la URL** 🌍  
   - Usa `requests.get(url, headers=self.headers)` para obtener la imagen desde el enlace.  
   - Incluye **cabeceras HTTP (`headers`)** para **simular una petición real de un navegador** y evitar bloqueos.  

2. **Verifica que la imagen se haya descargado correctamente** ✅  
   - Si el código de respuesta (`response.status_code`) es **200**, significa que la imagen se descargó sin problemas.  

3. **Crea el directorio si no existe** 📂  
   - Usa `os.makedirs(os.path.dirname(path), exist_ok=True)` para asegurarse de que la carpeta donde se guardará la imagen **exista**.  
   - `exist_ok=True` evita errores si la carpeta ya está creada.  

4. **Guarda la imagen en el archivo especificado** 💾  
   - Abre el archivo en modo escritura binaria (`'wb'`).  
   - Escribe el contenido de la imagen en el archivo.  
   - Imprime un mensaje confirmando que la imagen se guardó correctamente.  

5. **Manejo de errores** ⚠️  
   - Si ocurre un error en la descarga, se captura con `except Exception as e`.  
   - Se imprime un mensaje indicando el problema y la función devuelve `False`.  

---

# Foto 

## 📸 Función `download_products_images`

Esta función **descarga imágenes de una página web de manera automática** 🌍📥.

### 🛠️ **¿Cómo funciona?**

1. **Abre la página web en Chrome** 🌐  
   - Usa **Selenium** para abrir la URL en un navegador.  
   - Configura el navegador en **modo maximizado** para evitar problemas de visualización.  

2. **Acepta las cookies si es necesario** 🍪  
   - Busca el botón de "Aceptar cookies" y hace clic en él.  
   - Si el botón no está presente, **el código sigue sin problemas**.  

3. **Espera a que las imágenes se carguen** ⏳  
   - Usa `WebDriverWait` para asegurarse de que las imágenes estén visibles antes de continuar.  
   - Utiliza **BeautifulSoup** para analizar el código HTML de la página y extraer las imágenes.  

4. **Busca y filtra imágenes relevantes** 🔍  
   - Extrae todas las etiquetas `<img>` que tengan atributos `src` (enlace de imagen) y `alt` (descripción).  
   - Obtiene la URL de cada imagen.  
   - Si la URL es **relativa** (empieza con `/`), se convierte en una URL **completa** agregando el dominio.  

5. **Descarga y guarda las imágenes** 📂  
   - Genera un **nombre de archivo único** (`image_{i}.jpg`) y lo guarda en una carpeta según su categoría.  
   - Llama a la función `self.download_image()` para almacenar la imagen correctamente.  

6. **Manejo de errores y cierre del navegador** ⚠️  
   - Si hay un error durante la ejecución, se muestra un mensaje con la URL afectada.  
   - Al final, **siempre se cierra el navegador** para liberar recursos.  

---

# Foto 

## 🚀 Función `run`

Esta función **ejecuta el scraper** y se encarga de **organizar y descargar las imágenes** de diferentes categorías 📥📂.

### 🛠️ **¿Cómo funciona?**

1. **Define la carpeta base donde se guardarán las imágenes** 📂  
   - `base_path = 'images'` establece el directorio principal donde se almacenarán las imágenes descargadas.  

2. **Crea las carpetas necesarias** 🏗️  
   - Usa `self.create_directories(base_path)` para asegurarse de que la carpeta base **exista antes de guardar las imágenes**.  
   - Si la carpeta ya existe, **evita errores y continúa con la ejecución**.  

3. **Recorre todas las categorías de productos** 🏷️  
   - Usa un **bucle `for`** para iterar sobre `self.category_urls.items()`, donde cada categoría tiene una URL específica.  
   - Extrae la `category` (nombre de la categoría) y `url` (dirección web donde se encuentran las imágenes).  

4. **Llama a la función de descarga de imágenes** 📸  
   - `self.download_products_images(url, category)` procesa la página y **descarga las imágenes correspondientes a cada categoría**.  

---

# FOTO 

## 🖥️ Bloque `if __name__ == "__main__"`

Este bloque de código **ejecuta el programa en local** y **pone en marcha el scraper** 🏁🚀.

### 🛠️ **¿Cómo funciona?**

1. **Verifica que el script se está ejecutando directamente** ▶️  
   - La línea `if __name__ == '__main__':` **asegura que el código solo se ejecute si este archivo es ejecutado directamente**, y **no si es importado como módulo en otro script**.  

2. **Crea una instancia del scraper** 🏗️  
   - `scrapper = PCscrapper()` inicializa un objeto de la clase `PCscrapper`, que contiene toda la lógica del scraping.  
   - Aquí se configuran las opciones y los parámetros del scraper.  

3. **Ejecuta el scraper** 🔄  
   - `scrapper.run()` llama a la función `run()` para iniciar la **descarga y organización de imágenes** desde las páginas web.  
   - Esto hace que **se ejecuten todos los procesos del scraper automáticamente**.  

---

# 🖥️ **Scraping de datos de ratones en PCComponentes para Power BI** 📊🐭  

Para la **visualización de datos en Power BI**, pensé que ya tenía las imágenes, así que… **¿qué tan difícil podría ser obtener los datos de los ratones ?** 🤔  

Bueno, resultó ser **el mayor reto al que me he enfrentado**.  

### 🚧 **El desafío**  
Por más que intentaba localizar los datos, **cambiaba el nombre de las class una y otra vez**, pero nada funcionaba. Cuando estaba **a punto de rendirme**, tomé aire, suspiré y decidí empezar **desde cero, paso a paso**.  

### 🔍 **Paso a paso, desentrañando los datos**  
1️⃣ **Extraer el nombre**: Fue lo más fácil, así que comencé por ahí. ✍️  
2️⃣ **Obtener el precio**: Perfecto, ahora tenía **2 de los 5 datos** que necesitaba. 💰  
3️⃣ **Conseguir la URL**: Tras algunos intentos, me di cuenta de que todas las URLs seguían el mismo patrón:  
   **Dominio de la web + Nombre del producto** 🌐🔗  
   ¡Un descubrimiento clave! De repente, **todas las URLs estaban listas**.  
4️⃣ **Valoraciones y cantidad de opiniones**: Ahora que entendía la estructura, estos datos vinieron **de inmediato**. ⭐💬  

### 🔄 **El problema de la paginación**  
Cuando intenté pasar a la **siguiente página**, **el navegador no respondía correctamente**. 😡  
Así que decidí **cerrarlo y abrirlo en cada nueva página**. ¡Funcionó! Ahora tenía **27 archivos CSV**, uno por cada página de productos. 📂✅  

### 🏆 **Lo que aprendí**  
✅ A veces, lo mejor es **empezar desde cero y avanzar poco a poco**.  
✅ **Observar patrones** en los datos puede hacerte la vida más fácil.  
✅ **Cada problema tiene una solución** (aunque implique reiniciar el navegador 🔄).  

Próximo paso: **unir los 27 CSV en un solo archivo** y prepararlo para **Power BI**. 🚀📊  

---

## Código para la obtención de datos. 

# Foto 

## 📦 **Módulos importados en el scraper**  

Este bloque de código **importa todas las librerías necesarias** para el funcionamiento del scraper. 📥🔎  

### 🛠️ **¿Para qué sirve cada una?**  

#### ⏳ **Manejo del tiempo**  
- `import time` → Permite **pausar la ejecución** del código en momentos clave.  

#### 📄 **Manejo de archivos CSV y texto**  
- `import csv` → Para **guardar los datos extraídos** en archivos CSV.  
- `import re` → **Expresiones regulares**, útil para limpiar y estructurar texto.  
- `import unidecode` → **Elimina acentos y caracteres especiales**, útil para URLs.  

#### 📂 **Manejo del sistema de archivos**  
- `import os` → Permite **crear directorios y manejar rutas de archivos**.  

#### 🌐 **Automatización del navegador con Selenium**  
- `from selenium import webdriver` → Para **controlar el navegador web**.  
- `from selenium.webdriver.chrome.service import Service` → Gestiona **el servicio de ChromeDriver**.  
- `from selenium.webdriver.chrome.options import Options` → Configura **opciones avanzadas del navegador**.  
- `from selenium.webdriver.common.by import By` → Facilita **la búsqueda de elementos en la web**.  
- `from selenium.webdriver.support.ui import WebDriverWait` → Permite **esperar a que aparezcan elementos en la página**.  
- `from selenium.webdriver.support import expected_conditions as EC` → Define **condiciones específicas para esperar elementos** (ejemplo: "cuando un botón sea clickeable").  

---

# Foto 

## 🖥️ **Clase `PCScraper`**

Esta clase define el **scraper** encargado de extraer información de ratones en **PCComponentes** 🐭🛒.

### 🛠️ **¿Cómo funciona?**

1. **Define el `chromedriver.exe` como controlador del navegador** 🏎️  
   - El parámetro `driver_path="chromedriver.exe"` establece **la ruta del driver de Chrome** para automatizar la navegación.  
   - Esto permite que Selenium **controle el navegador y acceda a las páginas de productos**.  

2. **Genera un diccionario con todas las URLs de las páginas** 🌐  
   - `self.category_urls` almacena un diccionario donde:  
     - La **clave** es el identificador de la página (`ratones_p1`, `ratones_p2`, etc.).  
     - El **valor** es la **URL completa** de cada página de productos.  
   - Usa **un bucle con `range(1, 29)`**, generando automáticamente **las 28 páginas** de resultados.  

3. **Guarda la ruta del controlador y la URL base** 🔗  
   - `self.driver_path = driver_path` almacena la ubicación del **ChromeDriver**.  
   - `self.base_url = "https://www.pccomponentes.com/"` establece la **URL base de la tienda**.  

---

# Foto 

## 🌐 **Función `start_driver`**

Esta función **inicia una nueva sesión del navegador Chrome** con configuraciones personalizadas para **optimizar el scraping** y **evitar bloqueos**. 🏎️💨  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Crea una configuración especial para el navegador** ⚙️  
   - `chrome_options = Options()` inicializa un objeto para **definir opciones avanzadas de Chrome**.  
   - `chrome_options.add_argument("--start-maximized")` hace que el navegador **se inicie en pantalla completa**, lo que **reduce errores de carga y mejora la visibilidad de los elementos**.  

2️⃣ **Evita la detección como bot** 🕵️‍♂️  
   - `chrome_options.add_argument("user-agent=Mozilla/...")` cambia el **User-Agent** del navegador.  
   - Simula que la petición proviene de un usuario real en lugar de un bot, lo que **disminuye la probabilidad de ser bloqueado** por la web.  

3️⃣ **Inicia el navegador con la configuración establecida** 🚀  
   - `self.driver = webdriver.Chrome(service=Service(self.driver_path), options=chrome_options)`  
   - **Se usa `Service(self.driver_path)`** para asegurarse de que el controlador **ChromeDriver** funcione correctamente.  
   - Todas las opciones configuradas se aplican para garantizar **una navegación fluida y sin detección**.  

---

# FOTO 

## ❌ **Función `close_driver`**  

Esta función **cierra el navegador** una vez que el scraping ha terminado, asegurando que los recursos del sistema se liberen correctamente. 🌐🔚  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Cierra la sesión del navegador** 🏁  
   - `self.driver.quit()` **cierra completamente la ventana de Chrome**, finalizando la sesión de Selenium.  
   - Esto **libera memoria y evita que queden procesos abiertos** innecesariamente.  

---

# FOTO 

## 🍪 **Función `accept_cookies`**  

Esta función **acepta las cookies automáticamente** si el botón está presente en la página, evitando interrupciones durante el scraping. 🌍🔘  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Espera a que el botón de aceptar cookies esté disponible** ⏳  
   - Usa `WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'cookiesAcceptAll')))` para **esperar hasta 5 segundos** a que el botón sea clickeable.  

2️⃣ **Hace clic en el botón de aceptación** 👆  
   - Si el botón se encuentra, `accept_button.click()` lo presiona automáticamente.  
   - `time.sleep(2)` agrega una pequeña pausa de **2 segundos** para asegurar que el clic se registre correctamente.  

3️⃣ **Manejo de errores** ⚠️  
   - Si el botón **no aparece o las cookies ya fueron aceptadas**, **se captura la excepción**.  
   - Muestra el mensaje `"🔹 No se encontró el botón de cookies o ya fueron aceptadas."`, permitiendo que el código **siga ejecutándose sin problemas**.  

---

# Foto 

## 🔗 **Función `generate_url`**  

Esta función **genera una URL válida** para un producto a partir de su nombre, asegurándose de que tenga el formato adecuado para ser usada en la web. 🌍🔄  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Elimina caracteres especiales y acentos** ✂️  
   - `unidecode.unidecode(product_name)` convierte caracteres con acentos (ej. `Cámara`) a su equivalente sin acento (`Camara`).  
   - Esto **garantiza compatibilidad con URLs**, evitando caracteres inválidos.  

2️⃣ **Filtra caracteres no deseados** 🔍  
   - `re.sub(r'[^a-zA-Z0-9\s]', '', clean_name)` elimina **todo lo que no sea letras, números o espacios**.  
   - Así se evita que caracteres especiales rompan la URL.  

3️⃣ **Convierte el texto a minúsculas y reemplaza espacios** 🔤  
   - `clean_name.lower()` transforma el texto a **minúsculas** para mantener consistencia.  
   - `.replace(" ", "-")` reemplaza los espacios por guiones (`-`), que son estándar en URLs.  

4️⃣ **Genera la URL final** 🔗  
   - `return f"{self.base_url}{clean_name}"` une la **URL base** con el nombre limpio del producto.  
   - Por ejemplo, si `product_name = "Ratón Óptico Gamer"`, la salida será:  
     ```
     https://www.pccomponentes.com/raton-optico-gamer
     ```  
--- 

# FOTO 

## 🛒 **Función `scrape_category`**  

Esta función **extrae los datos de una sola página de una categoría específica** dentro de la tienda online. 📦🔍  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Inicia el navegador** 🌐  
   - `self.start_driver()` abre una nueva ventana de Chrome para realizar el scraping.  
   - Se asegura de que el navegador **esté configurado correctamente** antes de comenzar.  

2️⃣ **Carga la página de la categoría** 🔗  
   - `self.driver.get(category_url)` accede a la URL de la categoría que se quiere analizar.  
   - Aquí es donde estarán **todos los productos de esa categoría**.  

3️⃣ **Acepta las cookies si es necesario** 🍪  
   - `self.accept_cookies()` busca y **hace clic en el botón de aceptar cookies** si aparece.  
   - Evita que este aviso bloquee la ejecución del scraper.  

### ⏳ **Esperando la carga de productos en `scrape_category`**  

Esta parte de la función **espera a que los productos de la categoría se carguen completamente** antes de extraerlos. 📊🕵️‍♂️  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Espera a que aparezcan los productos** ⏳  
   - `WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(...))`  
   - **Se espera hasta 15 segundos** para que al menos un producto cargue correctamente.  
   - Busca un `h3.product-card__title`, que es el **título del producto** en la página.  

2️⃣ **Añade una pausa extra** ⌛  
   - `time.sleep(5)` da **5 segundos adicionales** para asegurarse de que **todos los elementos de la página estén listos**.  
   - Esto ayuda a evitar errores si el contenido se carga lentamente.  

3️⃣ **Extrae la lista de productos** 🛍️  
   - `products = self.driver.find_elements(By.CSS_SELECTOR, "div.product-card")`  
   - Encuentra **todos los productos** en la página, cada uno dentro de un `div.product-card`.  
   - Guarda estos elementos en la lista `products`.  

4️⃣ **Prepara la lista de datos** 📋  
   - `product_data = []` crea una lista vacía donde **se guardará la información de cada producto**.  
   - En los siguientes pasos, se extraerán detalles como **nombre, precio, valoraciones, etc.** y se guardarán aquí.  

### 🛍️ **Extracción de datos de los productos**  

Esta parte de la función **recorre todos los productos de la categoría** y extrae información clave como el **nombre, URL y precio**. 🏷️💰  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Recorre todos los productos encontrados** 🔄  
   - `for product in products:` itera sobre **cada producto en la lista `products`**.  
   - Cada **`product`** representa un artículo en la página.  

2️⃣ **Extrae el nombre del producto** 📝  
   - `name = product.find_element(By.CSS_SELECTOR, "h3.product-card__title").text.strip()`  
   - Busca el **título del producto** dentro de la tarjeta (`product-card`).  
   - Usa `.strip()` para **eliminar espacios extra** antes y después del texto.  
   - Si el título **no está disponible**, asigna `"No disponible"`.  

3️⃣ **Genera la URL del producto automáticamente** 🔗  
   - `url = self.generate_url(name)`  
   - Llama a la función `generate_url(name)` para **crear una URL válida basada en el nombre**.  
   - Reemplaza espacios y caracteres especiales para que la URL sea compatible con la web.  

4️⃣ **Extrae el precio del producto** 💲  
   - `price = product.find_element(By.CSS_SELECTOR, "span[data-e2e='price-card']").text.strip()`  
   - Busca el precio dentro de un `span` con el atributo `data-e2e='price-card'`.  
   - Si el precio **no está disponible**, asigna `"No disponible"`. 

### ⭐ **Extracción de Valoraciones y Opiniones**  

Esta parte de la función **extrae la valoración (rating) y el número de opiniones** de cada producto, asegurándose de que la información se capture correctamente. 📊🔎  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Inicializa valores predeterminados** 🔄  
   - `rating = "No disponible"` y `opinions = "0"` aseguran que si no se encuentra información, **no haya valores vacíos**.  

2️⃣ **Verifica si el producto tiene valoraciones** ⭐  
   - `rating_container = product.find_element(By.CSS_SELECTOR, ".product-card__rating-container")`  
   - Busca el **contenedor de valoraciones** dentro de la tarjeta del producto.  
   - Si no existe, el código **continúa sin errores**.  

3️⃣ **Extrae la valoración numérica del producto** 🔢  
   - Se buscan `span` dentro del `rating_container`.  
   - Se analiza cada `span.text` para detectar patrones como `4.5/5` o `4,5/5`.  
   - Usa `re.search(r'[0-9][.,][0-9]/[0-9]', text)` para identificar formatos válidos.  
   - Si se encuentra, se guarda en `rating` y se detiene la búsqueda.  

4️⃣ **Extrae el número de opiniones** 💬  
   - Busca palabras clave como `"opinión"` dentro del contenedor de valoraciones.  
   - Extrae el primer número encontrado (`\d+`) y lo asigna a `opinions`.  
   - Si no hay opiniones visibles, el valor **permanece en "0"**.  

5️⃣ **Manejo de errores** ⚠️  
   - Si el contenedor de valoraciones **no existe**, el código **sigue sin fallar**.  
   - Se usa `try-except` en varios niveles para **evitar que errores en una parte bloqueen la ejecución completa**.  

### 📋 **Almacenamiento de Datos y Manejo de Errores**  

Esta última parte de la función **guarda los datos extraídos en una lista y maneja posibles errores**, asegurando que el scraping se complete correctamente. 📊✅  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Guarda los datos en una lista** 📂  
   - `product_data.append([name, price, rating, opinions, url])`  
   - **Cada producto** se almacena como una lista con los siguientes valores:  
     - 📌 `name` → Nombre del producto.  
     - 💲 `price` → Precio actual.  
     - ⭐ `rating` → Valoración promedio.  
     - 💬 `opinions` → Número de opiniones.  
     - 🔗 `url` → Enlace al producto.  
   - Esto permite que todos los datos queden organizados y listos para su uso posterior (ej. guardado en CSV o base de datos).  

2️⃣ **Manejo de errores en productos individuales** ⚠  
   - `except Exception as e:` captura cualquier **error durante la extracción de un producto**.  
   - Si un producto falla, muestra el mensaje `⚠ Error extrayendo datos de un producto: {e}`.  
   - **El resto de los productos se siguen procesando sin interrupciones**.  

3️⃣ **Devuelve la lista de productos extraídos** ✅  
   - `return product_data` devuelve **todos los datos recopilados** en la categoría actual.  
   - Si no se encuentran productos, se devuelve una **lista vacía** `[]`.  

4️⃣ **Manejo de errores en toda la categoría** ❌  
   - Si hay un error **en toda la página**, lo captura `except Exception as e:`.  
   - Muestra `❌ Error al obtener los productos de {category_url}: {e}` para indicar qué falló.  
   - En este caso, también devuelve `[]`, asegurando que el scraper no se detenga completamente.  

5️⃣ **Cierra el navegador al finalizar** 🌐🔚  
   - `finally: self.close_driver()`  
   - **Se cierra el navegador en todos los casos**, ya sea que la extracción haya sido exitosa o haya ocurrido un error.  
   - Esto evita **consumo innecesario de recursos** y posibles bloqueos en futuras ejecuciones.  

---

# Foto 

### 📂 **Función `scrape_all_categories`**  

Esta función **recorre todas las páginas de productos de la categoría y guarda los datos en archivos CSV separados**. 📊🛍️  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Recorre todas las categorías disponibles** 🔄  
   - `for category_name, category_url in self.category_urls.items():`  
   - Itera sobre el **diccionario `self.category_urls`**, que contiene los nombres y URLs de cada categoría.  

2️⃣ **Llama a la función `scrape_category` para extraer los productos** 🛒  
   - `product_data = self.scrape_category(category_name, category_url)`  
   - Llama a la función `scrape_category` para **extraer los productos de la página actual**.  
   - Si la categoría **tiene productos**, se procede a guardarlos.  

3️⃣ **Guarda los datos en un archivo CSV** 💾  
   - **Genera un nombre de archivo** basado en la categoría:  
     ```python
     csv_filename = f"{category_name}.csv"
     ```
   - **Abre el archivo CSV en modo escritura (`"w"`)**, asegurando que se cree desde cero.  
   - **Escribe los encabezados** en la primera fila:  
     - 📌 `Nombre del Producto`  
     - 💲 `Precio`  
     - ⭐ `Valoraciones`  
     - 💬 `Opiniones`  
     - 🔗 `URL`  
   - **Escribe los datos de los productos** fila por fila con `writer.writerows(product_data)`.  

4️⃣ **Muestra un mensaje de éxito** ✅  
   - Indica cuántos productos se han guardado y en qué archivo CSV.  
   - Ejemplo de salida:  
     ```
     ✅ Se han guardado 50 productos en 'ratones_p1.csv'.
     ```

5️⃣ **Espera 5 segundos antes de continuar con la siguiente página** ⏳  
   - `time.sleep(5)`  
   - **Evita que el scraper sea detectado como bot**, simulando un comportamiento humano.  

---

# Foto 

## 🏁 **Ejecución del Scraper**  

Este bloque de código **pone en marcha el scraper**, iniciando el proceso de extracción de datos de todas las categorías. 🚀📊  

### 🛠️ **¿Cómo funciona?**  

1️⃣ **Verifica que el script se está ejecutando directamente** ▶️  
   - `if __name__ == "__main__":`  
   - Este condicional asegura que el código **solo se ejecute si el script es ejecutado directamente**, y **no si es importado como módulo** en otro archivo.  

2️⃣ **Crea una instancia del scraper** 🏗️  
   - `scraper = PCScraper()`  
   - Se inicializa un objeto de la clase `PCScraper`, que contiene toda la lógica de scraping.  
   - Aquí se configuran **las URLs de las categorías y las opciones del navegador**.  

3️⃣ **Ejecuta el scraping de todas las categorías** 🔄  
   - `scraper.scrape_all_categories()`  
   - Llama a la función que **recorre todas las páginas de productos y guarda los datos en archivos CSV**.  
   - **Cada categoría se procesa de manera independiente**, asegurando que todas las páginas sean analizadas.  

---

# 🎯 **Conclusión del Apartado de Obtención de Datos**  

Hemos completado con éxito el proceso de **extracción de datos** con un scraper totalmente funcional. 🚀📊  

## ✅ **¿Qué hemos logrado?**  

1️⃣ **Automatización completa** 🔄  
   - Desde **abrir el navegador** hasta **guardar los datos en archivos CSV**.  

2️⃣ **Extracción eficiente** 📊  
   - Obtención de **nombre del producto, precio, valoraciones, opiniones y URL**.  

3️⃣ **Manejo de errores inteligente** ⚠️  
   - **El scraper sigue funcionando** incluso si algunos datos no están disponibles.  

4️⃣ **Optimización anti-detección** 🕵️‍♂️  
   - **User-Agent personalizado** para evitar bloqueos.  
   - **Pausas estratégicas** para simular un usuario real.  

5️⃣ **Datos listos para análisis** 📂  
   - Todos los productos se han almacenado en **archivos CSV organizados**.  
   - **Perfecto para su visualización en Power BI u otras herramientas de análisis**.  

---

## 3. Limpieza de datos (eliminación de nulos y datos erróneos, etc.). Descripción de los datos. Se debe dar una descripción completa de los datos indicando qué significa cada uno de los atributos.

# 🧹 **Limpieza de Datos**  

El proceso de limpieza de datos en este proyecto es **sencillo pero esencial** para garantizar que la información extraída sea **relevante y precisa**. 🚀📊  

---

## 🎯 **¿Qué limpiaremos?**  

🔹 **Imágenes duplicadas y no relevantes** 🖼️  
   - Se han detectado **imágenes promocionales** que **se repiten en el mismo orden** para ratones, teclados y portátiles.  
   - Estas imágenes **usan la misma clase (`class`) que las imágenes de productos**, por lo que se han incluido accidentalmente en la extracción.  

🔹 **Filtrado de imágenes según patrones** 🔍  
   - Dado que **las imágenes promocionales siguen un patrón específico**, se pueden **identificar y eliminar fácilmente**.  
   - Aunque el código varía ligeramente entre categorías (**ratones, teclados, portátiles**), la lógica **es la misma** en todos los casos.  

---

## 🛠️ **¿Cómo se hace la limpieza?**  

1️⃣ **Identificación de imágenes no deseadas**  
   - Se analizan **los patrones de repetición** en las imágenes extraídas.  
   - Se detectan aquellas que corresponden a **banners publicitarios o contenido promocional**.  

2️⃣ **Filtrado automático en el código**  
   - Se implementa una lógica que **excluye las imágenes** basándose en su posición o en atributos específicos.  
   - Si una imagen **coincide con el patrón promocional**, **se descarta antes de almacenarla**.  

3️⃣ **Mantenimiento de la calidad de datos**  
   - Solo se conservan **imágenes relevantes de los productos reales**.  
   - Se evita la presencia de contenido duplicado en la base de datos.  

---

## 🔥 **¿Por qué es importante este proceso?**  

✅ **Elimina imágenes irrelevantes**, manteniendo el dataset limpio.  
✅ **Evita duplicados**, mejorando la calidad de los datos.    

---

# Foto 

# 🗑️ **Eliminación de Imágenes No Deseadas**  

Este código **elimina imágenes repetidas o no relevantes** dentro de la carpeta de portátiles, asegurando que solo se mantengan las imágenes útiles. 🖼️🚮  

---

## 🛠️ **¿Cómo funciona?**  

1️⃣ **Define la carpeta principal** 📂  
   - `main_folder = "imagenes_portatiles"`  
   - Aquí es donde se encuentran las subcarpetas con las imágenes almacenadas.  

2️⃣ **Lista de archivos a eliminar** ❌  
   - `files_to_delete = {"image"}`  
   - Se crea un **conjunto** con los nombres de archivos que deben ser eliminados.  
   - En este caso, cualquier archivo llamado `"image"` será **borrado automáticamente**.  

3️⃣ **Recorre todas las subcarpetas** 🔄  
   - Usa `os.walk(main_folder)` para **iterar sobre cada subcarpeta** dentro de `imagenes_portatiles`.  
   - En cada subcarpeta, **verifica los archivos almacenados**.  

4️⃣ **Elimina archivos innecesarios** 🗑️  
   - Si un archivo coincide con un nombre en `files_to_delete`, se borra usando `os.remove(file_path)`.  
   - Se muestra un mensaje confirmando cada eliminación con `print(f"Eliminado: {file_path}")`.  

5️⃣ **Manejo de errores** ⚠️  
   - Si ocurre un error al eliminar un archivo, se captura y muestra un mensaje de advertencia:  
     ```
     Error al eliminar <ruta_del_archivo>: <detalle_del_error>
     ```  
   - Esto evita que el código se detenga si hay problemas con permisos o archivos inexistentes.  

6️⃣ **Finaliza el proceso** ✅  
   - Al terminar, imprime `"Proceso completado."` indicando que la limpieza ha sido exitosa.  


📌 **Con esta limpieza, garantizamos que los datos extraídos sean útiles y sin ruido.**  

## 4. Exploración y visualización de los datos. Se realizará un estudio de los datos buscando correlaciones, mostrando gráficas de diferente tipología, observando si hay valores nulos, etc.


# FOto

# 🖼️ **Almacenamiento de Imágenes en CSV**  

Después de eliminar las imágenes no deseadas, el siguiente paso es **registrarlas en un archivo CSV**. 📂🔄  

## 🎯 **¿Por qué guardar las imágenes en un CSV?**  

🔹 **Organización** → Permite estructurar los datos para su fácil análisis.  
🔹 **Integración con Power BI** → Facilita la vinculación con otros datos, como precios o valoraciones.  
🔹 **Accesibilidad** → Un CSV es ligero y compatible con múltiples herramientas de análisis.  

---

# Foto 

# 📂 **Definición de Carpetas y Lista de Datos**  

Antes de procesar las imágenes, es necesario **definir las carpetas de origen** y **crear una lista para almacenar la información** extraída. 🖼️📊  

---

## 🛠️ **¿Cómo funciona esta parte del código?**  

1️⃣ **Definir las carpetas donde están las imágenes** 📂  
   - `carpetas_principales = ["../../ikea_muebles/sillas"]`  
   - Se establece una lista con **las rutas de las carpetas principales**, donde se encuentran las imágenes organizadas en subcarpetas.  
   - En este caso, se está procesando la carpeta `"sillas"` dentro de `"ikea_muebles"`.  

2️⃣ **Crear una lista para almacenar los datos** 📝  
   - `data = []`  
   - Se inicializa una **lista vacía** que **almacenará la información de cada imagen**.  
   - Posteriormente, en esta lista se guardarán datos como:  
     - 🖼️ `Nombre del archivo`  
     - 📂 `Ruta de la imagen`  
     - 🔠 `Imagen codificada en base64`  

---

# Foto

# 🖼️ **Función `procesar_carpeta`**  

Esta función **recorre carpetas y subcarpetas**, buscando imágenes, **convirtiéndolas a Base64** y almacenándolas en una lista con formato HTML. 📂📊  

---

## 🛠️ **¿Cómo funciona?**  

1️⃣ **Recorre todas las carpetas y subcarpetas** 🔄  
   - `os.walk(os.path.abspath(carpeta_raiz))`  
   - Convierte la **ruta relativa en absoluta** para evitar errores.  
   - **Recorre recursivamente** todas las carpetas y subcarpetas dentro de `carpeta_raiz`.  

2️⃣ **Filtra archivos de imagen** 🏷️  
   - `if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):`  
   - **Solo procesa archivos de imagen** con extensiones comunes.  
   - Ignora otros tipos de archivos no relevantes.  

3️⃣ **Convierte la imagen a Base64** 🔄  
   - `with open(ruta_imagen, "rb") as img_file:`  
   - Abre la imagen en **modo lectura binaria (`rb`)**.  
   - `base64.b64encode(img_file.read()).decode('utf-8')`  
   - **Codifica la imagen en Base64** y la convierte en un **string de texto**.  

4️⃣ **Genera una etiqueta HTML con la imagen en Base64** 🖼️  
   - `img_html = f'<img src="data:image/png;base64,{base64_str}" width="100"/>'`  
   - **Crea un fragmento HTML** que puede ser interpretado directamente en Power BI u otras herramientas.  
   - Se establece un **ancho de `100px`** para previsualización.  

5️⃣ **Agrega la imagen a la lista de datos** 📋  
   - `data.append([img_html])`  
   - Guarda la información en la lista `data`, para su posterior almacenamiento en CSV.  

6️⃣ **Manejo de errores** ⚠️  
   - Si ocurre algún problema al procesar una imagen, el error **se muestra en consola** y el programa sigue ejecutándose.  

---

# Foto 

# 📄 **Conversión de Imágenes a CSV**  

Después de procesar todas las imágenes, este código **crea un DataFrame y lo guarda en un archivo CSV**, asegurando que esté listo para su uso en Power BI u otras herramientas. 📂📊  

---

## 🛠️ **¿Cómo funciona?**  

1️⃣ **Procesa todas las carpetas principales** 📂  
   - `for carpeta in carpetas_principales:`  
   - **Recorre cada carpeta** y ejecuta `procesar_carpeta(carpeta)`.  
   - Se almacenan las imágenes **convertidas a Base64 con formato HTML** en la lista `data`.  

2️⃣ **Crea un DataFrame con los datos** 🏗️  
   - `df = pd.DataFrame(data, columns=["chair"])`  
   - Se genera un **DataFrame de Pandas** con una columna llamada `"chair"`.  
   - **Cada fila contiene una imagen en formato Base64 con etiqueta HTML**.  

3️⃣ **Guarda el DataFrame en un archivo CSV** 💾  
   - `csv_path = "chair.csv"` define el nombre del archivo.  
   - `df.to_csv(csv_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL, escapechar="\\")`  
     - 🔹 **`index=False`** → No guarda el índice del DataFrame.  
     - 🔹 **`encoding="utf-8-sig"`** → Asegura compatibilidad con **Power BI y Excel**.  
     - 🔹 **`quoting=csv.QUOTE_MINIMAL`** → Evita problemas con comillas en los datos.  
     - 🔹 **`escapechar="\\ "`** → Escapa caracteres especiales para evitar errores en la lectura del CSV.  

4️⃣ **Muestra un mensaje de éxito** ✅  
   - `print(f"✅ Archivo CSV guardado correctamente en: {csv_path}")`  
   - Confirma que el archivo se ha guardado **sin errores y listo para su análisis**.  

---

# Foto 

# 📦 **Importación de Módulos para la Prueba y Visualización**  

Antes de verificar el correcto funcionamiento de los datos, necesitamos **importar las librerías necesarias** para **cargar, procesar y visualizar las imágenes** almacenadas en el CSV. 📊🖼️  

---

## 🛠️ **¿Qué hace cada módulo?**  

1️⃣ **`pandas` → Manejo de Datos Tabulares** 📊  
   - `import pandas as pd`  
   - Permite **cargar el CSV** y trabajar con él como un **DataFrame**.  
   - Se usará para leer y verificar la estructura de los datos.  

2️⃣ **`matplotlib.pyplot` → Visualización de Datos** 📈  
   - `import matplotlib.pyplot as plt`  
   - Nos permite **mostrar las imágenes** contenidas en el CSV.  
   - Se usará para graficar y confirmar que las imágenes se han guardado correctamente.  

3️⃣ **`base64` → Decodificación de Imágenes** 🔄  
   - `import base64`  
   - Convierte las imágenes **de Base64 a un formato visualizable**.  
   - Se usará para reconstruir las imágenes almacenadas en el CSV.  

4️⃣ **`BytesIO` → Manejo de Archivos en Memoria** 💾  
   - `from io import BytesIO`  
   - Permite trabajar con **imágenes sin necesidad de guardarlas en disco**.  
   - Se usará para cargar imágenes directamente en memoria antes de visualizarlas.  

5️⃣ **`PIL.Image` → Procesamiento de Imágenes** 🖼️  
   - `from PIL import Image`  
   - Nos permite **abrir, procesar y mostrar imágenes** en Python.  
   - Se usará para reconstruir las imágenes en Base64 y mostrarlas en pantalla.  

---

# Foto 

# 📄 **Lectura y Extracción de Imágenes desde CSV**  

En este paso, **cargamos el archivo CSV y extraemos la primera imagen** almacenada en formato Base64 para verificar su correcta codificación. 📂🖼️  

---

## 🛠️ **¿Cómo funciona?**  

1️⃣ **Carga el archivo CSV** 📄  
   - `df = pd.read_csv('chair.csv')`  
   - **Lee el archivo `chair.csv`** usando Pandas y lo almacena en un **DataFrame**.  
   - Contiene la columna `"chair"` con imágenes en formato **Base64 dentro de etiquetas HTML**.  

2️⃣ **Obtiene la primera fila del DataFrame** 🔍  
   - `first_row = df.iloc[0]`  
   - Usa `.iloc[0]` para **seleccionar la primera fila** del DataFrame.  
   - Se extrae una imagen **para verificar que los datos están bien guardados**.  

3️⃣ **Extrae la imagen en Base64** 🏗️  
   - `img_base64 = first_row['chair']`  
   - Se accede a la columna `"chair"` de la primera fila.  
   - **Aquí se encuentra el código Base64 dentro de una etiqueta HTML**.  

---

# Foto 

# 🖼️ **Verificación, Decodificación y Visualización de la Imagen**  

Este código **verifica que la imagen en Base64 esté en el formato correcto, la decodifica y la muestra en pantalla**. 📂🔍  

---

## 🛠️ **¿Cómo funciona?**  

1️⃣ **Verifica si la cadena Base64 tiene un prefijo de datos** 🔎  
   - `if ',' in img_base64:`  
   - Algunas imágenes en Base64 **pueden incluir un prefijo**, por ejemplo:  
     ```
     data:image/png;base64,iVBORw...
     ```
   - Si hay una coma `,`, significa que el prefijo está presente.  
   - `img_base64.split(',')[1]` extrae **solo la parte Base64**, eliminando `"data:image/png;base64,"`.  

2️⃣ **Asegura que la longitud de la cadena sea un múltiplo de 4** 🔢  
   - `padding = len(img_base64) % 4`  
   - Base64 **debe tener una longitud en múltiplos de 4**.  
   - Si no lo es, **se agregan los caracteres `=` necesarios** para corregir la cadena.  
   - `img_base64 += '=' * (4 - padding)` **corrige la longitud si es necesario**.  

3️⃣ **Intenta decodificar la imagen** 🏗️  
   - `img_data = base64.b64decode(img_base64)`  
   - Convierte la cadena **de Base64 a datos binarios de imagen**.  

4️⃣ **Convierte los datos en una imagen visualizable** 🖼️  
   - `img = Image.open(BytesIO(img_data))`  
   - Usa `BytesIO` para **convertir los datos binarios en una imagen sin guardarla en disco**.  
   - `Image.open()` abre la imagen lista para ser visualizada.  

5️⃣ **Muestra la imagen** 📊  
   - `plt.figure()` → Crea una nueva figura para la imagen.  
   - `plt.imshow(img)` → Muestra la imagen decodificada.  
   - `plt.axis('off')` → Oculta los ejes para mejorar la visualización.  
   - `plt.show()` → Muestra la imagen en pantalla.  

6️⃣ **Manejo de errores** ⚠️  
   - Si ocurre un error en la decodificación, se captura con `except Exception as e`.  
   - Se imprime un mensaje de error con `print(f"Error al decodificar la imagen: {e}")`.  

---

# Foto 

# 🖱️ **Verificación de Datos de Ratones**  

Ahora que hemos extraído y almacenado los datos, **vamos a verificar su integridad** antes de proceder con la visualización en Power BI. 📊  

---

# Foto

## 🛠️ **¿Cómo funciona esta prueba?**  

1️⃣ **Carga el archivo CSV** 📂  
   - `df_datos = pd.read_csv('/content/ratones_p1.csv')`  
   - Usa Pandas para **leer los datos almacenados en el archivo CSV**.  

2️⃣ **Muestra las primeras filas** 🔍  
   - `print(df_datos.head())`  
   - Permite visualizar las primeras 5 filas del dataset para asegurarnos de que los datos están bien organizados.  

3️⃣ **Verifica si hay valores nulos** ⚠️  
   - `print(df_datos.isna())`  
   - Devuelve un **DataFrame con valores `True` o `False`**, indicando si hay datos faltantes.  

4️⃣ **Cuenta los valores nulos por columna** 🔢  
   - `print(df_datos.isna().sum())`  
   - Muestra **cuántos valores nulos hay en cada columna**, ayudando a identificar posibles problemas en los datos.  

---

## 5. Preparación de los datos para los algoritmos de Machine Learning. Se deben tratar los datos (limpiando, escalando, separando y todo lo que sea necesario) de tal forma que queden listos para entrenar el modelo.

## 6. Entrenamiento del modelo y comprobación del rendimiento. Se entrenarán uno o varios modelos, comprobando en cada caso el rendimiento que ofrecen mediante las apropiadas medidas de error y/o acierto.

## 7. Se tiene que incluir alguna de las técnicas estudiadas en el tema de Procesamiento de Lenguaje Natural: expresiones regulares, tokenización, generación de texto, análisis de sentimientos, etc.

## 8. Se debe realizar también una aplicación web que haga uso del modelo entrenado.

## 9. Conclusiones. Se expondrán las conclusiones que se han obtenido en la realización del TFM.
