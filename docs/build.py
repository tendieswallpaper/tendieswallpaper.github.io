#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for tendieswallpaper.github.io
Generates the English landing page + 9 localized versions (TOP-10 global languages),
each with Google Analytics (GA4) + Microsoft Clarity tracking, Tailwind CSS (Play CDN)
styling, hreflang alternates and localized JSON-LD.

Usage:  python3 docs/build.py
Output: docs/  (index.html + <code>/index.html + robots.txt + sitemap.xml + .nojekyll)
"""

import os
import json

BASE_URL = "https://tendieswallpaper.github.io"

# ---------------------------------------------------------------------------
# Locales (TOP-10 world languages by popularity / number of speakers)
# ---------------------------------------------------------------------------
LOCALES = [
    {"code": "en",   "path": "/",       "hreflang": "en",   "html_lang": "en",   "dir": "ltr", "og_locale": "en_US", "native": "English"},
    {"code": "zh",   "path": "/zh-CN/", "hreflang": "zh-CN", "html_lang": "zh-CN", "dir": "ltr", "og_locale": "zh_CN", "native": "\u7b80\u4f53\u4e2d\u6587"},
    {"code": "es",   "path": "/es/",    "hreflang": "es",   "html_lang": "es",   "dir": "ltr", "og_locale": "es_ES", "native": "Espa\u00f1ol"},
    {"code": "hi",   "path": "/hi/",    "hreflang": "hi",   "html_lang": "hi",   "dir": "ltr", "og_locale": "hi_IN", "native": "\u0939\u093f\u0928\u094d\u0926\u0940"},
    {"code": "fr",   "path": "/fr/",    "hreflang": "fr",   "html_lang": "fr",   "dir": "ltr", "og_locale": "fr_FR", "native": "Fran\u00e7ais"},
    {"code": "ar",   "path": "/ar/",    "hreflang": "ar",   "html_lang": "ar",   "dir": "rtl", "og_locale": "ar_SA", "native": "\u0627\u0644\u0639\u0631\u0628\u064a\u0629"},
    {"code": "pt",   "path": "/pt-BR/", "hreflang": "pt-BR", "html_lang": "pt-BR", "dir": "ltr", "og_locale": "pt_BR", "native": "Portugu\u00eas"},
    {"code": "ru",   "path": "/ru/",    "hreflang": "ru",   "html_lang": "ru",   "dir": "ltr", "og_locale": "ru_RU", "native": "\u0420\u0443\u0441\u0441\u043a\u0438\u0439"},
    {"code": "ja",   "path": "/ja/",    "hreflang": "ja",   "html_lang": "ja",   "dir": "ltr", "og_locale": "ja_JP", "native": "\u65e5\u672c\u8a9e"},
    {"code": "de",   "path": "/de/",    "hreflang": "de",   "html_lang": "de",   "dir": "ltr", "og_locale": "de_DE", "native": "Deutsch"},
]

TRACKING = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RB3B62DPGK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-RB3B62DPGK');
</script>

<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "y3n4py6860");
</script>
"""

# ---------------------------------------------------------------------------
# English source strings (keys used across all languages)
# ---------------------------------------------------------------------------
EN = {
    # nav
    "nav_wiki": "What is it",
    "nav_tendies": ".tendies file",
    "nav_install": "Install",
    "nav_gallery": "Gallery",
    "nav_faq": "FAQ",
    "nav_cta": "Browse Wallpapers",
    "lang_label": "Language",

    # hero
    "hero_kicker": "The official home of Tendies Wallpaper",
    "hero_h1_lead": "Dynamic iOS wallpapers for",
    "hero_h1_after": "Your lock screen, alive.",
    "hero_lead": "Tendies Wallpaper is a curated collection of animated, dynamic wallpapers for iPhone and iPad, installed through the open-source Nugget tool with a simple .tendies file. No jailbreak, no compromise. Supported on iOS and iPadOS 17&ndash;27.",
    "hero_btn1": "Explore the Wallpaper Library",
    "hero_btn2": "How to install",
    "hero_btn3": "Read the tutorial",
    "stat1a": "iOS 17&ndash;27",
    "stat1b": "Full version support",
    "stat2a": "No jailbreak",
    "stat2b": "Uses SparseRestore / BookRestore",
    "stat3a": "100% free",
    "stat3b": "Open-source &amp; community driven",

    # about
    "about_tag": "What is Tendies Wallpaper?",
    "about_h2": "Animated wallpapers for iPhone and iPad, done right",
    "about_p": "Tendies Wallpaper is the brand behind a growing library of dynamic lock-screen wallpapers built for the Nugget ecosystem. Every wallpaper is packaged as a <strong>.tendies file</strong> &mdash; a PosterBoard wallpaper bundle that turns Apple's native lock screen into a living, breathing canvas. The full collection is hosted at <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "Truly dynamic",
    "c1d": "Motion, depth and animation on the native lock screen, not a static image. Each tendies wallpaper is crafted to feel like a premium live screen.",
    "c2t": "No jailbreak",
    "c2d": "Tendies wallpapers are applied with Nugget, which uses Apple's own SparseRestore and BookRestore restore mechanisms to write files safely.",
    "c3t": "Curated library",
    "c3d": "Anime, manga, sports, Marvel, space dreamscapes and more, a hand-picked gallery updated weekly on the Nugget Wallpaper site.",
    "c4t": "Powered by Nugget",
    "c4d": "Built on the open-source <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget tool</a> by leminlimez, trusted by a community of thousands of users.",
    "c5t": "iPhone &amp; iPad",
    "c5d": "Works across compatible iPhones and iPads running iOS and iPadOS 17 through 27, Dynamic Island or not.",
    "c6t": "Reversible &amp; safe",
    "c6d": "Everything is reversible. Back up before applying; restore through iTunes or Finder anytime to return to stock.",

    # tendies (technical terms kept in English everywhere)
    "tendies_tag": "The .tendies file",
    "tendies_h2": "What is a tendies file?",
    "tendies_p": "A <strong>.tendies file</strong> is the wallpaper bundle format used across the Nugget / PosterBoard ecosystem (including Cowabunga and Pocket Poster). It stores the exact PosterBoard file structure that Nugget restores onto your device, so the wallpaper shows up right inside the native lock-screen wallpaper picker.",
    "tv1_t": "Container format",
    "tv1_d": "Restores directly to the PosterBoard app container, keeping the exact file structure and wallpaper IDs untouched.",
    "tv2_t": "Descriptor format",
    "tv2_d": "Restores to the wallpaper descriptors folder with randomized UUIDs so multiple tendies wallpapers never conflict.",
    "tv3_t": "Extra variants",
    "tv3_d": "Video and photo variants target Suggested Photos; mercury variants target the Mercury Poster on supported iOS versions.",

    # install
    "install_tag": "Getting started",
    "install_h2": "Install a tendies wallpaper in 4 steps",
    "install_p": "The entire process takes a few minutes with a USB cable and the free Nugget app. Full details are in the official tutorial.",
    "s1_t": "Download the file",
    "s1_d": "Pick a wallpaper from the library and download its <strong>.tendies</strong> file.",
    "s2_t": "Connect your device",
    "s2_d": "Plug your iPhone/iPad into your computer via USB and trust it. Works on Windows, macOS and Linux.",
    "s3_t": "Import &amp; apply",
    "s3_d": "Open PosterBoard inside Nugget, select the file, then hit Apply Changes.",
    "s4_t": "Reboot &amp; enjoy",
    "s4_d": "After reboot, open the lock-screen editor and find your new wallpaper under Collections or Favorites.",
    "install_note": "Facing an issue? Read the official <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper tutorial</a> or join the community channels below.",

    # gallery
    "gallery_tag": "The library",
    "gallery_h2": "Browse the Tendies Wallpaper gallery",
    "gallery_p": "Every tendies wallpaper below is hosted and downloadable on <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Sort the gallery by <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">Latest</a> or <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">Hot</a> to see what's trending.",
    "g_t1": "Anime",
    "g_d1": "Evangelion, Sylphiette &amp; more",
    "g_t2": "Sports &amp; Marvel",
    "g_d2": "Clubs, heroes, brand-new days",
    "g_t3": "Dreamscapes",
    "g_d3": "Planets, stars &amp; abstracts",
    "g_t4": "Official",
    "g_d4": "Apple-style poster picks",
    "gallery_cta": "View All Wallpapers",

    # faq
    "faq_tag": "FAQ",
    "faq_h2": "Frequently asked questions",
    "faq_p": "Everything you need to know about tendies wallpapers before you get started.",
    "f1q": "What is a tendies wallpaper?",
    "f1a": "A tendies wallpaper is a dynamic, animated wallpaper for iPhone and iPad, shipped as a .tendies file that is installed through the Nugget tool. Tendies files restore PosterBoard wallpaper descriptors onto iOS 17-27 devices so the wallpaper appears in the lock-screen Collections picker.",
    "f2q": "What is a .tendies file?",
    "f2a": "A .tendies file is the wallpaper bundle format used by Nugget and Pocket Poster. It stores the PosterBoard file structure that gets restored to your iPhone or iPad, and it is what you import when you want to install a custom dynamic lock-screen wallpaper.",
    "f3q": "Do tendies wallpapers require a jailbreak?",
    "f3a": "No. Tendies wallpapers are applied with the open-source Nugget tool, which uses Apple's own SparseRestore and BookRestore mechanisms to modify files safely, no jailbreak is required.",
    "f4q": "Which iOS versions support tendies wallpapers?",
    "f4a": "Tendies wallpapers support iOS and iPadOS 17 through 27 on compatible iPhones and iPads. Some wallpapers may require a specific iOS version, so always check the wallpaper page for compatibility notes.",
    "f5q": "Where can I download tendies wallpapers?",
    "f5a": "Browse and download tendies wallpapers from the Nugget Wallpaper library at mwallx.com, which hosts a curated collection of dynamic and static wallpapers including anime, sports, Marvel and more.",
    "f6q": "How do I install a tendies wallpaper on my iPhone?",
    "f6a": "Download the .tendies file, open the PosterBoard feature inside Nugget, select the file, apply changes, and reboot your device. After rebooting, open the lock-screen wallpaper editor and find the new wallpaper under Collections or Favorites.",
    "f7q": "Is using tendies wallpapers safe?",
    "f7a": "Nugget is a widely used open-source project with thousands of users. As with any system modification, back up your device first. Changes are reversible by restoring your device through iTunes or Finder.",
    "f8q": "What is the difference between Nugget Wallpaper and tendies wallpaper?",
    "f8a": "Tendies Wallpaper is the brand name for the collection of dynamic wallpapers, while Nugget Wallpaper (mwallx.com) is the library that hosts them. Both are part of the same ecosystem, powered by the open-source Nugget tool for iOS customization.",

    # community
    "comm_tag": "Community",
    "comm_h2": "Join the Nugget Wallpaper community",
    "comm_p": "Follow the channels for new wallpaper drops, previews and quick install tips.",
    "comm_tt": "TikTok",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg": "Telegram",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x": "X (Twitter)",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh": "Nugget GitHub",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host": "Nugget Host",
    "comm_host_d": "Official iOS tool site",

    # cta
    "cta_h2": "Ready to bring your lock screen to life?",
    "cta_p": "Download a free tendies wallpaper today, no jailbreak required. Browse the full library, check prices, track orders and follow the step-by-step tutorial on the Nugget Wallpaper site.",
    "cta_btn1": "Start Exploring",
    "cta_btn2": "See Pricing",

    # footer
    "foot_tw": "Tendies Wallpaper",
    "foot_tw1": "Home",
    "foot_tw2": "What is it",
    "foot_tw3": "The .tendies file",
    "foot_tw4": "Install guide",
    "foot_tw5": "FAQ",
    "foot_nw": "Nugget Wallpaper",
    "foot_nw1": "Browse all wallpapers",
    "foot_nw2": "Latest additions",
    "foot_nw3": "Hot right now",
    "foot_nw4": "Import tutorial",
    "foot_pr": "Project",
    "foot_pr1": "Nugget on GitHub",
    "foot_pr2": "Official Nugget tool",
    "foot_pr3": "Pricing",
    "foot_pr4": "Orders",
    "foot_pol": "Official Policies (mwallx.com)",
    "foot_pol1": "Privacy Policy",
    "foot_pol2": "Terms of Service",
    "foot_pol3": "DMCA Policy",
    "foot_pol4": "UGC Policy",
    "copyright": "Tendies Wallpaper is an introduction and referral page for the curated wallpaper library hosted at <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Nugget wallpapers are applied via the open-source Nugget tool (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple, iPhone, iPad and iOS are trademarks of Apple Inc. This site is not affiliated with Apple.",

    # meta
    "title": "Tendies Wallpaper &mdash; iOS Dynamic Wallpapers for Nugget",
    "desc": "Tendies Wallpaper is the home of dynamic iOS &amp; iPadOS wallpapers for Nugget. Learn what a .tendies file is, how to install animated lock-screen wallpapers without a jailbreak, and browse the full library at Nugget Wallpaper.",
    "kw": "tendies wallpaper, tendies file, Nugget wallpaper, dynamic wallpaper iOS, PosterBoard wallpaper, ios 18 wallpaper, ios 27 wallpaper, animated lock screen wallpaper",
}

# ---------------------------------------------------------------------------
# Translations (missing keys fall back to English)
# ---------------------------------------------------------------------------
T = {"en": EN}

T["es"] = {
    "nav_wiki": "Qu\u00e9 es",
    "nav_install": "Instalar",
    "nav_gallery": "Galer\u00eda",
    "nav_faq": "Preguntas",
    "nav_cta": "Ver Wallpapers",
    "lang_label": "Idioma",
    "hero_kicker": "El hogar oficial de Tendies Wallpaper",
    "hero_h1_lead": "Fondos din\u00e1micos iOS para",
    "hero_h1_after": "Tu pantalla de bloqueo, en movimiento.",
    "hero_lead": "Tendies Wallpaper es una colecci\u00f3n curada de fondos animados y din\u00e1micos para iPhone y iPad instalados mediante la herramienta de c\u00f3digo abierto Nugget con un sencillo archivo .tendies. Sin jailbreak y sin concesiones. Compatible con iOS y iPadOS 17&ndash;27.",
    "hero_btn1": "Explorar la biblioteca",
    "hero_btn2": "C\u00f3mo instalar",
    "hero_btn3": "Leer el tutorial",
    "stat1b": "Soporte completo de versiones",
    "stat2b": "Usa SparseRestore / BookRestore",
    "stat3b": "C\u00f3digo abierto y comunidad",
    "about_tag": "\u00bfQu\u00e9 es Tendies Wallpaper?",
    "about_h2": "Fondos animados para iPhone y iPad, bien hechos",
    "about_p": "Tendies Wallpaper es la marca detr\u00e1s de una biblioteca creciente de fondos din\u00e1micos para la pantalla de bloqueo creados para el ecosistema Nugget. Cada fondo se empaqueta como un <strong>archivo .tendies</strong> &mdash; un paquete de fondos de PosterBoard que convierte la pantalla de bloqueo nativa de Apple en un lienzo vivo. La colecci\u00f3n completa se aloja en <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "Realmente din\u00e1micos",
    "c1d": "Movimiento, profundidad y animaci\u00f3n en la pantalla de bloqueo nativa, no una imagen est\u00e1tica. Cada fondo tendies est\u00e1 dise\u00f1ado para sentirse como una pantalla en vivo premium.",
    "c2t": "Sin jailbreak",
    "c2d": "Los fondos tendies se aplican con Nugget, que usa los mecanismos SparseRestore y BookRestore de Apple para escribir archivos de forma segura.",
    "c3t": "Biblioteca curada",
    "c3d": "Anime, manga, deportes, Marvel, paisajes espaciales y m\u00e1s: una galer\u00eda seleccionada que se actualiza cada semana en el sitio de Nugget Wallpaper.",
    "c4t": "Impulsado por Nugget",
    "c4d": "Construido sobre la herramienta de c\u00f3digo abierto <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> de leminlimez, confiada por una comunidad de miles de usuarios.",
    "c5t": "iPhone y iPad",
    "c5d": "Funciona en iPhones e iPads compatibles con iOS y iPadOS 17 a 27, con o sin Dynamic Island.",
    "c6t": "Reversible y seguro",
    "c6d": "Todo es reversible. Haz una copia de seguridad antes de aplicar; restaura mediante iTunes o Finder en cualquier momento.",
    "tendies_h2": "\u00bfQu\u00e9 es un archivo tendies?",
    "tendies_p": "Un <strong>archivo .tendies</strong> es el formato de paquete de fondos usado en el ecosistema Nugget / PosterBoard (incluidos Cowabunga y Pocket Poster). Guarda la estructura exacta de archivos de PosterBoard que Nugget restaura en tu dispositivo, para que el fondo aparezca dentro del selector nativo de fondos de la pantalla de bloqueo.",
    "tv1_d": "Restaura directamente al contenedor de la app PosterBoard, manteniendo intactos la estructura de archivos y los ID de los fondos.",
    "tv2_d": "Restaura a la carpeta de descriptores con UUID aleatorios para que varios fondos tendies no entren en conflicto.",
    "tv3_d": "Las variantes de v\u00eddeo y foto apuntan a Suggested Photos; las variantes mercury apuntan al Mercury Poster en versiones de iOS compatibles.",
    "install_tag": "Primeros pasos",
    "install_h2": "Instala un fondo tendies en 4 pasos",
    "install_p": "Todo el proceso toma unos minutos con un cable USB y la app gratuita Nugget. Los detalles completos est\u00e1n en el tutorial oficial.",
    "s1_t": "Descarga el archivo",
    "s1_d": "Elige un fondo de la biblioteca y descarga su <strong>archivo .tendies</strong>.",
    "s2_t": "Conecta tu dispositivo",
    "s2_d": "Conecta tu iPhone/iPad al ordenador por USB y conf\u00edalo. Funciona en Windows, macOS y Linux.",
    "s3_t": "Importa y aplica",
    "s3_d": "Abre PosterBoard dentro de Nugget, selecciona el archivo y pulsa Apply Changes.",
    "s4_t": "Reinicia y disfruta",
    "s4_d": "Tras reiniciar, abre el editor de la pantalla de bloqueo y encuentra tu nuevo fondo en Colecciones o Favoritos.",
    "install_note": "\u00bfTienes alg\u00fan problema? Lee el <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">tutorial oficial de Nugget Wallpaper</a> o \u00fanete a los canales de la comunidad.",
    "gallery_tag": "La biblioteca",
    "gallery_h2": "Explora la galer\u00eda de Tendies Wallpaper",
    "gallery_p": "Cada fondo tendies de abajo se aloja y descarga en <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Ordena la galer\u00eda por <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">Novedades</a> o <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">Populares</a> para ver las tendencias.",
    "g_t1": "Anime",
    "g_d1": "Evangelion, Sylphiette y m\u00e1s",
    "g_t2": "Deportes y Marvel",
    "g_d2": "Clubes, h\u00e9roes y nuevos d\u00edas",
    "g_t3": "Paisajes on\u00edricos",
    "g_d3": "Planetas, estrellas y abstractos",
    "g_t4": "Oficial",
    "g_d4": "Selecciones estilo Apple",
    "gallery_cta": "Ver todos los fondos",
    "faq_h2": "Preguntas frecuentes",
    "faq_p": "Todo lo que necesitas saber sobre los fondos tendies antes de empezar.",
    "f1q": "\u00bfQu\u00e9 es un fondo tendies?",
    "f1a": "Un fondo tendies es un fondo animado y din\u00e1mico para iPhone y iPad distribuido como archivo .tendies que se instala con la herramienta Nugget. Los archivos tendies restauran descriptores de fondos de PosterBoard en dispositivos iOS 17-27 para que el fondo aparezca en el selector de Colecciones de la pantalla de bloqueo.",
    "f2q": "\u00bfQu\u00e9 es un archivo .tendies?",
    "f2a": "Un archivo .tendies es el formato de paquete de fondos usado por Nugget y Pocket Poster. Guarda la estructura de archivos de PosterBoard que se restaura en tu iPhone o iPad, y es lo que importas para instalar un fondo din\u00e1mico personalizado en la pantalla de bloqueo.",
    "f3q": "\u00bfLos fondos tendies requieren jailbreak?",
    "f3a": "No. Los fondos tendies se aplican con la herramienta de c\u00f3digo abierto Nugget, que usa los mecanismos SparseRestore y BookRestore de Apple para modificar archivos de forma segura, sin necesidad de jailbreak.",
    "f4q": "\u00bfQu\u00e9 versiones de iOS admiten fondos tendies?",
    "f4a": "Los fondos tendies admiten iOS y iPadOS 17 a 27 en iPhones e iPads compatibles. Algunos fondos pueden requerir una versi\u00f3n espec\u00edfica de iOS; revisa siempre las notas de compatibilidad en la p\u00e1gina del fondo.",
    "f5q": "\u00bfD\u00f3nde puedo descargar fondos tendies?",
    "f5a": "Explora y descarga fondos tendies en la biblioteca de Nugget Wallpaper, en mwallx.com, que aloja una colecci\u00f3n curada de fondos din\u00e1micos y est\u00e1ticos, incluidos anime, deportes, Marvel y m\u00e1s.",
    "f6q": "\u00bfC\u00f3mo instalo un fondo tendies en mi iPhone?",
    "f6a": "Descarga el archivo .tendies, abre la funci\u00f3n PosterBoard dentro de Nugget, selecciona el archivo, aplica los cambios y reinicia el dispositivo. Tras reiniciar, abre el editor de la pantalla de bloqueo y encuentra el fondo en Colecciones o Favoritos.",
    "f7q": "\u00bfEs seguro usar fondos tendies?",
    "f7a": "Nugget es un proyecto de c\u00f3digo abierto muy usado con miles de usuarios. Como con cualquier modificaci\u00f3n del sistema, haz una copia de seguridad primero. Los cambios son reversibles restaurando el dispositivo con iTunes o Finder.",
    "f8q": "\u00bfQu\u00e9 diferencia hay entre Nugget Wallpaper y los fondos tendies?",
    "f8a": "Tendies Wallpaper es el nombre de la marca de la colecci\u00f3n de fondos din\u00e1micos, mientras que Nugget Wallpaper (mwallx.com) es la biblioteca que los aloja. Ambos forman parte del mismo ecosistema, impulsado por la herramienta de c\u00f3digo abierto Nugget para personalizar iOS.",
    "comm_h2": "\u00danete a la comunidad de Nugget Wallpaper",
    "comm_p": "Sigue los canales para ver novedades, avances y consejos de instalaci\u00f3n.",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_host_d": "Sitio oficial de la herramienta iOS",
    "cta_h2": "\u00bfListo para dar vida a tu pantalla de bloqueo?",
    "cta_p": "Descarga hoy un fondo tendies gratuito sin necesidad de jailbreak. Explora la biblioteca completa, consulta precios, sigue tus pedidos y lee el tutorial paso a paso en el sitio de Nugget Wallpaper.",
    "cta_btn1": "Empezar a explorar",
    "cta_btn2": "Ver precios",
    "foot_tw1": "Inicio",
    "foot_tw2": "Qu\u00e9 es",
    "foot_tw3": "El archivo .tendies",
    "foot_tw4": "Gu\u00eda de instalaci\u00f3n",
    "foot_nw1": "Ver todos los fondos",
    "foot_nw2": "\u00daltimos a\u00f1adidos",
    "foot_nw3": "Populares ahora",
    "foot_nw4": "Tutorial de importaci\u00f3n",
    "foot_pr1": "Nugget en GitHub",
    "foot_pr3": "Precios",
    "foot_pr4": "Pedidos",
    "foot_pol1": "Pol\u00edtica de privacidad",
    "foot_pol2": "T\u00e9rminos del servicio",
    "foot_pol3": "Pol\u00edtica DMCA",
    "foot_pol4": "Pol\u00edtica de contenido UGC",
    "copyright": "Tendies Wallpaper es una p\u00e1gina de presentaci\u00f3n y referidos de la biblioteca curada alojada en <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Los fondos Nugget se aplican con la herramienta de c\u00f3digo abierto Nugget (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple, iPhone, iPad e iOS son marcas de Apple Inc. Este sitio no est\u00e1 afiliado a Apple.",
    "title": "Tendies Wallpaper &mdash; Fondos din\u00e1micos iOS para Nugget",
    "desc": "Tendies Wallpaper es el hogar de fondos din\u00e1micos iOS e iPadOS para Nugget. Descubre qu\u00e9 es un archivo .tendies, c\u00f3mo instalar fondos animados sin jailbreak y explora la biblioteca completa en Nugget Wallpaper.",
    "kw": "fondo tendies, archivo tendies, fondo Nugget, fondo din\u00e1mico iOS, fondo PosterBoard, fondo ios 18, fondo ios 27, fondo animado pantalla de bloqueo",
}

T["zh"] = {
    "nav_wiki": "\u8fd9\u662f\u4ec0\u4e48",
    "nav_install": "\u5b89\u88c5",
    "nav_gallery": "\u58c1\u7eb8\u5e93",
    "nav_faq": "FAQ",
    "nav_cta": "\u6d4f\u89c8\u58c1\u7eb8",
    "lang_label": "\u8bed\u8a00",
    "hero_kicker": "Tendies Wallpaper \u5b98\u65b9\u7f51\u7ad9",
    "hero_h1_lead": "\u4e13\u4e3a Nugget \u6253\u9020\u7684 iOS \u52a8\u6001\u58c1\u7eb8",
    "hero_h1_after": "\u8ba9\u4f60\u7684\u9501\u5c4f\u6d3b\u8d77\u6765\u3002",
    "hero_lead": "Tendies Wallpaper \u662f\u4e00\u4e2a\u7cbe\u9009\u7684 iPhone \u548c iPad \u52a8\u753b\u52a8\u6001\u58c1\u7eb8\u5408\u96c6\uff0c\u901a\u8fc7\u5f00\u6e90\u5de5\u5177 Nugget\uff0c\u7528\u7b80\u5355\u7684 .tendies \u6587\u4ef6\u5373\u53ef\u5b89\u88c5\u3002\u65e0\u9700\u8d8a\u72f1\uff0c\u4e5f\u65e0\u9700\u59a5\u534f\u3002\u652f\u6301 iOS \u548c iPadOS 17&ndash;27\u3002",
    "hero_btn1": "\u6d4f\u89c8\u58c1\u7eb8\u5e93",
    "hero_btn2": "\u5982\u4f55\u5b89\u88c5",
    "hero_btn3": "\u9605\u8bfb\u6559\u7a0b",
    "stat1b": "\u5b8c\u6574\u7248\u672c\u652f\u6301",
    "stat2b": "\u57fa\u4e8e SparseRestore / BookRestore",
    "stat3b": "\u5f00\u6e90\u4e14\u793e\u533a\u9a71\u52a8",
    "about_tag": "\u4ec0\u4e48\u662f Tendies Wallpaper\uff1f",
    "about_h2": "\u4e3a iPhone \u548c iPad \u6253\u9020\u7684\u52a8\u6001\u58c1\u7eb8",
    "about_p": "Tendies Wallpaper \u662f\u4e00\u4e2a\u5feb\u901f\u53d1\u5c55\u7684\u52a8\u6001\u9501\u5c4f\u58c1\u7eb8\u5e93\u54c1\u724c\uff0c\u4e13\u4e3a Nugget \u751f\u6001\u6253\u9020\u3002\u6bcf\u5f20\u58c1\u7eb8\u90fd\u4ee5 <strong>.tendies \u6587\u4ef6</strong> \u5f62\u5f0f\u6253\u5305\uff0c\u8fd9\u662f\u4e00\u79cd PosterBoard \u58c1\u7eb8\u5305\uff0c\u80fd\u628a Apple \u539f\u751f\u9501\u5c4f\u53d8\u6210\u5145\u6ee1\u751f\u673a\u7684\u753b\u5e03\u3002\u5b8c\u6574\u5408\u96c6\u6258\u7ba1\u5728 <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper\uff08mwallx.com\uff09</a>\u3002",
    "c1t": "\u771f\u6b63\u52a8\u6001",
    "c1d": "\u5728\u539f\u751f\u9501\u5c4f\u4e0a\u5448\u73b0\u52a8\u611f\u3001\u7eb5\u6df1\u548c\u52a8\u753b\uff0c\u800c\u975e\u9759\u6001\u56fe\u7247\u3002\u6bcf\u5f20 tendies \u58c1\u7eb8\u90fd\u529b\u6c42\u5e26\u6765\u9ad8\u7ea7\u7684\u751f\u52a8\u5c4f\u5e55\u4f53\u9a8c\u3002",
    "c2t": "\u65e0\u9700\u8d8a\u72f1",
    "c2d": "tendies \u58c1\u7eb8\u901a\u8fc7 Nugget \u5e94\u7528\uff0cNugget \u4f7f\u7528 Apple \u81ea\u6709\u7684 SparseRestore \u548c BookRestore \u8fd8\u539f\u673a\u5236\uff0c\u5b89\u5168\u5199\u5165\u6587\u4ef6\u3002",
    "c3t": "\u7cbe\u9009\u58c1\u7eb8\u5e93",
    "c3d": "\u52a8\u6f2b\u3001\u6f2b\u753b\u3001\u4f53\u80b2\u3001\u6f2b\u5a01\u3001\u592a\u7a7a\u68a6\u5883\u7b49\uff0c\u6bcf\u5468\u5728 Nugget Wallpaper \u7f51\u7ad9\u4e0a\u66f4\u65b0\u7cbe\u9009\u753b\u5eca\u3002",
    "c4t": "\u7531 Nugget \u9a71\u52a8",
    "c4d": "\u57fa\u4e8e leminlimez \u7684\u5f00\u6e90\u5de5\u5177 <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> \u6784\u5efa\uff0c\u53d7\u5230\u6570\u5343\u540d\u7528\u6237\u793e\u533a\u7684\u4fe1\u4efb\u3002",
    "c5t": "iPhone \u4e0e iPad",
    "c5d": "\u517c\u5bb9\u8fd0\u884c iOS \u548c iPadOS 17\u201326 \u7684 iPhone \u4e0e iPad\uff0c\u65e0\u8bba\u662f\u5426\u6709\u7075\u52a8\u5c9b\u3002",
    "c6t": "\u53ef\u9006\u4e14\u5b89\u5168",
    "c6d": "\u6240\u6709\u66f4\u6539\u90fd\u53ef\u64a4\u6d88\u3002\u5e94\u7528\u524d\u505a\u597d\u5907\u4efd\uff1b\u968f\u65f6\u53ef\u901a\u8fc7 iTunes \u6216 Finder \u6062\u590d\u5230\u539f\u59cb\u72b6\u6001\u3002",
    "tendies_h2": "\u4ec0\u4e48\u662f tendies \u6587\u4ef6\uff1f",
    "tendies_p": "<strong>.tendies \u6587\u4ef6</strong> \u662f\u6574\u4e2a Nugget / PosterBoard \u751f\u6001\uff08\u5305\u62ec Cowabunga \u548c Pocket Poster\uff09\u4f7f\u7528\u7684\u58c1\u7eb8\u5305\u683c\u5f0f\u3002\u5b83\u4fdd\u5b58\u4e86 Nugget \u4f1a\u8fd8\u539f\u5230\u8bbe\u5907\u4e0a\u7684 PosterBoard \u6587\u4ef6\u7ed3\u6784\uff0c\u8ba9\u58c1\u7eb8\u76f4\u63a5\u663e\u793a\u5728\u539f\u751f\u9501\u5c4f\u58c1\u7eb8\u9009\u62e9\u5668\u4e2d\u3002",
    "tv1_d": "\u76f4\u63a5\u8fd8\u539f\u5230 PosterBoard \u5e94\u7528\u5bb9\u5668\uff0c\u4fdd\u6301\u539f\u6709\u6587\u4ef6\u7ed3\u6784\u4e0e\u58c1\u7eb8 ID \u4e0d\u53d8\u3002",
    "tv2_d": "\u8fd8\u539f\u5230\u58c1\u7eb8\u63cf\u8ff0\u7b26\u6587\u4ef6\u5939\uff0cUUID \u968f\u673a\u5316\uff0c\u591a\u5f20 tendies \u58c1\u7eb8\u4e92\u4e0d\u51b2\u7a81\u3002",
    "tv3_d": "\u89c6\u9891\u548c\u7167\u7247\u53d8\u4f53\u9002\u7528\u4e8e\u5efa\u8bae\u7167\u7247\uff1bmercury \u53d8\u4f53\u9002\u7528\u4e8e\u652f\u6301\u7684 iOS \u7248\u672c\u4e0a\u7684 Mercury Poster\u3002",
    "install_tag": "\u5feb\u901f\u5f00\u59cb",
    "install_h2": "4 \u6b65\u5b89\u88c5 tendies \u58c1\u7eb8",
    "install_p": "\u7528\u4e00\u6839 USB \u6570\u636e\u7ebf\u548c\u514d\u8d39\u7684 Nugget \u5e94\u7528\uff0c\u6574\u4e2a\u8fc7\u7a0b\u53ea\u9700\u51e0\u5206\u949f\u3002\u5b8c\u6574\u7ec6\u8282\u8bf7\u53c2\u9605\u5b98\u65b9\u6559\u7a0b\u3002",
    "s1_t": "\u4e0b\u8f7d\u6587\u4ef6",
    "s1_d": "\u4ece\u58c1\u7eb8\u5e93\u6311\u9009\u4e00\u5f20\u58c1\u7eb8\uff0c\u4e0b\u8f7d\u5176 <strong>.tendies</strong> \u6587\u4ef6\u3002",
    "s2_t": "\u8fde\u63a5\u8bbe\u5907",
    "s2_d": "\u7528 USB \u5c06 iPhone/iPad \u8fde\u63a5\u5230\u7535\u8111\u5e76\u4fe1\u4efb\u3002\u652f\u6301 Windows\u3001macOS \u548c Linux\u3002",
    "s3_t": "\u5bfc\u5165\u5e76\u5e94\u7528",
    "s3_d": "\u5728 Nugget \u4e2d\u6253\u5f00 PosterBoard\uff0c\u9009\u62e9\u6587\u4ef6\uff0c\u7136\u540e\u70b9\u51fb\u201c\u5e94\u7528\u66f4\u6539\u201d\u3002",
    "s4_t": "\u91cd\u542f\u5e76\u4eab\u53d7",
    "s4_d": "\u91cd\u542f\u540e\u6253\u5f00\u9501\u5c4f\u7f16\u8f91\u5668\uff0c\u5728\u201c\u5408\u96c6\u201d\u6216\u201c\u6536\u85cf\u201d\u4e2d\u627e\u5230\u4f60\u7684\u65b0\u58c1\u7eb8\u3002",
    "install_note": "\u9047\u5230\u95ee\u9898\uff1f\u8bf7\u9605\u8bfb<a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper \u5b98\u65b9\u6559\u7a0b</a>\uff0c\u6216\u52a0\u5165\u4e0b\u65b9\u793e\u533a\u9891\u9053\u3002",
    "gallery_tag": "\u58c1\u7eb8\u5e93",
    "gallery_h2": "\u6d4f\u89c8 Tendies Wallpaper \u753b\u5eca",
    "gallery_p": "\u4e0b\u65b9\u7684\u6bcf\u5f20 tendies \u58c1\u7eb8\u90fd\u6258\u7ba1\u5728 <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper\uff08mwallx.com\uff09</a> \u5e76\u53ef\u4e0b\u8f7d\u3002\u53ef\u6309<a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">\u6700\u65b0</a>\u6216<a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">\u70ed\u95e8</a>\u6392\u5e8f\u67e5\u770b\u8d8b\u52bf\u3002",
    "g_t1": "\u52a8\u6f2b",
    "g_d1": "\u798f\u97f3\u6218\u58eb\u3001Sylphiette \u7b49",
    "g_t2": "\u4f53\u80b2\u4e0e\u6f2b\u5a01",
    "g_d2": "\u7403\u961f\u3001\u82f1\u96c4\u4e0e\u5d1b\u65b0\u4e00\u5929",
    "g_t3": "\u68a6\u5e7b\u661f\u7a7a",
    "g_d3": "\u884c\u661f\u3001\u661f\u8fb0\u4e0e\u62bd\u8c61",
    "g_t4": "\u5b98\u65b9\u7cbe\u9009",
    "g_d4": "\u82f9\u679c\u98ce\u683c\u6d77\u62a5\u7cbe\u9009",
    "gallery_cta": "\u67e5\u770b\u6240\u6709\u58c1\u7eb8",
    "faq_h2": "\u5e38\u89c1\u95ee\u9898",
    "faq_p": "\u5f00\u59cb\u4e4b\u524d\uff0c\u4f60\u9700\u8981\u4e86\u89e3\u7684 tendies \u58c1\u7eb8\u4e00\u5207\u4fe1\u606f\u3002",
    "f1q": "\u4ec0\u4e48\u662f tendies \u58c1\u7eb8\uff1f",
    "f1a": "tendies \u58c1\u7eb8\u662f\u4e13\u4e3a iPhone \u548c iPad \u8bbe\u8ba1\u7684\u52a8\u6001\u52a8\u753b\u58c1\u7eb8\uff0c\u4ee5 .tendies \u6587\u4ef6\u5f62\u5f0f\u4ea4\u4ed8\uff0c\u901a\u8fc7 Nugget \u5de5\u5177\u5b89\u88c5\u3002tendies \u6587\u4ef6\u4f1a\u5c06 PosterBoard \u58c1\u7eb8\u63cf\u8ff0\u7b26\u8fd8\u539f\u5230 iOS 17-27 \u8bbe\u5907\uff0c\u4f7f\u58c1\u7eb8\u663e\u793a\u5728\u9501\u5c4f\u7684\u201c\u5408\u96c6\u201d\u9009\u62e9\u5668\u4e2d\u3002",
    "f2q": "\u4ec0\u4e48\u662f .tendies \u6587\u4ef6\uff1f",
    "f2a": ".tendies \u6587\u4ef6\u662f Nugget \u548c Pocket Poster \u4f7f\u7528\u7684\u58c1\u7eb8\u5305\u683c\u5f0f\u3002\u5b83\u4fdd\u5b58\u4e86\u8fd8\u539f\u5230 iPhone \u6216 iPad \u7684 PosterBoard \u6587\u4ef6\u7ed3\u6784\uff0c\u4e5f\u662f\u5b89\u88c5\u81ea\u5b9a\u4e49\u52a8\u6001\u9501\u5c4f\u58c1\u7eb8\u65f6\u9700\u8981\u5bfc\u5165\u7684\u6587\u4ef6\u3002",
    "f3q": "tendies \u58c1\u7eb8\u9700\u8981\u8d8a\u72f1\u5417\uff1f",
    "f3a": "\u4e0d\u9700\u8981\u3002tendies \u58c1\u7eb8\u901a\u8fc7\u5f00\u6e90\u5de5\u5177 Nugget \u5b89\u88c5\uff0cNugget \u4f7f\u7528 Apple \u81ea\u6709\u7684 SparseRestore \u4e0e BookRestore \u673a\u5236\u5b89\u5168\u4fee\u6539\u6587\u4ef6\uff0c\u65e0\u9700\u8d8a\u72f1\u3002",
    "f4q": "\u54ea\u4e9b iOS \u7248\u672c\u652f\u6301 tendies \u58c1\u7eb8\uff1f",
    "f4a": "tendies \u58c1\u7eb8\u5728\u517c\u5bb9\u7684 iPhone \u548c iPad \u4e0a\u652f\u6301 iOS \u4e0e iPadOS 17\u201326\u3002\u90e8\u5206\u58c1\u7eb8\u53ef\u80fd\u8981\u6c42\u7279\u5b9a iOS \u7248\u672c\uff0c\u8bf7\u59cb\u7ec8\u67e5\u770b\u58c1\u7eb8\u9875\u9762\u4e0a\u7684\u517c\u5bb9\u6027\u8bf4\u660e\u3002",
    "f5q": "\u5728\u54ea\u91cc\u53ef\u4ee5\u4e0b\u8f7d tendies \u58c1\u7eb8\uff1f",
    "f5a": "\u524d\u5f80 mwallx.com \u7684 Nugget Wallpaper \u58c1\u7eb8\u5e93\u6d4f\u89c8\u5e76\u4e0b\u8f7d tendies \u58c1\u7eb8\uff0c\u8fd9\u91cc\u6536\u5f55\u4e86\u52a8\u6f2b\u3001\u4f53\u80b2\u3001\u6f2b\u5a01\u7b49\u591a\u79cd\u7cbe\u9009\u52a8\u6001\u4e0e\u9759\u6001\u58c1\u7eb8\u3002",
    "f6q": "\u5982\u4f55\u5728 iPhone \u4e0a\u5b89\u88c5 tendies \u58c1\u7eb8\uff1f",
    "f6a": "\u4e0b\u8f7d .tendies \u6587\u4ef6\uff0c\u5728 Nugget \u4e2d\u6253\u5f00 PosterBoard \u529f\u80fd\uff0c\u9009\u62e9\u6587\u4ef6\uff0c\u5e94\u7528\u66f4\u6539\u5e76\u91cd\u542f\u8bbe\u5907\u3002\u91cd\u542f\u540e\u5728\u9501\u5c4f\u7f16\u8f91\u5668\u91cc\uff0c\u5728\u201c\u5408\u96c6\u201d\u6216\u201c\u6536\u85cf\u201d\u4e2d\u627e\u5230\u65b0\u58c1\u7eb8\u3002",
    "f7q": "\u4f7f\u7528 tendies \u58c1\u7eb8\u5b89\u5168\u5417\uff1f",
    "f7a": "Nugget \u662f\u5e7f\u53d7\u6b22\u8fce\u7684\u5f00\u6e90\u9879\u76ee\uff0c\u62e5\u6709\u6570\u5343\u540d\u7528\u6237\u3002\u4e0e\u4efb\u4f55\u7cfb\u7edf\u4fee\u6539\u4e00\u6837\uff0c\u8bf7\u5148\u5907\u4efd\u8bbe\u5907\u3002\u6240\u6709\u66f4\u6539\u5747\u53ef\u901a\u8fc7 iTunes \u6216 Finder \u8fd8\u539f\u8bbe\u5907\u6765\u64a4\u6d88\u3002",
    "f8q": "Nugget Wallpaper \u4e0e tendies \u58c1\u7eb8\u6709\u4ec0\u4e48\u533a\u522b\uff1f",
    "f8a": "Tendies Wallpaper \u662f\u52a8\u6001\u58c1\u7eb8\u5408\u96c6\u7684\u54c1\u724c\u540d\uff0c\u800c Nugget Wallpaper\uff08mwallx.com\uff09\u662f\u627f\u8f7d\u5b83\u4eec\u7684\u58c1\u7eb8\u5e93\u3002\u4e24\u8005\u540c\u5c5e\u4e00\u4e2a\u751f\u6001\uff0c\u7531\u7528\u4e8e iOS \u81ea\u5b9a\u4e49\u7684\u5f00\u6e90\u5de5\u5177 Nugget \u9a71\u52a8\u3002",
    "comm_h2": "\u52a0\u5165 Nugget Wallpaper \u793e\u533a",
    "comm_p": "\u5173\u6ce8\u9891\u9053\u83b7\u53d6\u65b0\u58c1\u7eb8\u53d1\u5e03\u3001\u9884\u89c8\u548c\u5feb\u901f\u5b89\u88c5\u6280\u5de7\u3002",
    "comm_host_d": "iOS \u5de5\u5177\u5b98\u7f51",
    "cta_h2": "\u51c6\u5907\u597d\u8ba9\u9501\u5c4f\u7115\u53d1\u751f\u673a\u4e86\u5417\uff1f",
    "cta_p": "\u7acb\u5373\u514d\u8d39\u4e0b\u8f7d tendies \u58c1\u7eb8\uff0c\u65e0\u9700\u8d8a\u72f1\u3002\u5728 Nugget Wallpaper \u7f51\u7ad9\u6d4f\u89c8\u5b8c\u6574\u58c1\u7eb8\u5e93\u3001\u67e5\u770b\u4ef7\u683c\u3001\u8ddf\u8e2a\u8ba2\u5355\uff0c\u5e76\u9605\u8bfb\u5206\u6b65\u6559\u7a0b\u3002",
    "cta_btn1": "\u5f00\u59cb\u63a2\u7d22",
    "cta_btn2": "\u67e5\u770b\u4ef7\u683c",
    "foot_tw1": "\u9996\u9875",
    "foot_tw2": "\u8fd9\u662f\u4ec0\u4e48",
    "foot_tw3": ".tendies \u6587\u4ef6",
    "foot_tw4": "\u5b89\u88c5\u6307\u5357",
    "foot_nw1": "\u6d4f\u89c8\u5168\u90e8\u58c1\u7eb8",
    "foot_nw2": "\u6700\u65b0\u6dfb\u52a0",
    "foot_nw3": "\u5f53\u524d\u70ed\u95e8",
    "foot_nw4": "\u5bfc\u5165\u6559\u7a0b",
    "foot_pr1": "GitHub \u4e0a\u7684 Nugget",
    "foot_pr3": "\u4ef7\u683c",
    "foot_pr4": "\u8ba2\u5355",
    "foot_pol1": "\u9690\u79c1\u653f\u7b56",
    "foot_pol2": "\u670d\u52a1\u6761\u6b3e",
    "foot_pol3": "DMCA \u653f\u7b56",
    "foot_pol4": "UGC \u653f\u7b56",
    "copyright": "Tendies Wallpaper \u662f\u6258\u7ba1\u4e8e <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper\uff08mwallx.com\uff09</a> \u7cbe\u9009\u58c1\u7eb8\u5e93\u7684\u7b80\u4ecb\u4e0e\u5f15\u6d41\u9875\u9762\u3002Nugget \u58c1\u7eb8\u901a\u8fc7\u5f00\u6e90\u5de5\u5177 Nugget\uff08<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>\uff09\u5e94\u7528\u3002Apple\u3001iPhone\u3001iPad \u548c iOS \u662f Apple Inc. \u7684\u5546\u6807\u3002\u672c\u7f51\u7ad9\u4e0e Apple \u65e0\u5173\u3002",
    "title": "Tendies Wallpaper &mdash; \u4e13\u4e3a Nugget \u6253\u9020\u7684 iOS \u52a8\u6001\u58c1\u7eb8",
    "desc": "Tendies Wallpaper \u662f\u4e13\u4e3a Nugget \u6253\u9020\u7684 iOS \u4e0e iPadOS \u52a8\u6001\u58c1\u7eb8\u4e4b\u5bb6\u3002\u4e86\u89e3 .tendies \u6587\u4ef6\u662f\u4ec0\u4e48\u3001\u5982\u4f55\u65e0\u9700\u8d8a\u72f1\u5b89\u88c5\u52a8\u753b\u9501\u5c4f\u58c1\u7eb8\uff0c\u5e76\u5728 Nugget Wallpaper \u6d4f\u89c8\u5b8c\u6574\u58c1\u7eb8\u5e93\u3002",
    "kw": "tendies \u58c1\u7eb8, tendies \u6587\u4ef6, Nugget \u58c1\u7eb8, iOS \u52a8\u6001\u58c1\u7eb8, PosterBoard \u58c1\u7eb8, ios 18 \u58c1\u7eb8, ios 27 \u58c1\u7eb8, \u52a8\u753b\u9501\u5c4f\u58c1\u7eb8",
}

