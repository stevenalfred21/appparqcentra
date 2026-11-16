# -*- coding: utf-8 -*-
"""Guiones de los 10 vídeos.

Cada escena tiene un tipo visual y una lista de "beats" (frases de la voz).
Los elementos de la escena (puntos, filas...) aparecen en pantalla cuando
empieza su beat: el elemento i aparece en el beat i + lead.

Datos comprobados el 16-nov-2026. Lo que no está confirmado por Rockstar
se dice así en el propio guion.
"""

CANAL = "NEÓN SEIS"

VIDEOS = []

def video(**kw):
    VIDEOS.append(kw)
    return kw

# ---------------------------------------------------------------- 01
video(
    slug="01-hora-de-salida",
    titulo="¿A qué hora sale GTA 6? Hora exacta en España, México, Argentina y más",
    miniatura=("¿A QUÉ HORA", "SALE?", "19 NOV"),
    descripcion=(
        "GTA 6 sale el jueves 19 de noviembre de 2026 en PS5 y Xbox Series X|S. "
        "Rockstar ha indicado que se desbloquea a medianoche, hora local de cada región. "
        "Aquí tienes qué significa eso en tu país y el matiz de los países con varios husos horarios."
    ),
    tags=["gta 6", "gta 6 hora", "a que hora sale gta 6", "gta 6 lanzamiento", "gta 6 19 noviembre", "gta vi"],
    escenas=[
        dict(tipo="title", kicker="LANZAMIENTO", title="¿A QUÉ HORA\nSALE GTA 6?", sub="Jueves 19 de noviembre · PS5 y Xbox Series X|S",
             beats=["¿A qué hora puedes jugar a GTA 6? Te lo digo en menos de tres minutos.",
                    "La fecha es el jueves diecinueve de noviembre de dos mil veintiséis, en PlayStation cinco y Xbox Series."]),
        dict(tipo="bignum", value="00:00", unit="HORA LOCAL", label="Medianoche en cada región",
             beats=["La regla es sencilla: según el artículo de soporte de Rockstar, el juego se desbloquea a medianoche, hora local, en cada región.",
                    "Es decir, no sale a la misma hora en todo el mundo. Va desbloqueándose país a país, según llega la medianoche."]),
        dict(tipo="times", heading="CUÁNDO SE DESBLOQUEA", rows=[
                ("Nueva Zelanda", "Primero del mundo"),
                ("España", "00:00 del jueves 19"),
                ("Argentina · Chile", "00:00 del jueves 19"),
                ("Colombia · Perú", "00:00 del jueves 19"),
                ("México", "00:00 del jueves 19*"),
                ("EE. UU.", "Ver aviso*")],
             lead=1,
             beats=["Este es el orden.",
                    "El primer sitio del planeta en jugar es Nueva Zelanda, porque es donde antes llega la medianoche.",
                    "En España, a las doce de la noche del miércoles al jueves.",
                    "En Argentina y Chile, igual: medianoche de su hora local.",
                    "Colombia y Perú, lo mismo.",
                    "En México, medianoche también, pero ojo con el asterisco, que ahora te lo explico.",
                    "Y en Estados Unidos hay un matiz importante."]),
        dict(tipo="warn", heading="EL MATIZ DE LOS HUSOS HORARIOS", text="Países con varias zonas horarias:\nla tienda puede usar UNA sola hora",
             beats=["En países con varias zonas horarias, como Estados Unidos, varios medios han visto que la tienda trata el país como una sola región, con la hora de la costa este.",
                    "Si eso se confirma, en la costa oeste se podría jugar desde las nueve de la noche del miércoles.",
                    "Pero Rockstar no lo ha confirmado. Así que si vives en un país con varios husos, mira la ficha de la tienda en tu consola: ahí aparece la cuenta atrás real."]),
        dict(tipo="bullets", heading="PARA JUGAR AL SEGUNDO", items=[
                "Precarga hecha (ya está abierta)",
                "Consola en modo reposo, no apagada",
                "Actualizaciones automáticas activadas",
                "Sesión iniciada en tu cuenta"],
             lead=1,
             beats=["Y para empezar justo a medianoche, cuatro cosas.",
                    "Ten la precarga hecha. Ya está disponible en las dos consolas.",
                    "Deja la consola en modo reposo, no apagada del todo, para que pueda descargar lo que falte.",
                    "Activa las actualizaciones automáticas, porque es muy probable que haya un parche de lanzamiento.",
                    "Y comprueba que tienes la sesión iniciada en la cuenta con la que compraste el juego."]),
        dict(tipo="cta", heading="Medianoche. Hora local.", sub="Suscríbete para la guía del día 1",
             beats=["Resumen: medianoche, hora local, el jueves diecinueve. Si te ha servido, suscríbete, que el día del lanzamiento subimos guías nuevas."]),
    ])

