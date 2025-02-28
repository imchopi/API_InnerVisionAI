## 1. Justificación y descripción del proyecto.
## 2. Obtención de datos. Se debe especificar la fuente de los datos. Se indicará por qué medios se han obtenido (encuestas, sensores, scrapping, etc.). Los datos se deben cargar en una estructura que permita su posterior manipulación y uso.
## 3. Limpieza de datos (eliminación de nulos y datos erróneos, etc.). Descripción de los datos. Se debe dar una descripción completa de los datos indicando qué significa cada uno de los atributos.
## 4. Exploración y visualización de los datos. Se realizará un estudio de los datos buscando correlaciones, mostrando gráficas de diferente tipología, observando si hay valores nulos, etc.
## 5. Preparación de los datos para los algoritmos de Machine Learning. Se deben tratar los datos (limpiando, escalando, separando y todo lo que sea necesario) de tal forma que queden listos para entrenar el modelo.
## 6. Entrenamiento del modelo y comprobación del rendimiento. Se entrenarán uno o varios modelos, comprobando en cada caso el rendimiento que ofrecen mediante las apropiadas medidas de error y/o acierto.
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

