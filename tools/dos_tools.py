import socket
import threading
import time
import sys
import os
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init()

def check_port_open(host="127.0.0.1", port=80, timeout=2):
    """
    Verifica si un puerto específico está abierto en el host.
    Útil para confirmar que la aplicación web está funcionando antes de las pruebas.
    
    Args:
        host: La dirección IP o URL a verificar (por defecto: 127.0.0.1)
        port: El puerto a verificar
        timeout: Tiempo de espera en segundos
        
    Returns:
        bool: True si el puerto está abierto, False en caso contrario
    """
    try:
        # Limpiar la URL si contiene protocolo o rutas
        original_host = host
        if host.startswith("http://"):
            host = host.replace("http://", "")
            if port == 80 or port == 443:  # Si el puerto es el predeterminado, usar 80 para HTTP
                port = 80
        elif host.startswith("https://"):
            host = host.replace("https://", "")
            if port == 80 or port == 443:  # Si el puerto es el predeterminado, usar 443 para HTTPS
                port = 443
            
        # Eliminar rutas y parámetros después del dominio
        if "/" in host:
            host = host.split("/")[0]
            
        # Mostrar información sobre el objetivo si se modificó
        if original_host != host:
            print(Fore.CYAN + f"\n[*] URL original: {original_host}" + Style.RESET_ALL)
            print(Fore.CYAN + f"[*] Host para conexión: {host}" + Style.RESET_ALL)
            print(Fore.CYAN + f"[*] Puerto para conexión: {port}" + Style.RESET_ALL)
            
        # Verificar si es una prueba en producción (no localhost)
        is_production = host not in ["127.0.0.1", "localhost", "::1"]
        
        if is_production:
            print(Fore.RED + "\n[!] ADVERTENCIA: Estás realizando una prueba en un entorno de producción" + Style.RESET_ALL)
            print(Fore.RED + "[!] Asegúrate de tener AUTORIZACIÓN EXPLÍCITA para realizar estas pruebas" + Style.RESET_ALL)
            print(Fore.RED + "[!] El uso no autorizado puede ser ILEGAL y resultar en consecuencias legales" + Style.RESET_ALL)
            
            confirm = input(Fore.YELLOW + "\n¿Tienes autorización para realizar esta prueba? (s/n): " + Style.RESET_ALL).lower()
            if confirm != 's':
                print(Fore.YELLOW + "\n[*] Prueba cancelada por el usuario" + Style.RESET_ALL)
                return False
            
            print(Fore.YELLOW + "\n[*] Procediendo con la prueba en entorno de producción..." + Style.RESET_ALL)
            print(Fore.YELLOW + "[*] Se recomienda usar una intensidad baja para evitar daños" + Style.RESET_ALL)
            
        print(Fore.CYAN + f"\n[*] Intentando conectar a {host} en el puerto {port}..." + Style.RESET_ALL)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(Fore.GREEN + f"\n[✓] El puerto {port} está abierto en {host}" + Style.RESET_ALL)
                return True
            else:
                print(Fore.RED + f"\n[!] El puerto {port} está cerrado en {host}" + Style.RESET_ALL)
                print(Fore.YELLOW + "[!] Asegúrate de que el objetivo esté en línea y el puerto especificado esté abierto" + Style.RESET_ALL)
                return False
        except socket.gaierror:
            print(Fore.RED + f"\n[!] No se pudo resolver el nombre de host: {host}" + Style.RESET_ALL)
            print(Fore.YELLOW + "[!] Verifica que la URL o dirección IP sea correcta" + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.RED + f"\n[!] Error al verificar el puerto: {str(e)}" + Style.RESET_ALL)
        return False