# ---------------------------------------------------------------- 02
video(
    slug="02-cuanto-pesa-precarga",
    titulo="¿Cuánto pesa GTA 6? Precarga, espacio necesario y cómo liberar sitio",
    miniatura=("¿CUÁNTO", "PESA?", "212 GB"),
    descripcion=(
        "La precarga de GTA 6 puede ocupar hasta 212 GB según la consola. "
        "Te explicamos cuándo abrió la precarga en PS5 y Xbox, cuánto espacio necesitas de verdad y cómo hacer sitio."
    ),
    tags=["gta 6", "gta 6 peso", "cuanto pesa gta 6", "gta 6 precarga", "gta 6 gb", "gta 6 ps5"],
    escenas=[
        dict(tipo="title", kicker="ANTES DE JUGAR", title="¿CUÁNTO\nPESA GTA 6?", sub="Precarga y espacio necesario",
             beats=["GTA 6 es enorme, y no solo el mapa. Vamos con cuánto ocupa y cómo dejar la consola lista."]),
        dict(tipo="bignum", value="212", unit="GB", label="Tamaño máximo de la precarga",
             beats=["La cifra que se ha publicado es de hasta doscientos doce gigas.",
                    "Ese dato es un máximo: el tamaño exacto cambia según la consola. Mira el número en tu propia tienda antes de borrar nada."]),
        dict(tipo="times", heading="CUÁNDO ABRIÓ LA PRECARGA", rows=[
                ("PS5", "10 nov · medianoche local"),
                ("Xbox Series X|S", "10 nov · 00:00 GMT"),
                ("Edición en caja", "Trae código: también precarga")],
             lead=1,
             beats=["La precarga ya está abierta.",
                    "En PlayStation cinco empezó el diez de noviembre, a medianoche de cada región.",
                    "En Xbox empezó a la vez en todo el mundo, a medianoche hora de Greenwich.",
                    "Y si compraste la caja física: no lleva disco, lleva un código de descarga. Canjéalo ya y precarga igual que en digital."]),
        dict(tipo="bullets", heading="CÓMO LIBERAR ESPACIO", items=[
                "Borra juegos que no tocas (se reinstalan)",
                "Revisa capturas y clips de vídeo",
                "Mueve juegos a un disco externo",
                "Deja margen extra para el parche"],
             lead=1,
             beats=["Si no te cabe, esto es lo que funciona.",
                    "Borra juegos que no tocas desde hace meses. Tus partidas guardadas no se pierden, y puedes volver a instalarlos cuando quieras.",
                    "Revisa la galería de capturas y clips: los vídeos ocupan muchísimo y casi nadie los borra.",
                    "Pasa juegos antiguos a un disco externo para liberar el interno.",
                    "Y no lo dejes justo: deja margen para el parche del día uno, que todavía no sabemos cuánto ocupará."]),
        dict(tipo="warn", heading="OJO", text="Comprueba el tamaño en TU tienda:\ncambia según la consola",
             beats=["Último consejo: no te fíes de capturas de otras personas. El dato bueno es el que aparece en la ficha del juego en tu consola."]),
        dict(tipo="cta", heading="Precarga hoy, juega el jueves", sub="Suscríbete para más guías de lanzamiento",
             beats=["Precarga hoy y el jueves solo tendrás que darle a jugar. Suscríbete si quieres más guías del lanzamiento."]),
    ])