T["hi"] = {
    "nav_wiki": "\u092f\u0939 \u0915\u094d\u092f\u093e \u0939\u0948",
    "nav_install": "\u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u0930\u0947\u0902",
    "nav_gallery": "\u0917\u0948\u0932\u0930\u0940",
    "nav_faq": "FAQ",
    "nav_cta": "\u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0926\u0947\u0916\u0947\u0902",
    "lang_label": "\u092d\u093e\u0937\u093e",
    "hero_kicker": "Tendies Wallpaper \u0915\u093e \u0906\u0927\u093f\u0915\u093e\u0930\u093f\u0915 \u0939\u094b\u092e",
    "hero_h1_lead": "Nugget \u0915\u0947 \u0932\u093f\u090f iOS \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0935\u0949\u0932\u092a\u0947\u092a\u0930",
    "hero_h1_after": "\u0906\u092a\u0915\u0940 \u0932\u0949\u0915 \u0938\u094d\u0915\u094d\u0930\u0940\u0928, \u091c\u0940\u0935\u093f\u0924\u0964",
    "hero_lead": "Tendies Wallpaper iPhone \u0914\u0930 iPad \u0915\u0947 \u0932\u093f\u090f \u090f\u0928\u093f\u092e\u0947\u091f\u0947\u0921, \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u093e \u091a\u0941\u0928\u093f\u0902\u0926\u093e \u0938\u0902\u0917\u094d\u0930\u0939 \u0939\u0948, \u091c\u093f\u0938\u0947 \u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 Nugget \u091f\u0942\u0932 \u0915\u0940 \u092e\u0926\u0926 \u0938\u0947 \u0938\u093f\u0930\u094d\u092b\u093c \u090f\u0915 .tendies \u092b\u093c\u093e\u0907\u0932 \u0926\u094d\u0935\u093e\u0930\u093e \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u093f\u092f\u093e \u091c\u093e\u0924\u093e \u0939\u0948\u0964 \u0915\u094b\u0908 \u091c\u0947\u0932\u092c\u094d\u0930\u0947\u0915 \u0928\u0939\u0940\u0902, \u0915\u094b\u0908 \u0938\u092e\u091d\u094c\u0924\u093e \u0928\u0939\u0940\u0902\u0964 iOS \u0914\u0930 iPadOS 17&ndash;27 \u092a\u0930 \u0938\u092e\u0930\u094d\u0925\u093f\u0924\u0964",
    "hero_btn1": "\u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0926\u0947\u0916\u0947\u0902",
    "hero_btn2": "\u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u0948\u0938\u0947 \u0915\u0930\u0947\u0902",
    "hero_btn3": "\u091f\u094d\u092f\u0942\u091f\u094b\u0930\u093f\u092f\u0932 \u092a\u095d\u0947\u0902",
    "stat1b": "\u092a\u0942\u0930\u094d\u0923 \u0935\u0930\u094d\u091c\u0928 \u0938\u092e\u0930\u094d\u0925\u0928",
    "stat2b": "SparseRestore / BookRestore \u0915\u093e \u0909\u092a\u092f\u094b\u0917",
    "stat3b": "\u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 \u0914\u0930 \u0915\u092e\u094d\u092f\u0942\u0928\u093f\u091f\u0940 \u091a\u093e\u0932\u093f\u0924",
    "about_tag": "Tendies Wallpaper \u0915\u094d\u092f\u093e \u0939\u0948?",
    "about_h2": "iPhone \u0914\u0930 iPad \u0915\u0947 \u0932\u093f\u090f \u0938\u0939\u0940 \u0924\u0930\u0940\u0915\u0947 \u0938\u0947 \u092c\u0928\u093e\u090f \u0917\u090f \u090f\u0928\u093f\u092e\u0947\u091f\u0947\u0921 \u0935\u0949\u0932\u092a\u0947\u092a\u0930",
    "about_p": "Tendies Wallpaper Nugget \u0907\u0915\u094b\u0938\u093f\u0938\u094d\u091f\u092e \u0915\u0947 \u0932\u093f\u090f \u092c\u0928\u0947 \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u0940 \u092c\u095d\u0924\u0940 \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0915\u0947 \u092a\u0940\u091b\u0947 \u0915\u093e \u092c\u094d\u0930\u093e\u0902\u0921 \u0939\u0948\u0964 \u0939\u0930 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u090f\u0915 <strong>.tendies \u092b\u093c\u093e\u0907\u0932</strong> \u0915\u0947 \u0930\u0942\u092a \u092e\u0947\u0902 \u092a\u0948\u0915 \u0915\u093f\u092f\u093e \u091c\u093e\u0924\u093e \u0939\u0948 &mdash; \u090f\u0915 PosterBoard \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092c\u0902\u0921\u0932 \u091c\u094b Apple \u0915\u0947 \u0928\u0947\u091f\u093f\u0935 \u0932\u0949\u0915 \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0915\u094b \u090f\u0915 \u091c\u0940\u0935\u093f\u0924 \u0915\u0948\u0928\u0935\u093e\u0938 \u092e\u0947\u0902 \u092c\u0926\u0932 \u0926\u0947\u0924\u093e \u0939\u0948\u0964 \u092a\u0942\u0930\u093e \u0938\u0902\u0917\u094d\u0930\u0939 <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> \u092a\u0930 \u0909\u092a\u0932\u092c\u094d\u0927 \u0939\u0948\u0964",
    "c1t": "\u0935\u093e\u0915\u0908 \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915",
    "c1d": "\u0928\u0947\u091f\u093f\u0935 \u0932\u0949\u0915 \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u092a\u0930 \u092e\u094b\u0936\u0928, \u0917\u0939\u0930\u093e\u0908 \u0914\u0930 \u090f\u0928\u093f\u092e\u0947\u0936\u0928 &mdash; \u0915\u094b\u0908 \u0938\u094d\u0925\u093f\u0930 \u091b\u0935\u093f \u0928\u0939\u0940\u0902\u0964 \u0939\u0930 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092a\u094d\u0930\u0940\u092e\u093f\u092f\u092e \u0932\u093e\u0907\u0935 \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u091c\u0948\u0938\u093e \u0905\u0928\u0941\u092d\u0935 \u0926\u0947\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0924\u0948\u092f\u093e\u0930 \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u0939\u0948\u0964",
    "c2t": "\u0915\u094b\u0908 \u091c\u0947\u0932\u092c\u094d\u0930\u0947\u0915 \u0928\u0939\u0940\u0902",
    "c2d": "tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 Nugget \u0938\u0947 \u0932\u0917\u093e\u090f \u091c\u093e\u0924\u0947 \u0939\u0948\u0902, \u091c\u094b \u092b\u093c\u093e\u0907\u0932\u0947\u0902 \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u0930\u0942\u092a \u0938\u0947 \u0932\u093f\u0916\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f Apple \u0915\u0947 SparseRestore \u0914\u0930 BookRestore \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u092e\u0948\u0915\u0947\u0928\u093f\u091c\u094d\u092e \u0915\u093e \u0909\u092a\u092f\u094b\u0917 \u0915\u0930\u0924\u093e \u0939\u0948\u0964",
    "c3t": "\u091a\u0941\u0928\u093f\u0902\u0926\u093e \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940",
    "c3d": "\u090f\u0928\u093f\u092e\u0947, \u092e\u0902\u0917\u093e, \u0938\u094d\u092a\u094b\u0930\u094d\u091f\u094d\u0938, Marvel, \u0938\u094d\u092a\u0947\u0938 \u0921\u094d\u0930\u0940\u092e\u0938\u094d\u0915\u0947\u092a \u0914\u0930 \u092c\u0939\u0941\u0924 \u0915\u0941\u091b &mdash; Nugget Wallpaper \u0938\u093e\u0907\u091f \u092a\u0930 \u0939\u0930 \u0939\u092b\u094d\u0924\u0947 \u0905\u092a\u0921\u0947\u091f \u0939\u094b\u0928\u0947 \u0935\u093e\u0932\u0940 \u091a\u0941\u0928\u093f\u0902\u0926\u093e \u0917\u0948\u0932\u0930\u0940\u0964",
    "c4t": "Nugget \u0926\u094d\u0935\u093e\u0930\u093e \u0938\u0902\u091a\u093e\u0932\u093f\u0924",
    "c4d": "leminlimez \u0915\u0947 \u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget \u091f\u0942\u0932</a> \u092a\u0930 \u0906\u0927\u093e\u0930\u093f\u0924, \u091c\u093f\u0938 \u092a\u0930 \u0939\u091c\u093e\u0930\u094b\u0902 \u0909\u092a\u092f\u094b\u0917\u0915\u0930\u094d\u0924\u093e\u0913\u0902 \u0915\u0940 \u0915\u092e\u094d\u092f\u0942\u0928\u093f\u091f\u0940 \u092d\u0930\u094b\u0938\u093e \u0915\u0930\u0924\u0940 \u0939\u0948\u0964",
    "c5t": "iPhone \u0914\u0930 iPad",
    "c5d": "iOS \u0914\u0930 iPadOS 17-27 \u091a\u0932\u093e\u0928\u0947 \u0935\u093e\u0932\u0947 \u0938\u0902\u0917\u0924 iPhone \u0914\u0930 iPad \u092a\u0930 \u0915\u093e\u092e \u0915\u0930\u0924\u093e \u0939\u0948 &mdash; Dynamic Island \u0915\u0947 \u0938\u093e\u0925 \u092f\u093e \u092c\u093f\u0928\u093e\u0964",
    "c6t": "\u0930\u093f\u0935\u0930\u094d\u0938\u093f\u092c\u0932 \u0914\u0930 \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924",
    "c6d": "\u0938\u092c \u0915\u0941\u091b \u0930\u093f\u0935\u0930\u094d\u0938\u093f\u092c\u0932 \u0939\u0948\u0964 \u0932\u0917\u093e\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 \u092c\u0948\u0915\u0905\u092a \u0932\u0947\u0902; \u0915\u092d\u0940 \u092d\u0940 iTunes \u092f\u093e Finder \u0938\u0947 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0915\u0947 \u092a\u0941\u0930\u093e\u0928\u0940 \u0938\u094d\u0925\u093f\u0924\u093f \u092e\u0947\u0902 \u0932\u094c\u091f\u0947\u0902\u0964",
    "tendies_h2": "tendies \u092b\u093c\u093e\u0907\u0932 \u0915\u094d\u092f\u093e \u0939\u0948?",
    "tendies_p": "<strong>.tendies \u092b\u093c\u093e\u0907\u0932</strong> Nugget / PosterBoard \u0907\u0915\u094b\u0938\u093f\u0938\u094d\u091f\u092e (Cowabunga \u0914\u0930 Pocket Poster \u0938\u0939\u093f\u0924) \u092e\u0947\u0902 \u0909\u092a\u092f\u094b\u0917 \u0939\u094b\u0928\u0947 \u0935\u093e\u0932\u093e \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092c\u0902\u0921\u0932 \u092b\u093c\u0949\u0930\u094d\u092e\u0947\u091f \u0939\u0948\u0964 \u092f\u0939 \u0938\u091f\u0940\u0915 PosterBoard \u092b\u093c\u093e\u0907\u0932 \u0938\u0902\u0930\u091a\u0928\u093e \u0938\u0902\u0917\u094d\u0930\u0939\u093f\u0924 \u0915\u0930\u0924\u093e \u0939\u0948 \u091c\u093f\u0938\u0947 Nugget \u0906\u092a\u0915\u0947 \u0921\u093f\u0935\u093e\u0907\u0938 \u092a\u0930 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0924\u093e \u0939\u0948, \u0924\u093e\u0915\u093f \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0928\u0947\u091f\u093f\u0935 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092a\u093f\u0915\u0930 \u0915\u0947 \u0905\u0902\u0926\u0930 \u0939\u0940 \u0926\u093f\u0916\u093e\u0908 \u0926\u0947\u0964",
    "tv1_d": "\u0938\u0940\u0927\u0947 PosterBoard \u090f\u092a \u0915\u0902\u091f\u0947\u0928\u0930 \u092e\u0947\u0902 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0924\u093e \u0939\u0948, \u092b\u093c\u093e\u0907\u0932 \u0938\u0902\u0930\u091a\u0928\u093e \u0914\u0930 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 ID \u0905\u092a\u0930\u093f\u0935\u0930\u094d\u0924\u093f\u0924 \u0930\u0916\u0924\u0947 \u0939\u0941\u090f\u0964",
    "tv2_d": "\u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0921\u093f\u0938\u094d\u0915\u094d\u0930\u093f\u092a\u094d\u091f\u0930 \u092b\u093c\u094b\u0932\u094d\u0921\u0930 \u092e\u0947\u0902 \u0930\u0948\u0902\u0921\u092e\u093e\u0907\u091c\u093c\u094d\u0921 UUID \u0915\u0947 \u0938\u093e\u0925 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0924\u093e \u0939\u0948 \u0924\u093e\u0915\u093f \u0915\u0908 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0906\u092a\u0938 \u092e\u0947\u0902 \u091f\u0915\u0930\u093e\u090f\u0902 \u0928\u0939\u0940\u0902\u0964",
    "tv3_d": "\u0935\u0940\u0921\u093f\u092f\u094b \u0914\u0930 \u092b\u093c\u094b\u091f\u094b \u0935\u0947\u0930\u093f\u090f\u0902\u091f Suggested Photos \u0915\u094b \u091f\u093e\u0930\u094d\u0917\u0947\u091f \u0915\u0930\u0924\u0947 \u0939\u0948\u0902; mercury \u0935\u0947\u0930\u093f\u090f\u0902\u091f \u0938\u092e\u0930\u094d\u0925\u093f\u0924 iOS \u0935\u0930\u094d\u091c\u0928 \u092a\u0930 Mercury Poster \u0915\u094b \u091f\u093e\u0930\u094d\u0917\u0947\u091f \u0915\u0930\u0924\u0947 \u0939\u0948\u0902\u0964",
    "install_tag": "\u0936\u0941\u0930\u0941\u0906\u0924",
    "install_h2": "4 \u091a\u0930\u0923\u094b\u0902 \u092e\u0947\u0902 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u0930\u0947\u0902",
    "install_p": "USB \u0915\u0947\u092c\u0932 \u0914\u0930 \u092e\u0941\u092b\u093c\u094d\u0924 Nugget \u090f\u092a \u0915\u0940 \u092e\u0926\u0926 \u0938\u0947 \u092a\u0942\u0930\u0940 \u092a\u094d\u0930\u0915\u094d\u0930\u093f\u092f\u093e \u092e\u0947\u0902 \u0915\u0941\u091b \u0939\u0940 \u092e\u093f\u0928\u091f \u0932\u0917\u0924\u0947 \u0939\u0948\u0902\u0964 \u092a\u0942\u0930\u0940 \u091c\u093e\u0928\u0915\u093e\u0930\u0940 \u0906\u0927\u093f\u0915\u093e\u0930\u093f\u0915 \u091f\u094d\u092f\u0942\u091f\u094b\u0930\u093f\u092f\u0932 \u092e\u0947\u0902 \u0939\u0948\u0964",
    "s1_t": "\u092b\u093c\u093e\u0907\u0932 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902",
    "s1_d": "\u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0938\u0947 \u0915\u094b\u0908 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u091a\u0941\u0928\u0947\u0902 \u0914\u0930 \u0909\u0938\u0915\u0940 <strong>.tendies</strong> \u092b\u093c\u093e\u0907\u0932 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902\u0964",
    "s2_t": "\u0921\u093f\u0935\u093e\u0907\u0938 \u0915\u0928\u0947\u0915\u094d\u091f \u0915\u0930\u0947\u0902",
    "s2_d": "\u0905\u092a\u0928\u0947 iPhone/iPad \u0915\u094b USB \u0938\u0947 \u0915\u0902\u092a\u094d\u092f\u0942\u091f\u0930 \u0938\u0947 \u091c\u094b\u0921\u093c\u0947\u0902 \u0914\u0930 \u091f\u094d\u0930\u0938\u094d\u091f \u0915\u0930\u0947\u0902\u0964 Windows, macOS \u0914\u0930 Linux \u092a\u0930 \u0915\u093e\u092e \u0915\u0930\u0924\u093e \u0939\u0948\u0964",
    "s3_t": "\u0907\u0902\u092a\u094b\u0930\u094d\u091f \u0914\u0930 \u0932\u093e\u0917\u0942 \u0915\u0930\u0947\u0902",
    "s3_d": "Nugget \u092e\u0947\u0902 PosterBoard \u0916\u094b\u0932\u0947\u0902, \u092b\u093c\u093e\u0907\u0932 \u091a\u0941\u0928\u0947\u0902, \u092b\u093f\u0930 Apply Changes \u0926\u092c\u093e\u090f\u0902\u0964",
    "s4_t": "\u0930\u0940\u092c\u0942\u091f \u0915\u0930\u0947\u0902 \u0914\u0930 \u092e\u091c\u093c\u0947 \u0915\u0930\u0947\u0902",
    "s4_d": "\u0930\u0940\u092c\u0942\u091f \u0915\u0947 \u092c\u093e\u0926 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u090f\u0921\u093f\u091f\u0930 \u0916\u094b\u0932\u0947\u0902 \u0914\u0930 Collections \u092f\u093e Favorites \u092e\u0947\u0902 \u0905\u092a\u0928\u093e \u0928\u092f\u093e \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092a\u093e\u090f\u0902\u0964",
    "install_note": "\u0915\u094b\u0908 \u0938\u092e\u0938\u094d\u092f\u093e? <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper \u0915\u093e \u0906\u0927\u093f\u0915\u093e\u0930\u093f\u0915 \u091f\u094d\u092f\u0942\u091f\u094b\u0930\u093f\u092f\u0932</a> \u092a\u095d\u0947\u0902 \u092f\u093e \u0928\u0940\u091a\u0947 \u0926\u093f\u090f \u0917\u090f \u0915\u092e\u094d\u092f\u0942\u0928\u093f\u091f\u0940 \u091a\u0948\u0928\u0932\u094d\u0938 \u0938\u0947 \u091c\u0941\u0921\u093c\u0947\u0902\u0964",
    "gallery_tag": "\u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940",
    "gallery_h2": "Tendies Wallpaper \u0917\u0948\u0932\u0930\u0940 \u0926\u0947\u0916\u0947\u0902",
    "gallery_p": "\u0928\u0940\u091a\u0947 \u0926\u093f\u090f \u0917\u090f \u0939\u0930 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0915\u094b <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> \u092a\u0930 \u0939\u094b\u0938\u094d\u091f \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u0939\u0948 \u0914\u0930 \u0935\u0939\u093e\u0902 \u0938\u0947 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u093f\u092f\u093e \u091c\u093e \u0938\u0915\u0924\u093e \u0939\u0948\u0964 \u091f\u094d\u0930\u0947\u0902\u0921\u093f\u0902\u0917 \u0926\u0947\u0916\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0917\u0948\u0932\u0930\u0940 \u0915\u094b <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">Latest</a> \u092f\u093e <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">Hot</a> \u0915\u0947 \u0939\u093f\u0938\u093e\u092c \u0938\u0947 \u0938\u094b\u0930\u094d\u091f \u0915\u0930\u0947\u0902\u0964",
    "g_t1": "\u090f\u0928\u093f\u092e\u0947",
    "g_d1": "Evangelion, Sylphiette \u0914\u0930 \u0905\u0928\u094d\u092f",
    "g_t2": "\u0938\u094d\u092a\u094b\u0930\u094d\u091f\u094d\u0938 \u0914\u0930 Marvel",
    "g_d2": "\u0915\u094d\u0932\u092c, \u0939\u0940\u0930\u094b, \u0928\u090f \u0926\u093f\u0928",
    "g_t3": "\u0921\u094d\u0930\u0940\u092e\u0938\u094d\u0915\u0947\u092a",
    "g_d3": "\u0917\u094d\u0930\u0939, \u0924\u093e\u0930\u0947 \u0914\u0930 \u090f\u092c\u0938\u094d\u091f\u094d\u0930\u0948\u0915\u094d\u091f",
    "g_t4": "\u0906\u0927\u093f\u0915\u093e\u0930\u093f\u0915",
    "g_d4": "Apple \u0938\u094d\u091f\u093e\u0907\u0932 \u092a\u094b\u0938\u094d\u091f\u0930 \u092a\u0938\u0902\u0926",
    "gallery_cta": "\u0938\u092d\u0940 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0926\u0947\u0916\u0947\u0902",
    "faq_h2": "\u0905\u0915\u094d\u0938\u0930 \u092a\u0942\u091b\u0947 \u091c\u093e\u0928\u0947 \u0935\u093e\u0932\u0947 \u0938\u0935\u093e\u0932",
    "faq_p": "\u0936\u0941\u0930\u0942 \u0915\u0930\u0928\u0947 \u0938\u0947 \u092a\u0939\u0932\u0947 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u0947 \u092c\u093e\u0930\u0947 \u092e\u0947\u0902 \u0906\u092a\u0915\u094b \u091c\u094b \u0915\u0941\u091b \u092d\u0940 \u091c\u093e\u0928\u0928\u093e \u0939\u0948\u0964",
    "f1q": "tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0915\u094d\u092f\u093e \u0939\u0948?",
    "f1a": "tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 iPhone \u0914\u0930 iPad \u0915\u0947 \u0932\u093f\u090f \u090f\u0915 \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915, \u090f\u0928\u093f\u092e\u0947\u091f\u0947\u0921 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0939\u0948, \u091c\u094b .tendies \u092b\u093c\u093e\u0907\u0932 \u0915\u0947 \u0930\u0942\u092a \u092e\u0947\u0902 \u092e\u093f\u0932\u0924\u093e \u0939\u0948 \u0914\u0930 Nugget \u091f\u0942\u0932 \u0938\u0947 \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u093f\u092f\u093e \u091c\u093e\u0924\u093e \u0939\u0948\u0964 tendies \u092b\u093c\u093e\u0907\u0932\u0947\u0902 PosterBoard \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0921\u093f\u0938\u094d\u0915\u094d\u0930\u093f\u092a\u094d\u091f\u0930 \u0915\u094b iOS 17-27 \u0921\u093f\u0935\u093e\u0907\u0938 \u092a\u0930 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0924\u0940 \u0939\u0948\u0902 \u0924\u093e\u0915\u093f \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 Collections \u092a\u093f\u0915\u0930 \u092e\u0947\u0902 \u0926\u093f\u0916\u0947\u0964",
    "f2q": ".tendies \u092b\u093c\u093e\u0907\u0932 \u0915\u094d\u092f\u093e \u0939\u0948?",
    "f2a": ".tendies \u092b\u093c\u093e\u0907\u0932 Nugget \u0914\u0930 Pocket Poster \u0926\u094d\u0935\u093e\u0930\u093e \u0909\u092a\u092f\u094b\u0917 \u0915\u093f\u092f\u093e \u091c\u093e\u0928\u0947 \u0935\u093e\u0932\u093e \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092c\u0902\u0921\u0932 \u092b\u093c\u0949\u0930\u094d\u092e\u0947\u091f \u0939\u0948\u0964 \u092f\u0939 PosterBoard \u092b\u093c\u093e\u0907\u0932 \u0938\u0902\u0930\u091a\u0928\u093e \u0938\u0902\u0917\u094d\u0930\u0939\u093f\u0924 \u0915\u0930\u0924\u0940 \u0939\u0948 \u091c\u094b \u0906\u092a\u0915\u0947 iPhone \u092f\u093e iPad \u092a\u0930 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0939\u094b\u0924\u0940 \u0939\u0948, \u0914\u0930 \u0915\u0938\u094d\u091f\u092e \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0907\u0938\u0940 \u0915\u094b \u0907\u0902\u092a\u094b\u0930\u094d\u091f \u0915\u093f\u092f\u093e \u091c\u093e\u0924\u093e \u0939\u0948\u0964",
    "f3q": "\u0915\u094d\u092f\u093e tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u0947 \u0932\u093f\u090f \u091c\u0947\u0932\u092c\u094d\u0930\u0947\u0915 \u091a\u093e\u0939\u093f\u090f?",
    "f3a": "\u0928\u0939\u0940\u0902\u0964 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 Nugget \u091f\u0942\u0932 \u0938\u0947 \u0932\u0917\u093e\u090f \u091c\u093e\u0924\u0947 \u0939\u0948\u0902, \u091c\u094b \u092b\u093c\u093e\u0907\u0932\u0947\u0902 \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u0930\u0942\u092a \u0938\u0947 \u0938\u0902\u0936\u094b\u0927\u093f\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f Apple \u0915\u0947 SparseRestore \u0914\u0930 BookRestore \u092e\u0948\u0915\u0947\u0928\u093f\u091c\u094d\u092e \u0915\u093e \u0909\u092a\u092f\u094b\u0917 \u0915\u0930\u0924\u093e \u0939\u0948 &mdash; \u091c\u0947\u0932\u092c\u094d\u0930\u0947\u0915 \u0915\u0940 \u091c\u093c\u0930\u0942\u0930\u0924 \u0928\u0939\u0940\u0902 \u0939\u0948\u0964",
    "f4q": "\u0915\u093f\u0928 iOS \u0935\u0930\u094d\u091c\u0928 \u092a\u0930 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0938\u092e\u0930\u094d\u0925\u093f\u0924 \u0939\u0948\u0902?",
    "f4a": "tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0938\u0902\u0917\u0924 iPhone \u0914\u0930 iPad \u092a\u0930 iOS \u0914\u0930 iPadOS 17-27 \u0915\u093e \u0938\u092e\u0930\u094d\u0925\u0928 \u0915\u0930\u0924\u0947 \u0939\u0948\u0902\u0964 \u0915\u0941\u091b \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u094b \u0935\u093f\u0936\u0947\u0937 iOS \u0935\u0930\u094d\u091c\u0928 \u0915\u0940 \u0930\u093e\u0936\u094d\u0924\u0947\u0928 \u0939\u094b \u0938\u0915\u0924\u0940 \u0939\u0948, \u0907\u0938\u0932\u093f\u090f \u0939\u092e\u0947\u0936\u093e \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092a\u0947\u091c \u092a\u0930 \u0915\u092e\u094d\u092a\u0947\u091f\u093f\u092c\u093f\u0932\u093f\u091f\u0940 \u0928\u094b\u091f \u0926\u0947\u0916\u0947\u0902\u0964",
    "f5q": "\u092e\u0948\u0902 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0915\u0939\u093e\u0902 \u0938\u0947 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930 \u0938\u0915\u0924\u093e \u0939\u0942\u0902?",
    "f5a": "mwallx.com \u092a\u0930 Nugget Wallpaper \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0938\u0947 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092c\u094d\u0930\u093e\u0909\u091c\u093c \u0914\u0930 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902, \u091c\u0939\u093e\u0902 \u090f\u0928\u093f\u092e\u0947, \u0938\u094d\u092a\u094b\u0930\u094d\u091f\u094d\u0938, Marvel \u0938\u0939\u093f\u0924 \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0914\u0930 \u0938\u094d\u091f\u0948\u091f\u093f\u0915 \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u093e \u091a\u0941\u0928\u093f\u0902\u0926\u093e \u0938\u0902\u0917\u094d\u0930\u0939 \u0939\u0948\u0964",
    "f6q": "\u092e\u0948\u0902 \u0905\u092a\u0928\u0947 iPhone \u092a\u0930 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0915\u0948\u0938\u0947 \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u0930\u0942\u0902?",
    "f6a": ".tendies \u092b\u093c\u093e\u0907\u0932 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902, Nugget \u092e\u0947\u0902 PosterBoard \u092b\u0940\u091a\u0930 \u0916\u094b\u0932\u0947\u0902, \u092b\u093c\u093e\u0907\u0932 \u091a\u0941\u0928\u0947\u0902, \u0932\u093e\u0917\u0942 \u0915\u0930\u0947\u0902 \u0914\u0930 \u0921\u093f\u0935\u093e\u0907\u0938 \u0930\u0940\u092c\u0942\u091f \u0915\u0930\u0947\u0902\u0964 \u0930\u0940\u092c\u0942\u091f \u0915\u0947 \u092c\u093e\u0926 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u090f\u0921\u093f\u091f\u0930 \u0916\u094b\u0932\u0947\u0902 \u0914\u0930 Collections \u092f\u093e Favorites \u092e\u0947\u0902 \u0928\u092f\u093e \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0926\u0947\u0916\u0947\u0902\u0964",
    "f7q": "\u0915\u094d\u092f\u093e tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0907\u0938\u094d\u0924\u0947\u092e\u093e\u0932 \u0915\u0930\u0928\u093e \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u0939\u0948?",
    "f7a": "Nugget \u090f\u0915 \u0935\u094d\u092f\u093e\u092a\u0915 \u0930\u0942\u092a \u0938\u0947 \u0909\u092a\u092f\u094b\u0917 \u0915\u093f\u092f\u093e \u091c\u093e\u0928\u0947 \u0935\u093e\u0932\u093e \u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 \u092a\u094d\u0930\u094b\u091c\u0947\u0915\u094d\u091f \u0939\u0948 \u091c\u093f\u0938\u0915\u0947 \u0939\u091c\u093e\u0930\u094b\u0902 \u0909\u092a\u092f\u094b\u0917\u0915\u0930\u094d\u0924\u093e \u0939\u0948\u0902\u0964 \u0915\u093f\u0938\u0940 \u092d\u0940 \u0938\u093f\u0938\u094d\u091f\u092e \u0938\u0902\u0936\u094b\u0927\u0928 \u0915\u0940 \u0924\u0930\u0939, \u092a\u0939\u0932\u0947 \u0905\u092a\u0928\u0947 \u0921\u093f\u0935\u093e\u0907\u0938 \u0915\u093e \u092c\u0948\u0915\u0905\u092a \u0932\u0947\u0902\u0964 iTunes \u092f\u093e Finder \u0938\u0947 \u0921\u093f\u0935\u093e\u0907\u0938 \u0930\u093f\u0938\u094d\u091f\u094b\u0930 \u0915\u0930\u0915\u0947 \u092c\u0926\u0932\u093e\u0935 \u0909\u0932\u091f\u093e\u092f\u093e \u091c\u093e \u0938\u0915\u0924\u093e \u0939\u0948\u0964",
    "f8q": "Nugget Wallpaper \u0914\u0930 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u092e\u0947\u0902 \u0915\u094d\u092f\u093e \u0905\u0902\u0924\u0930 \u0939\u0948?",
    "f8a": "Tendies Wallpaper \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u0947 \u0938\u0902\u0917\u094d\u0930\u0939 \u0915\u093e \u092c\u094d\u0930\u093e\u0902\u0921 \u0928\u093e\u092e \u0939\u0948, \u091c\u092c\u0915\u093f Nugget Wallpaper (mwallx.com) \u0935\u0939 \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0939\u0948 \u091c\u094b \u0909\u0928\u094d\u0939\u0947\u0902 \u0939\u094b\u0938\u094d\u091f \u0915\u0930\u0924\u0940 \u0939\u0948\u0964 \u0926\u094b\u0928\u094b\u0902 \u090f\u0915 \u0939\u0940 \u0907\u0915\u094b\u0938\u093f\u0938\u094d\u091f\u092e \u0915\u093e \u0939\u093f\u0938\u094d\u0938\u093e \u0939\u0948\u0902, \u091c\u094b iOS \u0915\u0938\u094d\u091f\u092e\u093e\u0907\u091c\u093c\u0947\u0936\u0928 \u0915\u0947 \u0932\u093f\u090f \u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 Nugget \u091f\u0942\u0932 \u0926\u094d\u0935\u093e\u0930\u093e \u0938\u0902\u091a\u093e\u0932\u093f\u0924 \u0939\u0948\u0964",
    "comm_h2": "Nugget Wallpaper \u0915\u092e\u094d\u092f\u0942\u0928\u093f\u091f\u0940 \u0938\u0947 \u091c\u0941\u0921\u093c\u0947\u0902",
    "comm_p": "\u0928\u090f \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0930\u093f\u0932\u0940\u091c\u093c, \u092a\u094d\u0930\u0940\u0935\u094d\u092f\u0942 \u0914\u0930 \u0924\u094d\u0935\u0930\u093f\u0924 \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u091f\u093f\u092a\u094d\u0938 \u0915\u0947 \u0932\u093f\u090f \u091a\u0948\u0928\u0932\u094d\u0938 \u092b\u0949\u0932\u094b \u0915\u0930\u0947\u0902\u0964",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "\u0906\u0927\u093f\u0915\u093e\u0930\u093f\u0915 iOS \u091f\u0942\u0932 \u0938\u093e\u0907\u091f",
    "cta_h2": "\u0905\u092a\u0928\u0940 \u0932\u0949\u0915 \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0915\u094b \u091c\u0940\u0935\u093f\u0924 \u092c\u0928\u093e\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0924\u0948\u092f\u093e\u0930?",
    "cta_p": "\u0906\u091c \u0939\u0940 \u092e\u0941\u092b\u093c\u094d\u0924 tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0921\u093e\u0909\u0928\u0932\u094b\u0921 \u0915\u0930\u0947\u0902 &mdash; \u091c\u0947\u0932\u092c\u094d\u0930\u0947\u0915 \u0915\u0940 \u091c\u093c\u0930\u0942\u0930\u0924 \u0928\u0939\u0940\u0902\u0964 Nugget Wallpaper \u0938\u093e\u0907\u091f \u092a\u0930 \u092a\u0942\u0930\u0940 \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0926\u0947\u0916\u0947\u0902, \u0915\u0940\u092e\u0924\u0947\u0902 \u091c\u093e\u0928\u0947\u0902, \u0911\u0930\u094d\u0921\u0930 \u091f\u094d\u0930\u0948\u0915 \u0915\u0930\u0947\u0902 \u0914\u0930 \u0938\u094d\u091f\u0947\u092a-\u092c\u093e\u0908-\u0938\u094d\u091f\u0947\u092a \u091f\u094d\u092f\u0942\u091f\u094b\u0930\u093f\u092f\u0932 \u092a\u095d\u0947\u0902\u0964",
    "cta_btn1": "\u090f\u0915\u094d\u0938\u092a\u094d\u0932\u094b\u0930 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902",
    "cta_btn2": "\u0915\u0940\u092e\u0924\u0947\u0902 \u0926\u0947\u0916\u0947\u0902",
    "foot_tw1": "\u0939\u094b\u092e",
    "foot_tw2": "\u0915\u094d\u092f\u093e \u0939\u0948",
    "foot_tw3": ".tendies \u092b\u093c\u093e\u0907\u0932",
    "foot_tw4": "\u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0917\u093e\u0907\u0921",
    "foot_nw1": "\u0938\u092d\u0940 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0926\u0947\u0916\u0947\u0902",
    "foot_nw2": "\u0928\u090f \u091c\u094b\u0921\u093c\u0947 \u0917\u090f",
    "foot_nw3": "\u0905\u092d\u0940 \u091f\u094d\u0930\u0947\u0902\u0921\u093f\u0902\u0917",
    "foot_nw4": "\u0907\u0902\u092a\u094b\u0930\u094d\u091f \u091f\u094d\u092f\u0942\u091f\u094b\u0930\u093f\u092f\u0932",
    "foot_pr1": "GitHub \u092a\u0930 Nugget",
    "foot_pr3": "\u0915\u0940\u092e\u0924\u0947\u0902",
    "foot_pr4": "\u0911\u0930\u094d\u0921\u0930",
    "foot_pol1": "\u092a\u094d\u0930\u093e\u0907\u0935\u0947\u0938\u0940 \u092a\u0949\u0932\u093f\u0938\u0940",
    "foot_pol2": "\u0928\u093f\u092f\u092e \u0914\u0930 \u0936\u0930\u094d\u0924\u0947\u0902",
    "foot_pol3": "DMCA \u092a\u0949\u0932\u093f\u0938\u0940",
    "foot_pol4": "UGC \u092a\u0949\u0932\u093f\u0938\u0940",
    "copyright": "Tendies Wallpaper, <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> \u092a\u0930 \u0939\u094b\u0938\u094d\u091f \u0915\u0940 \u0917\u0908 \u091a\u0941\u0928\u093f\u0902\u0926\u093e \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0915\u093e \u092a\u0930\u093f\u091a\u092f \u0914\u0930 \u0930\u0947\u092b\u093c\u0930\u0932 \u092a\u0947\u091c \u0939\u0948\u0964 Nugget \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0913\u092a\u0928-\u0938\u094b\u0930\u094d\u0938 Nugget \u091f\u0942\u0932 (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>) \u0938\u0947 \u0932\u0917\u093e\u090f \u091c\u093e\u0924\u0947 \u0939\u0948\u0902\u0964 Apple, iPhone, iPad \u0914\u0930 iOS Apple Inc. \u0915\u0947 \u091f\u094d\u0930\u0947\u0921\u092e\u093e\u0930\u094d\u0915 \u0939\u0948\u0902\u0964 \u092f\u0939 \u0938\u093e\u0907\u091f Apple \u0938\u0947 \u0938\u0902\u092c\u0926\u094d\u0927 \u0928\u0939\u0940\u0902 \u0939\u0948\u0964",
    "title": "Tendies Wallpaper &mdash; Nugget \u0915\u0947 \u0932\u093f\u090f iOS \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0935\u0949\u0932\u092a\u0947\u092a\u0930",
    "desc": "Tendies Wallpaper, Nugget \u0915\u0947 \u0932\u093f\u090f \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 iOS \u0914\u0930 iPadOS \u0935\u0949\u0932\u092a\u0947\u092a\u0930\u094b\u0902 \u0915\u093e \u0939\u094b\u092e \u0939\u0948\u0964 \u091c\u093e\u0928\u0947\u0902 .tendies \u092b\u093c\u093e\u0907\u0932 \u0915\u094d\u092f\u093e \u0939\u0948, \u092c\u093f\u0928\u093e \u091c\u0947\u0932\u092c\u094d\u0930\u0947\u0915 \u0915\u0947 \u090f\u0928\u093f\u092e\u0947\u091f\u0947\u0921 \u0932\u0949\u0915-\u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0935\u0949\u0932\u092a\u0947\u092a\u0930 \u0915\u0948\u0938\u0947 \u0907\u0902\u0938\u094d\u091f\u0949\u0932 \u0915\u0930\u0947\u0902, \u0914\u0930 Nugget Wallpaper \u092a\u0930 \u092a\u0942\u0930\u0940 \u0932\u093e\u0907\u092c\u094d\u0930\u0947\u0930\u0940 \u0926\u0947\u0916\u0947\u0902\u0964",
    "kw": "tendies \u0935\u0949\u0932\u092a\u0947\u092a\u0930, tendies \u092b\u093c\u093e\u0907\u0932, Nugget \u0935\u0949\u0932\u092a\u0947\u092a\u0930, iOS \u0921\u093e\u092f\u0928\u093e\u092e\u093f\u0915 \u0935\u0949\u0932\u092a\u0947\u092a\u0930, PosterBoard \u0935\u0949\u0932\u092a\u0947\u092a\u0930, ios 18 \u0935\u0949\u0932\u092a\u0947\u092a\u0930, ios 27 \u0935\u0949\u0932\u092a\u0947\u092a\u0930, \u090f\u0928\u093f\u092e\u0947\u091f\u0947\u0921 \u0932\u0949\u0915 \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u0935\u0949\u0932\u092a\u0947\u092a\u0930",
}