def dos_test(target="127.0.0.1", port=80, duration=5, intensity="baja"):
    """
    Realiza una prueba de DoS enviando paquetes al objetivo especificado.
    Esta función es SOLO para fines educativos y pruebas autorizadas.
    Simula un ataque más realista con diferentes tipos de solicitudes.
    
    Args:
        target: La dirección IP o URL objetivo (por defecto: 127.0.0.1)
        port: El puerto objetivo (por defecto: 80)
        duration: Duración de la prueba en segundos (por defecto: 5)
        intensity: Intensidad de la prueba ("baja", "media", "alta") (por defecto: "baja")
    """
    # Limpiar la URL si contiene protocolo o rutas
    original_target = target
    if target.startswith("http://"):
        target = target.replace("http://", "")
        if port == 80 or port == 443:  # Si el puerto es el predeterminado, usar 80 para HTTP
            port = 80
    elif target.startswith("https://"):
        target = target.replace("https://", "")
        if port == 80 or port == 443:  # Si el puerto es el predeterminado, usar 443 para HTTPS
            port = 443
        
    # Eliminar rutas y parámetros después del dominio
    if "/" in target:
        target = target.split("/")[0]
    
    # Verificar si es una prueba en producción (no localhost)
    is_production = target not in ["127.0.0.1", "localhost", "::1"]
    
    # Mostrar información sobre el objetivo
    if original_target != target:
        print(Fore.CYAN + f"\n[*] URL original: {original_target}" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Host para conexión: {target}" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Puerto para conexión: {port}" + Style.RESET_ALL)
    
    if is_production:
        print(Fore.RED + "\n[!] ADVERTENCIA: Estás realizando una prueba en un entorno de producción" + Style.RESET_ALL)
        print(Fore.RED + "[!] Asegúrate de tener AUTORIZACIÓN EXPLÍCITA para realizar estas pruebas" + Style.RESET_ALL)
        print(Fore.RED + "[!] El uso no autorizado puede ser ILEGAL y resultar en consecuencias legales" + Style.RESET_ALL)
        
        confirm = input(Fore.YELLOW + "\n¿Tienes autorización para realizar esta prueba? (s/n): " + Style.RESET_ALL).lower()
        if confirm != 's':
            print(Fore.YELLOW + "\n[*] Prueba cancelada por el usuario" + Style.RESET_ALL)
            return False
    
    # Configurar la intensidad de la prueba
    pause_time = 0.1  # Pausa predeterminada (baja intensidad)
    if intensity == "media":
        pause_time = 0.05
    elif intensity == "alta":
        pause_time = 0.01
    
    is_production = target not in ["127.0.0.1", "localhost", "::1"]
    target_type = "producción" if is_production else "local"
    
    print(Fore.CYAN + f"\n[*] Iniciando prueba de DoS en entorno de {target_type}: {target}:{port}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"[*] Duración: {duration} segundos, Intensidad: {intensity}" + Style.RESET_ALL)
    
    # Contador de paquetes y estadísticas
    packet_count = 0
    success_count = 0
    failed_count = 0
    start_time = time.time()
    
    # Tipos de solicitudes para simular un ataque más realista
    host_header = target
    http_requests = [
        f"GET / HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode(),
        f"POST / HTTP/1.1\r\nHost: {host_header}\r\nContent-Length: 1000\r\n\r\n".encode() + b"A" * 1000,
        f"GET /search?q=".encode() + b"A" * 500 + f" HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode(),
        f"GET / HTTP/1.1\r\nHost: {host_header}\r\nConnection: keep-alive\r\n".encode() + b"X-Header: " + b"A" * 200 + b"\r\n" * 10,
    ]
    
    print(Fore.CYAN + "\n[*] Iniciando prueba con diferentes patrones de ataque" + Style.RESET_ALL)
    
    try:
        # Crear socket y enviar diferentes tipos de solicitudes
        while time.time() - start_time < duration:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)  # Timeout de 1 segundo
                s.connect((target, port))
                
                # Seleccionar un tipo de solicitud aleatoria
                request = http_requests[packet_count % len(http_requests)]
                s.send(request)
                
                packet_count += 1
                success_count += 1
                print(Fore.GREEN + f"[+] Paquete {packet_count} enviado (Patrón: {packet_count % len(http_requests) + 1})" + Style.RESET_ALL, end="\r")
                s.close()
                time.sleep(pause_time)  # Pausa basada en la intensidad seleccionada
            except socket.error as e:
                failed_count += 1
                print(Fore.RED + f"[!] Error: {str(e)}" + Style.RESET_ALL)
                time.sleep(0.5)
                continue
        
        # Mostrar estadísticas detalladas
        elapsed_time = time.time() - start_time
        print(Fore.GREEN + f"\n[✓] Prueba completada: {packet_count} paquetes enviados en {elapsed_time:.2f} segundos" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Estadísticas:" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes exitosos: {success_count}" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes fallidos: {failed_count}" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Tasa de éxito: {(success_count/packet_count*100) if packet_count > 0 else 0:.2f}%" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes por segundo: {packet_count/elapsed_time if elapsed_time > 0 else 0:.2f}" + Style.RESET_ALL)
        
        # Evaluación de resistencia
        if success_count > 0 and failed_count == 0:
            print(Fore.GREEN + "[✓] Tu aplicación parece estar manejando bien la carga de DoS básica" + Style.RESET_ALL)
        elif failed_count > 0 and success_count > 0:
            print(Fore.YELLOW + "[!] Tu aplicación muestra signos de estrés bajo la carga de DoS" + Style.RESET_ALL)
        elif failed_count > 0 and success_count == 0:
            print(Fore.RED + "[!] Tu aplicación parece vulnerable a ataques DoS" + Style.RESET_ALL)
        
        return True
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Prueba interrumpida por el usuario" + Style.RESET_ALL)
        return False

def ddos_simulation(target="127.0.0.1", port=80, threads=3, duration=5, intensity="baja"):
    """
    Simula un ataque DDoS usando múltiples hilos y diferentes patrones de ataque.
    Esta función es SOLO para fines educativos y pruebas autorizadas.
    Simula un ataque más realista con diferentes tipos de solicitudes y múltiples hilos.
    
    Args:
        target: La dirección IP o URL objetivo (por defecto: 127.0.0.1)
        port: El puerto objetivo (por defecto: 80)
        threads: Número de hilos a utilizar (por defecto: 3)
        duration: Duración de la prueba en segundos (por defecto: 5)
        intensity: Intensidad de la prueba ("baja", "media", "alta") (por defecto: "baja")
    """
    # Limpiar la URL si contiene protocolo o rutas
    original_target = target
    if target.startswith("http://"):
        target = target.replace("http://", "")
        if port == 80 or port == 443:  # Si el puerto es el predeterminado, usar 80 para HTTP
            port = 80
    elif target.startswith("https://"):
        target = target.replace("https://", "")
        if port == 80 or port == 443:  # Si el puerto es el predeterminado, usar 443 para HTTPS
            port = 443
        
    # Eliminar rutas y parámetros después del dominio
    if "/" in target:
        target = target.split("/")[0]
    
    # Verificar si es una prueba en producción (no localhost)
    is_production = target not in ["127.0.0.1", "localhost", "::1"]
    
    # Mostrar información sobre el objetivo
    if original_target != target:
        print(Fore.CYAN + f"\n[*] URL original: {original_target}" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Host para conexión: {target}" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Puerto para conexión: {port}" + Style.RESET_ALL)
    
    if is_production:
        print(Fore.RED + "\n[!] ADVERTENCIA: Estás realizando una prueba en un entorno de producción" + Style.RESET_ALL)
        print(Fore.RED + "[!] Asegúrate de tener AUTORIZACIÓN EXPLÍCITA para realizar estas pruebas" + Style.RESET_ALL)
        print(Fore.RED + "[!] El uso no autorizado puede ser ILEGAL y resultar en consecuencias legales" + Style.RESET_ALL)
        
        confirm = input(Fore.YELLOW + "\n¿Tienes autorización para realizar esta prueba? (s/n): " + Style.RESET_ALL).lower()
        if confirm != 's':
            print(Fore.YELLOW + "\n[*] Prueba cancelada por el usuario" + Style.RESET_ALL)
            return False
    
    # Configurar la intensidad de la prueba
    pause_time = 0.1  # Pausa predeterminada (baja intensidad)
    if intensity == "media":
        pause_time = 0.05
    elif intensity == "alta":
        pause_time = 0.01
    
    target_type = "producción" if is_production else "local"
    
    print(Fore.CYAN + f"\n[*] Iniciando simulación de DDoS en entorno de {target_type}: {target}:{port}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"[*] Hilos: {threads}, Duración: {duration} segundos, Intensidad: {intensity}" + Style.RESET_ALL)
    
    # Contadores globales para estadísticas
    stats = {
        "packets": 0,
        "success": 0,
        "failed": 0,
        "thread_stats": {}
    }
    
    # Evento para detener los hilos
    stop_event = threading.Event()
    
    # Tipos de solicitudes para simular un ataque más realista
    host_header = target
    http_requests = [
        f"GET / HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode(),
        f"POST / HTTP/1.1\r\nHost: {host_header}\r\nContent-Length: 1000\r\n\r\n".encode() + b"A" * 1000,
        f"GET /search?q=".encode() + b"A" * 500 + f" HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode(),
        f"GET / HTTP/1.1\r\nHost: {host_header}\r\nConnection: keep-alive\r\n".encode() + b"X-Header: " + b"A" * 200 + b"\r\n" * 10,
        f"GET /admin HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode(),
        f"GET /login HTTP/1.1\r\nHost: {host_header}\r\n\r\n".encode(),
        f"POST /login HTTP/1.1\r\nHost: {host_header}\r\nContent-Length: 50\r\n\r\nusername=admin&password=".encode() + b"A" * 30,
    ]
    
    # Mutex para acceso seguro a las estadísticas
    stats_lock = threading.Lock()
    
    def attack_thread(thread_id):
        # Inicializar estadísticas del hilo
        with stats_lock:
            stats["thread_stats"][thread_id] = {
                "packets": 0,
                "success": 0,
                "failed": 0
            }
        
        try:
            while not stop_event.is_set():
                try:
                    # Crear socket y conectar
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)  # Timeout de 1 segundo
                    s.connect((target, port))
                    
                    # Seleccionar un tipo de solicitud aleatoria
                    request_idx = (thread_id + stats["thread_stats"][thread_id]["packets"]) % len(http_requests)
                    request = http_requests[request_idx]
                    s.send(request)
                    
                    # Actualizar estadísticas
                    with stats_lock:
                        stats["packets"] += 1
                        stats["success"] += 1
                        stats["thread_stats"][thread_id]["packets"] += 1
                        stats["thread_stats"][thread_id]["success"] += 1
                        total = stats["packets"]
                    
                    print(Fore.GREEN + f"[+] Hilo {thread_id}: Paquete enviado (Patrón: {request_idx+1}, Total: {total})" + Style.RESET_ALL, end="\r")
                    s.close()
                    time.sleep(pause_time)  # Pausa basada en la intensidad seleccionada
                except socket.error as e:
                    with stats_lock:
                        stats["failed"] += 1
                        stats["thread_stats"][thread_id]["failed"] += 1
                    print(Fore.RED + f"[!] Hilo {thread_id}: Error: {str(e)}" + Style.RESET_ALL)
                    time.sleep(0.5)
                    continue
        except Exception as e:
            print(Fore.RED + f"[!] Error en hilo {thread_id}: {str(e)}" + Style.RESET_ALL)
    
    # Crear y iniciar hilos
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=attack_thread, args=(i+1,))
        t.daemon = True  # Hilo daemon para que termine cuando el programa principal termine
        thread_list.append(t)
        t.start()
        print(Fore.CYAN + f"[*] Hilo {i+1} iniciado" + Style.RESET_ALL)
    
    # Esperar la duración especificada
    try:
        start_time = time.time()
        time.sleep(duration)
        stop_event.set()  # Señal para detener los hilos
        
        # Esperar a que todos los hilos terminen
        for t in thread_list:
            t.join(1)  # Esperar máximo 1 segundo por hilo
        
        # Calcular estadísticas finales
        elapsed_time = time.time() - start_time
        total_packets = stats["packets"]
        success_packets = stats["success"]
        failed_packets = stats["failed"]
        
        # Mostrar estadísticas detalladas
        print(Fore.GREEN + f"\n[✓] Simulación DDoS completada" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Estadísticas generales:" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes totales: {total_packets}" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes exitosos: {success_packets}" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes fallidos: {failed_packets}" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Tasa de éxito: {(success_packets/total_packets*100) if total_packets > 0 else 0:.2f}%" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Paquetes por segundo: {total_packets/elapsed_time if elapsed_time > 0 else 0:.2f}" + Style.RESET_ALL)
        print(Fore.CYAN + f"    - Duración real: {elapsed_time:.2f} segundos" + Style.RESET_ALL)
        
        # Estadísticas por hilo
        print(Fore.CYAN + f"\n[*] Estadísticas por hilo:" + Style.RESET_ALL)
        for thread_id, thread_stat in stats["thread_stats"].items():
            print(Fore.CYAN + f"    - Hilo {thread_id}: {thread_stat['packets']} paquetes, {thread_stat['success']} exitosos, {thread_stat['failed']} fallidos" + Style.RESET_ALL)
        
        # Evaluación de resistencia
        if success_packets > 0 and failed_packets == 0:
            print(Fore.GREEN + "\n[✓] Tu aplicación parece estar manejando bien la carga de DDoS simulada" + Style.RESET_ALL)
            print(Fore.YELLOW + "[!] Considera aumentar el número de hilos o la duración para pruebas más intensivas" + Style.RESET_ALL)
        elif failed_packets > 0 and success_packets > failed_packets:
            print(Fore.YELLOW + "\n[!] Tu aplicación muestra algunos signos de estrés bajo la carga de DDoS" + Style.RESET_ALL)
            print(Fore.YELLOW + "[!] Considera implementar medidas de mitigación como limitación de tasa o balanceo de carga" + Style.RESET_ALL)
        elif failed_packets >= success_packets:
            print(Fore.RED + "\n[!] Tu aplicación parece vulnerable a ataques DDoS" + Style.RESET_ALL)
            print(Fore.RED + "[!] Se recomienda implementar protecciones como WAF, limitación de tasa y detección de anomalías" + Style.RESET_ALL)
        
        return True
    
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[*] Simulación interrumpida por el usuario" + Style.RESET_ALL)
        stop_event.set()  # Señal para detener los hilos
        return False