# ---------------------------------------------------------------- 03
video(
    slug="03-standard-vs-ultimate",
    titulo="GTA 6 Standard vs Ultimate: ¿cuál comprar? Precio y contenido",
    miniatura=("STANDARD", "VS ULTIMATE", "¿CUÁL?"),
    descripcion=(
        "Comparamos las dos ediciones de GTA 6: Standard (79,99 €) y Ultimate (99,99 €, solo digital). "
        "Qué incluye cada una, la mejora posterior y los extras de reserva."
    ),
    tags=["gta 6", "gta 6 ultimate", "gta 6 precio", "gta 6 ediciones", "gta 6 standard", "gta 6 cual comprar"],
    escenas=[
        dict(tipo="title", kicker="GUÍA DE COMPRA", title="STANDARD\nVS ULTIMATE", sub="¿Merecen la pena los 20 € de diferencia?",
             beats=["Standard o Ultimate. Te cuento qué trae cada edición de GTA 6 para que no pagues de más."]),
        dict(tipo="compare", heading="LAS DOS EDICIONES", cols=[
                dict(name="STANDARD", price="79,99 €", items=["El juego completo", "Física (código) o digital", "Se puede mejorar después"]),
                dict(name="ULTIMATE", price="99,99 €", items=["El juego completo", "Solo digital", "Extras de contenido"])],
             lead=1,
             beats=["Hay dos ediciones.",
                    "La Standard cuesta setenta y nueve con noventa y nueve euros, o setenta y nueve con noventa y nueve dólares en Estados Unidos. Es el juego completo, y está en digital o en caja con código.",
                    "La Ultimate cuesta veinte más: noventa y nueve con noventa y nueve. Y es solo digital."]),
        dict(tipo="bullets", heading="QUÉ AÑADE LA ULTIMATE", items=[
                "Dos misiones exclusivas",
                "Coches clásicos y garaje",
                "Ropa, peinados y patrón de arma",
                "Tiendas y talleres extra"],
             lead=1,
             beats=["¿Qué te dan esos veinte euros? Según la tienda oficial de Rockstar:",
                    "Dos misiones exclusivas.",
                    "Una colección de coches clásicos, con un garaje.",
                    "Ropa, peinados y un patrón exclusivo para armas.",
                    "Y varias tiendas y talleres adicionales. Rockstar dice que todo esto se va desbloqueando a lo largo de la historia de Jason y Lucía, no de golpe."]),
        dict(tipo="bullets", heading="LO QUE CONVIENE SABER", items=[
                "Puedes pasar de Standard a Ultimate luego",
                "Reserva: Vintage Vice City Pack",
                "Digital: un mes de GTA+",
                "Confirma el precio en tu tienda"],
             lead=1,
             beats=["Y tres detalles importantes.",
                    "Si compras la Standard, más adelante puedes comprar la mejora a Ultimate. No te quedas atrapado.",
                    "Las compras antes del veinte de noviembre incluyen el Vintage Vice City Pack, según la página de la tienda.",
                    "Las compras digitales traen un mes de GTA plus.",
                    "Los precios cambian por país y por ofertas, así que confirma siempre en tu tienda."]),
        dict(tipo="verdict", heading="MI RECOMENDACIÓN", text="Duda = STANDARD.\nTe gusta el contenido extra = ULTIMATE.",
             beats=["Mi recomendación: si dudas, coge la Standard. Lo importante es el juego, y siempre puedes mejorar después.",
                    "Si sabes que vas a exprimirlo y te gustan los coches y la ropa extra, la Ultimate tiene sentido."]),
        dict(tipo="cta", heading="¿Standard o Ultimate?", sub="Dímelo en comentarios",
             beats=["¿Cuál has cogido tú? Déjalo en comentarios y suscríbete para más guías."]),
    ])