T["fr"] = {
    "nav_wiki": "Qu'est-ce que c'est",
    "nav_install": "Installer",
    "nav_gallery": "Galerie",
    "nav_faq": "FAQ",
    "nav_cta": "Voir les fonds",
    "lang_label": "Langue",
    "hero_kicker": "Le site officiel de Tendies Wallpaper",
    "hero_h1_lead": "Fonds d'\u00e9cran dynamiques iOS pour",
    "hero_h1_after": "Votre \u00e9cran de verrouillage s'anime.",
    "hero_lead": "Tendies Wallpaper est une collection soigneusement s\u00e9lectionn\u00e9e de fonds d'\u00e9cran anim\u00e9s et dynamiques pour iPhone et iPad, install\u00e9s via l'outil open source Nugget avec un simple fichier .tendies. Sans jailbreak, sans compromis. Compatible avec iOS et iPadOS 17&ndash;27.",
    "hero_btn1": "Explorer la biblioth\u00e8que",
    "hero_btn2": "Comment installer",
    "hero_btn3": "Lire le tutoriel",
    "stat1b": "Compatibilit\u00e9 toutes versions",
    "stat2b": "Utilise SparseRestore / BookRestore",
    "stat3b": "Open source et communautaire",
    "about_tag": "Qu'est-ce que Tendies Wallpaper ?",
    "about_h2": "Des fonds d'\u00e9cran anim\u00e9s pour iPhone et iPad, bien faits",
    "about_p": "Tendies Wallpaper est la marque derri\u00e8re une biblioth\u00e8que grandissante de fonds d'\u00e9cran dynamiques pour l'\u00e9cran de verrouillage, pens\u00e9e pour l'\u00e9cosyst\u00e8me Nugget. Chaque fond d'\u00e9cran est emball\u00e9 sous forme de <strong>fichier .tendies</strong> &mdash; un bundle PosterBoard qui transforme l'\u00e9cran de verrouillage natif d'Apple en une toile vivante. La collection compl\u00e8te est h\u00e9berg\u00e9e sur <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "Vraiment dynamique",
    "c1d": "Mouvement, profondeur et animation sur l'\u00e9cran de verrouillage natif, et non une image statique. Chaque fond tendies est con\u00e7u pour offrir une exp\u00e9rience d'\u00e9cran vivante premium.",
    "c2t": "Sans jailbreak",
    "c2d": "Les fonds tendies sont appliqu\u00e9s avec Nugget, qui utilise les m\u00e9canismes de restauration SparseRestore et BookRestore d'Apple pour \u00e9crire les fichiers en toute s\u00e9curit\u00e9.",
    "c3t": "Biblioth\u00e8que s\u00e9lectionn\u00e9e",
    "c3d": "Anime, manga, sport, Marvel, r\u00eaves spatiaux et plus encore, une galerie soigneusement choisie, mise \u00e0 jour chaque semaine sur le site de Nugget Wallpaper.",
    "c4t": "Propuls\u00e9 par Nugget",
    "c4d": "Construit sur l'outil open source <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> de leminlimez, adopt\u00e9 par une communaut\u00e9 de milliers d'utilisateurs.",
    "c5t": "iPhone et iPad",
    "c5d": "Fonctionne sur les iPhone et iPad compatibles sous iOS et iPadOS 17 \u00e0 27, avec ou sans Dynamic Island.",
    "c6t": "R\u00e9versible et s\u00fbr",
    "c6d": "Tout est r\u00e9versible. Sauvegardez avant d'appliquer ; restaurez via iTunes ou Finder \u00e0 tout moment pour revenir \u00e0 l'\u00e9tat d'origine.",
    "tendies_h2": "Qu'est-ce qu'un fichier tendies ?",
    "tendies_p": "Un <strong>fichier .tendies</strong> est le format de bundle de fonds d'\u00e9cran utilis\u00e9 dans l'\u00e9cosyst\u00e8me Nugget / PosterBoard (notamment Cowabunga et Pocket Poster). Il stocke la structure exacte des fichiers PosterBoard que Nugget restaure sur votre appareil, afin que le fond d'\u00e9cran apparaisse directement dans le s\u00e9lecteur natif de l'\u00e9cran de verrouillage.",
    "tv1_d": "Restaure directement dans le conteneur de l'app PosterBoard, en conservant la structure de fichiers et les ID des fonds inchang\u00e9s.",
    "tv2_d": "Restaure dans le dossier des descripteurs avec des UUID randomis\u00e9s pour que plusieurs fonds tendies ne se contredisent jamais.",
    "tv3_d": "Les variantes vid\u00e9o et photo ciblent Photos sugg\u00e9r\u00e9es ; les variantes mercury ciblent le Mercury Poster sur les versions iOS compatibles.",
    "install_tag": "Pour commencer",
    "install_h2": "Installez un fond tendies en 4 \u00e9tapes",
    "install_p": "Le processus complet prend quelques minutes avec un c\u00e2ble USB et l'app gratuite Nugget. Tous les d\u00e9tails sont dans le tutoriel officiel.",
    "s1_t": "T\u00e9l\u00e9chargez le fichier",
    "s1_d": "Choisissez un fond dans la biblioth\u00e8que et t\u00e9l\u00e9chargez son <strong>fichier .tendies</strong>.",
    "s2_t": "Connectez votre appareil",
    "s2_d": "Branchez votre iPhone/iPad \u00e0 votre ordinateur en USB et validez la confiance. Fonctionne sur Windows, macOS et Linux.",
    "s3_t": "Importez et appliquez",
    "s3_d": "Ouvrez PosterBoard dans Nugget, s\u00e9lectionnez le fichier, puis cliquez sur Apply Changes.",
    "s4_t": "Red\u00e9marrez et profitez",
    "s4_d": "Apr\u00e8s le red\u00e9marrage, ouvrez l'\u00e9diteur d'\u00e9cran de verrouillage et retrouvez votre fond dans Collections ou Favoris.",
    "install_note": "Un probl\u00e8me ? Lisez le <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">tutoriel officiel de Nugget Wallpaper</a> ou rejoignez les canaux communautaires ci-dessous.",
    "gallery_tag": "La biblioth\u00e8que",
    "gallery_h2": "Parcourir la galerie Tendies Wallpaper",
    "gallery_p": "Chaque fond tendies ci-dessous est h\u00e9berg\u00e9 et t\u00e9l\u00e9chargeable sur <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Triez la galerie par <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">R\u00e9cent</a> ou <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">Populaire</a> pour voir les tendances.",
    "g_t1": "Anime",
    "g_d1": "Evangelion, Sylphiette et plus",
    "g_t2": "Sport et Marvel",
    "g_d2": "Clubs, h\u00e9ros, nouveaux jours",
    "g_t3": "Paysages oniriques",
    "g_d3": "Plan\u00e8tes, \u00e9toiles et abstraits",
    "g_t4": "Officiel",
    "g_d4": "S\u00e9lections au style Apple",
    "gallery_cta": "Voir tous les fonds d'\u00e9cran",
    "faq_h2": "Questions fr\u00e9quentes",
    "faq_p": "Tout ce qu'il faut savoir sur les fonds tendies avant de commencer.",
    "f1q": "Qu'est-ce qu'un fond d'\u00e9cran tendies ?",
    "f1a": "Un fond tendies est un fond d'\u00e9cran dynamique et anim\u00e9 pour iPhone et iPad, fourni sous forme de fichier .tendies install\u00e9 via l'outil Nugget. Les fichiers tendies restaurent les descripteurs de fonds PosterBoard sur les appareils iOS 17-27, afin que le fond apparaisse dans le s\u00e9lecteur Collections de l'\u00e9cran de verrouillage.",
    "f2q": "Qu'est-ce qu'un fichier .tendies ?",
    "f2a": "Un fichier .tendies est le format de bundle utilis\u00e9 par Nugget et Pocket Poster. Il stocke la structure de fichiers PosterBoard restitu\u00e9e sur votre iPhone ou iPad, et c'est lui que vous importez pour installer un fond d'\u00e9cran dynamique personnalis\u00e9.",
    "f3q": "Les fonds tendies n\u00e9cessitent-ils un jailbreak ?",
    "f3a": "Non. Les fonds tendies sont appliqu\u00e9s avec l'outil open source Nugget, qui utilise les m\u00e9canismes SparseRestore et BookRestore d'Apple pour modifier les fichiers en toute s\u00e9curit\u00e9, sans jailbreak.",
    "f4q": "Quelles versions d'iOS prennent en charge les fonds tendies ?",
    "f4a": "Les fonds tendies prennent en charge iOS et iPadOS 17 \u00e0 27 sur les iPhone et iPad compatibles. Certains fonds peuvent exiger une version pr\u00e9cise d'iOS ; v\u00e9rifiez toujours les notes de compatibilit\u00e9 sur la page du fond.",
    "f5q": "O\u00f9 puis-je t\u00e9l\u00e9charger des fonds tendies ?",
    "f5a": "Parcourez et t\u00e9l\u00e9chargez les fonds tendies depuis la biblioth\u00e8que Nugget Wallpaper sur mwallx.com, qui h\u00e9berge une collection s\u00e9lectionn\u00e9e de fonds dynamiques et statiques, dont des anime, du sport, du Marvel et plus encore.",
    "f6q": "Comment installer un fond tendies sur mon iPhone ?",
    "f6a": "T\u00e9l\u00e9chargez le fichier .tendies, ouvrez la fonction PosterBoard dans Nugget, s\u00e9lectionnez le fichier, appliquez les changements et red\u00e9marrez. Apr\u00e8s red\u00e9marrage, ouvrez l'\u00e9diteur d'\u00e9cran de verrouillage et retrouvez le fond dans Collections ou Favoris.",
    "f7q": "Est-il s\u00fbr d'utiliser des fonds tendies ?",
    "f7a": "Nugget est un projet open source tr\u00e8s utilis\u00e9, adopt\u00e9 par des milliers d'utilisateurs. Comme pour toute modification syst\u00e8me, sauvegardez d'abord votre appareil. Les changements sont r\u00e9versibles en restaurant l'appareil via iTunes ou Finder.",
    "f8q": "Quelle est la diff\u00e9rence entre Nugget Wallpaper et les fonds tendies ?",
    "f8a": "Tendies Wallpaper est le nom de la marque de la collection de fonds dynamiques, tandis que Nugget Wallpaper (mwallx.com) est la biblioth\u00e8que qui les h\u00e9berge. Les deux font partie du m\u00eame \u00e9cosyst\u00e8me, propuls\u00e9 par l'outil open source Nugget de personnalisation iOS.",
    "comm_h2": "Rejoignez la communaut\u00e9 Nugget Wallpaper",
    "comm_p": "Suivez les canaux pour les nouveaut\u00e9s, aper\u00e7us et astuces d'installation.",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "Site officiel de l'outil iOS",
    "cta_h2": "Pr\u00eat \u00e0 donner vie \u00e0 votre \u00e9cran de verrouillage ?",
    "cta_p": "T\u00e9l\u00e9chargez d\u00e8s aujourd'hui un fond tendies gratuit, sans jailbreak. Parcourez la biblioth\u00e8que compl\u00e8te, consultez les prix, suivez vos commandes et lisez le tutoriel pas \u00e0 pas sur le site de Nugget Wallpaper.",
    "cta_btn1": "Commencer \u00e0 explorer",
    "cta_btn2": "Voir les tarifs",
    "foot_tw1": "Accueil",
    "foot_tw2": "Qu'est-ce que c'est",
    "foot_tw3": "Le fichier .tendies",
    "foot_tw4": "Guide d'installation",
    "foot_nw1": "Voir tous les fonds",
    "foot_nw2": "Derni\u00e8res nouveaut\u00e9s",
    "foot_nw3": "Populaires en ce moment",
    "foot_nw4": "Tutoriel d'import",
    "foot_pr1": "Nugget sur GitHub",
    "foot_pr2": "Outil officiel Nugget",
    "foot_pr3": "Tarifs",
    "foot_pr4": "Commandes",
    "foot_pol1": "Politique de confidentialit\u00e9",
    "foot_pol2": "Conditions d'utilisation",
    "foot_pol3": "Politique DMCA",
    "foot_pol4": "Politique UGC",
    "copyright": "Tendies Wallpaper est une page de pr\u00e9sentation et de r\u00e9f\u00e9rences de la biblioth\u00e8que h\u00e9berg\u00e9e sur <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Les fonds Nugget sont appliqu\u00e9s via l'outil open source Nugget (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple, iPhone, iPad et iOS sont des marques d'Apple Inc. Ce site n'est pas affili\u00e9 \u00e0 Apple.",
    "title": "Tendies Wallpaper &mdash; Fonds d'\u00e9cran dynamiques iOS pour Nugget",
    "desc": "Tendies Wallpaper est la maison des fonds d'\u00e9cran dynamiques iOS et iPadOS pour Nugget. D\u00e9couvrez ce qu'est un fichier .tendies, comment installer des fonds anim\u00e9s sans jailbreak et parcourez la biblioth\u00e8que compl\u00e8te sur Nugget Wallpaper.",
    "kw": "fond tendies, fichier tendies, fond Nugget, fond dynamique iOS, fond PosterBoard, fond iOS 18, fond iOS 27, fond anim\u00e9 \u00e9cran de verrouillage",
}

