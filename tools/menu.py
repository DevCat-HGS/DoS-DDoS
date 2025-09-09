import sys
import time
import os
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, delay=0.05, color=Fore.GREEN):
    cursor = '█'
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
        # Efecto de cursor parpadeante
        sys.stdout.write(color + cursor + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.01)
        sys.stdout.write('\b')
    print()

def show_menu():
    print(Fore.CYAN + "\n[*] Menú de Herramientas de Prueba DoS/DDoS" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[ADVERTENCIA] Este software es para fines educativos y pruebas autorizadas" + Style.RESET_ALL)
    print(Fore.RED + "[IMPORTANTE] No utilizar en redes o sistemas sin autorización explícita" + Style.RESET_ALL)
    
    options = [
        "1. Prueba de DoS (localhost o URL/IP externa)",
        "2. Prueba de DDoS simulada (localhost o URL/IP externa)",
        "3. Información sobre ataques DoS/DDoS",
        "4. Recomendaciones para proteger tu aplicación web",
        "5. Generar informe de resistencia",
        "6. Salir"
    ]
    
    for option in options:
        print(Fore.GREEN + "\n" + option + Style.RESET_ALL)
    
    choice = input(Fore.CYAN + "\nSelecciona una opción [1-6]: " + Style.RESET_ALL)
    
    if choice == "1":
        run_dos_test()
    elif choice == "2":
        run_ddos_simulation()
    elif choice == "3":
        show_info()
    elif choice == "4":
        show_protection_recommendations()
    elif choice == "5":
        from tools.dos_tools import generate_resistance_report
        clear_screen()
        generate_resistance_report()
        input(Fore.CYAN + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
        clear_screen()
        show_menu()
    elif choice == "6":
        print(Fore.YELLOW + "\n[*] Saliendo..." + Style.RESET_ALL)
        sys.exit(0)
    else:
        print(Fore.RED + "\n[!] Opción inválida. Intenta de nuevo." + Style.RESET_ALL)
        time.sleep(1)
        clear_screen()
        show_menu()

def run_dos_test():
    clear_screen()
    print(Fore.CYAN + "\n[*] Prueba de DoS" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[NOTA] Esta herramienta permite realizar pruebas tanto en localhost como en objetivos externos (con autorización)" + Style.RESET_ALL)
    
    # Importar las funciones necesarias
    from tools.dos_tools import dos_test, check_port_open
    
    # Configurar parámetros
    target = input(Fore.CYAN + "\nIngresa la dirección IP o URL objetivo (por defecto localhost): " + Style.RESET_ALL) or "localhost"
    
    port = 80
    try:
        port = int(input(Fore.CYAN + "Ingresa el puerto a probar (por defecto 80): " + Style.RESET_ALL) or "80")
    except ValueError:
        print(Fore.RED + "\n[!] Puerto inválido, usando puerto 80" + Style.RESET_ALL)
        port = 80
    
    duration = 5
    try:
        duration = int(input(Fore.CYAN + "Ingresa la duración en segundos (por defecto 5, máximo 3600): " + Style.RESET_ALL) or "5")
        if duration <= 0:
            print(Fore.RED + "\n[!] La duración debe ser mayor que 0, usando 5 segundos" + Style.RESET_ALL)
            duration = 5
        elif duration > 3600:
            print(Fore.YELLOW + "\n[!] Por seguridad, limitando la duración a 3600 segundos (1 hora)" + Style.RESET_ALL)
            duration = 3600
    except ValueError:
        print(Fore.RED + "\n[!] Duración inválida, usando 5 segundos" + Style.RESET_ALL)
        duration = 5
    
    # Seleccionar intensidad
    print(Fore.CYAN + "\nSelecciona la intensidad de la prueba:" + Style.RESET_ALL)
    print(Fore.GREEN + "1. Baja (recomendado para pruebas iniciales)" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. Media" + Style.RESET_ALL)
    print(Fore.RED + "3. Alta (puede afectar el rendimiento del sistema)" + Style.RESET_ALL)
    
    intensity_choice = input(Fore.CYAN + "Selecciona una opción [1-3]: " + Style.RESET_ALL) or "1"
    intensity = "baja"
    if intensity_choice == "2":
        intensity = "media"
    elif intensity_choice == "3":
        intensity = "alta"
    
    # Verificar si el puerto está abierto antes de iniciar la prueba
    print(Fore.CYAN + "\n[*] Verificando si el puerto está abierto..." + Style.RESET_ALL)
    if check_port_open(host=target, port=port):
        print(Fore.GREEN + "\n[*] Iniciando prueba de DoS..." + Style.RESET_ALL)
        # Ejecutar la prueba
        dos_test(target=target, port=port, duration=duration, intensity=intensity)
    else:
        print(Fore.RED + "\n[!] No se puede realizar la prueba porque el puerto está cerrado" + Style.RESET_ALL)
        print(Fore.YELLOW + "[!] Asegúrate de que el objetivo esté en línea y el puerto especificado esté abierto" + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
    clear_screen()
    show_menu()

def run_ddos_simulation():
    clear_screen()
    print(Fore.CYAN + "\n[*] Simulación de DDoS" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[NOTA] Esta herramienta permite realizar pruebas tanto en localhost como en objetivos externos (con autorización)" + Style.RESET_ALL)
    
    # Importar las funciones necesarias
    from tools.dos_tools import ddos_simulation, check_port_open
    
    # Configurar parámetros
    target = input(Fore.CYAN + "\nIngresa la dirección IP o URL objetivo (por defecto localhost): " + Style.RESET_ALL) or "localhost"
    
    port = 80
    try:
        port = int(input(Fore.CYAN + "Ingresa el puerto a probar (por defecto 80): " + Style.RESET_ALL) or "80")
    except ValueError:
        print(Fore.RED + "\n[!] Puerto inválido, usando puerto 80" + Style.RESET_ALL)
        port = 80
    
    threads = 3
    try:
        threads = int(input(Fore.CYAN + "Ingresa el número de hilos (por defecto 3): " + Style.RESET_ALL) or "3")
        if threads <= 0:
            print(Fore.RED + "\n[!] El número de hilos debe ser mayor que 0, usando 3 hilos" + Style.RESET_ALL)
            threads = 3
        elif threads > 1000:
            print(Fore.YELLOW + "\n[!] Advertencia: Un número muy alto de hilos puede afectar el rendimiento de tu sistema" + Style.RESET_ALL)
            print(Fore.RED + "\n[!] Usando " + str(threads) + " hilos. Ten en cuenta que esto puede sobrecargar tu sistema." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "\n[!] Valor inválido, usando 3 hilos" + Style.RESET_ALL)
        threads = 3
    
    duration = 5
    try:
        duration = int(input(Fore.CYAN + "Ingresa la duración en segundos (por defecto 5, máximo 3600): " + Style.RESET_ALL) or "5")
        if duration <= 0:
            print(Fore.RED + "\n[!] La duración debe ser mayor que 0, usando 5 segundos" + Style.RESET_ALL)
            duration = 5
        elif duration > 3600:
            print(Fore.YELLOW + "\n[!] Por seguridad, limitando la duración a 3600 segundos (1 hora)" + Style.RESET_ALL)
            duration = 3600
    except ValueError:
        print(Fore.RED + "\n[!] Duración inválida, usando 5 segundos" + Style.RESET_ALL)
        duration = 5
    
    # Seleccionar intensidad
    print(Fore.CYAN + "\nSelecciona la intensidad de la prueba:" + Style.RESET_ALL)
    print(Fore.GREEN + "1. Baja (recomendado para pruebas iniciales)" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. Media" + Style.RESET_ALL)
    print(Fore.RED + "3. Alta (puede afectar el rendimiento del sistema)" + Style.RESET_ALL)
    
    intensity_choice = input(Fore.CYAN + "Selecciona una opción [1-3]: " + Style.RESET_ALL) or "1"
    intensity = "baja"
    if intensity_choice == "2":
        intensity = "media"
    elif intensity_choice == "3":
        intensity = "alta"
    
    # Verificar si el puerto está abierto antes de iniciar la simulación
    print(Fore.CYAN + "\n[*] Verificando si el puerto está abierto..." + Style.RESET_ALL)
    if check_port_open(host=target, port=port):
        print(Fore.GREEN + "\n[*] Iniciando simulación de DDoS..." + Style.RESET_ALL)
        # Ejecutar la simulación
        ddos_simulation(target=target, port=port, threads=threads, duration=duration, intensity=intensity)
    else:
        print(Fore.RED + "\n[!] No se puede realizar la simulación porque el puerto está cerrado" + Style.RESET_ALL)
        print(Fore.YELLOW + "[!] Asegúrate de que el objetivo esté en línea y el puerto especificado esté abierto" + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
    clear_screen()
    show_menu()

def show_info():
    clear_screen()
    print(Fore.CYAN + "\n[*] Información sobre ataques DoS/DDoS" + Style.RESET_ALL)
    
    # Importar la función de información educativa
    from tools.dos_tools import show_educational_info
    
    # Mostrar información
    show_educational_info()
    
    input(Fore.CYAN + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
    clear_screen()
    show_menu()

def show_protection_recommendations():
    clear_screen()
    print(Fore.CYAN + "\n[*] Recomendaciones para proteger tu aplicación web" + Style.RESET_ALL)
    
    recommendations = """
    === RECOMENDACIONES PARA PROTEGER TU APLICACIÓN WEB ===
    
    1. PROTECCIÓN A NIVEL DE INFRAESTRUCTURA:
       ✓ Utiliza servicios de protección DDoS como Cloudflare, AWS Shield o Akamai
       ✓ Implementa balanceadores de carga para distribuir el tráfico
       ✓ Configura un firewall de aplicaciones web (WAF)
       ✓ Utiliza una CDN para distribuir contenido estático
       ✓ Configura límites de conexiones por IP en tu servidor web
    
    2. PROTECCIÓN A NIVEL DE APLICACIÓN:
       ✓ Implementa limitación de tasa (rate limiting) para APIs y endpoints críticos
       ✓ Utiliza CAPTCHA para formularios y acciones importantes
       ✓ Implementa tiempos de espera adecuados para conexiones
       ✓ Utiliza caché para contenido estático y respuestas frecuentes
       ✓ Optimiza consultas de base de datos y utiliza índices apropiados
       ✓ Implementa validación estricta de entradas de usuario
    
    3. MONITOREO Y RESPUESTA:
       ✓ Configura alertas para patrones de tráfico anormales
       ✓ Implementa logging detallado de solicitudes sospechosas
       ✓ Desarrolla un plan de respuesta a incidentes
       ✓ Realiza pruebas regulares de carga y estrés
       ✓ Monitorea el uso de recursos (CPU, memoria, ancho de banda)
    
    4. ARQUITECTURA RESISTENTE:
       ✓ Diseña tu aplicación para escalar horizontalmente
       ✓ Implementa colas de tareas para procesos intensivos
       ✓ Separa componentes críticos y no críticos
       ✓ Utiliza microservicios para aislar funcionalidades
       ✓ Implementa circuit breakers para prevenir fallos en cascada
    
    5. BUENAS PRÁCTICAS DE DESARROLLO:
       ✓ Mantén todas las dependencias y frameworks actualizados
       ✓ Realiza auditorías de seguridad periódicas
       ✓ Implementa autenticación robusta (MFA cuando sea posible)
       ✓ Utiliza HTTPS para todas las comunicaciones
       ✓ Minimiza la información expuesta en cabeceras HTTP
    """
    
    print(Fore.WHITE + recommendations + Style.RESET_ALL)
    
    # Preguntar por el tipo de aplicación para dar recomendaciones específicas
    print(Fore.CYAN + "\n[*] ¿Qué tipo de aplicación web estás desarrollando?" + Style.RESET_ALL)
    print(Fore.GREEN + "\n1. Sitio web estático/informativo" + Style.RESET_ALL)
    print(Fore.GREEN + "2. Aplicación con autenticación de usuarios" + Style.RESET_ALL)
    print(Fore.GREEN + "3. API REST/GraphQL" + Style.RESET_ALL)
    print(Fore.GREEN + "4. E-commerce/Tienda online" + Style.RESET_ALL)
    print(Fore.GREEN + "5. Otro/No especificar" + Style.RESET_ALL)
    
    app_type = input(Fore.CYAN + "\nSelecciona una opción [1-5]: " + Style.RESET_ALL)
    
    # Recomendaciones específicas según el tipo de aplicación
    if app_type == "1":  # Sitio web estático
        specific_rec = """
        RECOMENDACIONES ESPECÍFICAS PARA SITIOS WEB ESTÁTICOS:
        
        ✓ Utiliza una CDN para servir todo tu contenido estático
        ✓ Implementa caché agresivo con tiempos de expiración largos
        ✓ Considera un hosting estático como GitHub Pages, Netlify o Vercel
        ✓ Minimiza y comprime archivos CSS, JavaScript e imágenes
        ✓ Implementa lazy loading para imágenes y recursos no críticos
        """
    elif app_type == "2":  # App con autenticación
        specific_rec = """
        RECOMENDACIONES ESPECÍFICAS PARA APLICACIONES CON AUTENTICACIÓN:
        
        ✓ Implementa limitación de intentos de login (rate limiting)
        ✓ Utiliza CAPTCHA después de intentos fallidos de login
        ✓ Implementa tokens JWT con tiempos de expiración adecuados
        ✓ Considera usar servicios de autenticación como Auth0 o Firebase Auth
        ✓ Implementa protección contra ataques de fuerza bruta
        ✓ Utiliza autenticación de múltiples factores (MFA)
        """
    elif app_type == "3":  # API
        specific_rec = """
        RECOMENDACIONES ESPECÍFICAS PARA APIs:
        
        ✓ Implementa autenticación basada en tokens con expiración
        ✓ Utiliza rate limiting por usuario/cliente y por endpoint
        ✓ Implementa cuotas de uso para diferentes niveles de usuarios
        ✓ Considera usar API Gateway para gestionar y proteger tus endpoints
        ✓ Implementa validación estricta de parámetros y payload
        ✓ Utiliza compresión para respuestas grandes
        ✓ Implementa circuit breakers para servicios dependientes
        """
    elif app_type == "4":  # E-commerce
        specific_rec = """
        RECOMENDACIONES ESPECÍFICAS PARA E-COMMERCE:
        
        ✓ Protege especialmente los endpoints de checkout y pago
        ✓ Implementa protección anti-bot para formularios de registro y checkout
        ✓ Utiliza servicios de procesamiento de pagos externos y seguros
        ✓ Implementa caché para catálogos y páginas de productos
        ✓ Considera servicios especializados de protección para e-commerce
        ✓ Implementa monitoreo de fraude y comportamientos sospechosos
        ✓ Utiliza CDN para imágenes de productos y recursos estáticos
        """
    else:  # Otro/No especificar
        specific_rec = """
        RECOMENDACIONES GENERALES ADICIONALES:
        
        ✓ Realiza pruebas de penetración periódicas
        ✓ Implementa una arquitectura de microservicios para mejor aislamiento
        ✓ Considera utilizar contenedores y orquestación (Docker, Kubernetes)
        ✓ Implementa redundancia geográfica si es posible
        ✓ Desarrolla un plan de continuidad de negocio y recuperación ante desastres
        """
    
    print(Fore.YELLOW + "\n" + specific_rec + Style.RESET_ALL)
    
    input(Fore.CYAN + "\nPresiona Enter para volver al menú..." + Style.RESET_ALL)
    clear_screen()
    show_menu()

if __name__ == "__main__":
    show_menu()