# ---------------------------------------------------------------- 04
video(
    slug="04-tiene-online",
    titulo="¿GTA 6 tiene online? Lo que se sabe del multijugador",
    miniatura=("¿TIENE", "ONLINE?", "DÍA 1"),
    descripcion=(
        "GTA 6 sale el 19 de noviembre como experiencia para un jugador. "
        "Rockstar no ha anunciado fecha para el multijugador. Esto es lo que hay confirmado y lo que solo son informes."
    ),
    tags=["gta 6", "gta 6 online", "gta 6 multijugador", "gta 6 online fecha", "gta online", "gta vi online"],
    escenas=[
        dict(tipo="title", kicker="MULTIJUGADOR", title="¿GTA 6\nTIENE ONLINE?", sub="Lo confirmado y lo que solo son informes",
             beats=["La pregunta que más se repite: ¿GTA 6 tiene online el día uno? Respuesta corta, y luego los detalles."]),
        dict(tipo="bignum", value="NO", unit="EL DÍA 1", label="Sale como experiencia para un jugador",
             beats=["No. Rockstar ha descrito el lanzamiento del diecinueve de noviembre como una experiencia para un jugador.",
                    "No hay modo online anunciado para ese día."]),
        dict(tipo="status", heading="ESTADO ACTUAL", rows=[
                ("Online el 19 de noviembre", "NO", "Lanzamiento para un jugador"),
                ("Fecha del multijugador", "?", "Sin anunciar"),
                ("Informes de 2027", "?", "Bloomberg · no oficial"),
                ("GTA Online actual", "SÍ", "Take-Two seguirá dándole soporte")],
             lead=1,
             beats=["Te lo resumo en cuatro puntos.",
                    "Online el día del lanzamiento: no.",
                    "Fecha oficial para el multijugador: no hay. Rockstar no ha dado fecha, ni nombre, ni ventana.",
                    "Hay informes, como los de Jason Schreier en Bloomberg, que apuntan a dos mil veintisiete. Pero no son oficiales; trátalo como lo que es, un informe.",
                    "Y el GTA Online que ya conoces sigue: Take-Two ha dicho que lo seguirá apoyando después del lanzamiento de GTA 6."]),
        dict(tipo="warn", heading="CUIDADO CON LOS BULOS", text="Si alguien te da una fecha del online,\npregunta de dónde la saca",
             beats=["Estos días vas a ver vídeos con fechas exactas del online. Ahora mismo, ninguna viene de Rockstar.",
                    "Cuando haya algo oficial, lo verás en la web de Rockstar, y aquí lo contaremos."]),
        dict(tipo="cta", heading="Te avisamos cuando haya fecha", sub="Activa la campanita",
             beats=["Si quieres enterarte en cuanto anuncien el online, suscríbete y activa la campanita."]),
    ])

# ---------------------------------------------------------------- 05
video(
    slug="05-gta6-pc",
    titulo="¿GTA 6 sale en PC? Lo que hay confirmado (y lo que no)",
    miniatura=("¿GTA 6", "EN PC?", "ESTADO REAL"),
    descripcion=(
        "GTA 6 sale el 19 de noviembre solo en PS5 y Xbox Series X|S. "
        "No hay versión de PC anunciada. Te contamos qué dicen Rockstar y Take-Two y qué esperar según la historia de la saga."
    ),
    tags=["gta 6", "gta 6 pc", "gta 6 pc fecha", "gta 6 steam", "gta 6 requisitos", "gta vi pc"],
    escenas=[
        dict(tipo="title", kicker="PLATAFORMAS", title="¿GTA 6\nEN PC?", sub="Lo confirmado y lo que no",
             beats=["¿Puedes jugar a GTA 6 en PC el jueves? Vamos con lo que hay de verdad."]),
        dict(tipo="status", heading="PLATAFORMAS EL 19 DE NOVIEMBRE", rows=[
                ("PlayStation 5", "SÍ", "Incluida PS5 Pro"),
                ("Xbox Series X|S", "SÍ", ""),
                ("PC", "NO", "Sin anunciar"),
                ("Requisitos de PC", "?", "No existen oficialmente")],
             lead=1,
             beats=["Plataformas del lanzamiento:",
                    "PlayStation cinco, sí.",
                    "Xbox Series X y S, sí.",
                    "PC: no. Ni Rockstar ni Take-Two han anunciado una versión para ordenador. En los documentos para inversores de Take-Two, GTA 6 aparece solo en PS5 y Xbox Series.",
                    "Y por eso mismo, cualquier lista de requisitos de PC que veas por ahí es inventada o especulación."]),
        dict(tipo="history", heading="LO QUE DICE LA HISTORIA", rows=[
                ("GTA IV", "Consolas 2008 → PC meses después"),
                ("GTA V", "Consolas 2013 → PC en 2015"),
                ("Red Dead 2", "Consolas 2018 → PC en 2019")],
             lead=1,
             beats=["¿Y qué podemos esperar? Aquí no hay datos, solo historia de Rockstar.",
                    "GTA cuatro salió en consolas y llegó a PC unos meses después.",
                    "GTA cinco salió en consolas en dos mil trece y en PC en dos mil quince.",
                    "Red Dead Redemption dos salió en consolas en dos mil dieciocho y en PC al año siguiente.",]),
        dict(tipo="warn", heading="CONCLUSIÓN HONESTA", text="Lo normal en Rockstar: PC más tarde.\nPero NO hay fecha ni anuncio.",
             beats=["Conclusión: el patrón de Rockstar es sacar la versión de PC más tarde. Pero eso es un patrón, no un anuncio.",
                    "Si solo juegas en PC, toca esperar. Y desconfía de cualquiera que te venda una fecha."]),
        dict(tipo="cta", heading="Te avisamos si hay versión PC", sub="Suscríbete",
             beats=["Si Rockstar anuncia la versión de PC, aquí lo tendrás. Suscríbete para no perdértelo."]),
    ])