T["ar"] = {
    "nav_wiki": "\u0645\u0627 \u0647\u064a",
    "nav_install": "\u0627\u0644\u062a\u062b\u0628\u064a\u062a",
    "nav_gallery": "\u0627\u0644\u0645\u0639\u0631\u0636",
    "nav_faq": "FAQ",
    "nav_cta": "\u062a\u0635\u0641\u062d \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a",
    "lang_label": "\u0627\u0644\u0644\u063a\u0629",
    "hero_kicker": "\u0627\u0644\u0645\u0648\u0642\u0639 \u0627\u0644\u0631\u0633\u0645\u064a \u0644\u0640 Tendies Wallpaper",
    "hero_h1_lead": "\u062e\u0644\u0641\u064a\u0627\u062a iOS \u0627\u0644\u0645\u062a\u062d\u0631\u0643\u0629 \u0644\u0640",
    "hero_h1_after": "\u0634\u0627\u0634\u0629 \u0642\u0641\u0644\u0643\u060c \u062a\u0646\u0628\u0636 \u0628\u0627\u0644\u062d\u064a\u0627\u0629.",
    "hero_lead": "Tendies Wallpaper \u0647\u0648 \u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u062e\u062a\u0627\u0631\u0629 \u0645\u0646 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u0645\u062a\u062d\u0631\u0643\u0629 \u0648\u0627\u0644\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0644\u0622\u064a\u0641\u0648\u0646 \u0648\u0622\u064a\u0628\u0627\u062f\u060c \u062a\u064f\u062b\u0628\u0651\u062a \u0639\u0628\u0631 \u0623\u062f\u0627\u0629 Nugget \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631 \u0628\u0645\u0644\u0641 .tendies \u0628\u0633\u064a\u0637\u060c \u062f\u0648\u0646 \u062c\u064a\u0644\u0628\u0631\u064a\u0643 \u0648\u0628\u062f\u0648\u0646 \u0623\u064a \u062a\u0646\u0627\u0632\u0644\u0627\u062a. \u0645\u062a\u0648\u0627\u0641\u0642 \u0645\u0639 iOS \u0648 iPadOS 17&ndash;27.",
    "hero_btn1": "\u0627\u0633\u062a\u0643\u0634\u0641 \u0645\u0643\u062a\u0628\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a",
    "hero_btn2": "\u0643\u064a\u0641\u064a\u0629 \u0627\u0644\u062a\u062b\u0628\u064a\u062a",
    "hero_btn3": "\u0627\u0642\u0631\u0623 \u0627\u0644\u062f\u0644\u064a\u0644",
    "stat1b": "\u062f\u0639\u0645 \u0643\u0627\u0645\u0644 \u0644\u0643\u0644 \u0627\u0644\u0625\u0635\u062f\u0627\u0631\u0627\u062a",
    "stat2b": "\u064a\u0639\u062a\u0645\u062f SparseRestore / BookRestore",
    "stat3b": "\u0645\u0641\u062a\u0648\u062d \u0627\u0644\u0645\u0635\u062f\u0631 \u0648\u0628\u0631\u0639\u0627\u064a\u0629 \u0627\u0644\u0645\u062c\u062a\u0645\u0639",
    "about_tag": "\u0645\u0627 \u0647\u064a Tendies Wallpaper\u061f",
    "about_h2": "\u062e\u0644\u0641\u064a\u0627\u062a \u0645\u062a\u062d\u0631\u0643\u0629 \u0644\u0622\u064a\u0641\u0648\u0646 \u0648\u0622\u064a\u0628\u0627\u062f\u060c \u0645\u064f\u062a\u0642\u0646\u0629 \u0627\u0644\u0635\u0646\u0639",
    "about_p": "Tendies Wallpaper \u0647\u064a \u0627\u0644\u0639\u0644\u0627\u0645\u0629 \u062e\u0644\u0641 \u0645\u0643\u062a\u0628\u0629 \u0645\u062a\u0646\u0627\u0645\u064a\u0629 \u0645\u0646 \u062e\u0644\u0641\u064a\u0627\u062a \u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644 \u0627\u0644\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0627\u0644\u0645\u062e\u0635\u0635\u0629 \u0644\u0646\u0638\u0627\u0645 Nugget \u0627\u0644\u0628\u064a\u0626\u064a. \u062a\u064f\u063a\u0644\u0651\u0641 \u0643\u0644 \u062e\u0644\u0641\u064a\u0629 \u0643\u0645\u0644\u0641 <strong>.tendies</strong> &mdash; \u062d\u0632\u0645\u0629 \u062e\u0644\u0641\u064a\u0627\u062a PosterBoard \u062a\u062d\u0648\u0651\u0644 \u0634\u0627\u0634\u0629 \u0642\u0641\u0644 \u0622\u0628\u0644 \u0627\u0644\u0623\u0635\u0644\u064a\u0629 \u0625\u0644\u0649 \u0644\u0648\u062d\u0629 \u0646\u0627\u0628\u0636\u0629 \u0628\u0627\u0644\u062d\u064a\u0627\u0629. \u062a\u064f\u0633\u062a\u0636\u0627\u0641 \u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u0627\u0644\u0643\u0627\u0645\u0644\u0629 \u0639\u0644\u0649 <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0628\u0627\u0644\u0643\u0627\u0645\u0644",
    "c1d": "\u062d\u0631\u0643\u0629 \u0648\u0639\u0645\u0642 \u0648\u0623\u0646\u064a\u0645\u064a\u0634\u0646 \u0639\u0644\u0649 \u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644 \u0627\u0644\u0623\u0635\u0644\u064a\u0629\u060c \u0648\u0644\u064a\u0633 \u0635\u0648\u0631\u0629 \u062b\u0627\u0628\u062a\u0629. \u0635\u064f\u0645\u0651\u0645\u062a \u0643\u0644 \u062e\u0644\u0641\u064a\u0629 tendies \u0644\u062a\u0645\u0646\u062d\u0643 \u0625\u062d\u0633\u0627\u0633\u0627\u064b \u0628\u0634\u0627\u0634\u0629 \u062d\u064a\u0651\u0629 \u0641\u0627\u062e\u0631\u0629.",
    "c2t": "\u062f\u0648\u0646 \u062c\u064a\u0644\u0628\u0631\u064a\u0643",
    "c2d": "\u062a\u064f\u0637\u0628\u0651\u0642 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u0639\u0628\u0631 Nugget \u0627\u0644\u0630\u064a \u064a\u0633\u062a\u062e\u062f\u0645 \u0622\u0644\u064a\u0627\u062a \u0627\u0644\u0627\u0633\u062a\u0639\u0627\u062f\u0629 \u0627\u0644\u062e\u0627\u0635\u0629 \u0628\u0622\u0628\u0644 SparseRestore \u0648 BookRestore \u0644\u0643\u062a\u0627\u0628\u0629 \u0627\u0644\u0645\u0644\u0641\u0627\u062a \u0628\u0623\u0645\u0627\u0646.",
    "c3t": "\u0645\u0643\u062a\u0628\u0629 \u0645\u062e\u062a\u0627\u0631\u0629",
    "c3d": "\u0623\u0646\u064a\u0645\u064a\u060c \u0645\u0627\u0646\u062c\u0627\u060c \u0631\u064a\u0627\u0636\u0629\u060c \u0645\u0627\u0631\u0641\u0644\u060c \u0639\u0648\u0627\u0644\u0645 \u0641\u0636\u0627\u0626\u064a\u0629 \u062d\u0627\u0644\u0645\u0629 \u0648\u0627\u0644\u0645\u0632\u064a\u062f: \u0645\u0639\u0631\u0636 \u0645\u0646\u062a\u0642\u0649 \u064a\u064f\u062d\u062f\u0651\u062b \u0623\u0633\u0628\u0648\u0639\u064a\u0627\u064b \u0639\u0644\u0649 \u0645\u0648\u0642\u0639 Nugget Wallpaper.",
    "c4t": "\u0645\u062f\u0639\u0648\u0645 \u0645\u0646 Nugget",
    "c4d": "\u0645\u0628\u0646\u064a \u0639\u0644\u0649 \u0623\u062f\u0627\u0629 <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631 \u0645\u0646 leminlimez\u060c \u0648\u062a\u062b\u0642 \u0628\u0647\u0627 \u0645\u062c\u062a\u0645\u0639\u0627\u062a \u062a\u0636\u0645 \u0622\u0644\u0627\u0641 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646.",
    "c5t": "\u0622\u064a\u0641\u0648\u0646 \u0648\u0622\u064a\u0628\u0627\u062f",
    "c5d": "\u064a\u0639\u0645\u0644 \u0639\u0644\u0649 \u0623\u062c\u0647\u0632\u0629 \u0622\u064a\u0641\u0648\u0646 \u0648\u0622\u064a\u0628\u0627\u062f \u0627\u0644\u0645\u062a\u0648\u0627\u0641\u0642\u0629 \u0627\u0644\u062a\u064a \u062a\u0634\u063a\u0651\u0644 iOS \u0648 iPadOS \u0645\u0646 17 \u0625\u0644\u0649 27\u060c \u0645\u0639 \u0623\u0648 \u0628\u062f\u0648\u0646 Dynamic Island.",
    "c6t": "\u0639\u0643\u0633\u064a \u0648\u0622\u0645\u0646",
    "c6d": "\u0643\u0644 \u0634\u064a\u0621 \u0642\u0627\u0628\u0644 \u0644\u0644\u0639\u0643\u0633. \u0627\u062d\u062a\u0641\u0638 \u0628\u0646\u0633\u062e\u0629 \u0627\u062d\u062a\u064a\u0627\u0637\u064a\u0629 \u0642\u0628\u0644 \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u061b \u0648\u0627\u0633\u062a\u0639\u062f \u0639\u0628\u0631 iTunes \u0623\u0648 Finder \u0641\u064a \u0623\u064a \u0648\u0642\u062a \u0644\u0644\u0639\u0648\u062f\u0629 \u0644\u0644\u0648\u0636\u0639 \u0627\u0644\u0623\u0635\u0644\u064a.",
    "tendies_h2": "\u0645\u0627 \u0647\u0648 \u0645\u0644\u0641 tendies\u061f",
    "tendies_p": "<strong>\u0645\u0644\u0641 .tendies</strong> \u0647\u0648 \u0635\u064a\u063a\u0629 \u062d\u0632\u0645 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0629 \u0641\u064a \u0646\u0638\u0627\u0645 Nugget / PosterBoard \u0627\u0644\u0628\u064a\u0626\u064a (\u0628\u0645\u0627 \u0641\u064a \u0630\u0644\u0643 Cowabunga \u0648 Pocket Poster). \u064a\u062e\u0632\u0651\u0646 \u0628\u0646\u064a\u0629 \u0645\u0644\u0641\u0627\u062a PosterBoard \u0627\u0644\u062f\u0642\u064a\u0642\u0629 \u0627\u0644\u062a\u064a \u064a\u0633\u062a\u0639\u064a\u062f\u0647\u0627 Nugget \u0639\u0644\u0649 \u062c\u0647\u0627\u0632\u0643\u060c \u0644\u062a\u0638\u0647\u0631 \u0627\u0644\u062e\u0644\u0641\u064a\u0629 \u0645\u0628\u0627\u0634\u0631\u0629 \u062f\u0627\u062e\u0644 \u0645\u0646\u062a\u0642\u064a \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u0623\u0635\u0644\u064a \u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644.",
    "tv1_d": "\u064a\u0633\u062a\u0639\u064a\u062f \u0645\u0628\u0627\u0634\u0631\u0629 \u0625\u0644\u0649 \u062d\u0627\u0648\u064a\u0629 \u062a\u0637\u0628\u064a\u0642 PosterBoard \u0645\u0639 \u0627\u0644\u062d\u0641\u0627\u0638 \u0639\u0644\u0649 \u0628\u0646\u064a\u0629 \u0627\u0644\u0645\u0644\u0641\u0627\u062a \u0648\u0645\u0639\u0631\u0651\u0641\u0627\u062a \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u062f\u0648\u0646 \u062a\u063a\u064a\u064a\u0631.",
    "tv2_d": "\u064a\u0633\u062a\u0639\u064a\u062f \u0625\u0644\u0649 \u0645\u062c\u0644\u062f \u0648\u0627\u0635\u0641\u0627\u062a \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0628\u0645\u0639\u0631\u0651\u0641\u0627\u062a UUID \u0639\u0634\u0648\u0627\u0626\u064a\u0629 \u062d\u062a\u0649 \u0644\u0627 \u062a\u062a\u0639\u0627\u0631\u0636 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u0627\u0644\u0645\u062a\u0639\u062f\u062f\u0629 \u0645\u0639 \u0628\u0639\u0636\u0647\u0627 \u0623\u0628\u062f\u0627\u064b.",
    "tv3_d": "\u0645\u062a\u063a\u064a\u0631\u0627\u062a \u0627\u0644\u0641\u064a\u062f\u064a\u0648 \u0648\u0627\u0644\u0635\u0648\u0631 \u062a\u0633\u062a\u0647\u062f\u0641 Suggested Photos\u061b \u0648\u0645\u062a\u063a\u064a\u0631\u0627\u062a mercury \u062a\u0633\u062a\u0647\u062f\u0641 Mercury Poster \u0639\u0644\u0649 \u0625\u0635\u062f\u0627\u0631\u0627\u062a iOS \u0627\u0644\u0645\u062f\u0639\u0648\u0645\u0629.",
    "install_tag": "\u0628\u062f\u0621 \u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645",
    "install_h2": "\u062b\u0628\u0651\u062a \u062e\u0644\u0641\u064a\u0629 tendies \u0641\u064a 4 \u062e\u0637\u0648\u0627\u062a",
    "install_p": "\u062a\u0633\u062a\u063a\u0631\u0642 \u0627\u0644\u0639\u0645\u0644\u064a\u0629 \u0628\u0623\u0643\u0645\u0644\u0647\u0627 \u0628\u0636\u0639 \u062f\u0642\u0627\u0626\u0642 \u0628\u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u0643\u0627\u0628\u0644 USB \u0648\u062a\u0637\u0628\u064a\u0642 Nugget \u0627\u0644\u0645\u062c\u0627\u0646\u064a. \u0627\u0644\u062a\u0641\u0627\u0635\u064a\u0644 \u0627\u0644\u0643\u0627\u0645\u0644\u0629 \u0641\u064a \u0627\u0644\u062f\u0644\u064a\u0644 \u0627\u0644\u0631\u0633\u0645\u064a.",
    "s1_t": "\u062d\u0645\u0651\u0644 \u0627\u0644\u0645\u0644\u0641",
    "s1_d": "\u0627\u062e\u062a\u0631 \u062e\u0644\u0641\u064a\u0629 \u0645\u0646 \u0627\u0644\u0645\u0643\u062a\u0628\u0629 \u0648\u062d\u0645\u0651\u0644 <strong>\u0645\u0644\u0641\u0647\u0627 .tendies</strong>.",
    "s2_t": "\u0635\u0644 \u062c\u0647\u0627\u0632\u0643",
    "s2_d": "\u0635\u0644 \u0622\u064a\u0641\u0648\u0646\u0643/\u0622\u064a\u0628\u0627\u062f\u0643 \u0628\u0627\u0644\u0643\u0645\u0628\u064a\u0648\u062a\u0631 \u0639\u0628\u0631 USB \u0648\u0627\u062e\u062a\u0631 \u0627\u0644\u0648\u062b\u0648\u0642. \u064a\u0639\u0645\u0644 \u0639\u0644\u0649 Windows \u0648 macOS \u0648 Linux.",
    "s3_t": "\u0627\u0633\u062a\u0648\u0631\u062f \u0648\u0637\u0628\u0651\u0642",
    "s3_d": "\u0627\u0641\u062a\u062d PosterBoard \u062f\u0627\u062e\u0644 Nugget\u060c \u0648\u0627\u062e\u062a\u0631 \u0627\u0644\u0645\u0644\u0641\u060c \u062b\u0645 \u0627\u0636\u063a\u0637 Apply Changes.",
    "s4_t": "\u0623\u0639\u062f \u0627\u0644\u062a\u0634\u063a\u064a\u0644 \u0648\u0627\u0633\u062a\u0645\u062a\u0639",
    "s4_d": "\u0628\u0639\u062f \u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u062a\u0634\u063a\u064a\u0644 \u0627\u0641\u062a\u062d \u0645\u062d\u0631\u0631 \u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644 \u0648\u0633\u062a\u062c\u062f \u062e\u0644\u0641\u064a\u062a\u0643 \u0627\u0644\u062c\u062f\u064a\u062f\u0629 \u0636\u0645\u0646 Collections \u0623\u0648 Favorites.",
    "install_note": "\u062a\u0648\u0627\u062c\u0647 \u0645\u0634\u0643\u0644\u0629\u061f \u0627\u0642\u0631\u0623 <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">\u062f\u0644\u064a\u0644 Nugget Wallpaper \u0627\u0644\u0631\u0633\u0645\u064a</a> \u0623\u0648 \u0627\u0646\u0636\u0645 \u0625\u0644\u0649 \u0642\u0646\u0648\u0627\u062a \u0627\u0644\u0645\u062c\u062a\u0645\u0639 \u0623\u062f\u0646\u0627\u0647.",
    "gallery_tag": "\u0627\u0644\u0645\u0643\u062a\u0628\u0629",
    "gallery_h2": "\u062a\u0635\u0641\u062d \u0645\u0639\u0631\u0636 Tendies Wallpaper",
    "gallery_p": "\u0643\u0644 \u062e\u0644\u0641\u064a\u0629 tendies \u0623\u062f\u0646\u0627\u0647 \u0645\u064f\u0633\u062a\u0636\u0627\u0641\u0629 \u0648\u0642\u0627\u0628\u0644\u0629 \u0644\u0644\u062a\u0646\u0632\u064a\u0644 \u0639\u0644\u0649 <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. \u0631\u062a\u0651\u0628 \u0627\u0644\u0645\u0639\u0631\u0636 \u062d\u0633\u0628 <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">\u0627\u0644\u0623\u062d\u062f\u062b</a> \u0623\u0648 <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">\u0627\u0644\u0623\u0643\u062b\u0631 \u0631\u0648\u0627\u062c\u0627\u064b</a> \u0644\u0645\u0634\u0627\u0647\u062f\u0629 \u0627\u0644\u0627\u062a\u062c\u0627\u0647\u0627\u062a.",
    "g_t1": "\u0623\u0646\u064a\u0645\u064a",
    "g_d1": "Eva\u060c Sylphiette \u0648\u0627\u0644\u0645\u0632\u064a\u062f",
    "g_t2": "\u0631\u064a\u0627\u0636\u0629 \u0648\u0645\u0627\u0631\u0641\u0644",
    "g_d2": "\u0623\u0646\u062f\u064a\u0629 \u0648\u0623\u0628\u0637\u0627\u0644 \u0648\u0623\u064a\u0627\u0645 \u062c\u062f\u064a\u062f\u0629",
    "g_t3": "\u0639\u0648\u0627\u0644\u0645 \u062d\u0627\u0644\u0645\u0629",
    "g_d3": "\u0643\u0648\u0627\u0643\u0628 \u0648\u0646\u062c\u0648\u0645 \u0648\u062a\u062c\u0631\u064a\u062f\u064a\u0627\u062a",
    "g_t4": "\u0631\u0633\u0645\u064a",
    "g_d4": "\u0645\u062e\u062a\u0627\u0631\u0627\u062a \u0628\u0623\u0633\u0644\u0648\u0628 \u0622\u0628\u0644",
    "gallery_cta": "\u0639\u0631\u0636 \u062c\u0645\u064a\u0639 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a",
    "faq_h2": "\u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0634\u0627\u0626\u0639\u0629",
    "faq_p": "\u0643\u0644 \u0645\u0627 \u062a\u062d\u062a\u0627\u062c \u0645\u0639\u0631\u0641\u062a\u0647 \u0639\u0646 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u0642\u0628\u0644 \u0627\u0644\u0628\u062f\u0621.",
    "f1q": "\u0645\u0627 \u0647\u064a \u062e\u0644\u0641\u064a\u0629 tendies\u061f",
    "f1a": "\u062e\u0644\u0641\u064a\u0629 tendies \u0647\u064a \u062e\u0644\u0641\u064a\u0629 \u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0645\u062a\u062d\u0631\u0643\u0629 \u0644\u0622\u064a\u0641\u0648\u0646 \u0648\u0622\u064a\u0628\u0627\u062f\u060c \u062a\u0623\u062a\u064a \u0643\u0645\u0644\u0641 .tendies \u064a\u064f\u062b\u0628\u0651\u062a \u0639\u0628\u0631 \u0623\u062f\u0627\u0629 Nugget. \u062a\u0633\u062a\u0639\u064a\u062f \u0645\u0644\u0641\u0627\u062a tendies \u0648\u0627\u0635\u0641\u0627\u062a \u062e\u0644\u0641\u064a\u0627\u062a PosterBoard \u0639\u0644\u0649 \u0623\u062c\u0647\u0632\u0629 iOS 17-27 \u0644\u062a\u0638\u0647\u0631 \u0627\u0644\u062e\u0644\u0641\u064a\u0629 \u0641\u064a \u0645\u0646\u062a\u0642\u064a Collections \u0628\u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644.",
    "f2q": "\u0645\u0627 \u0647\u0648 \u0645\u0644\u0641 .tendies\u061f",
    "f2a": "\u0645\u0644\u0641 .tendies \u0647\u0648 \u0635\u064a\u063a\u0629 \u062d\u0632\u0645 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0629 \u0641\u064a Nugget \u0648 Pocket Poster. \u064a\u062e\u0632\u0651\u0646 \u0628\u0646\u064a\u0629 \u0645\u0644\u0641\u0627\u062a PosterBoard \u0627\u0644\u062a\u064a \u062a\u064f\u0633\u062a\u0639\u0627\u062f \u0639\u0644\u0649 \u0622\u064a\u0641\u0648\u0646\u0643 \u0623\u0648 \u0622\u064a\u0628\u0627\u062f\u0643\u060c \u0648\u0647\u0648 \u0645\u0627 \u062a\u0633\u062a\u0648\u0631\u062f\u0647 \u0644\u062a\u062b\u0628\u064a\u062a \u062e\u0644\u0641\u064a\u0629 \u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0645\u062e\u0635\u0635\u0629 \u0644\u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644.",
    "f3q": "\u0647\u0644 \u062a\u062a\u0637\u0644\u0628 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u062c\u064a\u0644\u0628\u0631\u064a\u0643\u061f",
    "f3a": "\u0644\u0627. \u062a\u064f\u0637\u0628\u0651\u0642 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u0639\u0628\u0631 \u0623\u062f\u0627\u0629 Nugget \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631\u060c \u0627\u0644\u062a\u064a \u062a\u0633\u062a\u062e\u062f\u0645 \u0622\u0644\u064a\u062a\u064a SparseRestore \u0648 BookRestore \u0627\u0644\u062e\u0627\u0635\u062a\u064a\u0646 \u0628\u0622\u0628\u0644 \u0644\u062a\u0639\u062f\u064a\u0644 \u0627\u0644\u0645\u0644\u0641\u0627\u062a \u0628\u0623\u0645\u0627\u0646\u060c \u062f\u0648\u0646 \u0627\u0644\u062d\u0627\u062c\u0629 \u0625\u0644\u0649 \u062c\u064a\u0644\u0628\u0631\u064a\u0643.",
    "f4q": "\u0645\u0627 \u0625\u0635\u062f\u0627\u0631\u0627\u062a iOS \u0627\u0644\u062a\u064a \u062a\u062f\u0639\u0645 \u062e\u0644\u0641\u064a\u0627\u062a tendies\u061f",
    "f4a": "\u062a\u062f\u0639\u0645 \u062e\u0644\u0641\u064a\u0627\u062a tendies iOS \u0648 iPadOS \u0645\u0646 17 \u0625\u0644\u0649 27 \u0639\u0644\u0649 \u0623\u062c\u0647\u0632\u0629 \u0622\u064a\u0641\u0648\u0646 \u0648\u0622\u064a\u0628\u0627\u062f \u0627\u0644\u0645\u062a\u0648\u0627\u0641\u0642\u0629. \u0642\u062f \u062a\u062a\u0637\u0644\u0628 \u0628\u0639\u0636 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0625\u0635\u062f\u0627\u0631 iOS \u0645\u062d\u062f\u062f\u0627\u064b\u060c \u0644\u0630\u0627 \u062a\u062d\u0642\u0651\u0642 \u062f\u0627\u0626\u0645\u0627\u064b \u0645\u0646 \u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0627\u0644\u062a\u0648\u0627\u0641\u0642 \u0641\u064a \u0635\u0641\u062d\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0629.",
    "f5q": "\u0623\u064a\u0646 \u064a\u0645\u0643\u0646\u0646\u064a \u062a\u0646\u0632\u064a\u0644 \u062e\u0644\u0641\u064a\u0627\u062a tendies\u061f",
    "f5a": "\u062a\u0635\u0641\u062d \u0648\u062d\u0645\u0651\u0644 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u0645\u0646 \u0645\u0643\u062a\u0628\u0629 Nugget Wallpaper \u0639\u0644\u0649 mwallx.com\u060c \u0627\u0644\u062a\u064a \u062a\u0633\u062a\u0636\u064a\u0641 \u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u062e\u062a\u0627\u0631\u0629 \u0645\u0646 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0648\u0627\u0644\u062b\u0627\u0628\u062a\u0629\u060c \u0628\u0645\u0627 \u0641\u064a \u0630\u0644\u0643 \u0627\u0644\u0623\u0646\u064a\u0645\u064a \u0648\u0627\u0644\u0631\u064a\u0627\u0636\u0629 \u0648\u0645\u0627\u0631\u0641\u0644 \u0648\u063a\u064a\u0631\u0647\u0627.",
    "f6q": "\u0643\u064a\u0641 \u0623\u062b\u0628\u0651\u062a \u062e\u0644\u0641\u064a\u0629 tendies \u0639\u0644\u0649 \u0622\u064a\u0641\u0648\u0646\u064a\u061f",
    "f6a": "\u062d\u0645\u0651\u0644 \u0645\u0644\u0641 .tendies\u060c \u0648\u0627\u0641\u062a\u062d \u0645\u064a\u0632\u0629 PosterBoard \u062f\u0627\u062e\u0644 Nugget\u060c \u0648\u0627\u062e\u062a\u0631 \u0627\u0644\u0645\u0644\u0641\u060c \u0648\u0637\u0628\u0651\u0642 \u0627\u0644\u062a\u063a\u064a\u064a\u0631\u0627\u062a \u0648\u0623\u0639\u062f \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u062c\u0647\u0627\u0632. \u0628\u0639\u062f \u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u062a\u0634\u063a\u064a\u0644\u060c \u0627\u0641\u062a\u062d \u0645\u062d\u0631\u0631 \u0634\u0627\u0634\u0629 \u0627\u0644\u0642\u0641\u0644 \u0648\u0633\u062a\u062c\u062f \u0627\u0644\u062e\u0644\u0641\u064a\u0629 \u0636\u0645\u0646 Collections \u0623\u0648 Favorites.",
    "f7q": "\u0647\u0644 \u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u062e\u0644\u0641\u064a\u0627\u062a tendies \u0622\u0645\u0646\u061f",
    "f7a": "Nugget \u0645\u0634\u0631\u0648\u0639 \u0645\u0641\u062a\u0648\u062d \u0627\u0644\u0645\u0635\u062f\u0631 \u0648\u0627\u0633\u0639 \u0627\u0644\u0627\u0646\u062a\u0634\u0627\u0631 \u064a\u062b\u0642 \u0628\u0647 \u0622\u0644\u0627\u0641 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646. \u0648\u0643\u0623\u064a \u062a\u0639\u062f\u064a\u0644 \u0639\u0644\u0649 \u0627\u0644\u0646\u0638\u0627\u0645\u060c \u0627\u062d\u062a\u0641\u0638 \u0628\u0646\u0633\u062e\u0629 \u0627\u062d\u062a\u064a\u0627\u0637\u064a\u0629 \u0623\u0648\u0644\u0627\u064b. \u0627\u0644\u062a\u063a\u064a\u064a\u0631\u0627\u062a \u0642\u0627\u0628\u0644\u0629 \u0644\u0644\u0639\u0643\u0633 \u0628\u0627\u0633\u062a\u0639\u0627\u062f\u0629 \u0627\u0644\u062c\u0647\u0627\u0632 \u0639\u0628\u0631 iTunes \u0623\u0648 Finder.",
    "f8q": "\u0645\u0627 \u0627\u0644\u0641\u0631\u0642 \u0628\u064a\u0646 Nugget Wallpaper \u0648\u062e\u0644\u0641\u064a\u0627\u062a tendies\u061f",
    "f8a": "Tendies Wallpaper \u0647\u064a \u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u062a\u062c\u0627\u0631\u064a \u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629\u060c \u0628\u064a\u0646\u0645\u0627 Nugget Wallpaper (mwallx.com) \u0647\u064a \u0627\u0644\u0645\u0643\u062a\u0628\u0629 \u0627\u0644\u062a\u064a \u062a\u0633\u062a\u0636\u064a\u0641\u0647\u0627. \u0643\u0644\u0627\u0647\u0645\u0627 \u062c\u0632\u0621 \u0645\u0646 \u0646\u0638\u0627\u0645 \u0628\u064a\u0626\u064a \u0648\u0627\u062d\u062f\u060c \u0645\u062f\u0639\u0648\u0645 \u0628\u0623\u062f\u0627\u0629 Nugget \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631 \u0644\u062a\u062e\u0635\u064a\u0635 iOS.",
    "comm_h2": "\u0627\u0646\u0636\u0645 \u0625\u0644\u0649 \u0645\u062c\u062a\u0645\u0639 Nugget Wallpaper",
    "comm_p": "\u062a\u0627\u0628\u0639 \u0627\u0644\u0642\u0646\u0648\u0627\u062a \u0644\u0644\u062a\u0639\u0631\u0641 \u0639\u0644\u0649 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u062c\u062f\u064a\u062f\u0629 \u0648\u0627\u0644\u0645\u0639\u0627\u064a\u0646\u0627\u062a \u0648\u0646\u0635\u0627\u0626\u062d \u0627\u0644\u062a\u062b\u0628\u064a\u062a \u0627\u0644\u0633\u0631\u064a\u0639.",
    "comm_tt": "TikTok",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg": "Telegram",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x": "X",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh": "Nugget \u0639\u0644\u0649 GitHub",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "\u0627\u0644\u0645\u0648\u0642\u0639 \u0627\u0644\u0631\u0633\u0645\u064a \u0644\u0623\u062f\u0627\u0629 iOS",
    "cta_h2": "\u0645\u0633\u062a\u0639\u062f \u0644\u0625\u062d\u064a\u0627\u0621 \u0634\u0627\u0634\u0629 \u0642\u0641\u0644\u0643\u061f",
    "cta_p": "\u062d\u0645\u0651\u0644 \u0627\u0644\u064a\u0648\u0645 \u062e\u0644\u0641\u064a\u0629 tendies \u0645\u062c\u0627\u0646\u064a\u0629\u060c \u062f\u0648\u0646 \u0627\u0644\u062d\u0627\u062c\u0629 \u0625\u0644\u0649 \u062c\u064a\u0644\u0628\u0631\u064a\u0643. \u062a\u0635\u0641\u062d \u0627\u0644\u0645\u0643\u062a\u0628\u0629 \u0627\u0644\u0643\u0627\u0645\u0644\u0629\u060c \u0648\u0627\u0637\u0644\u0639 \u0639\u0644\u0649 \u0627\u0644\u0623\u0633\u0639\u0627\u0631\u060c \u0648\u062a\u0627\u0628\u0639 \u0637\u0644\u0628\u0627\u062a\u0643\u060c \u0648\u0627\u0642\u0631\u0623 \u0627\u0644\u062f\u0644\u064a\u0644 \u062e\u0637\u0648\u0629 \u0628\u062e\u0637\u0648\u0629 \u0639\u0644\u0649 \u0645\u0648\u0642\u0639 Nugget Wallpaper.",
    "cta_btn1": "\u0627\u0628\u062f\u0623 \u0627\u0644\u0627\u0633\u062a\u0643\u0634\u0627\u0641",
    "cta_btn2": "\u0639\u0631\u0636 \u0627\u0644\u0623\u0633\u0639\u0627\u0631",
    "foot_tw1": "\u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629",
    "foot_tw2": "\u0645\u0627 \u0647\u064a",
    "foot_tw3": "\u0645\u0644\u0641 .tendies",
    "foot_tw4": "\u062f\u0644\u064a\u0644 \u0627\u0644\u062a\u062b\u0628\u064a\u062a",
    "foot_nw1": "\u0639\u0631\u0636 \u062c\u0645\u064a\u0639 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a",
    "foot_nw2": "\u0623\u062d\u062f\u062b \u0627\u0644\u0625\u0636\u0627\u0641\u0627\u062a",
    "foot_nw3": "\u0627\u0644\u0623\u0643\u062b\u0631 \u0631\u0648\u0627\u062c\u0627\u064b \u0627\u0644\u0622\u0646",
    "foot_nw4": "\u062f\u0644\u064a\u0644 \u0627\u0644\u0627\u0633\u062a\u064a\u0631\u0627\u062f",
    "foot_pr1": "Nugget \u0639\u0644\u0649 GitHub",
    "foot_pr2": "\u0623\u062f\u0627\u0629 Nugget \u0627\u0644\u0631\u0633\u0645\u064a\u0629",
    "foot_pr3": "\u0627\u0644\u0623\u0633\u0639\u0627\u0631",
    "foot_pr4": "\u0627\u0644\u0637\u0644\u0628\u0627\u062a",
    "foot_pol1": "\u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u062e\u0635\u0648\u0635\u064a\u0629",
    "foot_pol2": "\u0634\u0631\u0648\u0637 \u0627\u0644\u062e\u062f\u0645\u0629",
    "foot_pol3": "\u0633\u064a\u0627\u0633\u0629 DMCA",
    "foot_pol4": "\u0633\u064a\u0627\u0633\u0629 UGC",
    "copyright": "Tendies Wallpaper \u0647\u064a \u0635\u0641\u062d\u0629 \u062a\u0639\u0631\u064a\u0641\u064a\u0629 \u0648\u0625\u062d\u0627\u0644\u0629 \u0644\u0645\u0643\u062a\u0628\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0627\u062a \u0627\u0644\u0645\u062e\u062a\u0627\u0631\u0629 \u0627\u0644\u0645\u0633\u062a\u0636\u0627\u0641\u0629 \u0639\u0644\u0649 <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. \u062a\u064f\u0637\u0628\u0651\u0642 \u062e\u0644\u0641\u064a\u0627\u062a Nugget \u0639\u0628\u0631 \u0623\u062f\u0627\u0629 Nugget \u0645\u0641\u062a\u0648\u062d\u0629 \u0627\u0644\u0645\u0635\u062f\u0631 (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple \u0648 iPhone \u0648 iPad \u0648 iOS \u0639\u0644\u0627\u0645\u0627\u062a \u062a\u062c\u0627\u0631\u064a\u0629 \u0644\u0634\u0631\u0643\u0629 Apple Inc. \u0647\u0630\u0627 \u0627\u0644\u0645\u0648\u0642\u0639 \u063a\u064a\u0631 \u062a\u0627\u0628\u0639 \u0644\u0634\u0631\u0643\u0629 \u0622\u0628\u0644.",
    "title": "Tendies Wallpaper &mdash; \u062e\u0644\u0641\u064a\u0627\u062a iOS \u0627\u0644\u0645\u062a\u062d\u0631\u0643\u0629 \u0644\u0623\u062f\u0627\u0629 Nugget",
    "desc": "Tendies Wallpaper \u0647\u064a \u0645\u0648\u0637\u0646 \u062e\u0644\u0641\u064a\u0627\u062a iOS \u0648 iPadOS \u0627\u0644\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629 \u0644\u0623\u062f\u0627\u0629 Nugget. \u062a\u0639\u0631\u0641 \u0639\u0644\u0649 \u0645\u0644\u0641 .tendies \u0648\u0643\u064a\u0641\u064a\u0629 \u062a\u062b\u0628\u064a\u062a \u062e\u0644\u0641\u064a\u0627\u062a \u0645\u062a\u062d\u0631\u0643\u0629 \u062f\u0648\u0646 \u062c\u064a\u0644\u0628\u0631\u064a\u0643\u060c \u0648\u0627\u0633\u062a\u0643\u0634\u0641 \u0627\u0644\u0645\u0643\u062a\u0628\u0629 \u0627\u0644\u0643\u0627\u0645\u0644\u0629 \u0639\u0644\u0649 Nugget Wallpaper.",
    "kw": "\u062e\u0644\u0641\u064a\u0629 tendies, \u0645\u0644\u0641 tendies, \u062e\u0644\u0641\u064a\u0629 Nugget, \u062e\u0644\u0641\u064a\u0629 iOS \u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u0629, \u062e\u0644\u0641\u064a\u0629 PosterBoard, \u062e\u0644\u0641\u064a\u0629 ios 18, \u062e\u0644\u0641\u064a\u0629 ios 27, \u062e\u0644\u0641\u064a\u0629 \u0634\u0627\u0634\u0629 \u0642\u0641\u0644 \u0645\u062a\u062d\u0631\u0643\u0629",
}

T["pt"] = {
    "nav_wiki": "O que \u00e9",
    "nav_install": "Instalar",
    "nav_gallery": "Galeria",
    "nav_faq": "FAQ",
    "nav_cta": "Ver pap\u00e9is",
    "lang_label": "Idioma",
    "hero_kicker": "A casa oficial do Tendies Wallpaper",
    "hero_h1_lead": "Pap\u00e9is de parede din\u00e2micos para iOS com",
    "hero_h1_after": "Sua tela de bloqueio, viva.",
    "hero_lead": "O Tendies Wallpaper \u00e9 uma cole\u00e7\u00e3o selecionada de pap\u00e9is de parede animados e din\u00e2micos para iPhone e iPad, instalados com a ferramenta de c\u00f3digo aberto Nugget por meio de um simples arquivo .tendies. Sem jailbreak, sem concess\u00f5es. Compat\u00edvel com iOS e iPadOS 17&ndash;27.",
    "hero_btn1": "Explorar a biblioteca",
    "hero_btn2": "Como instalar",
    "hero_btn3": "Ler o tutorial",
    "stat1b": "Suporte a todas as vers\u00f5es",
    "stat2b": "Usa SparseRestore / BookRestore",
    "stat3b": "C\u00f3digo aberto e comunit\u00e1rio",
    "about_tag": "O que \u00e9 o Tendies Wallpaper?",
    "about_h2": "Pap\u00e9is de parede animados para iPhone e iPad, bem feitos",
    "about_p": "O Tendies Wallpaper \u00e9 a marca por tr\u00e1s de uma biblioteca crescente de pap\u00e9is de parede din\u00e2micos para a tela de bloqueio, criados para o ecossistema Nugget. Cada papel de parede \u00e9 empacotado como um <strong>arquivo .tendies</strong>, um pacote PosterBoard que transforma a tela de bloqueio nativa da Apple em uma tela viva. A cole\u00e7\u00e3o completa fica em <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "Realmente din\u00e2mico",
    "c1d": "Movimento, profundidade e anima\u00e7\u00e3o na tela de bloqueio nativa, e n\u00e3o uma imagem est\u00e1tica. Cada papel tendies \u00e9 criado para parecer uma tela viva premium.",
    "c2t": "Sem jailbreak",
    "c2d": "Os pap\u00e9is tendies s\u00e3o aplicados com o Nugget, que usa os mecanismos de restaura\u00e7\u00e3o SparseRestore e BookRestore da Apple para gravar arquivos com seguran\u00e7a.",
    "c3t": "Biblioteca selecionada",
    "c3d": "Anime, mang\u00e1, esportes, Marvel, sonhos espaciais e muito mais, uma galeria selecionada atualizada toda semana no site do Nugget Wallpaper.",
    "c4t": "Movido por Nugget",
    "c4d": "Constru\u00eddo sobre a ferramenta de c\u00f3digo aberto <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> do leminlimez, confi\u00e1vel para uma comunidade de milhares de usu\u00e1rios.",
    "c5t": "iPhone e iPad",
    "c5d": "Funciona em iPhones e iPads compat\u00edveis com iOS e iPadOS 17 a 27, com ou sem Dynamic Island.",
    "c6t": "Revers\u00edvel e seguro",
    "c6d": "Tudo \u00e9 revers\u00edvel. Fa\u00e7a um backup antes de aplicar; restaure pelo iTunes ou Finder a qualquer momento para voltar ao original.",
    "tendies_h2": "O que \u00e9 um arquivo tendies?",
    "tendies_p": "Um <strong>arquivo .tendies</strong> \u00e9 o formato de pacote de pap\u00e9is de parede usado no ecossistema Nugget / PosterBoard (incluindo Cowabunga e Pocket Poster). Ele guarda a estrutura exata de arquivos do PosterBoard que o Nugget restaura no seu aparelho, para que o papel apare\u00e7a dentro do seletor nativo de pap\u00e9is de parede da tela de bloqueio.",
    "tv1_d": "Restaura diretamente no cont\u00eainer do app PosterBoard, mantendo a estrutura de arquivos e os IDs dos pap\u00e9is intactos.",
    "tv2_d": "Restaura na pasta de descriptors com UUIDs aleat\u00f3rios para que v\u00e1rios pap\u00e9is tendies nunca entrem em conflito.",
    "tv3_d": "As variantes de v\u00eddeo e foto visam o Suggested Photos; as variantes mercury visam o Mercury Poster nas vers\u00f5es compat\u00edveis de iOS.",
    "install_tag": "Come\u00e7ando",
    "install_h2": "Instale um papel tendies em 4 etapas",
    "install_p": "Todo o processo leva alguns minutos com um cabo USB e o app gratuito Nugget. Todos os detalhes est\u00e3o no tutorial oficial.",
    "s1_t": "Baixe o arquivo",
    "s1_d": "Escolha um papel na biblioteca e baixe o <strong>arquivo .tendies</strong> dele.",
    "s2_t": "Conecte seu aparelho",
    "s2_d": "Conecte seu iPhone/iPad ao computador via USB e confie nele. Funciona no Windows, macOS e Linux.",
    "s3_t": "Importe e aplique",
    "s3_d": "Abra o PosterBoard dentro do Nugget, selecione o arquivo e clique em Apply Changes.",
    "s4_t": "Reinicie e aproveite",
    "s4_d": "Ap\u00f3s reiniciar, abra o editor da tela de bloqueio e encontre seu novo papel em Collections ou Favorites.",
    "install_note": "Com problemas? Leia o <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">tutorial oficial do Nugget Wallpaper</a> ou entre nos canais da comunidade abaixo.",
    "gallery_tag": "A biblioteca",
    "gallery_h2": "Explore a galeria do Tendies Wallpaper",
    "gallery_p": "Cada papel tendies abaixo est\u00e1 hospedado e dispon\u00edvel para download no <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Ordene a galeria por <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">Recentes</a> ou <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">Populares</a> para ver as tend\u00eancias.",
    "g_t1": "Anime",
    "g_d1": "Evangelion, Sylphiette e mais",
    "g_t2": "Esportes e Marvel",
    "g_d2": "Clubes, her\u00f3is e novos dias",
    "g_t3": "Sonhos espaciais",
    "g_d3": "Planetas, estrelas e abstratos",
    "g_t4": "Oficial",
    "g_d4": "Sele\u00e7\u00f5es no estilo Apple",
    "gallery_cta": "Ver todos os pap\u00e9is",
    "faq_h2": "Perguntas frequentes",
    "faq_p": "Tudo o que voc\u00ea precisa saber sobre pap\u00e9is tendies antes de come\u00e7ar.",
    "f1q": "O que \u00e9 um papel de parede tendies?",
    "f1a": "Um papel tendies \u00e9 um papel de parede din\u00e2mico e animado para iPhone e iPad, enviado como arquivo .tendies instalado pela ferramenta Nugget. Os arquivos tendies restauram os descriptors do PosterBoard em aparelhos iOS 17-27 para que o papel apare\u00e7a no seletor de Collections da tela de bloqueio.",
    "f2q": "O que \u00e9 um arquivo .tendies?",
    "f2a": "Um arquivo .tendies \u00e9 o formato de pacote usado por Nugget e Pocket Poster. Ele guarda a estrutura de arquivos do PosterBoard que \u00e9 restaurada no seu iPhone ou iPad, e \u00e9 o que voc\u00ea importa para instalar um papel din\u00e2mico personalizado na tela de bloqueio.",
    "f3q": "Pap\u00e9is tendies exigem jailbreak?",
    "f3a": "N\u00e3o. Os pap\u00e9is tendies s\u00e3o aplicados com a ferramenta de c\u00f3digo aberto Nugget, que usa os mecanismos SparseRestore e BookRestore da Apple para modificar arquivos com seguran\u00e7a, sem necessidade de jailbreak.",
    "f4q": "Quais vers\u00f5es do iOS suportam pap\u00e9is tendies?",
    "f4a": "Os pap\u00e9is tendies suportam iOS e iPadOS 17 a 27 em iPhones e iPads compat\u00edveis. Alguns pap\u00e9is podem exigir uma vers\u00e3o espec\u00edfica do iOS, ent\u00e3o sempre confira as notas de compatibilidade na p\u00e1gina do papel.",
    "f5q": "Onde posso baixar pap\u00e9is tendies?",
    "f5a": "Navegue e baixe pap\u00e9is tendies na biblioteca do Nugget Wallpaper em mwallx.com, que re\u00fane uma cole\u00e7\u00e3o selecionada de pap\u00e9is din\u00e2micos e est\u00e1ticos, incluindo anime, esportes, Marvel e muito mais.",
    "f6q": "Como instalo um papel tendies no meu iPhone?",
    "f6a": "Baixe o arquivo .tendies, abra o recurso PosterBoard dentro do Nugget, selecione o arquivo, aplique as altera\u00e7\u00f5es e reinicie o aparelho. Ap\u00f3s reiniciar, abra o editor da tela de bloqueio e encontre o papel em Collections ou Favorites.",
    "f7q": "Usar pap\u00e9is tendies \u00e9 seguro?",
    "f7a": "O Nugget \u00e9 um projeto de c\u00f3digo aberto muito usado, com milhares de usu\u00e1rios. Como em qualquer modifica\u00e7\u00e3o de sistema, fa\u00e7a um backup primeiro. As altera\u00e7\u00f5es s\u00e3o revers\u00edveis restaurando o aparelho pelo iTunes ou Finder.",
    "f8q": "Qual a diferen\u00e7a entre Nugget Wallpaper e pap\u00e9is tendies?",
    "f8a": "Tendies Wallpaper \u00e9 o nome da marca da cole\u00e7\u00e3o de pap\u00e9is din\u00e2micos, enquanto Nugget Wallpaper (mwallx.com) \u00e9 a biblioteca que os hospeda. Ambos fazem parte do mesmo ecossistema, movido pela ferramenta de c\u00f3digo aberto Nugget de personaliza\u00e7\u00e3o do iOS.",
    "comm_h2": "Entre para a comunidade Nugget Wallpaper",
    "comm_p": "Siga os canais para novos pap\u00e9is, pr\u00e9vias e dicas r\u00e1pidas de instala\u00e7\u00e3o.",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "Site oficial da ferramenta iOS",
    "cta_h2": "Pronto para dar vida \u00e0 sua tela de bloqueio?",
    "cta_p": "Baixe hoje um papel tendies gr\u00e1tis, sem jailbreak. Explore a biblioteca completa, veja pre\u00e7os, acompanhe pedidos e siga o tutorial passo a passo no site do Nugget Wallpaper.",
    "cta_btn1": "Come\u00e7ar a explorar",
    "cta_btn2": "Ver pre\u00e7os",
    "foot_tw1": "In\u00edcio",
    "foot_tw2": "O que \u00e9",
    "foot_tw3": "O arquivo .tendies",
    "foot_tw4": "Guia de instala\u00e7\u00e3o",
    "foot_nw1": "Ver todos os pap\u00e9is",
    "foot_nw2": "Adi\u00e7\u00f5es recentes",
    "foot_nw3": "Populares agora",
    "foot_nw4": "Tutorial de importa\u00e7\u00e3o",
    "foot_pr1": "Nugget no GitHub",
    "foot_pr2": "Ferramenta oficial Nugget",
    "foot_pr3": "Pre\u00e7os",
    "foot_pr4": "Pedidos",
    "foot_pol1": "Pol\u00edtica de privacidade",
    "foot_pol2": "Termos de servi\u00e7o",
    "foot_pol3": "Pol\u00edtica DMCA",
    "foot_pol4": "Pol\u00edtica UGC",
    "copyright": "O Tendies Wallpaper \u00e9 uma p\u00e1gina de apresenta\u00e7\u00e3o e refer\u00eancia da biblioteca de pap\u00e9is de parede hospedada em <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. Os pap\u00e9is Nugget s\u00e3o aplicados pela ferramenta de c\u00f3digo aberto Nugget (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple, iPhone, iPad e iOS s\u00e3o marcas da Apple Inc. Este site n\u00e3o \u00e9 afiliado \u00e0 Apple.",
    "title": "Tendies Wallpaper &mdash; Pap\u00e9is de parede din\u00e2micos iOS para Nugget",
    "desc": "O Tendies Wallpaper \u00e9 a casa dos pap\u00e9is de parede din\u00e2micos para iOS e iPadOS com Nugget. Saiba o que \u00e9 um arquivo .tendies, como instalar pap\u00e9is animados sem jailbreak e explore a biblioteca completa no Nugget Wallpaper.",
    "kw": "papel tendies, arquivo tendies, papel Nugget, papel din\u00e2mico iOS, papel PosterBoard, papel ios 18, papel ios 27, papel animado tela de bloqueio",
}