# Función para mostrar información educativa
def show_educational_info():
    """
    Muestra información educativa sobre ataques DoS y DDoS y cómo proteger aplicaciones web.
    """
    info = """
    === INFORMACIÓN EDUCATIVA SOBRE ATAQUES DOS Y DDOS ===
    
    DoS (Denegación de Servicio):
    - Un ataque DoS intenta hacer que un servicio, red o sitio web sea inaccesible
      para usuarios legítimos al saturar el objetivo con tráfico o solicitudes.
    - Generalmente proviene de una única fuente o dispositivo.
    - Limitado por el ancho de banda y recursos del atacante.
    
    DDoS (Denegación de Servicio Distribuida):
    - Similar al DoS pero el ataque proviene de múltiples fuentes coordinadas.
    - Utiliza múltiples sistemas infectados (botnets) para generar tráfico malicioso.
    - Más difícil de mitigar debido a su naturaleza distribuida.
    - Puede generar volúmenes de tráfico extremadamente altos (Tbps).
    - Mucho más potente que un ataque DoS simple.
    
    Tipos comunes de ataques:
    1. Inundación SYN: Envía muchas solicitudes SYN sin completar el handshake TCP.
    2. Inundación HTTP: Sobrecarga servidores web con muchas solicitudes HTTP.
    3. Amplificación DNS: Utiliza servidores DNS para amplificar el tráfico.
    4. Inundación UDP: Envía gran cantidad de paquetes UDP a puertos aleatorios.
    5. Ataques de capa de aplicación: Apuntan a vulnerabilidades específicas en aplicaciones web.
    6. Ataques de agotamiento de recursos: Consumen CPU, memoria o conexiones disponibles.
    
    === PROTECCIÓN DE APLICACIONES WEB ===
    
    Nivel de Infraestructura:
    - Servicios de protección DDoS (Cloudflare, AWS Shield, Akamai)
    - Balanceadores de carga y escalado automático
    - Firewalls de aplicaciones web (WAF)
    - Proveedores de CDN (Red de Distribución de Contenido)
    
    Nivel de Aplicación:
    - Implementar limitación de tasa (rate limiting)
    - Usar CAPTCHA para solicitudes sospechosas
    - Implementar tiempos de espera adecuados
    - Caché de contenido estático
    - Optimizar consultas de base de datos
    - Monitoreo y alertas en tiempo real
    
    Buenas Prácticas:
    1. Diseñar para escalar horizontalmente
    2. Implementar colas de tareas para procesos intensivos
    3. Establecer umbrales y alertas de tráfico anormal
    4. Tener un plan de respuesta a incidentes
    5. Realizar pruebas regulares de carga y estrés
    6. Mantener el software actualizado
    7. Separar recursos críticos y no críticos
    
    Evaluación de Resistencia:
    - Las pruebas locales son útiles pero limitadas
    - Considerar servicios profesionales de pruebas de penetración
    - Monitorear el rendimiento bajo diferentes niveles de carga
    - Identificar y corregir cuellos de botella
    
    IMPORTANTE: Realizar estos ataques sin autorización es ILEGAL y puede resultar en:
    - Sanciones penales severas
    - Multas económicas significativas
    - Responsabilidad civil por daños causados
    
    Este software es ÚNICAMENTE para fines educativos y pruebas en entornos controlados
    con la debida autorización.
    """
    
    print(Fore.WHITE + info + Style.RESET_ALL)
    return True