# ---------------------------------------------------------------- 06
video(
    slug="06-esta-en-espanol",
    titulo="¿GTA 6 está en español? Doblaje, subtítulos y cómo cambiar el idioma",
    miniatura=("¿ESTÁ EN", "ESPAÑOL?", "IDIOMAS"),
    descripcion=(
        "GTA 6 llega con voces en inglés y textos y subtítulos en español (España y México), "
        "según las fichas de las tiendas. Te explicamos qué significa y cómo cambiar el idioma en tu consola."
    ),
    tags=["gta 6", "gta 6 español", "gta 6 doblaje", "gta 6 subtitulos", "gta 6 idioma", "gta 6 latino"],
    escenas=[
        dict(tipo="title", kicker="IDIOMAS", title="¿GTA 6 ESTÁ\nEN ESPAÑOL?", sub="Doblaje, subtítulos y cómo cambiarlo",
             beats=["¿GTA 6 está doblado al español? Respuesta rápida y luego cómo configurarlo."]),
        dict(tipo="status", heading="IDIOMAS", rows=[
                ("Voces en español", "NO", "Solo inglés"),
                ("Subtítulos España", "SÍ", "Según la ficha de la tienda"),
                ("Subtítulos México", "SÍ", "Según la ficha de la tienda"),
                ("Doblaje futuro", "?", "Nadie lo ha anunciado")],
             lead=1,
             beats=["Lo que dicen las fichas de las tiendas:",
                    "Voces en español: no. Las voces son solo en inglés, como en todos los GTA anteriores.",
                    "Textos y subtítulos en español de España: sí.",
                    "Y en español de México, también.",
                    "¿Habrá doblaje más adelante? Nadie lo ha anunciado, así que no cuentes con ello."]),
        dict(tipo="warn", heading="UN MATIZ", text="Dato de las fichas de tienda,\nno de un comunicado de Rockstar",
             beats=["Un matiz: esto sale de las fichas de idiomas de las tiendas, como la de Microsoft. Rockstar no ha hecho un comunicado específico. Lo normal es que coincida, pero dilo así si lo compartes."]),
        dict(tipo="bullets", heading="CÓMO ELEGIR EL IDIOMA", items=[
                "El juego suele seguir el idioma de la consola",
                "PS5: Ajustes › Sistema › Idioma",
                "Xbox: Configuración › Sistema › Idioma",
                "Dentro del juego: revisa el menú de opciones"],
             lead=1,
             beats=["¿Cómo te aseguras de tenerlo en español?",
                    "Normalmente el juego usa el idioma de tu consola.",
                    "En PS5, ve a Ajustes, Sistema, Idioma.",
                    "En Xbox, Configuración, Sistema, Idioma y ubicación.",
                    "Y una vez dentro, revisa el menú de opciones del juego, por si quieres ajustar el tamaño de los subtítulos."]),
        dict(tipo="cta", heading="Voces en inglés, textos en español", sub="Suscríbete para más guías",
             beats=["Resumen: voces en inglés, textos y subtítulos en español. Suscríbete si te ha servido."]),
    ])