T["ru"] = {
    "nav_wiki": "\u0427\u0442\u043e \u044d\u0442\u043e",
    "nav_install": "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430",
    "nav_gallery": "\u0413\u0430\u043b\u0435\u0440\u0435\u044f",
    "nav_faq": "\u0427\u0410\u0412",
    "nav_cta": "\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u043e\u0431\u043e\u0438",
    "lang_label": "\u042f\u0437\u044b\u043a",
    "hero_kicker": "\u041e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0434\u043e\u043c Tendies Wallpaper",
    "hero_h1_lead": "\u0414\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043e\u0431\u043e\u0438 iOS \u0441",
    "hero_h1_after": "\u0412\u0430\u0448 \u044d\u043a\u0440\u0430\u043d \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u0436\u0438\u0432\u0435\u0442.",
    "hero_lead": "Tendies Wallpaper \u2014 \u044d\u0442\u043e \u043a\u0443\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0430 \u0430\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043e\u0431\u043e\u0435\u0432 \u0434\u043b\u044f iPhone \u0438 iPad, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u043c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u043c Nugget \u0441 \u043f\u043e\u043c\u043e\u0449\u044c\u044e \u043f\u0440\u043e\u0441\u0442\u043e\u0433\u043e \u0444\u0430\u0439\u043b\u0430 .tendies. \u0411\u0435\u0437 \u0434\u0436\u0435\u0439\u043b\u0431\u0440\u0435\u0439\u043a\u0430 \u0438 \u0431\u0435\u0437 \u043a\u043e\u043c\u043f\u0440\u043e\u043c\u0438\u0441\u0441\u043e\u0432. iOS \u0438 iPadOS 17&ndash;27.",
    "hero_btn1": "\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430",
    "hero_btn2": "\u041a\u0430\u043a \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c",
    "hero_btn3": "\u041f\u043e\u0447\u0438\u0442\u0430\u0442\u044c \u0433\u0430\u0439\u0434",
    "stat1b": "\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430 \u0432\u0441\u0435\u0445 \u0432\u0435\u0440\u0441\u0438\u0439",
    "stat2b": "\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 SparseRestore / BookRestore",
    "stat3b": "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u043a\u043e\u0434 \u0438 \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u043e",
    "about_tag": "\u0427\u0442\u043e \u0442\u0430\u043a\u043e\u0435 Tendies Wallpaper?",
    "about_h2": "\u0410\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043e\u0431\u043e\u0438 \u0434\u043b\u044f iPhone \u0438 iPad, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u0434\u0435\u043b\u0430\u044e\u0442\u0441\u044f \u043f\u043e \u0434\u043e\u043c\u0443",
    "about_p": "Tendies Wallpaper \u2014 \u0431\u0440\u0435\u043d\u0434 \u0440\u0430\u0441\u0442\u0443\u0449\u0435\u0439 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438 \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043e\u0431\u043e\u0435\u0432 \u0434\u043b\u044f \u044d\u043a\u0440\u0430\u043d\u0430 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u044d\u043a\u043e\u0441\u0438\u0441\u0442\u0435\u043c\u044b Nugget. \u041a\u0430\u0436\u0434\u044b\u0435 \u043e\u0431\u043e\u0438 \u0443\u043f\u0430\u043a\u043e\u0432\u0430\u043d\u044b \u043a\u0430\u043a <strong>\u0444\u0430\u0439\u043b .tendies</strong> \u2014 \u043f\u0430\u043a\u0435\u0442 PosterBoard, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u043f\u0440\u0435\u0432\u0440\u0430\u0449\u0430\u0435\u0442 \u043d\u0430\u0442\u0438\u0432\u043d\u044b\u0439 \u044d\u043a\u0440\u0430\u043d \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 Apple \u0432 \u0436\u0438\u0432\u043e\u0439 \u044d\u043a\u0440\u0430\u043d. \u041f\u043e\u043b\u043d\u0430\u044f \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f \u043d\u0430\u0445\u043e\u0434\u0438\u0442\u0441\u044f \u043d\u0430 <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">\u0441\u0430\u0439\u0442\u0435 Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u043d\u044b\u0435",
    "c1d": "\u0414\u0432\u0438\u0436\u0435\u043d\u0438\u0435, \u0433\u043b\u0443\u0431\u0438\u043d\u0430 \u0438 \u0430\u043d\u0438\u043c\u0430\u0446\u0438\u044f \u043d\u0430 \u043d\u0430\u0442\u0438\u0432\u043d\u043e\u043c \u044d\u043a\u0440\u0430\u043d\u0435 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438, \u0430 \u043d\u0435 \u0441\u0442\u0430\u0442\u0438\u0447\u043d\u0430\u044f \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0430. \u041a\u0430\u0436\u0434\u044b\u0435 \u043e\u0431\u043e\u0438 tendies \u0441\u043e\u0437\u0434\u0430\u043d\u044b, \u0447\u0442\u043e\u0431\u044b \u0432\u044b\u0433\u043b\u044f\u0434\u0435\u0442\u044c \u043a\u0430\u043a \u043f\u0440\u0435\u043c\u0438\u0443\u043c-\u0436\u0438\u0432\u043e\u0439 \u044d\u043a\u0440\u0430\u043d.",
    "c2t": "\u0411\u0435\u0437 \u0434\u0436\u0435\u0439\u043b\u0431\u0440\u0435\u0439\u043a\u0430",
    "c2d": "\u041e\u0431\u043e\u0438 tendies \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0447\u0435\u0440\u0435\u0437 Nugget, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 \u043c\u0435\u0445\u0430\u043d\u0438\u0437\u043c\u044b \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f SparseRestore \u0438 BookRestore \u0434\u043b\u044f \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0439 \u0437\u0430\u043f\u0438\u0441\u0438 \u0444\u0430\u0439\u043b\u043e\u0432.",
    "c3t": "\u041a\u0443\u0440\u0438\u0440\u0443\u0435\u043c\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430",
    "c3d": "\u0410\u043d\u0438\u043c\u0435, \u043c\u0430\u043d\u0433\u0430, \u0441\u043f\u043e\u0440\u0442, Marvel, \u043a\u043e\u0441\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u043d\u044b \u0438 \u043c\u043d\u043e\u0433\u043e\u0435 \u0434\u0440\u0443\u0433\u043e\u0435 \u2014 \u043a\u0443\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0433\u0430\u043b\u0435\u0440\u0435\u044f, \u043f\u043e\u043f\u043e\u043b\u043d\u044f\u044e\u0449\u0430\u044f\u0441\u044f \u043a\u0430\u0436\u0434\u0443\u044e \u043d\u0435\u0434\u0435\u043b\u044e \u043d\u0430 \u0441\u0430\u0439\u0442\u0435 Nugget Wallpaper.",
    "c4t": "\u0420\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u043d\u0430 Nugget",
    "c4d": "\u041f\u043e\u0441\u0442\u0440\u043e\u0435\u043d\u0430 \u043d\u0430 \u043e\u0442\u043a\u0440\u044b\u0442\u043e\u043c \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0435 <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> \u043e\u0442 leminlimez, \u043a\u043e\u0442\u043e\u0440\u043e\u043c\u0443 \u0434\u043e\u0432\u0435\u0440\u044f\u044e\u0442 \u0442\u044b\u0441\u044f\u0447\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439.",
    "c5t": "iPhone \u0438 iPad",
    "c5d": "\u0420\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u043d\u0430 iPhone \u0438 iPad \u0441 iOS \u0438 iPadOS 17&ndash;27, \u0441 Dynamic Island \u0438 \u0431\u0435\u0437 \u043d\u0435\u0435.",
    "c6t": "\u041e\u0431\u0440\u0430\u0442\u0438\u043c\u043e \u0438 \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e",
    "c6d": "\u0412\u0441\u0435 \u043e\u0431\u0440\u0430\u0442\u0438\u043c\u043e. \u0421\u0434\u0435\u043b\u0430\u0439\u0442\u0435 \u0440\u0435\u0437\u0435\u0440\u0432\u043d\u0443\u044e \u043a\u043e\u043f\u0438\u044e \u043f\u0435\u0440\u0435\u0434 \u043f\u0440\u0438\u043c\u0435\u043d\u0435\u043d\u0438\u0435\u043c; \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435 \u0447\u0435\u0440\u0435\u0437 iTunes \u0438\u043b\u0438 Finder \u0432 \u043b\u044e\u0431\u043e\u0435 \u0432\u0440\u0435\u043c\u044f, \u0447\u0442\u043e\u0431\u044b \u0432\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u043a \u043e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u0443.",
    "tendies_h2": "\u0427\u0442\u043e \u0442\u0430\u043a\u043e\u0435 \u0444\u0430\u0439\u043b tendies?",
    "tendies_p": "<strong>\u0424\u0430\u0439\u043b .tendies</strong> \u2014 \u0444\u043e\u0440\u043c\u0430\u0442 \u043f\u0430\u043a\u0435\u0442\u0430 \u043e\u0431\u043e\u0435\u0432 \u044d\u043a\u043e\u0441\u0438\u0441\u0442\u0435\u043c\u044b Nugget / PosterBoard (\u0432\u043a\u043b\u044e\u0447\u0430\u044f Cowabunga \u0438 Pocket Poster). \u041e\u043d \u0445\u0440\u0430\u043d\u0438\u0442 \u0442\u043e\u0447\u043d\u0443\u044e \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0443 \u0444\u0430\u0439\u043b\u043e\u0432 PosterBoard, \u043a\u043e\u0442\u043e\u0440\u0443\u044e Nugget \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442 \u043d\u0430 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e, \u0447\u0442\u043e\u0431\u044b \u043e\u0431\u043e\u0438 \u043f\u043e\u044f\u0432\u0438\u043b\u0438\u0441\u044c \u0432 \u043d\u0430\u0442\u0438\u0432\u043d\u043e\u043c \u0432\u044b\u0431\u043e\u0440\u0435 \u043e\u0431\u043e\u0435\u0432 \u044d\u043a\u0440\u0430\u043d\u0430 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438.",
    "tv1_d": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442 \u043d\u0430\u043f\u0440\u044f\u043c\u0443\u044e \u0432 \u043a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f PosterBoard, \u0441\u043e\u0445\u0440\u0430\u043d\u044f\u044f \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0443 \u0444\u0430\u0439\u043b\u043e\u0432 \u0438 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u044b \u043e\u0431\u043e\u0435\u0432.",
    "tv2_d": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442 \u0432 \u043f\u0430\u043f\u043a\u0443 descriptors \u0441 \u0441\u043b\u0443\u0447\u0430\u0439\u043d\u044b\u043c\u0438 UUID, \u0447\u0442\u043e\u0431\u044b \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u043e\u0431\u043e\u0435\u0432 tendies \u043d\u0438\u043a\u043e\u0433\u0434\u0430 \u043d\u0435 \u043a\u043e\u043d\u0444\u043b\u0438\u043a\u0442\u043e\u0432\u0430\u043b\u0438.",
    "tv3_d": "\u0412\u0438\u0434\u0435\u043e- \u0438 \u0444\u043e\u0442\u043e-\u0432\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u044e\u0442 Suggested Photos; \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u044b mercury \u2014 \u043f\u043e\u0441\u0442\u0435\u0440 Mercury \u0432 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u043c\u044b\u0445 \u0432\u0435\u0440\u0441\u0438\u044f\u0445 iOS.",
    "install_tag": "\u041d\u0430\u0447\u0430\u043b\u043e",
    "install_h2": "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043e\u0431\u043e\u0435\u0432 tendies \u0437\u0430 4 \u0448\u0430\u0433\u0430",
    "install_p": "\u0412\u0435\u0441\u044c \u043f\u0440\u043e\u0446\u0435\u0441\u0441 \u0437\u0430\u0439\u043c\u0435\u0442 \u043f\u0430\u0440\u0443 \u043c\u0438\u043d\u0443\u0442 \u0441 USB-\u043a\u0430\u0431\u0435\u043b\u0435\u043c \u0438 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u043c \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435\u043c Nugget. \u0412\u0441\u0435 \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u043e\u0441\u0442\u0438 \u2014 \u0432 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u043c \u0433\u0430\u0439\u0434\u0435.",
    "s1_t": "\u0421\u043a\u0430\u0447\u0430\u0439\u0442\u0435 \u0444\u0430\u0439\u043b",
    "s1_d": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043e\u0431\u043e\u0438 \u0432 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0435 \u0438 \u0441\u043a\u0430\u0447\u0430\u0439\u0442\u0435 \u0435\u0433\u043e <strong>\u0444\u0430\u0439\u043b .tendies</strong>.",
    "s2_t": "\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e",
    "s2_d": "\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u0435 iPhone/iPad \u043a \u043a\u043e\u043c\u043f\u044c\u044e\u0442\u0435\u0440\u0443 \u0447\u0435\u0440\u0435\u0437 USB \u0438 \u0434\u043e\u0432\u0435\u0440\u044c\u0442\u0435\u0441\u044c \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0443. \u0420\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u043d\u0430 Windows, macOS \u0438 Linux.",
    "s3_t": "\u0418\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u0443\u0439\u0442\u0435 \u0438 \u043f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u0435",
    "s3_d": "\u041e\u0442\u043a\u0440\u043e\u0439\u0442\u0435 PosterBoard \u0432 Nugget, \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b \u0438 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 Apply Changes.",
    "s4_t": "\u041f\u0435\u0440\u0435\u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0438 \u043d\u0430\u0441\u043b\u0430\u0436\u0434\u0430\u0439\u0442\u0435\u0441\u044c",
    "s4_d": "\u041f\u043e\u0441\u043b\u0435 \u043f\u0435\u0440\u0435\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438 \u043e\u0442\u043a\u0440\u043e\u0439\u0442\u0435 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u044d\u043a\u0440\u0430\u043d\u0430 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u0438 \u043d\u0430\u0439\u0434\u0438\u0442\u0435 \u043d\u043e\u0432\u044b\u0435 \u043e\u0431\u043e\u0438 \u0432 Collections \u0438\u043b\u0438 Favorites.",
    "install_note": "\u041d\u0435 \u043f\u043e\u043b\u0443\u0447\u0430\u0435\u0442\u0441\u044f? \u041f\u0440\u043e\u0447\u0438\u0442\u0430\u0439\u0442\u0435 <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">\u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0433\u0430\u0439\u0434 Nugget Wallpaper</a> \u0438\u043b\u0438 \u043f\u0440\u0438\u0441\u043e\u0435\u0434\u0438\u043d\u044f\u0439\u0442\u0435\u0441\u044c \u043a \u043a\u0430\u043d\u0430\u043b\u0430\u043c \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0430 \u043d\u0438\u0436\u0435.",
    "gallery_tag": "\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430",
    "gallery_h2": "\u0418\u0441\u0441\u043b\u0435\u0434\u0443\u0439\u0442\u0435 \u0433\u0430\u043b\u0435\u0440\u0435\u044e Tendies Wallpaper",
    "gallery_p": "\u041a\u0430\u0436\u0434\u044b\u0435 \u043e\u0431\u043e\u0438 tendies \u043d\u0438\u0436\u0435 \u0445\u0440\u0430\u043d\u044f\u0442\u0441\u044f \u0438 \u0441\u043a\u0430\u0447\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0441 <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. \u0421\u043e\u0440\u0442\u0438\u0440\u0443\u0439\u0442\u0435 \u043f\u043e <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">\u043d\u043e\u0432\u0438\u043d\u043a\u0430\u043c</a> \u0438\u043b\u0438 <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">\u043f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u043c\u0443</a>, \u0447\u0442\u043e\u0431\u044b \u0443\u0432\u0438\u0434\u0435\u0442\u044c \u0442\u0440\u0435\u043d\u0434\u044b.",
    "g_t1": "\u0410\u043d\u0438\u043c\u0435",
    "g_d1": "Evangelion, Sylphiette \u0438 \u0434\u0440\u0443\u0433\u0438\u0435",
    "g_t2": "\u0421\u043f\u043e\u0440\u0442 \u0438 Marvel",
    "g_d2": "\u041a\u043b\u0443\u0431\u044b, \u0433\u0435\u0440\u043e\u0438 \u0438 \u043d\u043e\u0432\u044b\u0435 \u0434\u043d\u0438",
    "g_t3": "\u041a\u043e\u0441\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0441\u043d\u044b",
    "g_d3": "\u041f\u043b\u0430\u043d\u0435\u0442\u044b, \u0437\u0432\u0435\u0437\u0434\u044b \u0438 \u0430\u0431\u0441\u0442\u0440\u0430\u043a\u0446\u0438\u0438",
    "g_t4": "\u041e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435",
    "g_d4": "\u041f\u043e\u0434\u0431\u043e\u0440\u043a\u0438 \u0432 \u0441\u0442\u0438\u043b\u0435 Apple",
    "gallery_cta": "\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0432\u0441\u0435 \u043e\u0431\u043e\u0438",
    "faq_h2": "\u0427\u0430\u0441\u0442\u043e \u0437\u0430\u0434\u0430\u0432\u0430\u0435\u043c\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b",
    "faq_p": "\u0412\u0441\u0435, \u0447\u0442\u043e \u043d\u0443\u0436\u043d\u043e \u0437\u043d\u0430\u0442\u044c \u043e\u0431 \u043e\u0431\u043e\u044f\u0445 tendies \u043f\u0435\u0440\u0435\u0434 \u0441\u0442\u0430\u0440\u0442\u043e\u043c.",
    "f1q": "\u0427\u0442\u043e \u0442\u0430\u043a\u043e\u0435 \u043e\u0431\u043e\u0438 tendies?",
    "f1a": "\u041e\u0431\u043e\u0438 tendies \u2014 \u044d\u0442\u043e \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0430\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043e\u0431\u043e\u0438 \u0434\u043b\u044f iPhone \u0438 iPad, \u0440\u0430\u0441\u043f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u044f\u0435\u043c\u044b\u0435 \u043a\u0430\u043a \u0444\u0430\u0439\u043b\u044b .tendies \u0438 \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u043c\u044b\u0435 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u043c Nugget. \u0424\u0430\u0439\u043b\u044b tendies \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e\u0442 \u0434\u0435\u0441\u043a\u0440\u0438\u043f\u0442\u043e\u0440\u044b PosterBoard \u043d\u0430 iOS 17-27, \u0447\u0442\u043e\u0431\u044b \u043e\u0431\u043e\u0438 \u043f\u043e\u044f\u0432\u0438\u043b\u0438\u0441\u044c \u0432 \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438 Collections \u044d\u043a\u0440\u0430\u043d\u0430 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438.",
    "f2q": "\u0427\u0442\u043e \u0442\u0430\u043a\u043e\u0435 \u0444\u0430\u0439\u043b .tendies?",
    "f2a": "\u0424\u0430\u0439\u043b .tendies \u2014 \u0444\u043e\u0440\u043c\u0430\u0442 \u043f\u0430\u043a\u0435\u0442\u0430, \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u043c\u044b\u0439 Nugget \u0438 Pocket Poster. \u041e\u043d \u0441\u043e\u0434\u0435\u0440\u0436\u0438\u0442 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0443 \u0444\u0430\u0439\u043b\u043e\u0432 PosterBoard, \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442\u0441\u044f \u043d\u0430 \u0432\u0430\u0448 iPhone \u0438\u043b\u0438 iPad, \u0438 \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0442\u0435\u043c, \u0447\u0442\u043e \u0432\u044b \u0438\u043c\u043f\u043e\u0440\u0442\u0438\u0440\u0443\u0435\u0442\u0435 \u0434\u043b\u044f \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0445 \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043e\u0431\u043e\u0435\u0432 \u044d\u043a\u0440\u0430\u043d\u0430 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438.",
    "f3q": "\u0422\u0440\u0435\u0431\u0443\u044e\u0442 \u043b\u0438 \u043e\u0431\u043e\u0438 tendies \u0434\u0436\u0435\u0439\u043b\u0431\u0440\u0435\u0439\u043a?",
    "f3a": "\u041d\u0435\u0442. \u041e\u0431\u043e\u0438 tendies \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u043c \u0441 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c \u043a\u043e\u0434\u043e\u043c Nugget, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 \u043c\u0435\u0445\u0430\u043d\u0438\u0437\u043c\u044b SparseRestore \u0438 BookRestore \u0434\u043b\u044f \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0439 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0444\u0430\u0439\u043b\u043e\u0432 \u0431\u0435\u0437 \u0434\u0436\u0435\u0439\u043b\u0431\u0440\u0435\u0439\u043a\u0430.",
    "f4q": "\u041a\u0430\u043a\u0438\u0435 \u0432\u0435\u0440\u0441\u0438\u0438 iOS \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u044e\u0442 \u043e\u0431\u043e\u0438 tendies?",
    "f4a": "\u041e\u0431\u043e\u0438 tendies \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u044e\u0442 iOS \u0438 iPadOS 17&ndash;27 \u043d\u0430 \u0441\u043e\u0432\u043c\u0435\u0441\u0442\u0438\u043c\u044b\u0445 iPhone \u0438 iPad. \u041d\u0435\u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043e\u0431\u043e\u0438 \u043c\u043e\u0433\u0443\u0442 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u0442\u044c \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u0443\u044e \u0432\u0435\u0440\u0441\u0438\u044e iOS, \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0432\u0441\u0435\u0433\u0434\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0439\u0442\u0435 \u0437\u0430\u043c\u0435\u0442\u043a\u0438 \u043e \u0441\u043e\u0432\u043c\u0435\u0441\u0442\u0438\u043c\u043e\u0441\u0442\u0438 \u043d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u043e\u0431\u043e\u0435\u0432.",
    "f5q": "\u0413\u0434\u0435 \u043c\u043e\u0436\u043d\u043e \u0441\u043a\u0430\u0447\u0430\u0442\u044c \u043e\u0431\u043e\u0438 tendies?",
    "f5a": "\u0412\u044b \u043c\u043e\u0436\u0435\u0442\u0435 \u043f\u0440\u043e\u0441\u043c\u0430\u0442\u0440\u0438\u0432\u0430\u0442\u044c \u0438 \u0441\u043a\u0430\u0447\u0438\u0432\u0430\u0442\u044c \u043e\u0431\u043e\u0438 tendies \u0432 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0435 Nugget Wallpaper \u043d\u0430 mwallx.com, \u0433\u0434\u0435 \u0441\u043e\u0431\u0440\u0430\u043d\u0430 \u043a\u0443\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0438 \u0441\u0442\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043e\u0431\u043e\u0435\u0432, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u0430\u043d\u0438\u043c\u0435, \u0441\u043f\u043e\u0440\u0442, Marvel \u0438 \u043c\u043d\u043e\u0433\u043e\u0435 \u0434\u0440\u0443\u0433\u043e\u0435.",
    "f6q": "\u041a\u0430\u043a \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u043e\u0431\u043e\u0438 tendies \u043d\u0430 \u043c\u043e\u0439 iPhone?",
    "f6a": "\u0421\u043a\u0430\u0447\u0430\u0439\u0442\u0435 \u0444\u0430\u0439\u043b .tendies, \u043e\u0442\u043a\u0440\u043e\u0439\u0442\u0435 PosterBoard \u0432 Nugget, \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b, \u043f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u0438 \u043f\u0435\u0440\u0435\u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e. \u041f\u043e\u0441\u043b\u0435 \u043f\u0435\u0440\u0435\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438 \u043e\u0442\u043a\u0440\u043e\u0439\u0442\u0435 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440 \u044d\u043a\u0440\u0430\u043d\u0430 \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u0438 \u043d\u0430\u0439\u0434\u0438\u0442\u0435 \u043e\u0431\u043e\u0438 \u0432 Collections \u0438\u043b\u0438 Favorites.",
    "f7q": "\u0411\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e \u043b\u0438 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u043e\u0431\u043e\u0438 tendies?",
    "f7a": "Nugget \u2014 \u043f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u044b\u0439 \u043f\u0440\u043e\u0435\u043a\u0442 \u0441 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c \u043a\u043e\u0434\u043e\u043c \u0438 \u0442\u044b\u0441\u044f\u0447\u0430\u043c\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439. \u041a\u0430\u043a \u0438 \u043f\u0440\u0438 \u043b\u044e\u0431\u043e\u0439 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0441\u0438\u0441\u0442\u0435\u043c\u044b, \u0441\u043d\u0430\u0447\u0430\u043b\u0430 \u0441\u0434\u0435\u043b\u0430\u0439\u0442\u0435 \u0440\u0435\u0437\u0435\u0440\u0432\u043d\u0443\u044e \u043a\u043e\u043f\u0438\u044e. \u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u043e\u0431\u0440\u0430\u0442\u0438\u043c\u044b: \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e \u0447\u0435\u0440\u0435\u0437 iTunes \u0438\u043b\u0438 Finder.",
    "f8q": "\u0412 \u0447\u0435\u043c \u0440\u0430\u0437\u043d\u0438\u0446\u0430 \u043c\u0435\u0436\u0434\u0443 Nugget Wallpaper \u0438 \u043e\u0431\u043e\u044f\u043c\u0438 tendies?",
    "f8a": "Tendies Wallpaper \u2014 \u044d\u0442\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0431\u0440\u0435\u043d\u0434\u0430 \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438 \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043e\u0431\u043e\u0435\u0432, \u0430 Nugget Wallpaper (mwallx.com) \u2014 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430, \u043a\u043e\u0442\u043e\u0440\u0430\u044f \u0438\u0445 \u0445\u0440\u0430\u043d\u0438\u0442. \u041e\u0431\u0430 \u044f\u0432\u043b\u044f\u044e\u0442\u0441\u044f \u0447\u0430\u0441\u0442\u044c\u044e \u043e\u0434\u043d\u043e\u0439 \u044d\u043a\u043e\u0441\u0438\u0441\u0442\u0435\u043c\u044b, \u0440\u0430\u0431\u043e\u0442\u0430\u044e\u0449\u0435\u0439 \u043d\u0430 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0435 \u043a\u0430\u0441\u0442\u043e\u043c\u0438\u0437\u0430\u0446\u0438\u0438 iOS Nugget \u0441 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c \u043a\u043e\u0434\u043e\u043c.",
    "comm_h2": "\u041f\u0440\u0438\u0441\u043e\u0435\u0434\u0438\u043d\u044f\u0439\u0442\u0435\u0441\u044c \u043a \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0443 Nugget Wallpaper",
    "comm_p": "\u041f\u043e\u0434\u043f\u0438\u0448\u0438\u0442\u0435\u0441\u044c \u043d\u0430 \u043a\u0430\u043d\u0430\u043b\u044b, \u0447\u0442\u043e\u0431\u044b \u0443\u0437\u043d\u0430\u0432\u0430\u0442\u044c \u043e \u043d\u043e\u0432\u044b\u0445 \u043e\u0431\u043e\u044f\u0445, \u043f\u0440\u0435\u0432\u044c\u044e \u0438 \u0431\u044b\u0441\u0442\u0440\u044b\u0445 \u0441\u043e\u0432\u0435\u0442\u0430\u0445 \u043f\u043e \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0435.",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "\u041e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0430\u0439\u0442 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u0430 iOS",
    "cta_h2": "\u0413\u043e\u0442\u043e\u0432\u044b \u043e\u0436\u0438\u0432\u0438\u0442\u044c \u044d\u043a\u0440\u0430\u043d \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438?",
    "cta_p": "\u0421\u043a\u0430\u0447\u0430\u0439\u0442\u0435 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u0435 \u043e\u0431\u043e\u0438 tendies \u0441\u0435\u0433\u043e\u0434\u043d\u044f \u2014 \u0431\u0435\u0437 \u0434\u0436\u0435\u0439\u043b\u0431\u0440\u0435\u0439\u043a\u0430. \u0418\u0441\u0441\u043b\u0435\u0434\u0443\u0439\u0442\u0435 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443, \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0438\u0442\u0435 \u0446\u0435\u043d\u044b, \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u0439\u0442\u0435 \u0437\u0430\u043a\u0430\u0437\u044b \u0438 \u0441\u043b\u0435\u0434\u0443\u0439\u0442\u0435 \u043f\u043e\u0448\u0430\u0433\u043e\u0432\u043e\u043c\u0443 \u0433\u0430\u0439\u0434\u0443 \u043d\u0430 \u0441\u0430\u0439\u0442\u0435 Nugget Wallpaper.",
    "cta_btn1": "\u041d\u0430\u0447\u0430\u0442\u044c \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440",
    "cta_btn2": "\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0446\u0435\u043d\u044b",
    "foot_tw1": "\u0413\u043b\u0430\u0432\u043d\u0430\u044f",
    "foot_tw2": "\u0427\u0442\u043e \u044d\u0442\u043e",
    "foot_tw3": "\u0424\u0430\u0439\u043b .tendies",
    "foot_tw4": "\u0413\u0430\u0439\u0434 \u043f\u043e \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0435",
    "foot_nw1": "\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0432\u0441\u0435 \u043e\u0431\u043e\u0438",
    "foot_nw2": "\u041d\u043e\u0432\u044b\u0435 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f",
    "foot_nw3": "\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0435 \u0441\u0435\u0439\u0447\u0430\u0441",
    "foot_nw4": "\u0422\u0443\u0442\u043e\u0440\u0438\u0430\u043b \u043f\u043e \u0438\u043c\u043f\u043e\u0440\u0442\u0443",
    "foot_pr1": "Nugget \u043d\u0430 GitHub",
    "foot_pr2": "\u041e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442 Nugget",
    "foot_pr3": "\u0426\u0435\u043d\u044b",
    "foot_pr4": "\u0417\u0430\u043a\u0430\u0437\u044b",
    "foot_pol1": "\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 \u043a\u043e\u043d\u0444\u0438\u0434\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0438",
    "foot_pol2": "\u0423\u0441\u043b\u043e\u0432\u0438\u044f \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f",
    "foot_pol3": "\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 DMCA",
    "foot_pol4": "\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 UGC",
    "copyright": "Tendies Wallpaper \u2014 \u044d\u0442\u043e \u043e\u0431\u0437\u043e\u0440\u043d\u0430\u044f \u0438 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438 \u043e\u0431\u043e\u0435\u0432, \u0440\u0430\u0437\u043c\u0435\u0449\u0435\u043d\u043d\u043e\u0439 \u043d\u0430 <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>. \u041e\u0431\u043e\u0438 Nugget \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u043e\u043c \u0441 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c \u043a\u043e\u0434\u043e\u043c Nugget (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple, iPhone, iPad \u0438 iOS \u2014 \u0442\u043e\u0440\u0433\u043e\u0432\u044b\u0435 \u043c\u0430\u0440\u043a\u0438 Apple Inc. \u042d\u0442\u043e\u0442 \u0441\u0430\u0439\u0442 \u043d\u0435 \u0430\u0444\u0444\u0438\u043b\u0438\u0440\u043e\u0432\u0430\u043d \u0441 Apple.",
    "title": "Tendies Wallpaper \u2014 \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043e\u0431\u043e\u0438 iOS \u0434\u043b\u044f Nugget",
    "desc": "Tendies Wallpaper \u2014 \u0434\u043e\u043c \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u043e\u0431\u043e\u0435\u0432 \u0434\u043b\u044f iOS \u0438 iPadOS \u0441 Nugget. \u0423\u0437\u043d\u0430\u0439\u0442\u0435, \u0447\u0442\u043e \u0442\u0430\u043a\u043e\u0435 \u0444\u0430\u0439\u043b .tendies, \u043a\u0430\u043a \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0430\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043e\u0431\u043e\u0438 \u0431\u0435\u0437 \u0434\u0436\u0435\u0439\u043b\u0431\u0440\u0435\u0439\u043a\u0430 \u0438 \u0438\u0437\u0443\u0447\u0438\u0442\u0435 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443 \u043d\u0430 Nugget Wallpaper.",
    "kw": "\u043e\u0431\u043e\u0438 tendies, \u0444\u0430\u0439\u043b tendies, \u043e\u0431\u043e\u0438 Nugget, \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043e\u0431\u043e\u0438 iOS, \u043e\u0431\u043e\u0438 PosterBoard, \u043e\u0431\u043e\u0438 ios 18, \u043e\u0431\u043e\u0438 ios 27, \u0430\u043d\u0438\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u044d\u043a\u0440\u0430\u043d \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438",
}

