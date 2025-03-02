## 1. Justificación y descripción del proyecto.
**Desarrolladores**
- Alejandro Fernández Barrionuevo
- Adrián Perogil Fernández
- Carlos

**Título**
InnerVisionAI

**Descripción**
Un proyecto basado en detección de obstáculos donde, gracias al uso de YOLO, podemos detectar con una cámara todo tipo de objetos en la vida real.

Su uso escalable y la intención con la que se hizo este proyecto fue para ayudar a personas con discapacidades visuales que mediante audio, guiara a las personas
y pudiera recibir un feedback en todo momento, así pudiendo caminar con mayor comodidad y seguridad. 

Como el tiempo que tuvimos era limitado y era muy ambicioso, nos vimos en la obligación de pensar "niveles" para empezar con algo básico hasta llegar al target.

**Código fuente**
[WEB](https://github.com/imchopi/InnerVisionAI/tree/feature_alex)
[API](https://github.com/imchopi/API_InnerVisionAI)

**Presentación en formato PDF**
Próximamente...

**Enlace a la aplicación web**
[Página Web](https://innervisionai.netlify.app/home)

**Recursos utilizados**
- Jira

**Vídeo**
Próximamente...

**Porcentaje que le corresponde a cada miembro del trabajo realizado de dicho proyecto.**
Alejandro Fernández Barrionuevo ()
Adrián Perogil Fernández ()
Carlos ()

## 2. Obtención de datos. Se debe especificar la fuente de los datos. Se indicará por qué medios se han obtenido (encuestas, sensores, scrapping, etc.). Los datos se deben cargar en una estructura que permita su posterior manipulación y uso.
## 3. Limpieza de datos (eliminación de nulos y datos erróneos, etc.). Descripción de los datos. Se debe dar una descripción completa de los datos indicando qué significa cada uno de los atributos.
## 4. Exploración y visualización de los datos. Se realizará un estudio de los datos buscando correlaciones, mostrando gráficas de diferente tipología, observando si hay valores nulos, etc.

## 5. Preparación de los datos para los algoritmos de Machine Learning. Se deben tratar los datos (limpiando, escalando, separando y todo lo que sea necesario) de tal forma que queden listos para entrenar el modelo.
### 5.1 Proceso de Fine-Tuning con YOLOv5

El objetivo del fine-tuning es adaptar un modelo preentrenado de YOLOv5 (yolov5nu.pt) a nuestro dataset, mejorando su capacidad de detección en nuestro caso de uso específico.

### 📂 5.1.1 Preparación del Dataset
Para entrenar el modelo, primero preparamos los datos siguiendo los pasos detallados a continuación:

1️⃣ Obtención del Dataset

Realizamos scraping de imágenes, almacenándolas en un archivo CSV en formato base64.

📌 Ejemplo de archivo:
![image](https://github.com/user-attachments/assets/6803008a-0ca4-4ad6-830b-18efb486ba31)

---

2️⃣ Conversión de Imágenes

Como las imágenes estaban almacenadas en formato base64, era necesario decodificarlas para poder usarlas en el entrenamiento.

Utilizamos el siguiente script en Python para convertir las imágenes de base64 a `.jpg`:

![image](https://github.com/user-attachments/assets/58af828c-a9dc-40a4-9005-2d6db3b7bb56)

---

3️⃣ Etiquetado de Imágenes

Para entrenar un modelo de detección de objetos, cada imagen necesita etiquetas con las coordenadas de los objetos. Utilizamos **Roboflow**, una plataforma que permite:

- ✅ Subir imágenes.
- ✅ Etiquetar imágenes manualmente o automáticamente con herramientas de anotación.
- ✅ Convertir el dataset a formatos compatibles con modelos de detección como YOLOv5.
- ✅ Dividir los datos en conjuntos de entrenamiento, validación y prueba.

Nuestro objetivo fue **etiquetar automáticamente** imágenes del dataset para detectar objetos de interés y exportarlas en formato YOLOv5.

🔹 Creación de un Proyecto en Roboflow

- Asignamos un nombre al proyecto, por ejemplo: cupboard_detection.
- Seleccionamos el tipo de modelo: Object Detection (YOLOv5, COCO, etc.)

![image](https://github.com/user-attachments/assets/6ad1ed78-265d-44b6-8ecb-ff13b256031b)
  

🔹 Subida de Imágenes al Proyecto

![image](https://github.com/user-attachments/assets/5c00338e-e366-49b7-b870-caab13064313)

🔹 Etiquetado Automático de Objetos

Dado que Roboflow cuenta con herramientas de etiquetado automático, utilizamos esta opción para generar anotaciones sin intervención manual.

![image](https://github.com/user-attachments/assets/65260858-f3dd-4f6e-b690-78e095ef2e20)

Si bien el etiquetado automático es preciso, verificamos que las anotaciones fueran correctas.

![image](https://github.com/user-attachments/assets/b50e683b-e12b-4f62-906e-a672ed6310d8)

En caso de errores, ajustamos manualmente las etiquetas antes de continuar para completar el proceso.

![image](https://github.com/user-attachments/assets/ebea7738-f6de-4def-853f-dd361ac78e29)

Después de la comprobación añadimos las etiquetas aprobadas.

![image](https://github.com/user-attachments/assets/faf2c310-4d9d-47ba-8a08-9e818f91ae73)



🔹 Exportación del Dataset en Formato YOLOv5

Para utilizar las imágenes etiquetadas en el entrenamiento del modelo, exportamos el dataset en formato YOLOv5.

Roboflow nos permite dividir el dataset en tres subconjuntos:
- 80% para entrenamiento (train)
- 10% para validación (valid)
- 10% para prueba (test)

![image](https://github.com/user-attachments/assets/9a021657-f59a-4b1c-bac5-f258790e0bf2)

En la sección de exportación, seleccionamos YOLOv5 como formato de salida y descargamos un archivo ZIP.

![image](https://github.com/user-attachments/assets/a4fd3ee4-1efb-4581-8b08-c9d18a9aefb9)

El archivo ZIP tiene la siguiente estructura:

```
/dataset
│── test/    # 10% de imágenes para prueba
│   ├── images/
│   ├── labels/   
│
│── train/   # 80% de imágenes para entrenamiento
│   ├── images/
│   ├── labels/
|
│── valid/   # 10% de imágenes para validación
│   ├── images/
│   ├── labels/
│
│── data.yaml    # Archivo de configuración del dataset
```

En el directorio `labels` obtenemos archivos .txt con las coordenadas de los objetos.


### 🛠 5.1.2 Entrenamiento del Modelo

Para el entrenamiento utilizamos el modelo preentrenado **yolov5nu.pt**. Ejecutamos el proceso en Google Colab con GPU habilitada para acelerar el cómputo. Clonamos el repositorio de YOLOv5. Usamos los siguientes parámetros en el script de entrenamiento:

```python
!python train.py \
  --weights /content/drive/MyDrive/Models/yolov5nu.pt \
  --data /content/drive/MyDrive/YOLO_Dataset/data.yaml \
  --epochs 50 \
  --batch-size 16 \
  --imgsz 640 \
  --optimizer SGD \
  --device 0
```

Sin embargo, durante la ejecución del entrenamiento encontramos errores relacionados con la configuración de los anchors en el modelo. El siguiente es un ejemplo de los errores que recibimos:

```
RuntimeError: shape '[3, -1, 2]' is invalid for input of size 3
```

Este error sugiere que los anchors definidos en el modelo no se ajustaban correctamente al número de clases u otras dimensiones esperadas. Intentamos modificar la configuración, pero el problema persistió.

---

⚠️ Problemas Encontrados y Conclusión

No logramos completar el fine-tuning debido a erroresencontrados. Las posibles causas incluyen:

1. **Incompatibilidad en los anchors**: La configuración de los anchors puede no haber sido adecuada para nuestro dataset. 
2. **Formato incorrecto en el archivo data.yaml**: Es posible que las clases o los parámetros en el archivo no estuvieran correctamente definidos.
3. **Modelo preentrenado incompatible**: Puede que el modelo **yolov5nu.pt** no estuviera configurado correctamente para ser reutilizado con nuevos datos.

Para solucionar estos problemas, proponemos:
- Revisar el formato de **data.yaml** y asegurarnos de que está bien definido.
- Ajustar los anchors manualmente o permitir que YOLO los recalibre automáticamente.
- Probar con otro modelo preentrenado de YOLOv5 para verificar compatibilidad.

A pesar de las dificultades, este proceso nos permitió comprender mejor el flujo de trabajo de YOLOv5 y los retos asociados a la personalización de modelos de detección de objetos. Con algunos ajustes, creemos que podemos completar con éxito el fine-tuning en futuras iteraciones.


## 6. Entrenamiento del modelo y comprobación del rendimiento. Se entrenarán uno o varios modelos, comprobando en cada caso el rendimiento que ofrecen mediante las apropiadas medidas de error y/o acierto.

### 6.1 Uso de YOLOv5 de Ultralytics y Chatbot personalizado

En este apartado, se describe el proceso de implementación de YOLOv5 de Ultralytics, desde la configuración del entorno hasta la integración con una API en Flask y un frontend en React. El objetivo es demostrar cómo este modelo puede ser utilizado para detectar objetos en tiempo real, enviando los resultados de las detecciones a una interfaz gráfica que permite visualizar las predicciones de manera intuitiva. 
Además, se aborda la importancia de optimizar el flujo de trabajo para garantizar un rendimiento óptimo, especialmente como tratar el funcionamiento con recursos gratuitos y el limite que establece Netlify y nuestra API con Flask en local.

También ideamos un chatbot con una API-KEY de OpenAI, donde con base en nuestro README.md, procese y responda preguntas y cuestiones sobre nuestro proyecto debido a, que nuestro readme va a ser bastante extenso.

Primero explicaremos el funcionamiento de YOLOv5 con Ultralytics.

#### Uso de la API con Flask

La API desarrollada con Flask sirve como el núcleo del proyecto, facilitando la comunicación entre el modelo de detección de objetos YOLOv5 y el chatbot basado en OpenAI. Esta API maneja tanto el procesamiento de imágenes en tiempo real mediante WebSockets como la interacción con el chatbot mediante solicitudes REST.

#### Configuración del Entorno

Antes de ejecutar la API, es necesario asegurarse de que se tienen instaladas todas las dependencias necesarias. Se pueden instalar mediante:

```bash
pip install -r requirements.txt
python app.py
```

(Aconsejable hacer un environment si necesitas versiones específica)

Como la versión de Python que usamos era la 3.10, con ejecutar el comando de arriba, te instalará siempre lo último de esta versión en concreto de python.

#### Uso de WebSocket para Detección de Objetos con YOLOv5

La API emplea flask_socketio para recibir imágenes desde el frontend en tiempo real, procesarlas con YOLOv5 y devolver las detecciones correspondientes.

#### Flujo de Trabajo

- El frontend envía frames codificados en base64 mediante WebSocket.

- La API recibe y decodifica la imagen, luego la redimensiona para mejorar la eficiencia.

- YOLOv5 procesa la imagen y genera predicciones sobre los objetos detectados.

- La API envía las detecciones de vuelta al frontend a través de WebSocket.

![api_websocket](https://github.com/user-attachments/assets/0be421ff-2753-4eea-8bb0-560b6aa6c703)

Aunque la anterior imagen representa la función y puede ser engorrosa, la siguiente captura será la zona importante y vital de entender.
Esta parte es la más importante ya que sin ella, no podríamos representar en el frontend mediante el uso de canvas, pintar los rectángulos de la detección de objetos ya que nos da:
- Las posiciones de cada objeto
- Redonde el score del objeto a 2 decimales
- Gracias a la id, accedemos al nombre de la clase, por ejemplo, 0 - Persona
- Añadimos esto a una lista finalmente
  
![api_socket2](https://github.com/user-attachments/assets/fe737556-a178-4f62-af07-5f0f63d33886)

#### Uso de API REST para el Chatbot Personalizado

Para permitir que los usuarios interactúen con el chatbot, la API implementa un endpoint /chat que recibe preguntas del usuario y responde basándose en el contenido del README.md del proyecto.

#### Flujo de Trabajo

- El usuario envía una solicitud POST a /chat con el mensaje en formato JSON.

- La API obtiene el contenido del README.md desde GitHub.

- Se construye un mensaje para OpenAI combinando la pregunta del usuario y la información del README.md.

- La API envía la solicitud a OpenAI y devuelve la respuesta generada.

La parte del frontend será expuesta en la sección **8. Desarrollo de la Aplicación Web**

![api_rest](https://github.com/user-attachments/assets/1045acd4-a22b-44f2-ae54-376e16ca642e)

Vemos aquí mas directamente la parte importante, que usará el rol de system, con lo cual nos permite generar un prompt anterior al promt del usuario, donde gracias a esta función, transformamos el readme...
![readme](https://github.com/user-attachments/assets/fc3a12d0-7bfc-4919-8424-545b98158e73)

Para conseguir así finalmente que "sesgemos" al modelo para que responda preguntas con base en nuestro Readme.
![api_chat2](https://github.com/user-attachments/assets/b0b03eec-27d0-43eb-b092-d6e35d641c51)

Las demás lineas de código son necesarias para permisos y utilidad como:

**CORS**
![cors1](https://github.com/user-attachments/assets/8f0fc1bd-7060-4089-80d7-5c7b572813e0)
![cors2](https://github.com/user-attachments/assets/cd79b6b5-5ae4-402f-9195-57947fed27bf)

**Optimización YOLO**
![yolo1](https://github.com/user-attachments/assets/15184317-f9f6-4be5-ab08-e465cf3b873e)

## 7. Se tiene que incluir alguna de las técnicas estudiadas en el tema de Procesamiento de Lenguaje Natural: expresiones regulares, tokenización, generación de texto, análisis de sentimientos, etc.


## 8. Desarrollo de la Aplicación Web

Nuestra aplicación web ha sido desarrollada utilizando **React** e **Ionic** con **TypeScript**, proporcionando una experiencia moderna y responsiva. A continuación, describimos los principales componentes de la web junto con capturas del código y la interfaz.

### 8.1 Estructura del Proyecto

El proyecto se organiza en distintos componentes de React y páginas específicas para cada funcionalidad. Nuestra estructura principal incluye:
- **Home.tsx** (Página de inicio)
- **Model.tsx** (Módulo de detección de objetos)
- **AboutUs.tsx** (Información del equipo)
- **Chatbot.tsx** (Asistente virtual basado en IA)

Con esta organización permitimos una estructura modular y escalable. 🚀

### 8.2 Inicio (Home.tsx)

Nuestra página principal (**Home.tsx**) presenta el proyecto y enlaza a su repositorio en GitHub. Hemos utilizado iconos para mejorar la accesibilidad visual.

#### ¿Qué hace este archivo?
- Muestra el diseño principal: Incluimos el encabezado, el contenido y cualquier elemento visual que queramos resaltar.
- Carga datos si es necesario: Dependiendo de lo que queremos mostrar, aquí podemos traer información desde una API o una base de datos.
- Facilita la navegación: Agregamos enlaces o botones para que los usuarios puedan moverse dentro de nuestra aplicación.
  
---

#### 8.2.1 Importación de librerías y estilos
El archivo `Home.tsx` es un componente de React que utiliza Ionic y otros elementos para la estructura y diseño de la pantalla principal de la aplicación.

📌 Código de importación:
![image](https://github.com/user-attachments/assets/b3ce7a56-9c89-4614-93ee-706c37b11121)

---

#### 8.2.2 Contenido de la página
En la sección principal de la pantalla, mostramos el título del proyecto junto con una breve descripción para que los usuarios comprendan su propósito de inmediato. Además, proporcionamos enlaces directos a los repositorios de GitHub, tanto para la web como para la API, con iconos interactivos que facilitan el acceso.

📌 Código del contenido:
![image](https://github.com/user-attachments/assets/1d891c5d-278b-42b3-8b11-5adc13391e66)

---

#### 8.2.3 Estilos Aplicados
En `Home.css`, definimos estilos para mejorar la apariencia del componente. 

📌 Ejemplo de diseño:

![image](https://github.com/user-attachments/assets/2b9051a9-4ea8-4f39-bdbf-de611e44f181)

Con estos estilos nos aseguramos que la página tenga un diseño centrado y estético.


✨ **Vista de la página de inicio:**  

![image](https://github.com/user-attachments/assets/a850f36f-605a-406a-a75b-50b4e671ce34)


Esta página brinda una bienvenida clara y acceso directo a la información clave del proyecto. 🚀

## 8.3 Modelo de Detección de Objetos (Model.tsx)

En esta página implementamos la detección de objetos en tiempo real utilizando la cámara del dispositivo. Para ello, hacemos uso de WebSockets para enviar frames al backend y recibir las detecciones procesadas.

#### ¿Qué hace este archivo?
- Captura video en tiempo real desde la cámara del dispositivo. El código a continuación solicita permisos para acceder a la cámara del dispositivo y captura el video en tiempo real:
  
  ![image](https://github.com/user-attachments/assets/9d704801-afd2-4f15-8cb7-8563a47fdeb5)

- Envía frames al backend. Usa WebSockets para enviar imágenes a la API, donde se realiza la detección de objetos.

  ![image](https://github.com/user-attachments/assets/3045fff8-ff73-4c49-b901-24192edad290)

  
- Recibe y dibuja detecciones. Recibe los resultados del backend y los dibuja sobre el video en un canvas.

  ![image](https://github.com/user-attachments/assets/aa6c6931-02fe-444d-83f4-0db89417b673)

---

#### 8.3.1 Importación de librerías y estilos
El archivo Model.tsx importa las siguientes librerías:

- react, useEffect, useRef: Para gestionar el ciclo de vida del componente y referencias.
- socket.io-client: Para la comunicación en tiempo real con el backend.
- @ionic/react: Para la estructura de la página en Ionic.
- @capacitor/core y @capacitor/status-bar: Para ajustar la interfaz en dispositivos móviles.

📌 Código de importación:
![image](https://github.com/user-attachments/assets/44c13030-c11c-450b-8eff-bf19317438da)

---

#### 8.3.2 Contenido de la página
Esta sección estructura la interfaz del módulo:

- Video en vivo: Capturamos la imagen de la cámara.
- Canvas de detecciones: Dibujamos los resultados del modelo de IA sobre el video.

📌 Código del contenido:
![image](https://github.com/user-attachments/assets/a9428b16-d8ba-474a-9211-cdd2a1f4d686)

---

#### 8.3.3 Comunicación con el Backend

Conexión al Backend (A nivel local)
![image](https://github.com/user-attachments/assets/9f55390b-f505-409d-a544-9972425c4e85)

Aquí se establece la conexión con el backend en el puerto 5000.

Cuando el backend detecta objetos en el frame enviado, devuelve las coordenadas y la confianza del modelo. Este código se encarga de dibujar los resultados sobre el video:

![image](https://github.com/user-attachments/assets/61bd5e5d-8bb5-4451-8c40-a219badb81d9)

Desconecta el socket cuando el usuario sale de la página:

![image](https://github.com/user-attachments/assets/c6493fce-0297-4b97-a311-39f34df48f0a)

---

#### 8.3.4 Estilos Aplicados
En Model.css, definimos estilos para:

Centrar el video en pantalla.
Ajustar el tamaño del video y el canvas.
Aplicar un fondo con degradado.

📌 Ejemplo de diseño:
![image](https://github.com/user-attachments/assets/c44fcc65-8273-48ec-b1da-ffd645ccf3e7)


✨ **Vista del modelo de detección de objetos:**

[Imagen del modelo funcionando]

Con esta implementación logramos un procesamiento ágil y preciso, permitiendo a los usuarios identificar objetos en tiempo real de manera intuitiva y eficaz. 🎯

## 8.4 Información del Equipo (AboutUs.tsx)

En esta página mostramos a los integrantes del equipo de desarrollo. En la página se puede visualizar una lista de miembros, su rol, su formación y enlaces a sus perfiles de GitHub y LinkedIn.

✨ **Vista de la página de Información del Equipo:**

![image](https://github.com/user-attachments/assets/e2236a86-5f5f-44dc-82c4-b8aa7872afaa)


## 8.5 Chatbot (Chatbot.tsx)

En esta página implementamos un chatbot interactivo que permite a los usuarios realizar preguntas. Utilizamos un backend en Node.js para procesar las consultas y devolver respuestas dinámicas.

### ¿Qué hace este archivo?
- **Muestra un chatbot en la aplicación.**
- **Permite la interacción con el usuario.** El usuario puede escribir preguntas y recibir respuestas en tiempo real.
- **Envía consultas a un backend en Node.js.** Se conecta a un servidor en `http://localhost:5000/chat` para procesar los mensajes.
- **Formatea las respuestas.** Convierte ciertos elementos de texto como negritas y listas en formato HTML para mejorar la legibilidad.

---

### 8.5.1 Importación de librerías y estilos
El archivo `Chatbot.tsx` importa las siguientes librerías:

- **react, useState**: Para gestionar el estado del chatbot y los mensajes.
- **axios**: Para enviar solicitudes HTTP al backend.
- **@ionic/react**: Para la estructura de la página.
- **Footer**: Componente reutilizable para el pie de página.
- **Chatbot.css**: Archivo de estilos para la apariencia del chatbot.

📌 **Código de importación:**
![image](https://github.com/user-attachments/assets/8822090b-325f-4af6-aa1f-72307de3ce1f)


### 8.5.2 Estado y manejo de mensajes
Almacenamos los mensajes en un array gestionado con `useState`. Inicialmente, contiene un mensaje de bienvenida del bot:

📌 **Código de inicialización:**
![image](https://github.com/user-attachments/assets/bf0786c2-d521-4084-a8a0-e469a4a0aa52)
![image](https://github.com/user-attachments/assets/59699bd8-f7bf-437c-bffb-d92c8e92b76d)


El usuario puede escribir un mensaje y enviarlo con `sendMessage()`, que realiza las siguientes acciones:
1. Agrega el mensaje del usuario al estado.
2. Envía la consulta al backend mediante una petición `POST`.
3. Recibe la respuesta del servidor y la formatea.
4. Agrega la respuesta del chatbot a la conversación.
5. Limpia el input después de enviar el mensaje.

📌 **Código de envío de mensajes:**
![image](https://github.com/user-attachments/assets/f6eabbe7-1417-42dd-88b0-25fa0b26bf11)


---

### 8.5.3 Renderizado del Chatbot

El chatbot se compone de:
- Un **contenedor de mensajes**, donde se muestran las interacciones previas.
- Un **input de texto** para que el usuario escriba su mensaje.
- Un **botón de envío** para enviar mensajes manualmente.
- La posibilidad de presionar **Enter** para enviar el mensaje.

📌 **Código del renderizado:**
![image](https://github.com/user-attachments/assets/ef0402ba-5a17-42e8-8ef4-591904aab9c8)


---

### 8.5.4 Formateo de respuestas

Para mejorar la presentación de las respuestas, convertimos ciertos elementos a formato HTML:
- **Negritas**: `**texto**` → `<strong>texto</strong>`
- **Saltos de línea**: `\n` → `<br>`
- **Listas numeradas**: `1. Texto` → `• Texto`

📌 **Código de formateo:**
![image](https://github.com/user-attachments/assets/ac19de25-1edd-4c50-b5e9-ac02fcf076a0)



---

✨ **Vista del chatbot funcionando:**

[Imagen del chatbot]

Con esta implementación ofrecemos una experiencia fluida y responsiva, permitiendo a los usuarios interactuar con el asistente virtual de manera sencilla y eficiente. 🚀