def generate_resistance_report():
    """
    Genera un informe detallado sobre la resistencia de la aplicación web
    basado en los resultados de las pruebas realizadas.
    """
    # Importar la función clear_screen
    try:
        from tools.menu import clear_screen
        clear_screen()
    except ImportError:
        # Si no se puede importar, limpiar la pantalla de otra manera
        os.system('cls' if os.name == 'nt' else 'clear')
        
    print(Fore.CYAN + "\n[*] GENERANDO INFORME DE RESISTENCIA" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[!] Este informe se basa en las pruebas realizadas en tu aplicación web" + Style.RESET_ALL)
    
    # Solicitar información sobre las pruebas realizadas
    print(Fore.CYAN + "\nPor favor, proporciona la siguiente información sobre tus pruebas:" + Style.RESET_ALL)
    
    # Tipo de aplicación web
    print(Fore.CYAN + "\n¿Qué tipo de aplicación web estás probando?" + Style.RESET_ALL)
    print("1. Aplicación estática (HTML, CSS, JS)")
    print("2. Aplicación dinámica (PHP, Python, Node.js, etc.)")
    print("3. API REST/GraphQL")
    print("4. Aplicación de comercio electrónico")
    print("5. Otro")
    
    app_type = 0
    while app_type not in [1, 2, 3, 4, 5]:
        try:
            app_type = int(input(Fore.CYAN + "Selecciona una opción [1-5]: " + Style.RESET_ALL))
            if app_type not in [1, 2, 3, 4, 5]:
                print(Fore.RED + "[!] Opción inválida. Por favor, selecciona una opción entre 1 y 5." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[!] Entrada inválida. Por favor, ingresa un número." + Style.RESET_ALL)
    
    # Resultados de las pruebas DoS
    print(Fore.CYAN + "\n¿Has realizado pruebas de DoS?" + Style.RESET_ALL)
    print("1. Sí")
    print("2. No")
    
    dos_test = 0
    while dos_test not in [1, 2]:
        try:
            dos_test = int(input(Fore.CYAN + "Selecciona una opción [1-2]: " + Style.RESET_ALL))
            if dos_test not in [1, 2]:
                print(Fore.RED + "[!] Opción inválida. Por favor, selecciona 1 o 2." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[!] Entrada inválida. Por favor, ingresa un número." + Style.RESET_ALL)
    
    dos_success_rate = 0
    if dos_test == 1:
        while True:
            try:
                dos_success_rate = float(input(Fore.CYAN + "¿Cuál fue la tasa de éxito de las solicitudes (%)? [0-100]: " + Style.RESET_ALL))
                if 0 <= dos_success_rate <= 100:
                    break
                else:
                    print(Fore.RED + "[!] El valor debe estar entre 0 y 100." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "[!] Entrada inválida. Por favor, ingresa un número." + Style.RESET_ALL)
    
    # Resultados de las pruebas DDoS
    print(Fore.CYAN + "\n¿Has realizado pruebas de DDoS?" + Style.RESET_ALL)
    print("1. Sí")
    print("2. No")
    
    ddos_test = 0
    while ddos_test not in [1, 2]:
        try:
            ddos_test = int(input(Fore.CYAN + "Selecciona una opción [1-2]: " + Style.RESET_ALL))
            if ddos_test not in [1, 2]:
                print(Fore.RED + "[!] Opción inválida. Por favor, selecciona 1 o 2." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[!] Entrada inválida. Por favor, ingresa un número." + Style.RESET_ALL)
    
    ddos_success_rate = 0
    if ddos_test == 1:
        while True:
            try:
                ddos_success_rate = float(input(Fore.CYAN + "¿Cuál fue la tasa de éxito de las solicitudes (%)? [0-100]: " + Style.RESET_ALL))
                if 0 <= ddos_success_rate <= 100:
                    break
                else:
                    print(Fore.RED + "[!] El valor debe estar entre 0 y 100." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "[!] Entrada inválida. Por favor, ingresa un número." + Style.RESET_ALL)
    
    # Medidas de protección implementadas
    print(Fore.CYAN + "\n¿Qué medidas de protección has implementado? (Selecciona todas las que apliquen)" + Style.RESET_ALL)
    print("1. Límites de tasa (rate limiting)")
    print("2. Balanceador de carga")
    print("3. Firewall de aplicación web (WAF)")
    print("4. CDN (Cloudflare, Akamai, etc.)")
    print("5. Caché")
    print("6. CAPTCHA")
    print("7. Ninguna")
    
    protections = []
    while True:
        try:
            protection = input(Fore.CYAN + "Ingresa los números separados por comas (o 'c' para continuar): " + Style.RESET_ALL)
            if protection.lower() == 'c':
                break
            
            selected = [int(p.strip()) for p in protection.split(',')]
            valid = all(1 <= p <= 7 for p in selected)
            
            if valid:
                protections.extend(selected)
                break
            else:
                print(Fore.RED + "[!] Opciones inválidas. Por favor, selecciona opciones entre 1 y 7." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[!] Entrada inválida. Por favor, ingresa números separados por comas." + Style.RESET_ALL)
    
    # Generar informe
    try:
        from tools.menu import clear_screen
        clear_screen()
    except ImportError:
        # Si no se puede importar, limpiar la pantalla de otra manera
        os.system('cls' if os.name == 'nt' else 'clear')
        
    print(Fore.CYAN + "\n[*] INFORME DE RESISTENCIA A ATAQUES DoS/DDoS" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n===== RESUMEN DE LA APLICACIÓN =====" + Style.RESET_ALL)
    
    app_types = {
        1: "Aplicación estática (HTML, CSS, JS)",
        2: "Aplicación dinámica (PHP, Python, Node.js, etc.)",
        3: "API REST/GraphQL",
        4: "Aplicación de comercio electrónico",
        5: "Otro tipo de aplicación"
    }
    
    print(f"Tipo de aplicación: {app_types[app_type]}")
    
    # Evaluación de resistencia DoS
    print(Fore.YELLOW + "\n===== RESISTENCIA A ATAQUES DoS =====" + Style.RESET_ALL)
    
    if dos_test == 1:
        if dos_success_rate >= 90:
            print(Fore.GREEN + "[✓] EXCELENTE: Tu aplicación muestra una alta resistencia a ataques DoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {dos_success_rate}%")
            print("    - La aplicación mantuvo un rendimiento óptimo durante las pruebas.")
        elif dos_success_rate >= 70:
            print(Fore.YELLOW + "[!] BUENA: Tu aplicación muestra una resistencia aceptable a ataques DoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {dos_success_rate}%")
            print("    - La aplicación experimentó cierta degradación pero se mantuvo funcional.")
        elif dos_success_rate >= 40:
            print(Fore.RED + "[!] REGULAR: Tu aplicación muestra una resistencia limitada a ataques DoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {dos_success_rate}%")
            print("    - La aplicación experimentó una degradación significativa durante las pruebas.")
        else:
            print(Fore.RED + "[!] DEFICIENTE: Tu aplicación es vulnerable a ataques DoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {dos_success_rate}%")
            print("    - La aplicación experimentó interrupciones severas durante las pruebas.")
    else:
        print(Fore.YELLOW + "[!] No se han realizado pruebas de DoS." + Style.RESET_ALL)
        print("    - Se recomienda realizar pruebas para evaluar la resistencia.")
    
    # Evaluación de resistencia DDoS
    print(Fore.YELLOW + "\n===== RESISTENCIA A ATAQUES DDoS =====" + Style.RESET_ALL)
    
    if ddos_test == 1:
        if ddos_success_rate >= 90:
            print(Fore.GREEN + "[✓] EXCELENTE: Tu aplicación muestra una alta resistencia a ataques DDoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {ddos_success_rate}%")
            print("    - La aplicación mantuvo un rendimiento óptimo durante las pruebas.")
        elif ddos_success_rate >= 70:
            print(Fore.YELLOW + "[!] BUENA: Tu aplicación muestra una resistencia aceptable a ataques DDoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {ddos_success_rate}%")
            print("    - La aplicación experimentó cierta degradación pero se mantuvo funcional.")
        elif ddos_success_rate >= 40:
            print(Fore.RED + "[!] REGULAR: Tu aplicación muestra una resistencia limitada a ataques DDoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {ddos_success_rate}%")
            print("    - La aplicación experimentó una degradación significativa durante las pruebas.")
        else:
            print(Fore.RED + "[!] DEFICIENTE: Tu aplicación es vulnerable a ataques DDoS." + Style.RESET_ALL)
            print(f"    - Tasa de éxito de solicitudes: {ddos_success_rate}%")
            print("    - La aplicación experimentó interrupciones severas durante las pruebas.")
    else:
        print(Fore.YELLOW + "[!] No se han realizado pruebas de DDoS." + Style.RESET_ALL)
        print("    - Se recomienda realizar pruebas para evaluar la resistencia.")
    
    # Evaluación de medidas de protección
    print(Fore.YELLOW + "\n===== MEDIDAS DE PROTECCIÓN IMPLEMENTADAS =====" + Style.RESET_ALL)
    
    protection_names = {
        1: "Límites de tasa (rate limiting)",
        2: "Balanceador de carga",
        3: "Firewall de aplicación web (WAF)",
        4: "CDN (Cloudflare, Akamai, etc.)",
        5: "Caché",
        6: "CAPTCHA",
        7: "Ninguna"
    }
    
    if 7 in protections or not protections:
        print(Fore.RED + "[!] No has implementado medidas de protección." + Style.RESET_ALL)
        print("    - Se recomienda implementar medidas de protección para mejorar la resistencia.")
    else:
        print(Fore.GREEN + "[✓] Medidas de protección implementadas:" + Style.RESET_ALL)
        for p in protections:
            if p != 7:  # Ignorar "Ninguna" si se seleccionaron otras opciones
                print(f"    - {protection_names[p]}")
    
    # Recomendaciones específicas según el tipo de aplicación
    print(Fore.YELLOW + "\n===== RECOMENDACIONES ESPECÍFICAS =====" + Style.RESET_ALL)
    
    if app_type == 1:  # Aplicación estática
        print("Para aplicaciones estáticas (HTML, CSS, JS):")
        print("1. Utiliza una CDN para distribuir el contenido estático")
        print("2. Implementa caché agresiva para reducir la carga del servidor")
        print("3. Considera el uso de hosting estático especializado (GitHub Pages, Netlify, etc.)")
        print("4. Minimiza y optimiza los archivos para reducir el tiempo de carga")
    elif app_type == 2:  # Aplicación dinámica
        print("Para aplicaciones dinámicas (PHP, Python, Node.js, etc.):")
        print("1. Implementa límites de tasa (rate limiting) para prevenir abusos")
        print("2. Utiliza caché para contenido que no cambia frecuentemente")
        print("3. Configura tiempos de espera adecuados para las conexiones")
        print("4. Considera el uso de un proxy inverso (Nginx, HAProxy) para filtrar tráfico malicioso")
        print("5. Implementa un sistema de escalado automático para manejar picos de tráfico")
    elif app_type == 3:  # API REST/GraphQL
        print("Para APIs (REST/GraphQL):")
        print("1. Implementa autenticación y autorización robustas (JWT, OAuth)")
        print("2. Utiliza límites de tasa por usuario/IP")
        print("3. Implementa validación estricta de entradas")
        print("4. Considera el uso de GraphQL para limitar la profundidad de las consultas")
        print("5. Implementa caché para respuestas frecuentes")
    elif app_type == 4:  # E-commerce
        print("Para aplicaciones de comercio electrónico:")
        print("1. Utiliza CAPTCHA para formularios críticos (registro, login, checkout)")
        print("2. Implementa protección contra bots para prevenir scraping y ataques automatizados")
        print("3. Utiliza CDN para contenido estático (imágenes, CSS, JS)")
        print("4. Implementa límites de tasa para APIs y endpoints críticos")
        print("5. Considera servicios especializados de protección DDoS para e-commerce")
    else:  # Otro
        print("Recomendaciones generales:")
        print("1. Implementa límites de tasa (rate limiting)")
        print("2. Utiliza un WAF para filtrar tráfico malicioso")
        print("3. Considera el uso de servicios de mitigación DDoS (Cloudflare, AWS Shield, etc.)")
        print("4. Implementa monitoreo continuo del tráfico")
        print("5. Desarrolla un plan de respuesta a incidentes")
    
    # Conclusión
    print(Fore.YELLOW + "\n===== CONCLUSIÓN =====" + Style.RESET_ALL)
    
    overall_score = 0
    factors = 0
    
    if dos_test == 1:
        overall_score += dos_success_rate
        factors += 1
    
    if ddos_test == 1:
        overall_score += ddos_success_rate
        factors += 1
    
    protection_score = 0
    if protections and 7 not in protections:
        protection_count = len(protections)
        protection_score = min(100, protection_count * 16.67)  # 16.67 = 100/6 (6 protecciones posibles)
        overall_score += protection_score
        factors += 1
    
    if factors > 0:
        final_score = overall_score / factors
        
        if final_score >= 90:
            print(Fore.GREEN + f"[✓] RESISTENCIA GENERAL: EXCELENTE ({final_score:.1f}%)" + Style.RESET_ALL)
            print("    Tu aplicación muestra una excelente resistencia a ataques DoS/DDoS.")
            print("    Continúa monitoreando y mejorando las medidas de protección.")
        elif final_score >= 70:
            print(Fore.YELLOW + f"[!] RESISTENCIA GENERAL: BUENA ({final_score:.1f}%)" + Style.RESET_ALL)
            print("    Tu aplicación muestra una buena resistencia a ataques DoS/DDoS.")
            print("    Considera implementar medidas adicionales para mejorar la resistencia.")
        elif final_score >= 40:
            print(Fore.RED + f"[!] RESISTENCIA GENERAL: REGULAR ({final_score:.1f}%)" + Style.RESET_ALL)
            print("    Tu aplicación muestra una resistencia limitada a ataques DoS/DDoS.")
            print("    Se recomienda implementar medidas adicionales de protección.")
        else:
            print(Fore.RED + f"[!] RESISTENCIA GENERAL: DEFICIENTE ({final_score:.1f}%)" + Style.RESET_ALL)
            print("    Tu aplicación es vulnerable a ataques DoS/DDoS.")
            print("    Se recomienda implementar medidas de protección urgentemente.")
    else:
        print(Fore.YELLOW + "[!] No se puede determinar la resistencia general." + Style.RESET_ALL)
        print("    Se recomienda realizar pruebas de DoS y DDoS para evaluar la resistencia.")
    
    print(Fore.CYAN + "\n[*] Este informe es solo una evaluación básica. Se recomienda realizar pruebas más exhaustivas y consultar con expertos en seguridad para una evaluación completa." + Style.RESET_ALL)
    return True