T["ja"] = {
    "nav_wiki": "\u3068\u306f",
    "nav_install": "\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb",
    "nav_gallery": "\u30ae\u30e3\u30e9\u30ea\u30fc",
    "nav_faq": "FAQ",
    "nav_cta": "\u58c1\u7d19\u3092\u898b\u308b",
    "lang_label": "\u8a00\u8a9e",
    "hero_kicker": "Tendies Wallpaper \u516c\u5f0f\u30db\u30fc\u30e0",
    "hero_h1_lead": "iOS \u52d5\u7684\u58c1\u7d19\u3067\u3001\u305d\u306e",
    "hero_h1_after": "\u30ed\u30c3\u30af\u753b\u9762\u3092\u751f\u304d\u305f\u3089\u308b\u3002",
    "hero_lead": "Tendies Wallpaper \u306f iPhone \u30fb iPad \u5411\u3051\u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3\u4ed8\u304d\u52d5\u7684\u58c1\u7d19\u306e\u30ad\u30e5\u30ec\u30fc\u30b7\u30e7\u30f3\u3002\u7121\u6599\u306e\u30aa\u30fc\u30d7\u30f3\u30bd\u30fc\u30b9\u30c4\u30fc\u30eb Nugget \u3068 .tendies \u30d5\u30a1\u30a4\u30eb\u3067\u898b\u3048\u304d\u308a\u306b\u306a\u308a\u307e\u3059\u3002\u30b8\u30a7\u30a4\u30eb\u30d6\u30ec\u30a4\u30af\u4e0d\u8981\u3001\u59a5\u5354\u306a\u3057\u3002iOS / iPadOS 17&ndash;27 \u5bfe\u5fdc\u3002",
    "hero_btn1": "\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u3092\u62c5\u5f53",
    "hero_btn2": "\u5c0e\u5165\u65b9\u6cd5",
    "hero_btn3": "\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb\u3092\u8aad\u3080",
    "stat1b": "\u5168\u30d0\u30fc\u30b8\u30e7\u30f3\u5bfe\u5fdc",
    "stat2b": "SparseRestore / BookRestore \u3092\u4f7f\u7528",
    "stat3b": "\u30aa\u30fc\u30d7\u30f3\u30bd\u30fc\u30b9\u3067\u30b3\u30df\u30e5\u30cb\u30c6\u30a3",
    "about_tag": "Tendies Wallpaper \u3068\u306f?",
    "about_h2": "iPhone \u30fb iPad \u306e\u52d5\u7684\u58c1\u7d19\u3001\u304f\u3063\u3061\u308a\u3057\u3066\u3044\u307e\u3059",
    "about_p": "Tendies Wallpaper \u306f Nugget \u30a8\u30b3\u30b7\u30b9\u30c6\u30e0\u5411\u3051\u30ed\u30c3\u30af\u753b\u9762\u306e\u52d5\u7684\u58c1\u7d19\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u306e\u30d6\u30e9\u30f3\u30c9\u3067\u3059\u3002\u5404\u58c1\u7d19\u306f <strong>.tendies \u30d5\u30a1\u30a4\u30eb</strong> \u3068\u3057\u3066\u30d1\u30c3\u30b1\u30fc\u30b8\u5316\u3055\u308c\u3001Apple \u306e\u30cd\u30a4\u30c6\u30a3\u30d6\u30ed\u30c3\u30af\u753b\u9762\u3092\u751f\u304d\u305f\u3089\u308b\u753b\u9762\u306b\u5909\u3048\u308b PosterBoard \u30d1\u30c3\u30b1\u30fc\u30b8\u306b\u306a\u308a\u307e\u3059\u3002\u5168\u30b3\u30ec\u30af\u30b7\u30e7\u30f3\u306f <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> \u306b\u3042\u308a\u307e\u3059\u3002",
    "c1t": "\u672c\u5f53\u306e\u52d5\u7684",
    "c1d": "\u30cd\u30a4\u30c6\u30a3\u30d6\u30ed\u30c3\u30af\u753b\u9762\u306b\u52d5\u304d\u3068\u5965\u884c\u304d\u3068\u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3\u3002\u9759\u6b62\u753b\u50cf\u3058\u3083\u3042\u308a\u307e\u305b\u3093\u3002\u305d\u308c\u305e\u308c\u306e tendies \u58c1\u7d19\u306f\u30d7\u30ec\u30df\u30a2\u30e0\u306a\u751f\u304d\u305f\u3089\u308b\u753b\u9762\u3092\u76ee\u6307\u3057\u3066\u4f5c\u3089\u308c\u3066\u3044\u307e\u3059\u3002",
    "c2t": "\u30b8\u30a7\u30a4\u30eb\u30d6\u30ec\u30a4\u30af\u4e0d\u8981",
    "c2d": "tendies \u58c1\u7d19\u306f Nugget \u3067\u9069\u7528\u3057\u307e\u3059\u3002Apple \u306e SparseRestore \u3068 BookRestore \u6a5f\u69cb\u3067\u5b89\u5168\u306b\u30d5\u30a1\u30a4\u30eb\u3092\u66f8\u304d\u8fbc\u307f\u307e\u3059\u3002",
    "c3t": "\u30ad\u30e5\u30ec\u30fc\u30b7\u30e7\u30f3\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc",
    "c3d": "\u30a2\u30cb\u30e1\u3001\u30de\u30f3\u30ac\u3001\u30b9\u30dd\u30fc\u30c4\u3001Marvel\u3001\u5b87\u5b99\u306e\u5922\u306a\u3069\u3002Nugget Wallpaper \u3067\u6bce\u9031\u66f4\u65b0\u3055\u308c\u308b\u30ad\u30e5\u30ec\u30fc\u30c8\u3055\u308c\u305f\u30ae\u30e3\u30e9\u30ea\u30fc\u3067\u3059\u3002",
    "c4t": "Nugget \u518d\u99d0\u307f",
    "c4d": "\u6570\u5343\u4e07\u4eba\u306e\u30e6\u30fc\u30b6\u30fc\u304c\u4fe1\u3089\u3089\u308c\u308b leminlimez \u6c0f\u306e\u30aa\u30fc\u30d7\u30f3\u30bd\u30fc\u30b9\u30c4\u30fc\u30eb <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> \u3092\u57fa\u76e4\u306b\u69cb\u7bc9\u3002",
    "c5t": "iPhone \u30fb iPad",
    "c5d": "iOS / iPadOS 17&ndash;27 \u5bfe\u5fdc\u306e iPhone \u30fb iPad \u3067\u4f7f\u7528\u3067\u304d\u307e\u3059\u3002Dynamic Island \u306e\u6709\u7121\u306b\u3088\u3089\u306a\u3044\u3002",
    "c6t": "\u53d6\u308a\u6d88\u3057\u304c\u53ef\u80fd\u3067\u5b89\u5168",
    "c6d": "\u3059\u3079\u3066\u53d6\u308a\u6d88\u3057\u53ef\u80fd\u3067\u3059\u3002\u9069\u7528\u524d\u306b\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u3092\u3002\u30aa\u30ea\u30b8\u30ca\u30eb\u306b\u623b\u3059\u306b\u306f iTunes \u307e\u305f\u306f Finder \u3067\u3044\u3064\u3067\u3082\u5fa9\u5143\u3067\u304d\u307e\u3059\u3002",
    "tendies_h2": "tendies \u30d5\u30a1\u30a4\u30eb\u3068\u306f?",
    "tendies_p": "<strong>.tendies \u30d5\u30a1\u30a4\u30eb</strong> \u306f Nugget / PosterBoard \u30a8\u30b3\u30b7\u30b9\u30c6\u30e0 (Cowabunga \u3084 Pocket Poster \u542b\u3080) \u306e\u58c1\u7d19\u30d1\u30c3\u30b1\u30fc\u30b8\u5f62\u5f0f\u3067\u3059\u3002Nugget \u304c\u7aef\u672b\u306b\u5fa9\u5143\u3059\u308b PosterBoard \u306e\u30d5\u30a1\u30a4\u30eb\u69cb\u9020\u3092\u305d\u306e\u307e\u307e\u53ce\u7d0d\u3057\u3001\u30ed\u30c3\u30af\u753b\u9762\u306e\u30cd\u30a4\u30c6\u30a3\u30d6\u58c1\u7d19\u9078\u629e\u306b\u8868\u793a\u3055\u308c\u307e\u3059\u3002",
    "tv1_d": "PosterBoard \u30a2\u30d7\u30ea\u306e\u30b3\u30f3\u30c6\u30ca\u306b\u76f4\u63a5\u5fa9\u5143\u3057\u3001\u30d5\u30a1\u30a4\u30eb\u69cb\u9020\u3068\u58c1\u7d19 ID \u3092\u4fdd\u6301\u3057\u307e\u3059\u3002",
    "tv2_d": "\u30e9\u30f3\u30c0\u30e0\u306a UUID \u306e descriptors \u30d5\u30a9\u30eb\u30c0\u3078\u5fa9\u5143\u3057\u3001\u8907\u6570\u306e tendies \u58c1\u7d19\u304c\u4e88\u7daf\u3057\u307e\u305b\u3093\u3002",
    "tv3_d": "\u52d5\u753b\u30fb\u5199\u771f\u30d0\u30ea\u30a8\u30fc\u30b7\u30e7\u30f3\u306f Suggested Photos \u3092\u3001mercury \u30d0\u30ea\u30a8\u30fc\u30b7\u30e7\u30f3\u306f\u5bfe\u5fdc\u306e iOS \u3067 Mercury Poster \u3092\u5bfe\u8c61\u306b\u3057\u307e\u3059\u3002",
    "install_tag": "\u307f\u305a\u304b\u304b\u3089",
    "install_h2": "tendies \u58c1\u7d19\u306e\u5c0e\u5165\u306f4\u30b9\u30c6\u30c3\u30d7",
    "install_p": "USB \u30b1\u30fc\u30d6\u30eb\u3068\u7121\u6599\u306e Nugget \u30a2\u30d7\u30ea\u3067\u6570\u5206\u3067\u5b8c\u4e86\u3002\u8a73\u7d30\u306f\u516c\u5f0f\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb\u306b\u3042\u308a\u307e\u3059\u3002",
    "s1_t": "\u30d5\u30a1\u30a4\u30eb\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9",
    "s1_d": "\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u304b\u3089\u58c1\u7d19\u3092\u9078\u3093\u3067 <strong>.tendies \u30d5\u30a1\u30a4\u30eb</strong> \u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3002",
    "s2_t": "\u7aef\u672b\u3092\u63a5\u7d9a",
    "s2_d": "iPhone/iPad \u3092 USB \u3067 PC \u306b\u63a5\u7d9a\u3057\u3066\u4fe1\u983c\u3057\u307e\u3059\u3002Windows\u30fbmacOS\u30fbLinux \u5bfe\u5fdc\u3002",
    "s3_t": "\u30a4\u30f3\u30dd\u30fc\u30c8\u3057\u3066\u9069\u7528",
    "s3_d": "Nugget \u5185\u306e PosterBoard \u3092\u958b\u3044\u3066\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u3073\u3001Apply Changes \u3092\u30af\u30ea\u30c3\u30af\u3002",
    "s4_t": "\u518d\u8d77\u52d5\u3057\u3066\u697d\u3057\u3080",
    "s4_d": "\u518d\u8d77\u52d5\u5f8c\u3001\u30ed\u30c3\u30af\u753b\u9762\u30a8\u30c7\u30a3\u30bf\u3067 Collections \u307e\u305f\u306f Favorites \u306b\u65b0\u3057\u3044\u58c1\u7d19\u304c\u3042\u308a\u307e\u3059\u3002",
    "install_note": "\u3064\u307e\u3065\u3044\u305f? <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper \u516c\u5f0f\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb</a> \u3092\u8aad\u3080\u304b\u3001\u4e0b\u8a18\u306e\u30b3\u30df\u30e5\u30cb\u30c6\u30a3\u306b\u304a\u8cb8\u3057\u4e0b\u3055\u3044\u3002",
    "gallery_tag": "\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc",
    "gallery_h2": "Tendies Wallpaper \u30ae\u30e3\u30e9\u30ea\u30fc\u3092\u63a2\u3059",
    "gallery_p": "\u4e0b\u8a18\u306e tendies \u58c1\u7d19\u306f\u3001\u3059\u3079\u3066 <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> \u3067\u516c\u958b\u30fb\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3067\u304d\u307e\u3059\u3002<a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">\u65b0\u7740\u9806</a> \u3084 <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">\u4eba\u6c17\u9806</a> \u3067\u30c8\u30ec\u30f3\u30c9\u3092\u78ba\u8a8d\u3067\u304d\u307e\u3059\u3002",
    "g_t1": "\u30a2\u30cb\u30e1",
    "g_d1": "Evangelion\u3001Sylphiette \u306a\u3069",
    "g_t2": "\u30b9\u30dd\u30fc\u30c4\u3068 Marvel",
    "g_d2": "\u30af\u30e9\u30d6\u3001\u30d2\u30fc\u30ed\u30fc\u3001\u65b0\u305f\u306a\u65e5",
    "g_t3": "\u5b87\u5b99\u306e\u5922",
    "g_d3": "\u60d1\u661f\u3001\u661f\u3001\u30a2\u30d5\u30a1\u30ec\u30fc\u30b7\u30e7\u30f3",
    "g_t4": "\u30aa\u30d5\u30a3\u30b7\u30e3\u30eb",
    "g_d4": "Apple \u98a8\u306e\u30bb\u30ec\u30af\u30b7\u30e7\u30f3",
    "gallery_cta": "\u3059\u3079\u3066\u306e\u58c1\u7d19\u3092\u898b\u308b",
    "faq_h2": "\u3088\u304f\u3042\u308b\u8cea\u554f",
    "faq_p": "\u59cb\u3081\u308b\u524d\u306b\u77e5\u3063\u3066\u304a\u304d\u305f\u3044 tendies \u58c1\u7d19\u306e\u3059\u3079\u3066\u3002",
    "f1q": "tendies \u58c1\u7d19\u3068\u306f?",
    "f1a": "tendies \u58c1\u7d19\u306f iPhone \u30fb iPad \u5411\u3051\u306e\u52d5\u7684\u3067\u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3\u4ed8\u304d\u58c1\u7d19\u3002.tendies \u30d5\u30a1\u30a4\u30eb\u3068\u3057\u3066 Nugget \u3067\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u3057\u307e\u3059\u3002tendies \u30d5\u30a1\u30a4\u30eb\u306f iOS 17-27 \u306e PosterBoard descriptor \u3092\u5fa9\u5143\u3057\u3001\u30ed\u30c3\u30af\u753b\u9762\u306e Collections \u9078\u629e\u306b\u58c1\u7d19\u304c\u8868\u793a\u3055\u308c\u307e\u3059\u3002",
    "f2q": ".tendies \u30d5\u30a1\u30a4\u30eb\u3068\u306f?",
    "f2a": ".tendies \u30d5\u30a1\u30a4\u30eb\u306f Nugget \u3068 Pocket Poster \u304c\u4f7f\u7528\u3059\u308b\u30d1\u30c3\u30b1\u30fc\u30b8\u5f62\u5f0f\u3067\u3059\u3002iPhone/iPad \u306b\u5fa9\u5143\u3055\u308c\u308b PosterBoard \u306e\u30d5\u30a1\u30a4\u30eb\u69cb\u9020\u3092\u53ce\u7d0d\u3057\u3066\u304a\u308a\u3001\u30ab\u30b9\u30bf\u30e0\u52d5\u7684\u58c1\u7d19\u3092\u30ed\u30c3\u30af\u753b\u9762\u306b\u5c0e\u5165\u3059\u308b\u305f\u3081\u306b\u30a4\u30f3\u30dd\u30fc\u30c8\u3059\u308b\u30d5\u30a1\u30a4\u30eb\u3067\u3059\u3002",
    "f3q": "tendies \u58c1\u7d19\u306f\u30b8\u30a7\u30a4\u30eb\u30d6\u30ec\u30a4\u30af\u304c\u5fc5\u8981?",
    "f3a": "\u3044\u3044\u3048\u3002tendies \u58c1\u7d19\u306f\u30aa\u30fc\u30d7\u30f3\u30bd\u30fc\u30b9\u30c4\u30fc\u30eb Nugget \u3067\u9069\u7528\u3057\u307e\u3059\u3002Apple \u306e SparseRestore \u3068 BookRestore \u6a5f\u69cb\u3067\u30d5\u30a1\u30a4\u30eb\u3092\u5b89\u5168\u306b\u5909\u66f4\u3059\u308b\u306e\u3067\u3001\u30b8\u30a7\u30a4\u30eb\u30d6\u30ec\u30a4\u30af\u306f\u4e0d\u8981\u3067\u3059\u3002",
    "f4q": "\u5bfe\u5fdc\u3057\u3066\u3044\u308b iOS \u30d0\u30fc\u30b8\u30e7\u30f3\u306f?",
    "f4a": "tendies \u58c1\u7d19\u306f\u5bfe\u5fdc iPhone/iPad \u306e iOS / iPadOS 17&ndash;27 \u306b\u5bfe\u5fdc\u3057\u3066\u3044\u307e\u3059\u3002\u58c1\u7d19\u306b\u3088\u3063\u3066\u306f\u7279\u5b9a\u306e iOS \u30d0\u30fc\u30b8\u30e7\u30f3\u304c\u5fc5\u8981\u306a\u5834\u5408\u304c\u3042\u308b\u306e\u3067\u3001\u58c1\u7d19\u30da\u30fc\u30b8\u306e\u4e92\u63db\u6027\u30ce\u30fc\u30c8\u3092\u78ba\u8a8d\u3057\u3066\u304f\u3060\u3055\u3044\u3002",
    "f5q": "tendies \u58c1\u7d19\u306f\u3069\u3053\u3067\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3067\u304d\u308b?",
    "f5a": "mwallx.com \u306e Nugget Wallpaper \u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u3067 tendies \u58c1\u7d19\u3092\u63a2\u3057\u3066\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3067\u304d\u307e\u3059\u3002\u30a2\u30cb\u30e1\u3001\u30b9\u30dd\u30fc\u30c4\u3001Marvel \u306a\u3069\u52d5\u7684\u30fb\u9759\u6b62\u58c1\u7d19\u306e\u30ad\u30e5\u30ec\u30fc\u30b7\u30e7\u30f3\u3092\u7f6e\u3044\u3066\u3044\u307e\u3059\u3002",
    "f6q": "iPhone \u306b tendies \u58c1\u7d19\u3092\u5c0e\u5165\u3059\u308b\u65b9\u6cd5\u306f?",
    "f6a": ".tendies \u30d5\u30a1\u30a4\u30eb\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3057\u3001Nugget \u306e PosterBoard \u3092\u958b\u3044\u3066\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u3073\u3001Apply Changes \u3067\u9069\u7528\u3057\u3066\u518d\u8d77\u52d5\u3002\u518d\u8d77\u52d5\u5f8c\u30ed\u30c3\u30af\u753b\u9762\u30a8\u30c7\u30a3\u30bf\u3067 Collections \u307e\u305f\u306f Favorites \u306b\u58c1\u7d19\u304c\u3042\u308a\u307e\u3059\u3002",
    "f7q": "tendies \u58c1\u7d19\u306e\u4f7f\u7528\u306f\u5b89\u5168?",
    "f7a": "Nugget \u306f\u6570\u5343\u4e07\u4eba\u306e\u30e6\u30fc\u30b6\u30fc\u3092\u62b1\u3048\u308b\u4eba\u6c17\u306e\u30aa\u30fc\u30d7\u30f3\u30bd\u30fc\u30b9\u30d7\u30ed\u30b8\u30a7\u30af\u30c8\u3067\u3059\u3002\u30b7\u30b9\u30c6\u30e0\u5909\u66f4\u3067\u3059\u306e\u3067\u5148\u306b\u30d0\u30c3\u30af\u30a2\u30c3\u30d7\u3092\u3002\u5909\u66f4\u306f iTunes / Finder \u3067\u306e\u5fa9\u5143\u306b\u3088\u308a\u53d6\u308a\u6d88\u3057\u53ef\u80fd\u3067\u3059\u3002",
    "f8q": "Nugget Wallpaper \u3068 tendies \u58c1\u7d19\u306e\u9055\u3044\u306f?",
    "f8a": "Tendies Wallpaper \u306f\u52d5\u7684\u58c1\u7d19\u30b3\u30ec\u30af\u30b7\u30e7\u30f3\u306e\u30d6\u30e9\u30f3\u30c9\u540d\u3001Nugget Wallpaper (mwallx.com) \u306f\u305d\u306e\u58c1\u7d19\u3092\u516c\u958b\u3059\u308b\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u3067\u3059\u3002\u4e21\u65b9\u3068\u3082 iOS \u30ab\u30b9\u30bf\u30de\u30a4\u30ba\u30c4\u30fc\u30eb Nugget \u3067\u52d5\u304f\u540c\u3058\u30a8\u30b3\u30b7\u30b9\u30c6\u30e0\u306e\u4e00\u90e8\u3067\u3059\u3002",
    "comm_h2": "Nugget Wallpaper \u30b3\u30df\u30e5\u30cb\u30c6\u30a3\u306b\u53c2\u52a0",
    "comm_p": "\u65b0\u3057\u3044\u58c1\u7d19\u3001\u30d7\u30ec\u30d3\u30e5\u30fc\u3001\u5c0e\u5165\u30c6\u30af\u30cb\u30c3\u30af\u3092\u30c1\u30e3\u30f3\u30cd\u30eb\u3067\u30d5\u30a9\u30ed\u30fc\u3002",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "iOS \u30c4\u30fc\u30eb\u516c\u5f0f\u30b5\u30a4\u30c8",
    "cta_h2": "\u30ed\u30c3\u30af\u753b\u9762\u3092\u751f\u304d\u305f\u3089\u308b\u51c6\u5099\u306f\u3067\u304d\u3066\u3044\u307e\u3059\u304b?",
    "cta_p": "\u4eca\u3059\u3050\u7121\u6599\u306e tendies \u58c1\u7d19\u3092\u3001\u30b8\u30a7\u30a4\u30eb\u30d6\u30ec\u30a4\u30af\u306a\u3057\u3067\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3002\u5168\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u3092\u63a2\u3059\u3001\u6599\u91d1\u3092\u78ba\u8a8d\u3059\u308b\u3001\u6ce8\u6587\u3092\u30c8\u30e9\u30c3\u30ad\u30f3\u30b0\u3059\u308b\u3001\u30b9\u30c6\u30c3\u30d7\u30d0\u30a4\u30b9\u30c6\u30c3\u30d7\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb\u306f Nugget Wallpaper \u3067\u3002",
    "cta_btn1": "\u3044\u305e\u3063\u3066\u63a2\u3059",
    "cta_btn2": "\u6599\u91d1\u3092\u78ba\u8a8d",
    "foot_tw1": "\u30db\u30fc\u30e0",
    "foot_tw2": "\u3068\u306f",
    "foot_tw3": ".tendies \u30d5\u30a1\u30a4\u30eb",
    "foot_tw4": "\u5c0e\u5165\u30ac\u30a4\u30c9",
    "foot_nw1": "\u3059\u3079\u3066\u306e\u58c1\u7d19\u3092\u898b\u308b",
    "foot_nw2": "\u65b0\u7740",
    "foot_nw3": "\u4eca\u3001\u4eba\u6c17\u306e\u58c1\u7d19",
    "foot_nw4": "\u30a4\u30f3\u30dd\u30fc\u30c8\u30c1\u30e5\u30fc\u30c8\u30ea\u30a2\u30eb",
    "foot_pr1": "GitHub \u306e Nugget",
    "foot_pr2": "\u516c\u5f0f Nugget \u30c4\u30fc\u30eb",
    "foot_pr3": "\u6599\u91d1",
    "foot_pr4": "\u6ce8\u6587",
    "foot_pol1": "\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30dd\u30ea\u30b7\u30fc",
    "foot_pol2": "\u5229\u7528\u898f\u7d04",
    "foot_pol3": "DMCA \u30dd\u30ea\u30b7\u30fc",
    "foot_pol4": "UGC \u30dd\u30ea\u30b7\u30fc",
    "copyright": "Tendies Wallpaper \u306f <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> \u306e\u58c1\u7d19\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u306e\u7d39\u4ecb\u30fb\u53c2\u8003\u30da\u30fc\u30b8\u3067\u3059\u3002Nugget \u58c1\u7d19\u306f\u30aa\u30fc\u30d7\u30f3\u30bd\u30fc\u30b9\u30c4\u30fc\u30eb Nugget (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>) \u3067\u9069\u7528\u3055\u308c\u307e\u3059\u3002Apple\u3001iPhone\u3001iPad\u3001iOS \u306f Apple Inc. \u306e\u5546\u6a19\u3067\u3059\u3002\u5f53\u30b5\u30a4\u30c8\u306f Apple \u3068\u306f\u7121\u95a2\u4fc2\u3067\u3059\u3002",
    "title": "Tendies Wallpaper \u2014 Nugget \u5411\u3051 iOS \u52d5\u7684\u58c1\u7d19",
    "desc": "Tendies Wallpaper \u306f Nugget \u3067\u4f7f\u3048\u308b iOS / iPadOS \u52d5\u7684\u58c1\u7d19\u306e\u30db\u30fc\u30e0\u3067\u3059\u3002.tendies \u30d5\u30a1\u30a4\u30eb\u306e\u8aac\u660e\u3001\u30b8\u30a7\u30a4\u30eb\u30d6\u30ec\u30a4\u30af\u306a\u3057\u306e\u30a2\u30cb\u30e1\u58c1\u7d19\u5c0e\u5165\u65b9\u6cd5\u3001Nugget Wallpaper \u306e\u5168\u30e9\u30a4\u30d6\u30e9\u30ea\u30fc\u3092\u898b\u308a\u307e\u3057\u3087\u3046\u3002",
    "kw": "tendies \u58c1\u7d19, tendies \u30d5\u30a1\u30a4\u30eb, Nugget \u58c1\u7d19, iOS \u52d5\u7684\u58c1\u7d19, PosterBoard \u58c1\u7d19, ios 18 \u58c1\u7d19, ios 27 \u58c1\u7d19, \u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3\u30ed\u30c3\u30af\u753b\u9762",
}

T["de"] = {
    "nav_wiki": "\u00dcber",
    "nav_install": "Installieren",
    "nav_gallery": "Galerie",
    "nav_faq": "FAQ",
    "nav_cta": "Wallpaper ansehen",
    "lang_label": "Sprache",
    "hero_kicker": "Das offizielle Zuhause von Tendies Wallpaper",
    "hero_h1_lead": "Dynamische iOS-Wallpaper \u2013 mit",
    "hero_h1_after": "Dein Sperrbildschirm wird lebendig.",
    "hero_lead": "Tendies Wallpaper ist eine kuratierte Sammlung animierter, dynamischer Wallpaper f\u00fcr iPhone und iPad \u2013 installiert mit dem kostenlosen Open-Source-Tool Nugget \u00fcber eine einfache .tendies-Datei. Kein Jailbreak, keine Kompromisse. Unterst\u00fctzt iOS und iPadOS 17&ndash;27.",
    "hero_btn1": "Bibliothek entdecken",
    "hero_btn2": "So installierst du",
    "hero_btn3": "Tutorial lesen",
    "stat1b": "Unterst\u00fctzt alle Versionen",
    "stat2b": "Nutzt SparseRestore / BookRestore",
    "stat3b": "Open Source & Community",
    "about_tag": "Was ist Tendies Wallpaper?",
    "about_h2": "Animierte Wallpaper f\u00fcr iPhone und iPad \u2013 ordentlich gemacht",
    "about_p": "Tendies Wallpaper ist die Marke hinter einer wachsenden Bibliothek dynamischer Sperrbildschirm-Wallpaper f\u00fcr das Nugget-\u00d6kosystem. Jedes Wallpaper ist als <strong>.tendies-Datei</strong> verpackt \u2013 ein PosterBoard-Paket, das Apples nativen Sperrbildschirm in einen lebendigen Bildschirm verwandelt. Die komplette Sammlung findest du auf <a href=\"https://tendieswallpaper.com/en\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a>.",
    "c1t": "Wirklich dynamisch",
    "c1d": "Bewegung, Tiefe und Animation auf dem nativen Sperrbildschirm \u2013 kein statisches Bild. Jedes Tendies-Wallpaper ist darauf ausgelegt, wie ein Premium-Live-Bildschirm auszusehen.",
    "c2t": "Ohne Jailbreak",
    "c2d": "Tendies-Wallpaper werden mit Nugget angewendet, das Apples Wiederherstellungsmechanismen SparseRestore und BookRestore nutzt, um Dateien sicher zu schreiben.",
    "c3t": "Kuratierte Bibliothek",
    "c3d": "Anime, Manga, Sport, Marvel, Space-Tr\u00e4ume und mehr \u2013 eine kuratierte Galerie, die auf der Nugget-Wallpaper-Seite w\u00f6chentlich aktualisiert wird.",
    "c4t": "Angetrieben von Nugget",
    "c4d": "Basiert auf dem Open-Source-Tool <a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">Nugget</a> von leminlimez, dem eine Community aus Tausenden von Nutzern vertraut.",
    "c5t": "iPhone & iPad",
    "c5d": "Funktioniert auf iPhones und iPads mit iOS und iPadOS 17 bis 27 \u2013 mit oder ohne Dynamic Island.",
    "c6t": "R\u00fcckg\u00e4ngig & sicher",
    "c6d": "Alles ist umkehrbar. Erstelle vor dem Anwenden ein Backup; stelle jederzeit \u00fcber iTunes oder Finder wieder her, um zum Original zur\u00fcckzukehren.",
    "tendies_h2": "Was ist eine Tendies-Datei?",
    "tendies_p": "Eine <strong>.tendies-Datei</strong> ist das Wallpaper-Paketformat des Nugget-/PosterBoard-\u00d6kosystems (inklusive Cowabunga und Pocket Poster). Sie enth\u00e4lt die exakte PosterBoard-Dateistruktur, die Nugget auf deinem Ger\u00e4t wiederherstellt, damit das Wallpaper in der nativen Wallpaper-Auswahl des Sperrbildschirms erscheint.",
    "tv1_d": "Stellt direkt im PosterBoard-App-Container wieder her und bewahrt Dateistruktur und Wallpaper-IDs intakt.",
    "tv2_d": "Stellt im descriptors-Ordner mit zuf\u00e4lligen UUIDs wieder her, damit sich mehrere Tendies-Wallpaper nie in die Quere kommen.",
    "tv3_d": "Video- und Foto-Varianten zielen auf Suggested Photos; mercury-Varianten auf das Mercury-Poster in unterst\u00fctzten iOS-Versionen.",
    "install_tag": "Los geht\u2019s",
    "install_h2": "Installiere ein Tendies-Wallpaper in 4 Schritten",
    "install_p": "Der ganze Vorgang dauert wenige Minuten mit einem USB-Kabel und der kostenlosen App Nugget. Alle Details findest du im offiziellen Tutorial.",
    "s1_t": "Datei herunterladen",
    "s1_d": "W\u00e4hle ein Wallpaper in der Bibliothek und lade seine <strong>.tendies-Datei</strong> herunter.",
    "s2_t": "Ger\u00e4t verbinden",
    "s2_d": "Verbinde dein iPhone/iPad per USB mit dem Computer und vertraue ihm. Funktioniert unter Windows, macOS und Linux.",
    "s3_t": "Importieren & anwenden",
    "s3_d": "\u00d6ffne PosterBoard in Nugget, w\u00e4hle die Datei und klicke auf Apply Changes.",
    "s4_t": "Neustart & genie\u00dfen",
    "s4_d": "Nach dem Neustart \u00f6ffne den Sperrbildschirm-Editor und finde dein neues Wallpaper unter Collections oder Favorites.",
    "install_note": "Probleme? Lies das <a href=\"https://tendieswallpaper.com/en/tutorial/nugget\" target=\"_blank\" rel=\"noopener nofollow\">offizielle Nugget-Wallpaper-Tutorial</a> oder tritt den Community-Kan\u00e4len unten bei.",
    "gallery_tag": "Die Bibliothek",
    "gallery_h2": "Entdecke die Tendies-Wallpaper-Galerie",
    "gallery_p": "Jedes unten gezeigte Tendies-Wallpaper ist auf <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> gehostet und verf\u00fcgbar. Sortiere die Galerie nach <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=latest\" target=\"_blank\" rel=\"noopener nofollow\">Neu</a> oder <a href=\"https://tendieswallpaper.com/en/wallpapers?sortBy=hot\" target=\"_blank\" rel=\"noopener nofollow\">Beliebt</a>, um Trends zu sehen.",
    "g_t1": "Anime",
    "g_d1": "Evangelion, Sylphiette & mehr",
    "g_t2": "Sport & Marvel",
    "g_d2": "Clubs, Helden und neue Tage",
    "g_t3": "Space-Tr\u00e4ume",
    "g_d3": "Planeten, Sterne & Abstraktes",
    "g_t4": "Offiziell",
    "g_d4": "Auswahl im Apple-Stil",
    "gallery_cta": "Alle Wallpaper ansehen",
    "faq_h2": "H\u00e4ufig gestellte Fragen",
    "faq_p": "Alles, was du vor dem Start \u00fcber Tendies-Wallpaper wissen musst.",
    "f1q": "Was ist ein Tendies-Wallpaper?",
    "f1a": "Ein Tendies-Wallpaper ist ein dynamisches, animiertes Wallpaper f\u00fcr iPhone und iPad, das als .tendies-Datei verteilt und mit dem Tool Nugget installiert wird. Tendies-Dateien stellen PosterBoard-Descriptors auf iOS 17-27 wieder her, sodass das Wallpaper in der Collections-Auswahl des Sperrbildschirms erscheint.",
    "f2q": "Was ist eine .tendies-Datei?",
    "f2a": "Eine .tendies-Datei ist das Paketformat, das von Nugget und Pocket Poster verwendet wird. Sie enth\u00e4lt die PosterBoard-Dateistruktur, die auf deinem iPhone oder iPad wiederhergestellt wird, und wird importiert, um ein benutzerdefiniertes dynamisches Wallpaper auf dem Sperrbildschirm zu installieren.",
    "f3q": "Ben\u00f6tigen Tendies-Wallpaper einen Jailbreak?",
    "f3a": "Nein. Tendies-Wallpaper werden mit dem Open-Source-Tool Nugget angewendet, das Apples SparseRestore- und BookRestore-Mechanismen nutzt, um Dateien ohne Jailbreak sicher zu ver\u00e4ndern.",
    "f4q": "Welche iOS-Versionen unterst\u00fctzen Tendies-Wallpaper?",
    "f4a": "Tendies-Wallpaper unterst\u00fctzen iOS und iPadOS 17 bis 27 auf kompatiblen iPhones und iPads. Manche Wallpaper erfordern m\u00f6glicherweise eine bestimmte iOS-Version \u2013 pr\u00fcfe daher immer die Kompatibilit\u00e4tshinweise auf der Wallpaper-Seite.",
    "f5q": "Wo kann ich Tendies-Wallpaper herunterladen?",
    "f5a": "Du kannst Tendies-Wallpaper in der Nugget-Wallpaper-Bibliothek auf mwallx.com durchst\u00f6bern und herunterladen \u2013 mit kuratierten dynamischen und statischen Wallpapers, darunter Anime, Sport, Marvel und mehr.",
    "f6q": "Wie installiere ich ein Tendies-Wallpaper auf meinem iPhone?",
    "f6a": "Lade die .tendies-Datei herunter, \u00f6ffne PosterBoard in Nugget, w\u00e4hle die Datei aus, wende die \u00c4nderungen an und starte das Ger\u00e4t neu. Nach dem Neustart \u00f6ffne den Sperrbildschirm-Editor und finde das Wallpaper unter Collections oder Favorites.",
    "f7q": "Ist die Verwendung von Tendies-Wallpapers sicher?",
    "f7a": "Nugget ist ein beliebtes Open-Source-Projekt mit Tausenden von Nutzern. Wie bei jeder Systemmodifikation solltest du zuerst ein Backup erstellen. Die \u00c4nderungen sind umkehrbar \u2013 stelle das Ger\u00e4t einfach \u00fcber iTunes oder Finder wieder her.",
    "f8q": "Was ist der Unterschied zwischen Nugget Wallpaper und Tendies-Wallpapers?",
    "f8a": "Tendies Wallpaper ist der Markenname der Kollektion dynamischer Wallpapers, w\u00e4hrend Nugget Wallpaper (mwallx.com) die Bibliothek ist, die sie hostet. Beide sind Teil desselben \u00d6kosystems, das auf dem Open-Source-iOS-Anpassungstool Nugget basiert.",
    "comm_h2": "Tritt der Nugget-Wallpaper-Community bei",
    "comm_p": "Folge den Kan\u00e4len f\u00fcr neue Wallpaper, Vorschauen und schnelle Installationstipps.",
    "comm_tt_d": "@nugget_wallpaper",
    "comm_tg_d": "nugget_wallpaper",
    "comm_x_d": "@nuggetwallpaper",
    "comm_gh_d": "leminlimez/Nugget",
    "comm_host_d": "Offizielle iOS-Tool-Website",
    "cta_h2": "Bereit, deinen Sperrbildschirm zum Leben zu erwecken?",
    "cta_p": "Lade noch heute ein kostenloses Tendies-Wallpaper herunter \u2013 ohne Jailbreak. Entdecke die komplette Bibliothek, sieh Preise, verfolge Bestellungen und folge dem Schritt-f\u00fcr-Schritt-Tutorial auf der Nugget-Wallpaper-Website.",
    "cta_btn1": "Entdecken starten",
    "cta_btn2": "Preise ansehen",
    "foot_tw1": "Start",
    "foot_tw2": "\u00dcber",
    "foot_tw3": "Die .tendies-Datei",
    "foot_tw4": "Installationsanleitung",
    "foot_nw1": "Alle Wallpaper ansehen",
    "foot_nw2": "Neue Hinzuf\u00fcgungen",
    "foot_nw3": "Jetzt beliebt",
    "foot_nw4": "Import-Tutorial",
    "foot_pr1": "Nugget auf GitHub",
    "foot_pr2": "Offizielles Nugget-Tool",
    "foot_pr3": "Preise",
    "foot_pr4": "Bestellungen",
    "foot_pol1": "Datenschutzrichtlinie",
    "foot_pol2": "Nutzungsbedingungen",
    "foot_pol3": "DMCA-Richtlinie",
    "foot_pol4": "UGC-Richtlinie",
    "copyright": "Tendies Wallpaper ist eine Vorstellungs- und Referenzseite f\u00fcr die Wallpaper-Bibliothek, die auf <a href=\"https://tendieswallpaper.com\" target=\"_blank\" rel=\"noopener nofollow\">Nugget Wallpaper (mwallx.com)</a> gehostet wird. Nugget-Wallpapers werden mit dem Open-Source-Tool Nugget angewendet (<a href=\"https://github.com/leminlimez/Nugget\" target=\"_blank\" rel=\"noopener nofollow\">leminlimez/Nugget</a>). Apple, iPhone, iPad und iOS sind Marken der Apple Inc. Diese Website ist nicht mit Apple verbunden.",
    "title": "Tendies Wallpaper \u2013 dynamische iOS-Wallpaper f\u00fcr Nugget",
    "desc": "Tendies Wallpaper ist die Heimat dynamischer iOS- und iPadOS-Wallpapers mit Nugget. Erfahre, was eine .tendies-Datei ist, wie du animierte Wallpapers ohne Jailbreak installierst und entdecke die komplette Bibliothek auf Nugget Wallpaper.",
    "kw": "tendies wallpaper, tendies datei, nugget wallpaper, dynamisches ios wallpaper, posterboard wallpaper, ios 18 wallpaper, ios 27 wallpaper, animierter sperrbildschirm",
}

# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

NOW = "2026-02-17"

WALL_URL = "https://tendieswallpaper.com/"
TUTORIAL_URL = "https://nugget.host/en/tutorial/nugget"
TOOL_URL = "https://nugget.host/"

LINK_REWRITES = [
    ("https://tendieswallpaper.com/en/tutorial/nugget", TUTORIAL_URL),
    ('https://tendieswallpaper.com/en"', 'https://tendieswallpaper.com/"'),
    ("https://github.com/leminlimez/Nugget", TOOL_URL),
    ("https://www.tiktok.com/@nugget_wallpaper", ""),
    ("https://t.me/nugget_wallpaper", ""),
    ("https://x.com/nuggetwallpaper", ""),
]

COMMUNITY = [
    {"label": "foot_nw", "desc": "foot_nw1", "href": WALL_URL},
    {"label": "comm_host", "desc": "comm_host_d", "href": TUTORIAL_URL},
]

def load_wallpapers_data():
    here = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(here, "data", "wallpapers.json")
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Warning: failed to load wallpapers.json:", e)
    return [
        {
            "slug": "steel-ball-run-jojo-spin-spin",
            "title": "Steel Ball Run — Spin Spin",
            "category": "Anime",
            "category_slug": "anime",
            "tag": "JoJo / Anime",
            "img": "https://wallpaper-oss.9527012346.xyz/nugget/previews/custom/gifs/JOJO_sbr_en.gif",
            "target_url": "https://tendieswallpaper.com/wallpapers/steel-ball-run-jojo-spin-spin",
            "summary": "High-octane dynamic lock screen featuring Gyro Zeppeli and Johnny Joestar with continuous Golden Spin particle physics. Custom 60 FPS ProMotion loop optimized for iOS 18 lock screen.",
            "description": "Experience the legendary Steel Ball Run horse race right on your iPhone lock screen. This animated .tendies wallpaper captures Gyro Zeppeli unleashing the Golden Spin alongside Johnny Joestar, rendered in crisp 60 FPS fluid motion. Designed specifically for OLED displays, the rich dark contrast preserves battery life while native PosterBoard integration ensures zero background CPU overhead.",
            "specs": {
                "resolution": "1179 × 2556 px (Retina XDR)",
                "fps": "60 FPS Fluid Animation",
                "format": ".tendies (PosterBoard Bundle)",
                "file_size": "14.2 MB",
                "depth_effect": "Supported (Clock Intersect)",
                "aod_support": "Supported (Smooth Ambient Fade)",
                "jailbreak": "No (Apple SparseRestore)",
                "compatibility": "iOS 17.0 – 27.0 (iPhone & iPad)"
            },
            "tags": ["JoJo", "Steel Ball Run", "Anime", "Gyro Zeppeli", "Dynamic Lock Screen", "60 FPS"]
        },
        {
            "slug": "my-dress-up-darling-marin-six-shots",
            "title": "My Dress-Up Darling — Marin, Six Shots",
            "category": "Anime",
            "category_slug": "anime",
            "tag": "Anime / Motion",
            "img": "https://wallpaper-oss.9527012346.xyz/nugget/previews-host/gifs/my_dress_up_darling_kitagawa_marin_6_shot_burst_en.gif",
            "target_url": "https://tendieswallpaper.com/wallpapers/my-dress-up-darling-marin-six-shots",
            "summary": "Vibrant lock screen animation featuring Marin Kitagawa in a dynamic 6-shot camera burst sequence. Tuned for OLED true blacks with high dynamic contrast.",
            "description": "Bring Marin Kitagawa's irresistible charisma to your daily unlock experience. This 6-shot burst animation loops seamlessly across key photoshoot moments from My Dress-Up Darling. Engineered as a native .tendies descriptor bundle, it works seamlessly with iOS 18 depth effects and honors system wake triggers without extra battery consumption.",
            "specs": {
                "resolution": "1179 × 2556 px (Retina XDR)",
                "fps": "60 FPS Fluid Animation",
                "format": ".tendies (PosterBoard Bundle)",
                "file_size": "18.6 MB",
                "depth_effect": "Supported (Multilayer Depth)",
                "aod_support": "Supported (Subtle Standby Dim)",
                "jailbreak": "No (Apple SparseRestore)",
                "compatibility": "iOS 17.0 – 27.0 (iPhone & iPad)"
            },
            "tags": ["My Dress-Up Darling", "Marin Kitagawa", "Anime", "Cosplay", "iOS 18 Wallpaper", "60 FPS"]
        },
        {
            "slug": "f1-hamilton-sunglasses",
            "title": "F1 — Hamilton in Sunglasses",
            "category": "Sports",
            "category_slug": "sports",
            "tag": "Sports / F1",
            "img": "https://wallpaper-oss.9527012346.xyz/nugget/previews-host/gifs/f1_lewis_hamilton_sunglasses_red_white_en.gif",
            "target_url": "https://tendieswallpaper.com/wallpapers/f1-hamilton-sunglasses",
            "summary": "Sleek Formula 1 lock screen animation capturing Lewis Hamilton in classic paddock aviator sunglasses with high-contrast red and white lighting.",
            "description": "For Formula 1 racing enthusiasts and Lewis Hamilton supporters. This ultra-clean dynamic wallpaper captures the 7-time World Champion under dramatic circuit lighting with subtle head movement and atmospheric lens flares. Styled with deep cinematic shadows to maintain peak lock-screen clock legibility.",
            "specs": {
                "resolution": "1179 × 2556 px (Retina XDR)",
                "fps": "60 FPS Fluid Animation",
                "format": ".tendies (PosterBoard Bundle)",
                "file_size": "11.8 MB",
                "depth_effect": "Supported (Subject Isolation)",
                "aod_support": "Supported (Monochrome Ambient)",
                "jailbreak": "No (Apple SparseRestore)",
                "compatibility": "iOS 17.0 – 27.0 (iPhone & iPad)"
            },
            "tags": ["Formula 1", "Lewis Hamilton", "Motorsport", "Sports", "Dark Aesthetic", "iOS 18"]
        },
        {
            "slug": "mushoku-tensei-sylphiette-fitz",
            "title": "Mushoku Tensei — Sylphiette (Fitz)",
            "category": "Anime",
            "category_slug": "anime",
            "tag": "Anime / Fantasy",
            "img": "https://wallpaper-oss.9527012346.xyz/nugget/previews/custom/gifs/mushoku_tensei_jobless_reincarnation_sylphiette_greyrat_sylphy_fitz_2.gif",
            "target_url": "https://tendieswallpaper.com/wallpapers/mushoku-tensei-sylphiette-fitz",
            "summary": "Enchanting animated wallpaper showcasing Sylphiette (Silent Fitz) from Jobless Reincarnation with gentle ambient wind and particle effects.",
            "description": "Immerse your iPhone in the magical atmosphere of Ranoa Academy. Featuring Sylphiette in her Silent Fitz persona from Mushoku Tensei, this dynamic wallpaper features graceful hair animation and gentle floating magical light motes. Balanced color grading ensures clock and lock-screen widget readability under all lighting conditions.",
            "specs": {
                "resolution": "1179 × 2556 px (Retina XDR)",
                "fps": "60 FPS Fluid Animation",
                "format": ".tendies (PosterBoard Bundle)",
                "file_size": "16.4 MB",
                "depth_effect": "Supported (Magic Layering)",
                "aod_support": "Supported (Soft Glowing Particles)",
                "jailbreak": "No (Apple SparseRestore)",
                "compatibility": "iOS 17.0 – 27.0 (iPhone & iPad)"
            },
            "tags": ["Mushoku Tensei", "Sylphiette", "Fitz", "Anime", "Fantasy", "Live Lock Screen"]
        }
    ]

