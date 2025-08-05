# 🎬 IMDb Scraper – Arquitectura Limpia para Scraping Distribuido y Persistencia Híbrida

Este proyecto es la solución integral a la prueba técnica, demostrando la capacidad de construir un sistema de extracción de datos robusto, escalable y mantenible. Se ha desarrollado un scraper para el Top 250 de IMDb, implementando técnicas avanzadas de evasión de bloqueos, persistencia en PostgreSQL y una arquitectura de software desacoplada, lista para evolucionar.

El diseño se fundamenta en principios de **Clean Architecture** y **Domain-Driven Design (DDD)**, está completamente **orquestado con Docker**, y documenta una estrategia clara para escalar hacia herramientas como Playwright o Selenium si las defensas del sitio objetivo lo requiriesen.

---
## 🧭 Tabla de Contenido

- [✅ Objetivos Cumplidos y Cobertura de Requisitos](#-objetivos-cumplidos-y-cobertura-de-requisitos)
- [🏛️ Filosofía de Arquitectura y Decisiones Técnicas](#️-filosofía-de-arquitectura-y-decisiones-técnicas)
- [🧱 Estructura del Proyecto](#-estructura-del-proyecto)
- [🧩 Estrategia de Red Distribuida: VPN + Proxies + TOR](#-estrategia-de-red-distribuida-vpn--proxies--tor)
- [🐳 Instrucciones de Despliegue con Docker](#-instrucciones-de-despliegue-con-docker)
- [🧠 SQL Analítico](#-sql-analítico)
- [4️⃣ Comparación y Escalabilidad: Scrapy vs. Playwright/Selenium](#4️⃣-comparación-y-escalabilidad-scrapy-vs-playwrightselenium)
- [🧵 Concurrencia Aplicada en el Scraper](#-concurrencia-aplicada-en-el-scraper)
- [🔍 Decisiones Técnicas Clave](#-decisiones-técnicas-clave)
- [📦 Entregables Finales](#-entregables-finales)
- [📣 Créditos](#-créditos)
---
## ✅ Objetivos Cumplidos y Cobertura de Requisitos

Se ha cumplido con el 100% de los requisitos solicitados, tanto obligatorios como opcionales, para demostrar una competencia exhaustiva en cada área evaluada.

| Área de Evaluación | ✅ Implementado | Detalle Técnico de la Implementación |
| :--- | :---: | :--- |
| **Scraping (60%)** | ✅ Sí | Se extraen las 250 películas del chart, obteniendo Título, Año, Calificación, Duración, Metascore y Actores desde las páginas de detalle. La solución es modular y maneja errores con reintentos y backoff exponencial. |
| **Arquitectura Avanzada** | ✅ Sí | Se implementó **Clean Architecture + DDD** y el patrón **Factory** para desacoplar la lógica de negocio de la infraestructura (ej. persistencia, scraping). |
| **Persistencia CSV + SQL** | ✅ Sí | Los datos se persisten de forma híbrida en archivos CSV y en un esquema relacional PostgreSQL con una relación `N:M` entre películas y actores. |
| **SQL Analítico (20%)** | ✅ Sí | Se crearon consultas analíticas complejas utilizando **funciones de ventana (`OVER/PARTITION BY`)**, vistas, índices y justificación de particionamiento. |
| **Proxies y Red (10%)** | ✅ Sí | Se implementó una arquitectura distribuida con múltiples capas de evasión: conexión mediante **VPN real (ProtonVPN vía Docker)**, uso de **proxies premium (DataImpulse)** y fallback automático a la **red TOR**. Además, se incluyó un sistema de **reintentos con backoff exponencial** y validación de IP para garantizar la obtención del dato. |
| **Dockerizado y Portable** | ✅ Sí | Todo el entorno (scraper, base de datos) se levanta con un solo comando (`docker-compose up`), garantizando la replicabilidad del entorno. |
| **Comparación Herramientas (10%)** | ✅ Sí | Se incluye una sección detallada justificando cuándo y cómo migrar a **Playwright/Selenium** para escenarios de JavaScript dinámico y CAPTCHAs. |
| **Evidencia y Documentación** | ✅ Sí | El repositorio incluye logs, scripts SQL, CSVs generados y este README detallado como evidencia del trabajo realizado. |

---

## 🏛️ Filosofía de Arquitectura y Decisiones Técnicas

### ¿Por qué Clean Architecture + Domain-Driven Design (DDD)?
Un enfoque profesional exige construir un **sistema mantenible y escalable**.

- **Separación de Responsabilidades (SoC):** Las dependencias apuntan hacia adentro. La lógica de negocio no sabe nada sobre la base de datos ni el scraping.
- **Testabilidad Aislada:** Las capas `domain` y `application` se pueden testear unitariamente sin dependencias externas.
- **Modelado del Dominio:** Entidades como `Movie` y `Actor` reflejan el lenguaje del problema, con validaciones integradas.

### ¿Por qué el Patrón Factory y Contenedor de Dependencias?
Para gestionar la creación de objetos y el ciclo de vida de los recursos (como la conexión a la base de datos), las fábricas individuales se han centralizado en un Contenedor de Inyección de Dependencias. Esta clase actúa como el único punto de ensamblaje de la aplicación, garantizando que los recursos se creen una sola vez y se liberen correctamente, además de desacoplar completamente el punto de entrada de la construcción de sus dependencias.

### ¿Por qué TOR para la Rotación de IPs?
TOR ofrece:

- **Rotación efectiva de IPs** sin costo adicional.
- **Independencia del proveedor:** Se puede sustituir fácilmente por otros proxies comerciales o VPNs.

---

## 🧱 Estructura del Proyecto

```
imbd_scraper_project/
├── .env                          # Variables de entorno (no versionar)
├── .gitignore                   # Ignora __pycache__, .env, logs, etc.
├── docker-compose.yml           # Orquestación de servicios: scraper, DB, TOR, VPN
├── Dockerfile                   # Imagen del scraper (instala psql, dependencias, etc.)
├── Readme.md                    # Documentación principal
├── requirements.txt             # Dependencias del proyecto

├── application/                 # Casos de uso orquestando la lógica de negocio
│   ├── __init__.py
│   └── use_cases/
│       ├── composite_save_movie_with_actors_use_case.py
│       ├── save_movie_with_actors_csv_use_case.py
│       ├── save_movie_with_actors_postgres_use_case.py
│       └── __init__.py

├── data/                        # Archivos CSV generados automáticamente
│   ├── actors.csv
│   ├── movies.csv
│   └── movie_actor.csv

├── docs/                        # Documentación técnica (PDF, diagramas)
│   └── IMBDSCRAPER_Documento_Arquitectura.pdf

├── domain/                      # Modelo de dominio + interfaces de uso
│   ├── __init__.py
│   ├── interfaces/              # Contratos (abstracciones)
│   │   ├── proxy_interface.py
│   │   ├── scraper_interface.py
│   │   ├── tor_interface.py
│   │   ├── use_case_interface.py
│   │   └── __init__.py
│   ├── models/                  # Entidades del dominio
│   │   ├── actor.py
│   │   ├── movie.py
│   │   ├── movie_actor.py
│   │   └── __init__.py
│   └── repositories/            # Interfaces de repositorio
│       ├── actor_repository.py
│       ├── movie_actor_repository.py
│       ├── movie_repository.py
│       └── __init__.py

├── infrastructure/              # Implementación técnica de la arquitectura
│   ├── __init__.py
│   ├── factory/                 # Contenedor de dependencias y factories
│   │   ├── dependency_container.py
│   │   └── __init__.py
│   ├── network/                 # Proveedor de proxies y rotador de TOR
│   │   ├── proxy_provider.py
│   │   ├── tor_rotator.py
│   │   └── __init__.py
│   ├── persistence/             # Persistencia CSV y PostgreSQL
│   │   ├── __init__.py
│   │   ├── csv/
│   │   │   ├── __init__.py
│   │   │   └── repositories/
│   │   │       ├── actor_csv_repository.py
│   │   │       ├── movie_actor_csv_repository.py
│   │   │       ├── movie_csv_repository.py
│   │   │       └── __init__.py
│   │   └── postgres/
│   │       ├── postgres_connection.py
│   │       └── repositories/
│   │           ├── actor_postgres_repository.py
│   │           ├── movie_actor_postgres_repository.py
│   │           ├── movie_postgres_repository.py
│   │           └── __init__.py
│   ├── provider/                # (Deprecable si ya se migró a /network)
│   │   └── __init__.py
│   ├── proxy_rotation/          # (Deprecable también; quedó solo __pycache__)
│   └── scraper/                 # Scraper principal y herramientas
│       ├── imdb_scraper.py
│       ├── utils.py
│       └── __init__.py

├── logs/                        # Logs generados por el scraper
│   └── scraper.log

├── presentation/                # CLI o interfaces de entrada al sistema
│   ├── __init__.py
│   └── cli/
│       ├── run_scraper.py       # Punto de entrada principal
│       └── __init__.py

├── shared/                      # Recursos reutilizables a lo largo del sistema
│   ├── __init__.py
│   ├── config/
│   │   ├── config.py
│   │   └── __init__.py
│   └── logger/
│       ├── logging_config.py
│       └── __init__.py

├── sql/                         # Scripts SQL ejecutables dentro del contenedor
│   ├── 01_schema.sql
│   ├── 02_procedures.sql
│   ├── 03_views.sql
│   ├── load_from_csv.sql
│   └── queries.sql

```
---

### 🧩 Estrategia de Red Distribuida: VPN + Proxies + TOR

El scraper está preparado para ejecutar en ambientes con **alta sensibilidad al bloqueo**, usando una combinación de estrategias en capas para garantizar la recolección de datos:

| Tecnología        | Propósito                                    | Implementación                                                      |
|------------------|----------------------------------------------|----------------------------------------------------------------------|
| **VPN (ProtonVPN)**     | Cambiar geolocalización y evitar bloqueo regional | Montada en **Docker**, validación de país vía healthcheck por imagen qmcgaw/gluetun            |
| **Proxies Premium**     | IPs rotativas anónimas, baja latencia            | Integración con **DataImpulse**, rotación automática por cada request |
| **TOR (Fallback)**      | Red distribuida anónima gratuita                 | Activación automática en caso de fallo en las otras capas            |

Además, se integró un **sistema de reintentos inteligentes con backoff exponencial** que asegura que la petición se repita en caso de fallo, cambiando IP si es necesario, y dejando trazabilidad en logs con la IP usada.

---

### 🔧 Posibles Mejoras Futuras

- **Proxy Pool Dinámico** con rotación basada en reputación/IP-bans.
- **Auto-restart de TOR/VPN** si el healthcheck falla.
- Integración con **servicios anti-CAPTCHA** como 2Captcha o Anti-Captcha.
- Compatibilidad con **geolocalización dinámica por país**, seleccionando el proxy o VPN más adecuado según el sitio.

---

## 🐳 Instrucciones de Despliegue con Docker

1. Crear el archivo `.env` en la carpeta raiz  
### 📄 Archivo `.env` (proporcionado solo con fines de evaluación)

Este archivo contiene la configuración necesaria para conectar con los servicios de base de datos, proxies y VPN utilizados en el entorno del scraper.

**⚠️ Importante:** Las credenciales contenidas en este archivo son simuladas y han sido incluidas únicamente para facilitar la evaluación del proyecto. En un entorno real, se recomienda gestionar estas variables de forma segura mediante servicios como Docker Secrets, AWS Parameter Store o `.env` ignorado por `.gitignore`.

Ejemplo de `.env`:

```env

POSTGRES_DB=imdb_scraper
POSTGRES_USER=aruiz
POSTGRES_PASSWORD=@ndresruiz@123
POSTGRES_PORT=5432
POSTGRES_HOST=postgres


PROXY_HOST=gw.dataimpulse.com
PROXY_PORT=823
PROXY_USER=f1bdc8e207aafe131216
PROXY_PASS=6c1b9cdd85f65f0b

VPN_PROVIDER=protonvpn
VPN_USERNAME=qlT5gZGnlHi2Y1uh
VPN_PASSWORD=mUiXGzoM9SeYHhYocElsEMuQwUUGuLFL
VPN_COUNTRY=Argentina

```
2. Ejecutar:
   
```bash
docker-compose build --no-cache
```

```bash
docker-compose up
```

- PostgreSQL expuesto en `localhost:5432`.
- Scraper inicia automáticamente.
- Logs en `logs/scraper.log`.
- Archivos `movies.csv`, `actors.csv`, `movie_actor.csv` generados en `/data`.

---

## 🧠 SQL Analítico

Incluye:

- 🎞️ **Top 5 por duración promedio por década** – con `ROW_NUMBER()` y `PARTITION BY`.
- 📈 **Desviación estándar de calificación por año** – mide dispersión de opiniones.
- ⚖️ **Comparación IMDb vs Metascore** – normalizado y filtrado por delta > 20%.
- 👥 **Vista Actor-Película** – facilita filtrado y joins.
- ⚡ **Índices y vistas materializadas** – optimización de rendimiento.

---

## 4️⃣ Comparación y Escalabilidad: Scrapy vs. Playwright/Selenium

Aunque este proyecto está construido con `requests` y `BeautifulSoup` por su requerimiento y control detallado del flujo, está preparado para escalar hacia herramientas como **Playwright** o **Selenium** en los siguientes escenarios:

### 🔧 Configuración avanzada de navegador
Ambas herramientas permiten lanzar navegadores con configuraciones avanzadas:

- **Modo headless o visible** (`headless=True/False`).
- **Modificación de headers personalizados** como User-Agent, Referer, Accept-Language, etc.
- **Evasión de detección WebDriver**:
  - Redefinir `navigator.webdriver`.
  - Inyectar scripts personalizados en el contexto de la página.
  - Usar extensiones anti-bot o librerías como `stealth.min.js` en Playwright.

### 🎯 Selectores dinámicos con espera explícita
- **Playwright**: `page.wait_for_selector("selector")` asegura que el DOM esté listo.
- **Selenium**: `WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located(...))` permite esperar elementos dinámicos cargados vía JavaScript.

Esto evita fallos comunes en scraping dinámico (ej: `element not found` o `NoneType`).

### 🛡️ Manejo de JavaScript rendering y CAPTCHAs
- **Renderizado completo del DOM** habilitado por defecto al usar navegadores reales.
- **CAPTCHAs**:
  - Detectar presencia de CAPTCHA mediante selectores.
  - Resolverlo usando APIs de servicios como **2Captcha**, **AntiCaptcha**, **DeathByCaptcha**.
  - Alternativamente, utilizar OCR básico si el CAPTCHA es visualmente simple.

### ⚙️ Control de concurrencia
- **Playwright**:
  - Permite abrir múltiples contextos (`browser.new_context()`) o múltiples páginas en paralelo.
  - Ideal para scraping distribuido sin overhead de múltiples procesos.

- **Selenium**:
  - Compatible con **Selenium Grid** para distribuir instancias en múltiples nodos.
  - Puede ejecutarse en contenedores paralelos coordinados mediante colas (ej. **Celery**, **RabbitMQ**).

- **Ambas** pueden integrarse en workers asíncronos si se envuelven correctamente.

### 📌 Justificación vs Scrapy
Aunque **Scrapy** es potente y extensible, **Playwright** y **Selenium** ofrecen ventajas cuando:
- El contenido depende de **JavaScript o eventos del navegador**.
- Se requiere **simular interacción humana real**: scroll, clics, selección dinámica.
- El sitio tiene **bloqueos activos** como CAPTCHAs, honeypots o detección de tráfico automatizado.

## 🧩 Implementación con Playwright o Selenium

Gracias a la aplicación de Clean Architecture y DDD, el sistema permite **agregar nuevos engines de scraping** (como Playwright o Selenium) sin reemplazar ni modificar la implementación actual basada en `requests + BeautifulSoup`.

### 🔄 ¿Cómo se logra esto?

La clave está en el uso de interfaces y un contenedor de dependencias desacoplado:

- `ScraperInterface` en `domain/` define el contrato único que todas las implementaciones deben seguir.
- Cada implementación (ej. `ImdbScraper`, `ImdbScraperPlaywright`) vive en su propio archivo dentro de `infrastructure/scraper/`.
- El **`DependencyContainer`** centraliza la lógica de construcción. Lee la configuración y decide qué `engine` (motor) de scraper debe instanciar y devolver.

### ⚙️ Alternativa para elegir el engine

Se debe cambiar una variable de entorno en `config.py` para permitir elegir dinámicamente el motor de scraping:

```python
# shared/config/config.py
SCRAPER_ENGINE = "Playwright"
```

```python
# infrastructure/factory/scraper_factory.py
from domain.interfaces.use_case_interface import UseCaseInterface
from domain.interfaces.scraper_interface import ScraperInterface

def get_scraper(source: str = "imdb", engine: str = "requests", use_case: UseCaseInterface = None) -> ScraperInterface:
    
    if use_case is None:
        raise ValueError("Se requiere un 'use_case' para inicializar el scraper.")

    source_clean = source.lower().strip()
    engine_clean = engine.lower().strip()

    if source_clean == "imdb":
        if engine_clean == "requests":
            from infrastructure.scraper.imdb_scraper import ImdbScraper
            return ImdbScraper(use_case=use_case, engine=engine_clean)

        elif engine_clean == "playwright":
            from infrastructure.scraper.imdb_scraper_playwright import ImdbScraperPlaywright
            return ImdbScraperPlaywright(use_case=use_case, engine=engine_clean)

        else:
            raise ValueError(f"Motor '{engine_clean}' no soportado para IMDb.")

    raise ValueError(f"Source '{source}' no es reconocido.")

```

### 🔁 ¿Y si quiero usar ambos al mismo tiempo?

También es posible. Puedes inyectar ambos scrapers en un **composite scraper** que combine o compare resultados, o usarlos como fallback uno del otro:

```python
class CompositeScraper(ScraperInterface):
    def __init__(self, primary_scraper, secondary_scraper):
        self.primary = primary_scraper
        self.secondary = secondary_scraper

    def scrape(self):
        try:
            return self.primary.scrape()
        except Exception:
            return self.secondary.scrape()
```

> Esto aporta escalabilidad sin comprometer el diseño, permitiendo usar múltiples motores sin reescribir los casos de uso.


---

## 🧵 Concurrencia Aplicada en el Scraper

El scraper utiliza **`ThreadPoolExecutor`** desde la librería `concurrent.futures` para acelerar la recolección de información de detalle por película.

### 🧠 Detalles técnicos:
- Se limita el número de threads para evitar saturar la red o el endpoint.
- Cada hilo ejecuta la función de extracción del detalle de la película (`/title/{id}/`) en paralelo.
- Esto mejora el rendimiento sin comprometer la trazabilidad ni la estructura del log.

Se podrían reemplazar por workers distribuidos en producción para escalar horizontalmente.

---

## 🔍 Decisiones Técnicas Clave

### 🧠 1. SQL Directo en lugar de ORM
Decidí **no utilizar un ORM como SQLAlchemy** y optar por sentencias SQL explícitas, basándome en:

- ✅ **Simplicidad del modelo de datos** (películas, actores y relación N:M).
- ✅ **Mayor control sobre las operaciones** de escritura, validaciones y consultas analíticas.
- ✅ **Separación limpia por repositorios**, que permite desacoplar la lógica de persistencia y facilitar una futura migración a un ORM sin modificar los casos de uso.
- ✅ **Mejor rendimiento para scraping masivo**, al evitar capas adicionales de abstracción.

> Esta decisión no limita la escalabilidad futura, ya que el diseño permite incorporar ORM cuando sea necesario.

---

### 🌐 2. Scraping distribuido con rotación de IPs y red privada

Para garantizar robustez y anonimato en la extracción de datos, el scraper está configurado con:

- 🧅 **Red TOR** activa para rotación básica de IPs.
- 🔄 **User-Agent aleatorios y headers realistas** en cada solicitud.
- 🧰 **Proxies premium de Data Impulso**, integrados con fallback automático.
- 🔐 **VPN real instalada dentro de Docker**, conectada a la red interna.
- 💣 Tolerancia a fallos mediante reintentos automáticos y separación del canal de scraping y persistencia.

---

### 🗂️ 3. Persistencia híbrida (CSV + PostgreSQL)

Para garantizar versatilidad en el análisis y almacenamiento:

- 🧾 **CSV**: Exportación directa a `movies.csv`, `actors.csv` y `movie_actor.csv`, útil para revisión rápida o carga en herramientas externas.
- 🛢️ **PostgreSQL**: Almacenamiento estructurado de películas, actores y relaciones, ideal para análisis SQL avanzado y consultas cruzadas.
- 🧱 Cada mecanismo de persistencia se implementó como un repositorio independiente bajo el patrón Strategy, permitiendo su uso simultáneo o alternativo.

---

### 🧼 4. Arquitectura Limpia (Clean Architecture + DDD)

Todo el proyecto fue estructurado en capas bien definidas:

- `domain/`: Modelos de negocio y contratos de repositorios (interfaces).
- `application/`: Casos de uso desacoplados.
- `infrastructure/`: Implementaciones concretas (scraper, CSV, DB).
- `presentation/`: Punto de entrada (`run_scraper.py`).
- `shared/`: Configuración, logging y constantes.

> Esta estructura facilita pruebas unitarias, extensibilidad y mantenimiento a largo plazo.

---

### 🐋 5. Entorno Dockerizado con Red Privada Segura

El entorno de ejecución está totalmente containerizado y preparado para producción:

- `docker-compose.yml` levanta servicios clave:
  - Scraper
  - PostgreSQL
  - Red TOR
  - **VPN montada en la red interna**
- Se utilizaron:
  - ✅ **Redes internas de Docker**
  - ✅ **Volúmenes persistentes**
  - ✅ **Variables externas (.env)**
- Se integraron **healthchecks propios de cada imagen Docker** para garantizar estabilidad de los servicios antes de ejecutar el scraping.
---
## 📦 Entregables Finales

- 🗃️ Código en GitHub
- 🐘 Scripts SQL en `/sql/`
- 📄 CSVs generados en `/data/`
- 🧾 Logs con rotación IP en `/logs/`
- 📘 Documentación técnica (este archivo) y Documento de arquitectura `/docs/`

---

## 📣 Créditos

Proyecto desarrollado por **Andrés Ruiz** para la prueba técnica de Scraping Senior.  
📫 Email: franklindbruiz@gmail.com  
🔗 GitHub: [frankdevg](https://github.com/frankdevg)