# ---------------------------------------------------------------- 07
video(
    slug="07-fps-ps5-pro-xbox",
    titulo="GTA 6 a 60 FPS? PS5, PS5 Pro y Xbox Series: lo que se sabe",
    miniatura=("¿60 FPS?", "PS5 PRO", "LA VERDAD"),
    descripcion=(
        "¿Va GTA 6 a 60 fps en PS5 Pro? No hay ningún modo a 60 anunciado. "
        "Repasamos lo que han publicado los medios y el análisis de Digital Foundry. "
        "NOTA: revisar el día del lanzamiento, puede haber novedades."
    ),
    tags=["gta 6", "gta 6 60 fps", "gta 6 ps5 pro", "gta 6 fps", "gta 6 xbox series s", "gta 6 rendimiento"],
    escenas=[
        dict(tipo="title", kicker="RENDIMIENTO", title="¿GTA 6\nA 60 FPS?", sub="PS5 · PS5 Pro · Xbox Series",
             beats=["¿Va a ir GTA 6 a sesenta fotogramas por segundo? Sobre todo en PS5 Pro. Vamos a separar lo que se sabe de lo que se dice."]),
        dict(tipo="bignum", value="30", unit="FPS", label="Lo que apuntan los informes",
             beats=["Lo primero: no hay ningún modo a sesenta anunciado.",
                    "Varios medios informan de que Rockstar apunta a treinta fotogramas por segundo en consolas, incluida la PS5 Pro."]),
        dict(tipo="bullets", heading="POR QUÉ NO 60 (SEGÚN LOS ANALISTAS)", items=[
                "El límite es el procesador, no la gráfica",
                "La CPU de PS5 Pro apenas mejora a la de PS5",
                "Ciudades densas = más carga",
                "Opción realista: un modo a 40 fps"],
             lead=1,
             beats=["¿Por qué? Esto es lo que explica Digital Foundry, y ellos mismos dicen que son suposiciones.",
                    "El cuello de botella sería el procesador, no la tarjeta gráfica.",
                    "Y la PS5 Pro mejora mucho la gráfica, pero el procesador es apenas más rápido que el de la PS5 normal.",
                    "Una ciudad llena de gente, coches y tráfico carga sobre todo el procesador.",
                    "Por eso ven más realista un modo a cuarenta en pantallas de ciento veinte hercios que uno a sesenta."]),
        dict(tipo="warn", heading="SE SABRÁ EL JUEVES", text="Cuando salga, el dato real\nserá el de los análisis técnicos",
             beats=["Lo bueno: el jueves dejaremos de especular. En cuanto salga, habrá análisis técnicos con datos reales, y te los resumimos aquí."]),
        dict(tipo="cta", heading="¿30 fps te parece suficiente?", sub="Opina en comentarios",
             beats=["¿A ti te importan los treinta fotogramas, o mientras se vea así te da igual? Comenta y suscríbete."]),
    ])