WALLPAPERS = load_wallpapers_data()

GALLERY = [
    {
        "title": w["title"],
        "img": w["img"],
        "href": w["target_url"],
        "slug": w["slug"],
        "tag": w["tag"],
    }
    for w in WALLPAPERS
]

NAV = [{"key": "nav_wiki", "href": "#about"}, {"key": "nav_install", "href": "#install"}, {"key": "nav_gallery", "href": "#gallery"}, {"key": "nav_faq", "href": "#faq"}]

TOOLS = [
    {"name": "tv1_t", "title": "posterboard", "icon": "\U0001F4F1", "d": "tv1_d"},
    {"name": "tv2_t", "title": "descriptors", "icon": "\U0001F4C1", "d": "tv2_d"},
    {"name": "tv3_t", "title": "suggested / mercury", "icon": "\U0001F3AC", "d": "tv3_d"},
]

FAQ = [
    ("f1q", "f1a"), ("f2q", "f2a"), ("f3q", "f3a"), ("f4q", "f4a"),
    ("f5q", "f5a"), ("f6q", "f6a"), ("f7q", "f7a"), ("f8q", "f8a"),
]

STEPS = [("s1_t", "s1_d", "01"), ("s2_t", "s2_d", "02"), ("s3_t", "s3_d", "03"), ("s4_t", "s4_d", "04")]


def t(lang, key):
    return T.get(lang, {}).get(key) or T["en"].get(key, "")


def alternates(lang, full):
    links = ""
    for loc in LOCALES:
        hreflang = loc["hreflang"]
        if loc["code"] == "en":
            href = BASE_URL + "/" if full else "/"
        else:
            href = (BASE_URL if full else "") + loc["path"]
        links += '<link rel="alternate" hreflang="%s" href="%s" />\n    ' % (hreflang, href)
    links += '<link rel="alternate" hreflang="x-default" href="%s/" />' % BASE_URL
    return links


def jsonld(lang, path):
    page_url = BASE_URL + path
    org = {
        "@type": "Organization",
        "@id": BASE_URL + "/#organization",
        "name": "Tendies Wallpaper",
        "url": BASE_URL + "/",
        "sameAs": [
            "https://tendieswallpaper.com/",
            "https://nugget.host/",
        ],
    }
    website = {
        "@type": "WebSite",
        "@id": BASE_URL + "/#website",
        "url": BASE_URL + "/",
        "name": "Tendies Wallpaper",
        "inLanguage": lang,
        "publisher": {"@id": BASE_URL + "/#organization"},
    }
    faq = []
    for qi, ai in FAQ:
        faq.append({
            "@type": "Question",
            "name": t(lang, qi),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": t(lang, ai),
            },
        })
    page = {
        "@type": "WebPage",
        "@id": page_url + "#webpage",
        "url": page_url,
        "name": t(lang, "title"),
        "description": t(lang, "desc"),
        "inLanguage": lang,
        "isPartOf": {"@id": BASE_URL + "/#website"},
        "about": {"@id": BASE_URL + "/#organization"},
    }
    howto_steps = []
    for idx, (title_key, desc_key, num) in enumerate(STEPS):
        howto_steps.append({
            "@type": "HowToStep",
            "position": idx + 1,
            "name": t(lang, title_key),
            "text": t(lang, desc_key),
            "url": page_url + "#install",
        })
    howto = {
        "@type": "HowTo",
        "@id": page_url + "#howto",
        "name": t(lang, "install_h2"),
        "description": t(lang, "install_p"),
        "inLanguage": lang,
        "totalTime": "PT5M",
        "step": howto_steps,
    }
    data = {
        "@context": "https://schema.org",
        "@graph": [org, website, page, howto, {
            "@type": "FAQPage",
            "@id": page_url + "#faq",
            "name": t(lang, "faq_h2"),
            "inLanguage": lang,
            "isPartOf": {"@id": page_url + "#webpage"},
            "mainEntity": faq,
        }],
    }
    return json.dumps(data, ensure_ascii=False)


def build_page(loc):
    code = loc["code"]
    path = loc["path"]
    rtl = loc["dir"] == "rtl"
    body_dir = ' dir="rtl"' if rtl else ""
    url = BASE_URL + path
    page_url = BASE_URL + (path if code != "en" else "/")

    # 语言切换器：为当前激活语言添加明显的状态高光与微章
    lang_switcher_items = []
    for x in LOCALES:
        is_active = (x["code"] == code)
        active_cls = (
            "bg-indigo-500/20 text-indigo-300 font-semibold border border-indigo-500/30"
            if is_active
            else "text-slate-300 hover:text-white hover:bg-white/[0.06] border border-transparent"
        )
        item_html = (
            '<a href="%s" class="%s transition-all duration-150 text-xs px-2.5 py-1.5 rounded-lg flex items-center justify-between">'
            '<span>%s</span>%s</a>'
        ) % (
            BASE_URL + ("/" if x["code"] == "en" else x["path"]),
            active_cls,
            x["native"],
            '<span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>' if is_active else "",
        )
        lang_switcher_items.append(item_html)
    lang_switcher = "".join(lang_switcher_items)

    # 导航链接：精致字距与聚焦环
    nav_links = "".join(
        '<li><a href="%s" class="text-slate-300 hover:text-white transition-colors duration-200 text-sm font-medium focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none rounded-md px-2 py-1">%s</a></li>'
        % (h["href"], t(code, h["key"]))
        for h in NAV
    )

    # 核心特性 Bento Grid：告别死板三列等长平铺，采用不对称层次布局
    bento_configs = [
        # (col_span, icon_svg, badge_text)
        (
            "md:col-span-2 lg:col-span-2",
            '<svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>',
            "Native Dynamic",
        ),
        (
            "col-span-1",
            '<svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>',
            "SparseRestore",
        ),
        (
            "col-span-1",
            '<svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>',
            "Weekly Curated",
        ),
        (
            "col-span-1",
            '<svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>',
            "Open Source",
        ),
        (
            "col-span-1",
            '<svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>',
            "iOS & iPadOS",
        ),
        (
            "col-span-1",
            '<svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>',
            "100% Safe",
        ),
    ]

    feature_cards = ""
    for i in range(1, 7):
        col_span, icon_svg, badge_text = bento_configs[i - 1]
        is_hero_card = (i == 1)
        if is_hero_card:
            feature_cards += (
                '<div class="%s relative overflow-hidden bg-gradient-to-br from-white/[0.05] via-[#101422] to-white/[0.02] border border-white/[0.08] hover:border-indigo-500/40 rounded-3xl p-7 sm:p-8 transition-all duration-300 group shadow-lg shadow-black/20">'
                '<div class="absolute -right-12 -bottom-12 w-56 h-56 bg-indigo-500/10 blur-3xl rounded-full pointer-events-none"></div>'
                '<div class="flex items-center justify-between mb-6">'
                '<div class="w-12 h-12 rounded-2xl bg-indigo-500/15 border border-indigo-400/30 flex items-center justify-center text-indigo-400 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.2)] group-hover:scale-105 transition-transform">%s</div>'
                '<span class="text-xs font-mono font-medium text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 rounded-full px-3 py-1 shadow-sm">%s</span>'
                '</div>'
                '<h3 class="text-white text-xl sm:text-2xl font-bold tracking-tight mb-3 text-balance">%s</h3>'
                '<p class="text-slate-300/80 leading-relaxed text-sm sm:text-base max-w-xl font-normal">%s</p>'
                '</div>'
            ) % (
                col_span,
                icon_svg,
                badge_text,
                t(code, "c%dt" % i).replace("&amp;", "&"),
                t(code, "c%dd" % i),
            )
        else:
            feature_cards += (
                '<div class="%s bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 hover:bg-white/[0.05] rounded-3xl p-6 sm:p-7 transition-all duration-300 group flex flex-col justify-between shadow-sm shadow-black/20">'
                '<div>'
                '<div class="flex items-center justify-between mb-5">'
                '<div class="w-10 h-10 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center text-indigo-400 group-hover:scale-105 transition-transform">%s</div>'
                '<span class="text-[11px] font-mono text-slate-400 bg-white/[0.04] border border-white/[0.06] rounded-md px-2 py-0.5">%s</span>'
                '</div>'
                '<h3 class="text-white text-base font-semibold tracking-tight mb-2">%s</h3>'
                '<p class="text-slate-400 text-sm leading-relaxed">%s</p>'
                '</div>'
                '</div>'
            ) % (
                col_span,
                icon_svg,
                badge_text,
                t(code, "c%dt" % i).replace("&amp;", "&"),
                t(code, "c%dd" % i),
            )

    # .tendies 组成剖析：极客架构卡片
    tools_html = ""
    for tool in TOOLS:
        tools_html += (
            '<div class="relative bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 rounded-3xl p-6 sm:p-7 transition-all duration-300 group shadow-sm shadow-black/20">'
            '<div class="flex items-center justify-between mb-5">'
            '<span class="text-2xl p-2.5 rounded-2xl bg-white/[0.04] border border-white/10 shadow-inner">%s</span>'
            '<span class="font-mono text-xs text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-1 rounded-md">.%s</span>'
            '</div>'
            '<h3 class="text-white font-semibold text-base mb-2 tracking-tight">%s <span class="text-slate-400 text-xs font-mono font-normal tracking-normal">&middot; %s</span></h3>'
            '<p class="text-slate-400 text-sm leading-relaxed">%s</p>'
            '</div>'
        ) % (tool["icon"], tool["title"].split()[0], t(code, tool["name"]), tool["title"], t(code, tool["d"]))

    # 安装步骤：数字流线与阶梯卡片
    steps_html = ""
    for title_key, desc_key, num in STEPS:
        steps_html += (
            '<div class="relative bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 rounded-3xl p-6 sm:p-7 transition-all duration-300 flex gap-5 group shadow-sm shadow-black/20">'
            '<div class="shrink-0 w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-400/25 flex items-center justify-center text-indigo-400 font-mono font-bold text-base shadow-[inset_0_1px_0_0_rgba(255,255,255,0.15)] group-hover:scale-105 transition-transform">%s</div>'
            '<div class="space-y-1.5">'
            '<h3 class="text-white font-semibold text-base tracking-tight">%s</h3>'
            '<p class="text-slate-400 text-sm leading-relaxed">%s</p>'
            '</div>'
            '</div>'
        ) % (num, t(code, title_key), t(code, desc_key))

    # 精品锁屏画廊：9:16 沉浸锁屏真机壁纸卡片（使用真实动态 GIF 预览与落地页链接）
    gallery_cards = ""
    for idx, g in enumerate(GALLERY):
        spoke_url = BASE_URL + "/wallpapers/" + g["slug"] + "/"
        gallery_cards += (
            '<div class="group bg-slate-900/60 border border-white/10 hover:border-indigo-400/50 rounded-3xl p-4 sm:p-5 flex flex-col justify-between transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:shadow-indigo-950/70">'
            '<a href="%s" class="block aspect-[9/16] rounded-2xl bg-black relative overflow-hidden focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">'
            '<img src="%s" alt="%s" loading="lazy" class="absolute inset-0 w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 will-change-transform" />'
            '<div class="absolute inset-0 bg-gradient-to-b from-black/70 via-transparent to-black/80 pointer-events-none"></div>'
            '<div class="relative z-10 flex items-center justify-between text-[11px] font-mono text-white/90 drop-shadow p-2">'
            '<span>09:41</span>'
            '<span class="w-12 h-3.5 bg-black/70 rounded-full border border-white/10 shadow-sm"></span>'
            '<span>5G</span>'
            '</div>'
            '<div class="absolute bottom-3 left-3 right-3 z-10 flex items-center justify-between text-xs text-white/90 drop-shadow">'
            '<span class="inline-block text-[11px] font-mono font-medium text-indigo-200 bg-black/60 border border-indigo-400/30 rounded-full px-2.5 py-0.5 backdrop-blur-md shadow-sm">%s</span>'
            '<span class="text-[11px] font-mono text-slate-300 bg-black/60 border border-white/10 rounded-full px-2 py-0.5 backdrop-blur-md">60 FPS</span>'
            '</div>'
            '</a>'
            '<div class="mt-4 flex flex-col justify-between flex-1">'
            '<div>'
            '<a href="%s" class="text-white font-semibold text-sm tracking-tight hover:text-indigo-300 transition-colors line-clamp-1 block">%s</a>'
            '<p class="text-slate-400 text-xs mt-1 leading-relaxed flex items-center gap-1.5">'
            '<span class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>'
            '<span>.tendies dynamic lockscreen</span>'
            '</p>'
            '</div>'
            '<div class="mt-4 pt-3 border-t border-white/[0.08] flex items-center justify-between text-xs">'
            '<a href="%s" class="text-indigo-400 hover:text-indigo-300 font-medium inline-flex items-center gap-1 transition-colors">Specs &amp; Guide &rarr;</a>'
            '<a href="%s" target="_blank" rel="noopener nofollow" class="w-7 h-7 rounded-lg bg-white/10 hover:bg-indigo-600 flex items-center justify-center text-white transition-all shadow-sm" title="Download on Official Store">&nearr;</a>'
            '</div>'
            '</div>'
            '</div>'
        ) % (spoke_url, g["img"], g["title"], g["tag"], spoke_url, g["title"], spoke_url, g["href"])

    # FAQ 可折叠问答：精致微玻璃卡片与顺滑旋转动效
    faq_html = ""
    for qi, ai in FAQ:
        faq_html += (
            '<details class="group bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 rounded-2xl p-5 sm:p-6 transition-all duration-200">'
            '<summary class="flex items-center justify-between gap-4 cursor-pointer text-white font-semibold text-base list-none focus-visible:outline-none focus-visible:text-indigo-400">'
            '<span class="tracking-tight">%s</span>'
            '<span class="shrink-0 w-8 h-8 rounded-xl bg-white/[0.04] border border-white/10 flex items-center justify-center text-slate-400 group-open:rotate-180 group-open:bg-indigo-500/10 group-open:text-indigo-400 group-open:border-indigo-500/30 transition-all duration-200">'
            '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>'
            '</span>'
            '</summary>'
            '<div class="mt-4 pt-4 border-t border-white/[0.06] text-slate-300/80 text-sm leading-relaxed text-pretty">'
            '%s'
            '</div>'
            '</details>'
        ) % (t(code, qi), t(code, ai))

    # 社区链接
    comm_html = ""
    for c in COMMUNITY:
        comm_html += (
            '<a href="%s" target="_blank" rel="noopener nofollow" '
            'class="bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 hover:bg-white/[0.06] rounded-3xl p-6 sm:p-7 flex flex-col justify-between transition-all duration-200 group focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none shadow-sm shadow-black/20">'
            '<div class="flex items-center justify-between mb-4">'
            '<span class="text-white font-semibold text-base group-hover:text-indigo-300 transition-colors tracking-tight">%s</span>'
            '<span class="text-slate-400 group-hover:translate-x-1 transition-transform text-sm">&rarr;</span>'
            '</div>'
            '<span class="text-slate-400 text-sm leading-relaxed">%s</span></a>'
        ) % (c["href"], t(code, c["label"]), t(code, c["desc"]))

    # 底部链接列
    footer_links = [
        ("foot_tw", [("foot_tw1", "#"), ("foot_tw2", "#about"), ("foot_tw3", "#tendies"), ("foot_tw4", "#install")]),
        ("foot_nw", [("foot_nw1", "https://tendieswallpaper.com/"), ("foot_nw2", "https://tendieswallpaper.com/en/wallpapers?sortBy=latest"), ("foot_nw3", "https://tendieswallpaper.com/en/wallpapers?sortBy=hot"), ("foot_nw4", TUTORIAL_URL)]),
        ("foot_pr", [("foot_pr1", TOOL_URL), ("foot_pr2", TUTORIAL_URL), ("foot_pr3", "https://tendieswallpaper.com/en/premium"), ("foot_pr4", "https://tendieswallpaper.com/en/orders")]),
        ("foot_pol", [("foot_pol1", "https://tendieswallpaper.com/en/privacy-policy"), ("foot_pol2", "https://tendieswallpaper.com/en/terms-of-service"), ("foot_pol3", "https://tendieswallpaper.com/en/dmca-policy"), ("foot_pol4", "https://tendieswallpaper.com/en/ugc-policy")]),
    ]
    footer_cols = ""
    for title_key, items in footer_links:
        lis = "\n".join(
            '<li><a href="%s" target="_blank" rel="noopener nofollow" class="text-slate-400 hover:text-white transition-colors text-sm focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none rounded">%s</a></li>' % (href, t(code, k)) for k, href in items
        )
        footer_cols += (
            '<div><h4 class="text-white font-semibold text-sm tracking-tight mb-4">%s</h4><ul class="space-y-2.5">%s</ul></div>' % (t(code, title_key), lis)
        )

    html = """<!DOCTYPE html>
<html lang="{html_lang}" dir="{dir}" data-locale="{code}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{page_url}">
{hreflang}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tendies Wallpaper">
<meta property="og:locale" content="{og_locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{page_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">
{ld}
</script>
{tracking}
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{
  theme: {{
    extend: {{
      colors: {{
        dark: {{
          950: '#07090e',
          900: '#0c0f17',
          850: '#111622',
          800: '#182030',
        }},
        brand: {{
          50: '#eef2ff', 100: '#e0e7ff', 200: '#c7d2fe', 300: '#a5b4fc', 400: '#818cf8',
          500: '#6366f1', 600: '#4f46e5', 700: '#4338ca', 800: '#3730a3', 900: '#312e81',
        }},
      }},
      fontFamily: {{
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      }},
    }},
  }},
}};
</script>
<style>
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: 'Plus Jakarta Sans', Inter, system-ui, -apple-system, sans-serif;
    background-color: #07090e;
    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
  }}
  .tabular-nums {{
    font-variant-numeric: tabular-nums;
  }}
  details summary::-webkit-details-marker {{ display: none; }}
  .noise-bg {{
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.02'/%3E%3C/svg%3E");
  }}
</style>
</head>
<body class="bg-[#07090e] text-slate-100 antialiased selection:bg-indigo-500/40 relative min-h-screen noise-bg" {bdir}>
  <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 z-[100] px-4 py-2 bg-indigo-600 text-white rounded-xl shadow-lg font-medium text-xs">Skip to content</a>

  <header>
    <nav class="sticky top-0 z-50 backdrop-blur-xl bg-[#07090e]/85 border-b border-white/[0.08] transition-all">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <a href="{home}" class="group flex items-center gap-2.5 font-bold text-lg tracking-tight text-white focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none rounded-lg p-1">
          <span class="w-8 h-8 rounded-xl bg-indigo-500/15 border border-indigo-400/30 text-indigo-400 flex items-center justify-center text-sm shadow-[inset_0_1px_0_0_rgba(255,255,255,0.2)] group-hover:scale-105 group-hover:border-indigo-400/60 transition-all">📱</span>
          <span>Tendies <span class="text-indigo-400 font-semibold">Wallpaper</span></span>
        </a>
        <div class="hidden md:flex items-center gap-8">
          <ul class="flex items-center gap-6">{nav_links}</ul>
          <a href="{gallery_url}" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">{nav_cta} &rarr;</a>
        </div>
        <div class="flex items-center gap-2">
          <label class="sr-only">{lang_label}</label>
          <details class="relative">
            <summary class="cursor-pointer list-none text-slate-300 hover:text-white text-xs font-medium px-2.5 py-1.5 rounded-lg border border-white/[0.08] hover:border-white/20 bg-white/[0.03] hover:bg-white/[0.08] transition-all flex items-center gap-1.5 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">
              <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span>{code_native}</span>
              <svg class="w-3 h-3 text-slate-400 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </summary>
            <div class="absolute {align_label} top-10 bg-[#0e131f] border border-white/10 rounded-2xl p-2 shadow-2xl w-56 grid gap-0.5 max-h-80 overflow-auto z-50">
              {lang_switcher}
            </div>
          </details>
          <a href="{gallery_url}" target="_blank" rel="noopener nofollow" class="md:hidden rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white">{nav_cta_short}</a>
        </div>
      </div>
    </nav>
  </header>

  <main id="main-content">
    <section class="relative overflow-hidden pt-12 pb-24 lg:pt-20 lg:pb-32">
      <!-- 柔和单色环境景深光 -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[380px] bg-indigo-500/15 blur-[140px] rounded-full pointer-events-none"></div>

      <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
        <div class="text-center max-w-3xl mx-auto">
          <div class="inline-flex items-center gap-2 text-xs font-medium text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 rounded-full px-3.5 py-1.5 mb-8 shadow-sm">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
            <span>{hero_kicker}</span>
          </div>

          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-[-0.035em] leading-[1.08] text-white" style="text-wrap: balance;">
            {hero_h1_lead} <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 via-indigo-100 to-indigo-400">{hero_h1_after}</span>
          </h1>

          <p class="mt-6 text-base sm:text-lg text-slate-300/90 leading-relaxed max-w-2xl mx-auto font-normal" style="text-wrap: pretty;">
            {hero_lead}
          </p>

          <div class="mt-10 flex flex-wrap items-center justify-center gap-3.5 sm:gap-4">
            <a href="{gallery_url}" target="_blank" rel="noopener nofollow" class="rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] px-7 py-3.5 font-semibold text-white shadow-lg shadow-indigo-600/30 hover:shadow-indigo-600/40 border-t border-white/20 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">{hero_btn1}</a>
            <a href="#install" class="rounded-xl border border-white/10 bg-white/[0.04] hover:bg-white/[0.08] hover:border-white/20 active:scale-[0.98] px-6 py-3.5 font-medium text-slate-200 hover:text-white transition-all duration-200 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">{hero_btn2}</a>
            <a href="{tutorial_url}" target="_blank" rel="noopener nofollow" class="rounded-xl border border-transparent hover:border-white/10 px-6 py-3.5 font-medium text-slate-400 hover:text-white transition-all duration-200 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">{hero_btn3} &rarr;</a>
          </div>
        </div>

        <!-- 拟态 iPhone 锁屏模型与三指标全景画卷 -->
        <div class="mt-16 sm:mt-20 max-w-4xl mx-auto">
          <div class="relative mx-auto rounded-3xl p-3 sm:p-5 bg-gradient-to-b from-white/[0.08] to-white/[0.02] border border-white/[0.1] shadow-2xl backdrop-blur-2xl">
            <div class="rounded-2xl bg-[#080a0f] border border-white/[0.06] overflow-hidden p-6 sm:p-10 relative">
              <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-950/40 via-transparent to-transparent pointer-events-none"></div>

              <div class="relative grid md:grid-cols-12 gap-8 items-center">
                <!-- 左翼特性指标 -->
                <div class="md:col-span-4 space-y-4 text-start">
                  <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:border-indigo-500/30 transition-colors">
                    <div class="flex items-center gap-2 font-mono text-xs text-indigo-400 uppercase tracking-wider font-semibold">
                      <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                      <span>{stat1a}</span>
                    </div>
                    <div class="mt-1.5 text-sm font-semibold text-white">{stat1b}</div>
                  </div>
                  <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:border-indigo-500/30 transition-colors">
                    <div class="flex items-center gap-2 font-mono text-xs text-indigo-400 uppercase tracking-wider font-semibold">
                      <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
                      <span>{stat2a}</span>
                    </div>
                    <div class="mt-1.5 text-sm font-semibold text-white">{stat2b}</div>
                  </div>
                </div>

                <!-- 居中拟真 iOS 锁屏动态壁纸机身 -->
                <div class="md:col-span-4 flex justify-center">
                  <div class="w-64 sm:w-72 aspect-[9/18.5] rounded-[2.5rem] p-2.5 bg-slate-900/90 border-2 border-slate-700/60 shadow-2xl shadow-indigo-950/60 relative overflow-hidden ring-1 ring-white/10 group">
                    <div class="w-full h-full rounded-[2.1rem] overflow-hidden relative flex flex-col justify-between p-5 bg-slate-950 border border-white/10">
                      <!-- 真实动态壁纸预览 -->
                      <img src="https://wallpaper-oss.9527012346.xyz/nugget/previews/custom/gifs/JOJO_sbr_en.gif" alt="Dynamic Wallpaper Live Preview" class="absolute inset-0 w-full h-full object-cover object-center opacity-85 group-hover:scale-105 transition-transform duration-700 pointer-events-none will-change-transform" />
                      <div class="absolute inset-0 bg-gradient-to-b from-black/70 via-black/25 to-black/80 pointer-events-none"></div>

                      <!-- 灵动岛 (Dynamic Island) -->
                      <div class="relative z-10 w-24 h-5 mx-auto bg-black rounded-full flex items-center justify-end px-2 gap-1.5 shadow-sm">
                        <span class="w-2 h-2 rounded-full bg-emerald-500/80"></span>
                      </div>
                      <!-- 锁屏时钟与日期 -->
                      <div class="relative z-10 text-center mt-2">
                        <p class="text-[10px] font-medium tracking-wide uppercase text-indigo-100/90 font-mono drop-shadow">Monday, October 14</p>
                        <div class="text-5xl font-extrabold tracking-tight text-white font-sans mt-0.5 tabular-nums drop-shadow-md" style="letter-spacing: -0.05em;">09:41</div>
                      </div>
                      <!-- 动态壁纸徽标 -->
                      <div class="relative z-10 my-auto text-center py-4">
                        <span class="inline-block text-[11px] font-mono font-medium text-indigo-200 bg-black/60 border border-indigo-400/30 rounded-full px-3 py-1 shadow-lg backdrop-blur-md">.tendies engine active</span>
                      </div>
                      <!-- 底部快捷按键 -->
                      <div class="relative z-10 flex items-center justify-between px-2 text-white/90">
                        <div class="w-9 h-9 rounded-full bg-black/50 backdrop-blur-md border border-white/20 flex items-center justify-center text-xs">🔦</div>
                        <div class="w-12 h-1 bg-white/50 rounded-full"></div>
                        <div class="w-9 h-9 rounded-full bg-black/50 backdrop-blur-md border border-white/20 flex items-center justify-center text-xs">📷</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 右翼特性指标 -->
                <div class="md:col-span-4 space-y-4 text-start">
                  <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:border-indigo-500/30 transition-colors">
                    <div class="flex items-center gap-2 font-mono text-xs text-indigo-400 uppercase tracking-wider font-semibold">
                      <span class="w-2 h-2 rounded-full bg-sky-400"></span>
                      <span>{stat3a}</span>
                    </div>
                    <div class="mt-1.5 text-sm font-semibold text-white">{stat3b}</div>
                  </div>
                  <div class="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-200 text-xs leading-relaxed">
                    <div class="font-semibold text-white mb-1">PosterBoard Engine</div>
                    Native lockscreen bundle integration via Apple restore mechanism.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="about" class="py-24 border-t border-white/[0.06]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">{about_tag}</p>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white max-w-2xl text-balance">{about_h2}</h2>
        <p class="mt-5 text-slate-400 leading-relaxed max-w-3xl text-pretty">{about_p}</p>
        <div class="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {feature_cards}
        </div>
      </div>
    </section>

    <section id="tendies" class="py-24 bg-[#0a0d15]/60 border-y border-white/[0.06]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">{tendies_tag}</p>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white text-balance">{tendies_h2}</h2>
        <p class="mt-5 text-slate-400 leading-relaxed max-w-3xl text-pretty">{tendies_p}</p>
        <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          {tools_html}
        </div>
      </div>
    </section>

    <section id="install" class="py-24 border-b border-white/[0.06]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">{install_tag}</p>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white text-balance">{install_h2}</h2>
        <p class="mt-5 text-slate-400 leading-relaxed max-w-2xl text-pretty">{install_p}</p>
        <div class="mt-12 grid md:grid-cols-2 gap-6">
          {steps_html}
        </div>
        <div class="mt-8 p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] text-slate-400 text-xs sm:text-sm flex items-center gap-3">
          <span class="text-indigo-400 text-base font-bold">&excl;</span>
          <span>{install_note}</span>
        </div>
      </div>
    </section>

    <section id="compare" class="py-20 bg-[#080a0f] border-b border-white/[0.06]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">Technical Architecture Comparison</p>
          <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-white text-balance">Why .tendies Beats Traditional Methods</h2>
          <p class="mt-4 text-slate-400 text-sm leading-relaxed text-pretty">Comparing native PosterBoard dynamic wallpaper bundles against legacy Live Photos and risky jailbreak tweaks.</p>
        </div>

        <div class="overflow-x-auto rounded-3xl border border-white/[0.08] bg-white/[0.02] shadow-2xl">
          <table class="w-full text-left border-collapse text-xs sm:text-sm">
            <thead>
              <tr class="border-b border-white/[0.08] bg-white/[0.03]">
                <th class="p-4 sm:p-5 font-semibold text-white">Feature &amp; Metric</th>
                <th class="p-4 sm:p-5 font-semibold text-indigo-400 bg-indigo-500/[0.06] border-x border-white/[0.08]">Tendies (.tendies + Nugget)</th>
                <th class="p-4 sm:p-5 font-semibold text-slate-400">Apple Live Photos</th>
                <th class="p-4 sm:p-5 font-semibold text-slate-400">Jailbreak / Dylib Injection</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.06] text-slate-300">
              <tr class="hover:bg-white/[0.02] transition-colors">
                <td class="p-4 sm:p-5 font-medium text-white">Dynamic Lockscreen Effect</td>
                <td class="p-4 sm:p-5 text-emerald-400 font-medium bg-indigo-500/[0.03] border-x border-white/[0.08]">True continuous native motion &amp; depth</td>
                <td class="p-4 sm:p-5 text-slate-400">3-second press-and-hold loop only</td>
                <td class="p-4 sm:p-5 text-slate-300">Continuous animation via hooked process</td>
              </tr>
              <tr class="hover:bg-white/[0.02] transition-colors">
                <td class="p-4 sm:p-5 font-medium text-white">Jailbreak Required?</td>
                <td class="p-4 sm:p-5 text-emerald-400 font-medium bg-indigo-500/[0.03] border-x border-white/[0.08]">❌ No (Apple SparseRestore / BookRestore)</td>
                <td class="p-4 sm:p-5 text-slate-400">❌ No</td>
                <td class="p-4 sm:p-5 text-rose-400 font-medium">✔️ Yes (Kernel / PPL bypass required)</td>
              </tr>
              <tr class="hover:bg-white/[0.02] transition-colors">
                <td class="p-4 sm:p-5 font-medium text-white">Battery &amp; Idle Drain</td>
                <td class="p-4 sm:p-5 text-emerald-400 font-medium bg-indigo-500/[0.03] border-x border-white/[0.08]">0% idle drain (Native Apple PosterBoard)</td>
                <td class="p-4 sm:p-5 text-slate-400">Zero idle drain</td>
                <td class="p-4 sm:p-5 text-amber-400">Moderate to severe background drain</td>
              </tr>
              <tr class="hover:bg-white/[0.02] transition-colors">
                <td class="p-4 sm:p-5 font-medium text-white">Compatibility</td>
                <td class="p-4 sm:p-5 font-mono text-white bg-indigo-500/[0.03] border-x border-white/[0.08]">iOS &amp; iPadOS 17.0 &ndash; 27 (All versions)</td>
                <td class="p-4 sm:p-5 font-mono text-slate-400">iOS 17+ (Limited devices)</td>
                <td class="p-4 sm:p-5 font-mono text-rose-300">Outdated iOS versions only</td>
              </tr>
              <tr class="hover:bg-white/[0.02] transition-colors">
                <td class="p-4 sm:p-5 font-medium text-white">System Safety &amp; Stock Restore</td>
                <td class="p-4 sm:p-5 text-emerald-400 font-medium bg-indigo-500/[0.03] border-x border-white/[0.08]">100% reversible anytime via iTunes/Finder</td>
                <td class="p-4 sm:p-5 text-slate-400">Stock feature</td>
                <td class="p-4 sm:p-5 text-rose-400">Risk of bootloops, voided warranty</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="gallery" class="py-24 bg-[#0a0d15]/60 border-b border-white/[0.06]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-6 mb-12">
          <div>
            <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">{gallery_tag}</p>
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white text-balance">{gallery_h2}</h2>
            <p class="mt-4 text-slate-400 leading-relaxed max-w-2xl text-pretty">{gallery_p}</p>
          </div>
          <div class="flex items-center gap-3 self-start sm:self-auto shrink-0">
            <a href="{wallpapers_hub_url}" class="inline-flex items-center gap-1.5 rounded-xl bg-white/[0.04] border border-white/10 hover:border-indigo-400/50 hover:bg-white/[0.08] px-4 py-2.5 font-medium text-slate-200 transition-all text-xs sm:text-sm">Browse Catalog &rarr;</a>
            <a href="{gallery_url}" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] px-5 py-2.5 font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all duration-200 text-xs sm:text-sm">{gallery_cta} &rarr;</a>
          </div>
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-5 sm:gap-6">
          {gallery_cards}
        </div>
      </div>
    </section>

    <section id="faq" class="py-24 border-b border-white/[0.06]">
      <div class="max-w-3xl mx-auto px-4 sm:px-6">
        <div class="text-center mb-12">
          <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">{faq_tag}</p>
          <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white text-balance">{faq_h2}</h2>
          <p class="mt-4 text-slate-400 max-w-xl mx-auto text-pretty">{faq_p}</p>
        </div>
        <div class="space-y-4">
          {faq_html}
        </div>
      </div>
    </section>

    <section id="community" class="py-24 bg-[#0a0d15]/60 border-b border-white/[0.06]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-3">{comm_tag}</p>
          <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white text-balance">{comm_h2}</h2>
          <p class="mt-4 text-slate-400 text-pretty">{comm_p}</p>
        </div>
        <div class="grid gap-6 sm:grid-cols-2 max-w-2xl mx-auto">
          {comm_html}
        </div>
      </div>
    </section>

    <section class="py-24">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="relative overflow-hidden rounded-3xl bg-gradient-to-b from-[#111625] to-[#0c0f18] border border-indigo-500/20 p-10 sm:p-16 text-center shadow-2xl">
          <div class="absolute -top-32 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-500/15 blur-[120px] rounded-full pointer-events-none"></div>
          <h2 class="relative text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white text-balance">{cta_h2}</h2>
          <p class="relative mt-5 text-slate-300 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed text-pretty">{cta_p}</p>
          <div class="relative mt-10 flex flex-wrap justify-center gap-4">
            <a href="{gallery_url}" target="_blank" rel="noopener nofollow" class="rounded-xl bg-white hover:bg-slate-100 active:scale-[0.98] px-7 py-3.5 font-semibold text-slate-950 shadow-lg shadow-white/10 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-white focus-visible:outline-none">{cta_btn1}</a>
            <a href="{pricing_url}" target="_blank" rel="noopener nofollow" class="rounded-xl border border-white/20 hover:border-white/40 hover:bg-white/[0.05] active:scale-[0.98] px-7 py-3.5 font-semibold text-white transition-all duration-200 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">{cta_btn2} &rarr;</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="bg-[#05070b] border-t border-white/[0.08] pt-16 pb-12">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8 pb-12">
        {footer_cols}
      </div>
      <div class="pt-8 border-t border-white/[0.06] text-slate-500 text-xs sm:text-sm leading-relaxed flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div class="max-w-2xl">{copyright}</div>
        <div class="shrink-0 text-slate-500">&copy; {year} Tendies Wallpaper &middot; <a href="{sitemap}" class="hover:text-white transition-colors underline decoration-slate-700 underline-offset-2">XML Sitemap</a></div>
      </div>
    </div>
  </footer>
</body>
</html>""".format(
        html_lang=loc["html_lang"],
        bdir=body_dir,
        dir=loc["dir"],
        code=loc["code"],
        code_native=loc["native"],
        og_locale=loc["og_locale"],
        align_label="right-0" if rtl else "left-0",
        title=t(code, "title"),
        desc=t(code, "desc"),
        kw=t(code, "kw"),
        page_url=page_url,
        home=BASE_URL + ("/" if code == "en" else loc["path"]),
        hreflang=alternates(code, True),
        ld=jsonld(code, path),
        tracking=TRACKING,
        nav_links=nav_links,
        nav_cta=t(code, "nav_cta"),
        nav_cta_short=t(code, "nav_cta"),
        lang_label=t(code, "lang_label"),
        lang_switcher=lang_switcher,
        hero_kicker=t(code, "hero_kicker"),
        hero_h1_lead=t(code, "hero_h1_lead"),
        hero_h1_after=t(code, "hero_h1_after"),
        hero_lead=t(code, "hero_lead"),
        hero_btn1=t(code, "hero_btn1"),
        hero_btn2=t(code, "hero_btn2"),
        hero_btn3=t(code, "hero_btn3"),
        stat1a=t(code, "stat1a"),
        stat1b=t(code, "stat1b"),
        stat2a=t(code, "stat2a"),
        stat2b=t(code, "stat2b"),
        stat3a=t(code, "stat3a"),
        stat3b=t(code, "stat3b"),
        gallery_url=WALL_URL,
        tutorial_url=TUTORIAL_URL,
        pricing_url="https://tendieswallpaper.com/en/premium",
        sitemap=BASE_URL + "/sitemap.xml",
        about_tag=t(code, "about_tag"),
        about_h2=t(code, "about_h2"),
        about_p=t(code, "about_p"),
        feature_cards=feature_cards,
        tendies_tag=t(code, "tendies_tag"),
        tendies_h2=t(code, "tendies_h2"),
        tendies_p=t(code, "tendies_p"),
        tools_html=tools_html,
        install_tag=t(code, "install_tag"),
        install_h2=t(code, "install_h2"),
        install_p=t(code, "install_p"),
        steps_html=steps_html,
        install_note=t(code, "install_note"),
        gallery_tag=t(code, "gallery_tag"),
        gallery_h2=t(code, "gallery_h2"),
        gallery_p=t(code, "gallery_p"),
        gallery_cards=gallery_cards,
        gallery_cta=t(code, "gallery_cta"),
        wallpapers_hub_url=BASE_URL + "/wallpapers/",
        faq_tag=t(code, "faq_tag"),
        faq_h2=t(code, "faq_h2"),
        faq_p=t(code, "faq_p"),
        faq_html=faq_html,
        comm_tag=t(code, "comm_tag"),
        comm_h2=t(code, "comm_h2"),
        comm_p=t(code, "comm_p"),
        comm_html=comm_html,
        cta_h2=t(code, "cta_h2"),
        cta_p=t(code, "cta_p"),
        cta_btn1=t(code, "cta_btn1"),
        cta_btn2=t(code, "cta_btn2"),
        footer_cols=footer_cols,
        copyright=t(code, "copyright"),
        year="2026",
    )

    for old, new in LINK_REWRITES:
        html = html.replace(old, new)
    return html


# ---------------------------------------------------------------------------
# Programmatic SEO (pSEO) Page Templates: Hub & Detail Pages
# ---------------------------------------------------------------------------

def render_base_head(title, desc, canonical, og_img=None, extra_ld=None):
    img_tags = ""
    if og_img:
        img_tags = f'<meta property="og:image" content="{og_img}">\n<meta name="twitter:image" content="{og_img}">'
    ld_script = ""
    if extra_ld:
        ld_script = f'<script type="application/ld+json">\n{json.dumps(extra_ld, ensure_ascii=False, indent=2)}\n</script>'

    return f"""<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Tendies Wallpaper">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
{img_tags}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{ld_script}
{TRACKING}
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{
  theme: {{
    extend: {{
      colors: {{
        dark: {{ 950: '#07090e', 900: '#0c0f17', 850: '#111622', 800: '#182030' }},
        brand: {{ 50: '#eef2ff', 100: '#e0e7ff', 200: '#c7d2fe', 300: '#a5b4fc', 400: '#818cf8', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca', 800: '#3730a3', 900: '#312e81' }}
      }},
      fontFamily: {{
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace']
      }}
    }}
  }}
}};
</script>
<style>
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: 'Plus Jakarta Sans', Inter, system-ui, -apple-system, sans-serif;
    background-color: #07090e;
    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
  }}
  .tabular-nums {{ font-variant-numeric: tabular-nums; }}
  details summary::-webkit-details-marker {{ display: none; }}
  .noise-bg {{
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.02'/%3E%3C/svg%3E");
  }}
</style>
</head>"""


def render_site_nav(active_page="wallpapers"):
    home_url = BASE_URL + "/"
    hub_url = BASE_URL + "/wallpapers/"
    return f"""<header>
    <nav class="sticky top-0 z-50 backdrop-blur-xl bg-[#07090e]/85 border-b border-white/[0.08] transition-all">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <a href="{home_url}" class="group flex items-center gap-2.5 font-bold text-lg tracking-tight text-white focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none rounded-lg p-1">
          <span class="w-8 h-8 rounded-xl bg-indigo-500/15 border border-indigo-400/30 text-indigo-400 flex items-center justify-center text-sm shadow-[inset_0_1px_0_0_rgba(255,255,255,0.2)] group-hover:scale-105 group-hover:border-indigo-400/60 transition-all">📱</span>
          <span>Tendies <span class="text-indigo-400 font-semibold">Wallpaper</span></span>
        </a>
        <div class="hidden md:flex items-center gap-8 text-sm">
          <ul class="flex items-center gap-6">
            <li><a href="{home_url}" class="text-slate-300 hover:text-white transition-colors">Home</a></li>
            <li><a href="{home_url}#about" class="text-slate-300 hover:text-white transition-colors">What is it</a></li>
            <li><a href="{home_url}#tendies" class="text-slate-300 hover:text-white transition-colors">.tendies file</a></li>
            <li><a href="{home_url}#install" class="text-slate-300 hover:text-white transition-colors">Install</a></li>
            <li><a href="{hub_url}" class="text-indigo-400 font-semibold">Wallpapers</a></li>
            <li><a href="{home_url}#faq" class="text-slate-300 hover:text-white transition-colors">FAQ</a></li>
          </ul>
          <a href="https://tendieswallpaper.com/" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition-all duration-200 focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">Official Store &rarr;</a>
        </div>
        <div class="flex items-center gap-2 md:hidden">
          <a href="{hub_url}" class="rounded-lg bg-white/10 px-3 py-1.5 text-xs font-semibold text-white">Catalog</a>
          <a href="https://tendieswallpaper.com/" target="_blank" rel="noopener nofollow" class="rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white">Store</a>
        </div>
      </div>
    </nav>
  </header>"""


def render_site_footer():
    home_url = BASE_URL + "/"
    hub_url = BASE_URL + "/wallpapers/"
    return f"""<footer class="bg-[#05070b] border-t border-white/[0.08] pt-16 pb-12 mt-20">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8 pb-12 text-sm">
        <div>
          <h4 class="text-white font-semibold mb-4">Tendies Wallpaper</h4>
          <ul class="space-y-2.5 text-slate-400">
            <li><a href="{home_url}" class="hover:text-white transition-colors">Home</a></li>
            <li><a href="{hub_url}" class="hover:text-white transition-colors">Wallpapers Directory</a></li>
            <li><a href="{home_url}#tendies" class="hover:text-white transition-colors">The .tendies format</a></li>
            <li><a href="{home_url}#install" class="hover:text-white transition-colors">How to Install</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Curated Wallpapers</h4>
          <ul class="space-y-2.5 text-slate-400">
            <li><a href="{BASE_URL}/wallpapers/steel-ball-run-jojo-spin-spin/" class="hover:text-white transition-colors">Steel Ball Run (JoJo)</a></li>
            <li><a href="{BASE_URL}/wallpapers/my-dress-up-darling-marin-six-shots/" class="hover:text-white transition-colors">Marin Kitagawa (Darling)</a></li>
            <li><a href="{BASE_URL}/wallpapers/f1-hamilton-sunglasses/" class="hover:text-white transition-colors">Lewis Hamilton F1</a></li>
            <li><a href="{BASE_URL}/wallpapers/mushoku-tensei-sylphiette-fitz/" class="hover:text-white transition-colors">Sylphiette (Jobless)</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Ecosystem &amp; Tools</h4>
          <ul class="space-y-2.5 text-slate-400">
            <li><a href="https://tendieswallpaper.com/" target="_blank" rel="noopener nofollow" class="hover:text-white transition-colors">Nugget Wallpaper Store</a></li>
            <li><a href="https://nugget.host/en/tutorial/nugget" target="_blank" rel="noopener nofollow" class="hover:text-white transition-colors">Nugget Install Tutorial</a></li>
            <li><a href="https://nugget.host/" target="_blank" rel="noopener nofollow" class="hover:text-white transition-colors">Nugget iOS Tool</a></li>
            <li><a href="https://tendieswallpaper.com/en/premium" target="_blank" rel="noopener nofollow" class="hover:text-white transition-colors">Premium Membership</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">System Compatibility</h4>
          <ul class="space-y-2.5 text-slate-400">
            <li><span class="text-slate-300">iOS &amp; iPadOS 17 &ndash; 27</span></li>
            <li><span class="text-slate-300">Apple PosterBoard Engine</span></li>
            <li><span class="text-emerald-400">No Jailbreak Required</span></li>
            <li><span class="text-slate-300">Reversible SparseRestore</span></li>
          </ul>
        </div>
      </div>
      <div class="pt-8 border-t border-white/[0.06] text-slate-500 text-xs sm:text-sm leading-relaxed flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div class="max-w-2xl">Tendies Wallpaper is an informational index and directory for .tendies lock screen wallpaper bundles. All trademarks belong to their respective owners.</div>
        <div class="shrink-0 text-slate-500">&copy; 2026 Tendies Wallpaper &middot; <a href="{BASE_URL}/sitemap.xml" class="hover:text-white underline">XML Sitemap</a></div>
      </div>
    </div>
  </footer>"""


def build_wallpapers_hub(wallpapers):
    page_url = BASE_URL + "/wallpapers/"
    home_url = BASE_URL + "/"
    title = "Tendies Wallpapers Library — 60 FPS Dynamic iOS Lock Screens"
    desc = "Browse curated 60 FPS .tendies dynamic lock screen wallpapers for iPhone & iPad on iOS 17–27. Anime, sports, and motion wallpapers for Nugget without jailbreak."

    # 构建卡片
    cards_html = ""
    for w in wallpapers:
        spoke_url = BASE_URL + "/wallpapers/" + w["slug"] + "/"
        cards_html += f"""
        <div class="group bg-slate-900/60 border border-white/10 hover:border-indigo-400/50 rounded-3xl p-5 flex flex-col justify-between transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:shadow-indigo-950/70">
          <a href="{spoke_url}" class="block aspect-[9/16] rounded-2xl bg-black relative overflow-hidden focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">
            <img src="{w['img']}" alt="{w['title']}" loading="lazy" class="absolute inset-0 w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 will-change-transform" />
            <div class="absolute inset-0 bg-gradient-to-b from-black/70 via-transparent to-black/80 pointer-events-none"></div>
            <div class="relative z-10 flex items-center justify-between text-[11px] font-mono text-white/90 drop-shadow p-2">
              <span>09:41</span>
              <span class="w-12 h-3.5 bg-black/70 rounded-full border border-white/10 shadow-sm"></span>
              <span>5G</span>
            </div>
            <div class="absolute bottom-3 left-3 right-3 z-10 flex items-center justify-between text-xs text-white/90 drop-shadow">
              <span class="inline-block text-[11px] font-mono font-medium text-indigo-200 bg-black/60 border border-indigo-400/30 rounded-full px-2.5 py-0.5 backdrop-blur-md shadow-sm">{w['tag']}</span>
              <span class="text-[11px] font-mono text-slate-300 bg-black/60 border border-white/10 rounded-full px-2 py-0.5 backdrop-blur-md">60 FPS</span>
            </div>
          </a>
          <div class="mt-5 flex flex-col justify-between flex-1">
            <div>
              <a href="{spoke_url}" class="text-white font-semibold text-base tracking-tight hover:text-indigo-300 transition-colors line-clamp-1 block">{w['title']}</a>
              <p class="text-slate-400 text-xs mt-2 leading-relaxed line-clamp-2">{w['summary']}</p>
            </div>
            <div class="mt-5 pt-3 border-t border-white/[0.08] flex items-center justify-between text-xs">
              <a href="{spoke_url}" class="text-indigo-400 hover:text-indigo-300 font-medium inline-flex items-center gap-1 transition-colors">Specifications &rarr;</a>
              <a href="{w['target_url']}" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 border border-indigo-400/30 hover:border-indigo-400 text-white font-medium transition-all shadow-sm">Get .tendies &nearr;</a>
            </div>
          </div>
        </div>
        """

    # Schema.org JSON-LD
    item_list = []
    for idx, w in enumerate(wallpapers):
        item_list.append({
            "@type": "ListItem",
            "position": idx + 1,
            "url": BASE_URL + "/wallpapers/" + w["slug"] + "/",
            "name": w["title"]
        })
    jsonld_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": page_url + "#webpage",
                "url": page_url,
                "name": title,
                "description": desc,
                "inLanguage": "en",
                "isPartOf": {"@id": BASE_URL + "/#website"},
                "breadcrumb": {"@id": page_url + "#breadcrumb"},
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": item_list
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": page_url + "#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": home_url
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Wallpapers",
                        "item": page_url
                    }
                ]
            }
        ]
    }

    head_html = render_base_head(title, desc, page_url, extra_ld=jsonld_data)
    nav_html = render_site_nav("wallpapers")
    footer_html = render_site_footer()

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
{head_html}
<body class="bg-[#07090e] text-slate-100 antialiased selection:bg-indigo-500/40 relative min-h-screen noise-bg">
  <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 z-[100] px-4 py-2 bg-indigo-600 text-white rounded-xl shadow-lg font-medium text-xs">Skip to content</a>
  {nav_html}

  <main id="main-content" class="max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
    <!-- 面包屑导航 -->
    <nav class="text-xs font-mono text-slate-400 flex items-center gap-2 mb-8">
      <a href="{home_url}" class="hover:text-white transition-colors">Home</a>
      <span>/</span>
      <span class="text-indigo-400">Wallpapers</span>
    </nav>

    <!-- Header 区域 -->
    <div class="max-w-3xl mb-12">
      <div class="inline-flex items-center gap-2 text-xs font-medium text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 rounded-full px-3.5 py-1.5 mb-6 shadow-sm">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
        <span>Curated .tendies Catalog</span>
      </div>
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
        Dynamic iOS Lock Screen Wallpapers
      </h1>
      <p class="mt-4 text-slate-300/80 text-base sm:text-lg leading-relaxed">
        Ultra-high-definition 60 FPS animated lock screens for Nugget. Zero background battery drain, native PosterBoard layer integration on iOS 17 through 27 without jailbreak.
      </p>

      <!-- 分类筛选胶囊 -->
      <div class="flex flex-wrap items-center gap-2.5 mt-8 text-xs font-mono">
        <span class="px-3.5 py-1.5 rounded-xl bg-indigo-600 text-white font-semibold shadow-md shadow-indigo-600/30">All Wallpapers (4)</span>
        <span class="px-3.5 py-1.5 rounded-xl bg-white/[0.04] border border-white/10 text-slate-300">Anime &amp; Manga (3)</span>
        <span class="px-3.5 py-1.5 rounded-xl bg-white/[0.04] border border-white/10 text-slate-300">Sports &amp; F1 (1)</span>
      </div>
    </div>

    <!-- 壁纸网格 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards_html}
    </div>

    <!-- 技术架构优势 Bento 模块 -->
    <section class="mt-24 pt-16 border-t border-white/[0.08]">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <h2 class="text-2xl sm:text-3xl font-bold tracking-tight text-white">Why .tendies Dynamic Wallpapers?</h2>
        <p class="text-slate-400 text-sm mt-3 leading-relaxed">Unlike battery-heavy video apps or 3-second Live Photos, .tendies files are native system assets that execute directly through Apple's PosterBoard daemon.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 transition-all">
          <div class="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-400/20 flex items-center justify-center text-indigo-400 font-mono font-bold text-sm mb-4">60</div>
          <h3 class="text-white font-semibold text-base mb-2">60 FPS Fluid ProMotion</h3>
          <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">Engineered specifically for iPhone Super Retina XDR displays with buttery-smooth refresh rates.</p>
        </div>
        <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 transition-all">
          <div class="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-400/20 flex items-center justify-center text-indigo-400 font-mono font-bold text-sm mb-4">0%</div>
          <h3 class="text-white font-semibold text-base mb-2">Zero Idle Battery Drain</h3>
          <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">Suspends seamlessly when locked or standby mode activates. No background processes or battery drain.</p>
        </div>
        <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] hover:border-indigo-500/30 transition-all">
          <div class="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-400/20 flex items-center justify-center text-indigo-400 font-mono font-bold text-sm mb-4">&check;</div>
          <h3 class="text-white font-semibold text-base mb-2">100% Stock &amp; Reversible</h3>
          <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">No kernel patching or jailbreak required. Revert anytime via iTunes or Finder with zero risk.</p>
        </div>
      </div>
    </section>
  </main>

  {footer_html}
</body>
</html>"""


def build_wallpaper_detail(item, all_items):
    slug = item["slug"]
    page_url = BASE_URL + "/wallpapers/" + slug + "/"
    home_url = BASE_URL + "/"
    hub_url = BASE_URL + "/wallpapers/"
    title = item.get("seo_title") or f"{item['title']} — Dynamic Wallpaper (.tendies)"
    desc = item.get("seo_desc") or f"Download {item['title']} dynamic .tendies wallpaper for iOS 17-26. 60 FPS fluid lock screen motion via Nugget."

    # 相关推荐（排除自身）
    related_items = [w for w in all_items if w["slug"] != slug][:4]
    related_html = ""
    for r in related_items:
        r_url = BASE_URL + "/wallpapers/" + r["slug"] + "/"
        related_html += f"""
        <div class="group bg-slate-900/60 border border-white/10 hover:border-indigo-400/50 rounded-3xl p-4 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl hover:shadow-indigo-950/50">
          <a href="{r_url}" class="block aspect-[9/16] rounded-2xl bg-black relative overflow-hidden focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:outline-none">
            <img src="{r['img']}" alt="{r['title']}" loading="lazy" class="absolute inset-0 w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 will-change-transform" />
            <div class="absolute inset-0 bg-gradient-to-b from-black/70 via-transparent to-black/80 pointer-events-none"></div>
            <div class="relative z-10 flex items-center justify-between text-[10px] font-mono text-white/90 drop-shadow p-2">
              <span>09:41</span>
              <span class="w-10 h-3 bg-black/70 rounded-full border border-white/10 shadow-sm"></span>
              <span>5G</span>
            </div>
            <div class="absolute bottom-2.5 left-2.5 right-2.5 z-10 flex items-center justify-between text-[11px] text-white/90 drop-shadow">
              <span class="inline-block font-mono font-medium text-indigo-200 bg-black/60 border border-indigo-400/30 rounded-full px-2 py-0.5 backdrop-blur-md">{r['tag']}</span>
            </div>
          </a>
          <div class="mt-3.5">
            <a href="{r_url}" class="text-white font-semibold text-sm tracking-tight hover:text-indigo-300 transition-colors line-clamp-1 block">{r['title']}</a>
            <div class="mt-3 pt-2.5 border-t border-white/[0.08] flex items-center justify-between text-xs">
              <a href="{r_url}" class="text-indigo-400 hover:text-indigo-300 font-medium">Specs &amp; Details &rarr;</a>
              <a href="{r['target_url']}" target="_blank" rel="noopener nofollow" class="text-slate-400 hover:text-white" title="Get .tendies">&nearr;</a>
            </div>
          </div>
        </div>
        """

    # Schema.org JSON-LD
    jsonld_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": page_url + "#webpage",
                "url": page_url,
                "name": title,
                "description": desc,
                "inLanguage": "en",
                "isPartOf": {"@id": BASE_URL + "/#website"},
                "breadcrumb": {"@id": page_url + "#breadcrumb"},
                "primaryImageOfPage": {"@id": page_url + "#primaryimage"}
            },
            {
                "@type": "ImageObject",
                "@id": page_url + "#primaryimage",
                "url": item["img"],
                "contentUrl": item["img"],
                "caption": item["title"] + " iOS Lock Screen Wallpaper Preview",
                "width": 1179,
                "height": 2556
            },
            {
                "@type": "BreadcrumbList",
                "@id": page_url + "#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": home_url
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Wallpapers",
                        "item": hub_url
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": item["title"],
                        "item": page_url
                    }
                ]
            },
            {
                "@type": "Product",
                "@id": page_url + "#product",
                "name": item["title"] + " .tendies Dynamic Wallpaper",
                "description": item["description"],
                "image": item["img"],
                "category": item["category"],
                "brand": {
                    "@type": "Brand",
                    "name": "Tendies Wallpaper"
                },
                "offers": {
                    "@type": "Offer",
                    "url": item["target_url"],
                    "price": "0.00",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock"
                }
            },
            {
                "@type": "HowTo",
                "@id": page_url + "#howto",
                "name": f"How to Install {item['title']} on iOS 17–27",
                "description": f"Step-by-step instructions to install {item['title']} dynamic .tendies wallpaper using Nugget.",
                "totalTime": "PT5M",
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": 1,
                        "name": "Download the .tendies file",
                        "text": f"Download the {item['title']} .tendies file bundle from the official library.",
                        "url": page_url + "#install-guide"
                    },
                    {
                        "@type": "HowToStep",
                        "position": 2,
                        "name": "Connect your iOS device",
                        "text": "Connect your iPhone or iPad to your PC or Mac via USB and trust the computer.",
                        "url": page_url + "#install-guide"
                    },
                    {
                        "@type": "HowToStep",
                        "position": 3,
                        "name": "Apply with Nugget PosterBoard",
                        "text": "Open the Nugget tool, select PosterBoard, import the file and hit Apply Changes.",
                        "url": page_url + "#install-guide"
                    },
                    {
                        "@type": "HowToStep",
                        "position": 4,
                        "name": "Reboot and Apply on Lock Screen",
                        "text": "After device restart, long-press the lock screen, tap Customize and select the wallpaper from Collections.",
                        "url": page_url + "#install-guide"
                    }
                ]
            }
        ]
    }

    head_html = render_base_head(title, desc, page_url, og_img=item["img"], extra_ld=jsonld_data)
    nav_html = render_site_nav("wallpapers")
    footer_html = render_site_footer()

    # 规格指标项
    specs = item.get("specs", {})
    specs_cards = f"""
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Resolution</div>
        <div class="mt-1 text-sm font-semibold text-white">{specs.get('resolution', '1179 × 2556 px')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Frame Rate</div>
        <div class="mt-1 text-sm font-semibold text-indigo-300">{specs.get('fps', '60 FPS')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Package Format</div>
        <div class="mt-1 text-sm font-semibold text-white">{specs.get('format', '.tendies')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">File Size</div>
        <div class="mt-1 text-sm font-semibold text-white">{specs.get('file_size', '14 MB')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Depth Effect</div>
        <div class="mt-1 text-sm font-semibold text-emerald-400">{specs.get('depth_effect', 'Supported')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Always-On (AOD)</div>
        <div class="mt-1 text-sm font-semibold text-white">{specs.get('aod_support', 'Supported')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Jailbreak?</div>
        <div class="mt-1 text-sm font-semibold text-emerald-400">{specs.get('jailbreak', 'No')}</div>
      </div>
      <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.08]">
        <div class="text-[11px] font-mono text-slate-400">Compatibility</div>
        <div class="mt-1 text-sm font-semibold text-white">{specs.get('compatibility', 'iOS 17–27')}</div>
      </div>
    </div>
    """

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
{head_html}
<body class="bg-[#07090e] text-slate-100 antialiased selection:bg-indigo-500/40 relative min-h-screen noise-bg">
  <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 z-[100] px-4 py-2 bg-indigo-600 text-white rounded-xl shadow-lg font-medium text-xs">Skip to content</a>
  {nav_html}

  <main id="main-content" class="max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
    <!-- 面包屑导航 -->
    <nav class="text-xs font-mono text-slate-400 flex items-center gap-2 mb-8">
      <a href="{home_url}" class="hover:text-white transition-colors">Home</a>
      <span>/</span>
      <a href="{hub_url}" class="hover:text-white transition-colors">Wallpapers</a>
      <span>/</span>
      <span class="text-indigo-400 truncate max-w-xs">{item['title']}</span>
    </nav>

    <!-- 核心详情区：左侧真机预览 + 右侧参数与 CTA -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-center">
      <!-- 左侧：iPhone 锁屏真机预览模型 -->
      <div class="lg:col-span-5 flex flex-col items-center">
        <div class="w-[280px] sm:w-[320px] aspect-[9/19] rounded-[48px] border-[5px] border-slate-700/80 p-3 bg-black shadow-2xl relative overflow-hidden ring-1 ring-white/15">
          <div class="w-full h-full rounded-[40px] overflow-hidden relative flex flex-col justify-between">
            <!-- 真实动图背景 -->
            <img src="{item['img']}" alt="{item['title']}" class="absolute inset-0 w-full h-full object-cover object-center" />
            <div class="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/75 pointer-events-none"></div>

            <!-- 顶部状态栏 -->
            <div class="relative z-10 flex items-center justify-between px-3 pt-2 text-[11px] font-mono text-white/90 drop-shadow">
              <span>09:41</span>
              <span class="w-16 h-4 bg-black/80 rounded-full border border-white/10 shadow-sm"></span>
              <span>5G</span>
            </div>

            <!-- 锁屏时钟 -->
            <div class="relative z-10 text-center mt-6">
              <div class="text-[12px] font-medium text-white/90 drop-shadow">Wednesday, September 16</div>
              <div class="text-6xl font-bold tracking-tight text-white font-sans drop-shadow-lg">09:41</div>
            </div>

            <!-- 动态壁纸标识 -->
            <div class="relative z-10 my-auto text-center py-4">
              <span class="inline-block text-[11px] font-mono font-medium text-indigo-200 bg-black/60 border border-indigo-400/30 rounded-full px-3 py-1 shadow-lg backdrop-blur-md">.tendies engine active</span>
            </div>

            <!-- 底部快捷按键与 Home 条 -->
            <div class="relative z-10 pb-2">
              <div class="flex items-center justify-between px-3 text-white/90 mb-3">
                <div class="w-9 h-9 rounded-full bg-black/50 backdrop-blur-md border border-white/20 flex items-center justify-center text-xs">🔦</div>
                <div class="w-9 h-9 rounded-full bg-black/50 backdrop-blur-md border border-white/20 flex items-center justify-center text-xs">📷</div>
              </div>
              <div class="w-28 h-1 bg-white/50 rounded-full mx-auto"></div>
            </div>
          </div>
        </div>
        <div class="mt-4 text-xs font-mono text-slate-400 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Native 60 FPS Lock Screen Simulation</span>
        </div>
      </div>

      <!-- 右侧：元数据、参数矩阵与 CTA -->
      <div class="lg:col-span-7 space-y-6">
        <div class="flex flex-wrap items-center gap-2">
          <span class="px-3 py-1 bg-indigo-500/10 border border-indigo-400/30 text-indigo-300 rounded-full text-xs font-mono font-medium">{item['category']}</span>
          <span class="px-3 py-1 bg-white/[0.04] border border-white/10 text-slate-300 rounded-full text-xs font-mono">60 FPS Motion</span>
          <span class="px-3 py-1 bg-emerald-500/10 border border-emerald-400/30 text-emerald-300 rounded-full text-xs font-mono">No Jailbreak</span>
        </div>

        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
          {item['title']}
        </h1>

        <p class="text-slate-300 text-base sm:text-lg leading-relaxed text-pretty">
          {item['description']}
        </p>

        <!-- 行动召唤组 -->
        <div class="pt-2 flex flex-wrap items-center gap-4">
          <a href="{item['target_url']}" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-[0.98] px-7 py-3.5 font-semibold text-white shadow-lg shadow-indigo-600/30 transition-all duration-200 text-sm sm:text-base">
            Get .tendies on Official Store &rarr;
          </a>
          <a href="#install-guide" class="inline-flex items-center gap-2 rounded-xl bg-white/[0.05] border border-white/10 hover:bg-white/[0.08] hover:border-white/20 active:scale-[0.98] px-5 py-3.5 font-medium text-slate-200 transition-all duration-200 text-sm sm:text-base">
            How to Install
          </a>
        </div>

        <!-- 规格矩阵表格 -->
        <div class="pt-4">
          <h2 class="text-xs font-mono text-slate-400 uppercase tracking-wider font-semibold mb-3">Technical Specifications</h2>
          {specs_cards}
        </div>
      </div>
    </div>

    <!-- 安装指导模块 -->
    <section id="install-guide" class="mt-24 pt-16 border-t border-white/[0.08]">
      <div class="max-w-3xl mx-auto">
        <div class="text-center mb-12">
          <p class="text-indigo-400 font-semibold text-xs uppercase tracking-widest mb-2">Step-by-Step Guide</p>
          <h2 class="text-2xl sm:text-3xl font-bold tracking-tight text-white">How to Install {item['title']}</h2>
          <p class="text-slate-400 text-sm mt-2">Applied using Apple's SparseRestore protocol via the free Nugget tool. Takes under 3 minutes.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] flex gap-4">
            <span class="w-10 h-10 shrink-0 rounded-xl bg-indigo-500/10 border border-indigo-400/20 text-indigo-400 flex items-center justify-center font-mono font-bold text-sm">01</span>
            <div>
              <h3 class="text-white font-semibold text-base mb-1">Get the .tendies file</h3>
              <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">Download the dynamic wallpaper bundle package from the official repository.</p>
            </div>
          </div>
          <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] flex gap-4">
            <span class="w-10 h-10 shrink-0 rounded-xl bg-indigo-500/10 border border-indigo-400/20 text-indigo-400 flex items-center justify-center font-mono font-bold text-sm">02</span>
            <div>
              <h3 class="text-white font-semibold text-base mb-1">Connect your iPhone / iPad</h3>
              <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">Plug your device into your computer (macOS/Windows) via USB and confirm "Trust This Computer".</p>
            </div>
          </div>
          <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] flex gap-4">
            <span class="w-10 h-10 shrink-0 rounded-xl bg-indigo-500/10 border border-indigo-400/20 text-indigo-400 flex items-center justify-center font-mono font-bold text-sm">03</span>
            <div>
              <h3 class="text-white font-semibold text-base mb-1">Import in Nugget</h3>
              <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">Open Nugget, select PosterBoard &rarr; Import .tendies file, then click "Apply Changes".</p>
            </div>
          </div>
          <div class="p-6 rounded-3xl bg-white/[0.03] border border-white/[0.08] flex gap-4">
            <span class="w-10 h-10 shrink-0 rounded-xl bg-indigo-500/10 border border-indigo-400/20 text-indigo-400 flex items-center justify-center font-mono font-bold text-sm">04</span>
            <div>
              <h3 class="text-white font-semibold text-base mb-1">Reboot &amp; Select</h3>
              <p class="text-slate-400 text-xs sm:text-sm leading-relaxed">After your device restarts, long-press your lock screen and find this wallpaper under Collections.</p>
            </div>
          </div>
        </div>

        <div class="mt-8 text-center">
          <a href="https://nugget.host/en/tutorial/nugget" target="_blank" rel="noopener nofollow" class="inline-flex items-center gap-1.5 text-xs font-mono text-indigo-400 hover:text-indigo-300 transition-colors">
            Read complete Nugget PosterBoard documentation &rarr;
          </a>
        </div>
      </div>
    </section>

    <!-- 相关壁纸横向互链 -->
    <section class="mt-24 pt-16 border-t border-white/[0.08]">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-white">More Curated Dynamic Wallpapers</h2>
          <p class="text-slate-400 text-xs sm:text-sm mt-1">Explore other 60 FPS motion lock screens in this series.</p>
        </div>
        <a href="{hub_url}" class="text-xs font-mono text-indigo-400 hover:text-indigo-300 transition-colors">Browse all &rarr;</a>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-5">
        {related_html}
      </div>
    </section>
  </main>

  {footer_html}
</body>
</html>"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    urls = []

    # 1. 生成多语言首页
    for loc in LOCALES:
        page = build_page(loc)
        out_dir = here if loc["code"] == "en" else os.path.join(here, loc["path"].strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(page)
        urls.append(BASE_URL + (loc["path"] if loc["code"] != "en" else "/"))
        print("wrote", os.path.join(out_dir, "index.html"))

    # 2. 生成 Programmatic SEO: Wallpapers Hub 目录页
    wallpapers_hub_html = build_wallpapers_hub(WALLPAPERS)
    hub_dir = os.path.join(here, "wallpapers")
    os.makedirs(hub_dir, exist_ok=True)
    with open(os.path.join(hub_dir, "index.html"), "w", encoding="utf-8") as fp:
        fp.write(wallpapers_hub_html)
    urls.append(BASE_URL + "/wallpapers/")
    print("wrote", os.path.join(hub_dir, "index.html"))

    # 3. 生成 Programmatic SEO: 各壁纸 Spoke 独立落地页
    for item in WALLPAPERS:
        detail_html = build_wallpaper_detail(item, WALLPAPERS)
        item_dir = os.path.join(hub_dir, item["slug"])
        os.makedirs(item_dir, exist_ok=True)
        with open(os.path.join(item_dir, "index.html"), "w", encoding="utf-8") as fp:
            fp.write(detail_html)
        urls.append(BASE_URL + "/wallpapers/" + item["slug"] + "/")
        print("wrote", os.path.join(item_dir, "index.html"))

    # 4. 生成 AI-SEO llms.txt
    llms_txt = (
        "# Tendies Wallpaper\n\n"
        "> Tendies Wallpaper is a curated collection of dynamic, animated lock-screen wallpapers for iPhone and iPad, installed via the open-source Nugget tool with a .tendies file format. No jailbreak is required, supporting iOS & iPadOS 17 through 27.\n\n"
        "## Core Overview\n"
        "- Official Project: https://tendieswallpaper.github.io/\n"
        "- Official Wallpaper Library: https://tendieswallpaper.com/\n"
        "- Tutorial & Guide: https://nugget.host/en/tutorial/nugget\n"
        "- Open-Source Tool: https://nugget.host/ (by leminlimez)\n"
        "- Package Format: .tendies (Apple PosterBoard restore bundle)\n"
        "- System Compatibility: iOS 17 – 27, iPadOS 17 – 27\n"
        "- Jailbreak Requirement: None (Safe restore via Apple SparseRestore / BookRestore protocols)\n\n"
        "## Key Resources & Wallpapers Catalog\n"
        "- [Wallpapers Hub Directory](https://tendieswallpaper.github.io/wallpapers/): Complete index of 60 FPS animated .tendies files.\n"
        "- [Steel Ball Run JoJo Dynamic Wallpaper](https://tendieswallpaper.github.io/wallpapers/steel-ball-run-jojo-spin-spin/)\n"
        "- [My Dress-Up Darling Marin Dynamic Wallpaper](https://tendieswallpaper.github.io/wallpapers/my-dress-up-darling-marin-six-shots/)\n"
        "- [Lewis Hamilton F1 Dynamic Wallpaper](https://tendieswallpaper.github.io/wallpapers/f1-hamilton-sunglasses/)\n"
        "- [Mushoku Tensei Sylphiette Dynamic Wallpaper](https://tendieswallpaper.github.io/wallpapers/mushoku-tensei-sylphiette-fitz/)\n"
        "- [Step-by-Step Installation](https://nugget.host/en/tutorial/nugget): Complete guide to install .tendies wallpapers using Nugget.\n"
        "- [Pricing & Access](https://tendieswallpaper.com/en/premium): Free and premium membership options.\n\n"
        "## Technical Architecture\n"
        "A `.tendies` file contains Apple PosterBoard lock screen descriptors:\n"
        "1. posterboard: Native container files, asset catalogs, and wallpaper IDs.\n"
        "2. descriptors: Randomized UUID plist entries restoring directly into Collections / Favorites.\n"
        "3. suggested / mercury: Video and motion layers targeting native PosterBoard processes with 0% idle battery drain.\n"
    )
    with open(os.path.join(here, "llms.txt"), "w", encoding="utf-8") as fp:
        fp.write(llms_txt)

    # 5. 生成 robots.txt
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "# AI search engines (GEO / AI SEO)\n"
        "User-agent: PerplexityBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: ChatGPT-User\n"
        "Allow: /\n"
        "\n"
        "User-agent: GPTBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: ClaudeBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: anthropic-ai\n"
        "Allow: /\n"
        "\n"
        "User-agent: Google-Extended\n"
        "Allow: /\n"
        "\n"
        "User-agent: Applebot-Extended\n"
        "Allow: /\n"
        "\n"
        "User-agent: Bytespider\n"
        "Allow: /\n"
        "\n"
        "Sitemap: %s/sitemap.xml\n" % BASE_URL
    )
    with open(os.path.join(here, "robots.txt"), "w", encoding="utf-8") as fp:
        fp.write(robots)

    # 6. 生成 sitemap.xml
    sitemap_urls = list(urls) + [BASE_URL + "/llms.txt"]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in sitemap_urls:
        priority = "1.0" if u == (BASE_URL + "/") else ("0.9" if "/wallpapers/" in u else "0.8")
        sitemap += "  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>\n" % (u, NOW, priority)
    sitemap += "</urlset>\n"
    with open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8") as fp:
        fp.write(sitemap)

    with open(os.path.join(here, ".nojekyll"), "w", encoding="utf-8") as fp:
        fp.write("")
    print("wrote robots.txt, sitemap.xml, llms.txt, .nojekyll")


if __name__ == "__main__":
    main()