# ---------------------------------------------------------------- 08
video(
    slug="08-mapa-leonida",
    titulo="El mapa de GTA 6: las 6 regiones de Leonida explicadas",
    miniatura=("EL MAPA", "DE LEONIDA", "6 REGIONES"),
    descripcion=(
        "Rockstar ha presentado seis regiones del estado de Leonida, su versión de Florida: "
        "Vice City, Leonida Keys, Grassrivers, Port Gellhorn, Ambrosia y Mount Kalaga. "
        "Esquema orientativo, no es el mapa oficial."
    ),
    tags=["gta 6", "gta 6 mapa", "leonida", "vice city", "gta 6 regiones", "gta 6 map"],
    escenas=[
        dict(tipo="title", kicker="EL MUNDO", title="EL MAPA\nDE LEONIDA", sub="Las 6 regiones presentadas por Rockstar",
             beats=["GTA 6 vuelve a Vice City, pero el mapa es mucho más que una ciudad. Te presento Leonida en seis regiones."]),
        dict(tipo="bignum", value="LEONIDA", unit="", label="La versión de Florida de Rockstar",
             beats=["Leonida es el estado ficticio del juego, la versión de Florida de Rockstar. Y Vice City es su Miami."]),
        dict(tipo="regions", heading="LAS 6 REGIONES", regions=[
                ("VICE CITY", "Playas, neón y vida nocturna"),
                ("LEONIDA KEYS", "Cadena de islas"),
                ("GRASSRIVERS", "Pantanos y naturaleza salvaje"),
                ("PORT GELLHORN", "Costa venida a menos"),
                ("AMBROSIA", "Interior industrial y rural"),
                ("MOUNT KALAGA", "Parque nacional")],
             lead=1,
             beats=["Estas son las seis regiones que ha enseñado Rockstar.",
                    "Vice City: la gran ciudad, con sus playas, su vida nocturna y el neón de siempre.",
                    "Leonida Keys: una cadena de islas, inspirada en los cayos de Florida.",
                    "Grassrivers: pantanos y naturaleza salvaje, la versión de los Everglades.",
                    "Port Gellhorn: una zona de costa con aire de lugar venido a menos.",
                    "Ambrosia: el interior más industrial y rural.",
                    "Y Mount Kalaga: un parque nacional con bosques y montaña."]),
        dict(tipo="warn", heading="IMPORTANTE", text="Esquema orientativo.\nRockstar no ha publicado el mapa oficial completo.",
             beats=["Un aviso: el esquema que ves es orientativo. Rockstar no ha publicado un mapa oficial completo, y muchos mapas que circulan mezclan datos oficiales con filtraciones.",
                    "El jueves por fin veremos el mapa real dentro del juego."]),
        dict(tipo="cta", heading="¿Qué región quieres explorar primero?", sub="Comenta y suscríbete",
             beats=["¿Por dónde vas a empezar a explorar? Comenta y suscríbete, que en cuanto salga hacemos la guía del mapa de verdad."]),
    ])

# ---------------------------------------------------------------- 09
video(
    slug="09-jason-y-lucia",
    titulo="Jason y Lucía: quiénes son los protagonistas de GTA 6",
    miniatura=("JASON", "& LUCÍA", "¿QUIÉNES SON?"),
    descripcion=(
        "Todo lo que Rockstar ha contado de Jason Duval y Lucía Caminos, los dos protagonistas de GTA 6, "
        "y de los personajes que les rodean. Sin spoilers ni filtraciones."
    ),
    tags=["gta 6", "gta 6 lucia", "gta 6 jason", "gta 6 personajes", "gta 6 historia", "gta 6 protagonistas"],
    escenas=[
        dict(tipo="title", kicker="LA HISTORIA", title="JASON\n& LUCÍA", sub="Los protagonistas · sin spoilers",
             beats=["Por primera vez en un GTA en tres dimensiones hay una pareja protagonista. Esto es lo que Rockstar ha contado de ellos. Sin filtraciones y sin spoilers."]),
        dict(tipo="profile", heading="LUCÍA CAMINOS", items=[
                "Su padre le enseñó a pelear",
                "Ha pasado por la cárcel en Leonida",
                "Quiere una vida mejor, cueste lo que cueste"],
             lead=1,
             beats=["Lucía Caminos.",
                    "Según Rockstar, su padre le enseñó a pelear desde pequeña.",
                    "La conocimos en el primer tráiler en la prisión de Leonida.",
                    "Y su objetivo es salir adelante y conseguir una vida mejor, cueste lo que cueste."]),
        dict(tipo="profile", heading="JASON DUVAL", items=[
                "Creció rodeado de estafadores",
                "Pasó por el ejército",
                "Trabaja en los cayos para gente peligrosa"],
             lead=1,
             beats=["Jason Duval.",
                    "Creció rodeado de timadores y gente de poco fiar.",
                    "Pasó por el ejército, buscando dejar ese mundo atrás.",
                    "Y ahora vive en los cayos de Leonida, haciendo trabajos para gente peligrosa, mientras intenta encontrar una salida."]),
        dict(tipo="bullets", heading="OTROS PERSONAJES PRESENTADOS", items=[
                "Cal Hampton",
                "Boobie Ike",
                "Dre'Quan Priest",
                "Real Dimez",
                "Raul Bautista",
                "Brian Heder"],
             lead=1,
             beats=["Rockstar también ha presentado a los personajes que los rodean.",
                    "Cal Hampton, amigo de Jason.",
                    "Boobie Ike, un tipo con negocios en Vice City.",
                    "Dre'Quan Priest, que quiere triunfar en la música.",
                    "Real Dimez, un dúo de raperas.",
                    "Raul Bautista, un atracador con experiencia.",
                    "Y Brian Heder, para quien trabaja Jason en los cayos."]),
        dict(tipo="warn", heading="SIN SPOILERS", text="Solo lo que Rockstar ha publicado.\nEl resto, el jueves.",
             beats=["Y hasta aquí. Todo lo demás lo descubriremos jugando. Si buscas filtraciones, este no es tu canal."]),
        dict(tipo="cta", heading="¿Jason o Lucía?", sub="Comenta y suscríbete",
             beats=["¿Con quién crees que vas a conectar más, con Jason o con Lucía? Comenta y suscríbete."]),
    ])

# ---------------------------------------------------------------- 10
video(
    slug="10-todo-lo-que-necesitas-saber",
    titulo="GTA 6: TODO lo que necesitas saber antes de jugar (resumen del lanzamiento)",
    miniatura=("TODO LO QUE", "DEBES SABER", "ANTES DE JUGAR"),
    descripcion=(
        "El resumen definitivo del lanzamiento de GTA 6: fecha y hora, plataformas, precio, ediciones, "
        "tamaño, idioma, online y mapa. Todo en un vídeo, solo con datos confirmados."
    ),
    tags=["gta 6", "gta 6 todo lo que sabemos", "gta 6 lanzamiento", "gta 6 guia", "gta 6 resumen", "gta vi"],
    escenas=[
        dict(tipo="title", kicker="RESUMEN", title="TODO LO QUE\nDEBES SABER", sub="GTA 6 · antes de jugar",
             beats=["Todo lo que necesitas saber de GTA 6 antes de jugar, en un solo vídeo. Solo datos confirmados."]),
        dict(tipo="status", heading="LO BÁSICO", rows=[
                ("Fecha", "SÍ", "Jueves 19 de noviembre de 2026"),
                ("Hora", "SÍ", "Medianoche, hora local"),
                ("Plataformas", "SÍ", "PS5 y Xbox Series X|S"),
                ("PC", "NO", "Sin anunciar")],
             lead=1,
             beats=["Lo básico.",
                    "Sale el jueves diecinueve de noviembre de dos mil veintiséis.",
                    "Se desbloquea a medianoche, hora local de cada región.",
                    "En PlayStation cinco y Xbox Series X y S.",
                    "En PC no hay versión anunciada."]),
        dict(tipo="status", heading="COMPRA E INSTALACIÓN", rows=[
                ("Standard", "SÍ", "79,99 € / 79,99 $"),
                ("Ultimate", "SÍ", "99,99 € · solo digital"),
                ("Precarga", "SÍ", "Abierta desde el 10 de noviembre"),
                ("Tamaño", "SÍ", "Hasta 212 GB según consola")],
             lead=1,
             beats=["Compra e instalación.",
                    "La edición Standard cuesta setenta y nueve con noventa y nueve.",
                    "La Ultimate, noventa y nueve con noventa y nueve, y es solo digital.",
                    "La precarga está abierta desde el diez de noviembre.",
                    "Y ocupa hasta doscientos doce gigas, según la consola."]),
        dict(tipo="status", heading="EL JUEGO", rows=[
                ("Online", "NO", "Lanzamiento para un jugador"),
                ("Voces en español", "NO", "Inglés + subtítulos ES/MX"),
                ("Mapa", "SÍ", "Leonida · 6 regiones"),
                ("Protagonistas", "SÍ", "Jason Duval y Lucía Caminos")],
             lead=1,
             beats=["Y el juego.",
                    "No hay online el día uno. Sale como experiencia para un jugador.",
                    "Voces en inglés, con textos y subtítulos en español de España y de México.",
                    "El mapa es Leonida, con seis regiones, Vice City incluida.",
                    "Y los protagonistas son Jason Duval y Lucía Caminos."]),
        dict(tipo="cta", heading="Nos vemos en Leonida", sub="Suscríbete · guías desde el día 1",
             beats=["Eso es todo. Nos vemos en Leonida el jueves. Suscríbete, que a partir del lanzamiento subimos guías con el juego en la mano."]),
    ])
