import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time
import json
import argparse
from datetime import datetime
import ssl

# Constantes de colores
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"

def banner():
    print("\033[1;31m")
    print("""
    	███████╗ ██████╗ █████╗ ██████╗ ██╗     ███████╗████████╗
    	██╔════╝██╔════╝██╔══██╗██╔══██╗██║     ██╔════╝╚══██╔══╝
    	███████╗██║     ███████║██████╔╝██║     █████╗     ██║   
    	╚════██║██║     ██╔══██║██╔══██╗██║     ██╔══╝     ██║   
    	███████║╚██████╗██║  ██║██║  ██║███████╗███████╗   ██║   
    	╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   
                                                         	
                	\033[0;32mPower by 3SC0B0T\033[0m

""")
    print("\033[0;37m")



def validate_url(url):
    """Valida que la URL tenga un formato correcto."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False

async def fetch(url, session, timeout=10):
    """
    Realiza una petición HTTP asíncrona a la URL especificada.
    
    Args:
        url: URL a consultar
        session: Sesión de aiohttp
        timeout: Tiempo máximo de espera en segundos
        
    Returns:
        Contenido HTML de la página o None en caso de error
    """
    try:
        async with session.get(url, timeout=ClientTimeout(total=timeout)) as response:
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type:
                return await response.text()
            else:
                await response.read()  # Consume response to avoid hanging
                return ''
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            print(f"{Colors.RED}Error 404: No encontrada - URL: {url}{Colors.RESET}")
        else:
            print(f"{Colors.RED}HTTP Error: {e.status} - URL: {url}{Colors.RESET}")
        return None
    except asyncio.TimeoutError:
        print(f"{Colors.RED}Timeout: {url}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"{Colors.RED}Error fetching URL: {url} - {e}{Colors.RESET}")
        return None

def is_same_domain(base_url, target_url):
    """
    Verifica si dos URLs pertenecen al mismo dominio base.
    
    Args:
        base_url: URL base de referencia
        target_url: URL a comparar
        
    Returns:
        True si ambas URLs pertenecen al mismo dominio, False en caso contrario
    """
    try:
        parsed_base_url = urlparse(base_url)
        parsed_target_url = urlparse(target_url)
        
        # Manejo especial para localhost y dominios simples
        base_parts = parsed_base_url.netloc.split('.')
        target_parts = parsed_target_url.netloc.split('.')
        
        if len(base_parts) < 2 or len(target_parts) < 2:
            return parsed_base_url.netloc == parsed_target_url.netloc
        
        base_domain = '.'.join(base_parts[-2:])
        target_domain = '.'.join(target_parts[-2:])
        return base_domain == target_domain
    except Exception:
        return False

def print_url(url, is_valid, is_subdomain):
    """
    Imprime una URL con formato de color según su estado.
    
    Args:
        url: URL a imprimir
        is_valid: Si la URL fue accesible correctamente
        is_subdomain: Si la URL pertenece a un subdominio diferente
    """
    if is_subdomain:
        color = Colors.BLUE
    else:
        color = Colors.YELLOW

    print(f"{color}{url}{Colors.RESET}")

async def extract_urls(base_url, url, urls_found, session, queue, semaphore, stats):
    """
    Extrae URLs de una página HTML y las añade a la cola de procesamiento.
    
    Args:
        base_url: URL base del dominio
        url: URL actual a procesar
        urls_found: Conjunto de URLs ya encontradas
        session: Sesión de aiohttp
        queue: Cola de URLs pendientes
        semaphore: Semáforo para controlar concurrencia
        stats: Diccionario con estadísticas
    """
    async with semaphore:
        html = await fetch(url, session)
        if html is not None and html != '':
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href.strip())
                    # Eliminar fragmentos (#)
                    full_url = full_url.split('#')[0]
                    
                    if is_same_domain(base_url, full_url) and full_url not in urls_found:
                        urls_found.add(full_url)
                        is_subdomain = urlparse(full_url).netloc != urlparse(base_url).netloc
                        print_url(full_url, is_valid=True, is_subdomain=is_subdomain)
                        queue.append(full_url)
                        stats['found'] += 1
            stats['processed'] += 1
        else:
            is_subdomain = urlparse(url).netloc != urlparse(base_url).netloc
            print_url(url, is_valid=False, is_subdomain=is_subdomain)
            stats['errors'] += 1

async def worker(base_url, urls_found, session, queue, semaphore, stats, max_urls=None):
    """
    Worker que procesa URLs de la cola de forma asíncrona.
    
    Args:
        base_url: URL base del dominio
        urls_found: Conjunto de URLs ya encontradas
        session: Sesión de aiohttp
        queue: Cola de URLs pendientes
        semaphore: Semáforo para controlar concurrencia
        stats: Diccionario con estadísticas
        max_urls: Límite máximo de URLs a procesar (None = sin límite)
    """
    while queue:
        if max_urls and stats['processed'] >= max_urls:
            break
        try:
            url = queue.popleft()
            await extract_urls(base_url, url, urls_found, session, queue, semaphore, stats)
        except IndexError:
            # La cola está vacía
            break
        await asyncio.sleep(0)  # Permitir que otros workers se ejecuten

def save_results(urls, filename='scarlet_results.json'):
    """
    Guarda los resultados en un archivo JSON.
    
    Args:
        urls: Conjunto de URLs encontradas
        filename: Nombre del archivo de salida
    """
    data = {
        'timestamp': datetime.now().isoformat(),
        'total_urls': len(urls),
        'urls': sorted(urls)
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n{Colors.GREEN} Resultados guardados en: {filename}{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error al guardar resultados [!]: {e}{Colors.RESET}")

def print_statistics(stats, start_time):
    """
    Imprime las estadísticas finales del crawling.
    
    Args:
        stats: Diccionario con estadísticas
        start_time: Tiempo de inicio del proceso
    """
    elapsed_time = time.time() - start_time
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}ESTADÍSTICAS FINALES{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}URLs encontradas:{Colors.RESET} {stats['found']}")
    print(f"{Colors.YELLOW}URLs procesadas:{Colors.RESET} {stats['processed']}")
    print(f"{Colors.RED}Errores:{Colors.RESET} {stats['errors']}")
    print(f"{Colors.MAGENTA}Tiempo total:{Colors.RESET} {elapsed_time:.2f} segundos")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def get_user_input():
    """
    Solicita y valida la URL base al usuario.
    
    Returns:
        URL validada ingresada por el usuario
    """
    while True:
        base_url = input(f'{Colors.GREEN}Ingrese la URL: {Colors.RESET}')
        
        if not base_url:
            print(f"{Colors.RED}[!] Error: Debe ingresar una URL{Colors.RESET}\n")
            continue
            
        if not validate_url(base_url):
            print(f"{Colors.RED}[!] Error: URL inválida. Debe incluir http:// o https://{Colors.RESET}\n")
            continue
            
        return base_url

async def main(url=None, max_urls=None, num_workers=10, output_file=None, ignore_ssl=False):
    """
    Función principal que coordina el proceso de crawling.
    
    Args:
        url: URL base a crawlear (None = solicitar al usuario)
        max_urls: Límite máximo de URLs a procesar (None = sin límite)
        num_workers: Número de workers concurrentes
        output_file: Archivo donde guardar los resultados (None = no guardar)
        ignore_ssl: Si True, ignora errores de certificado SSL
    """
    # Obtener URL desde parámetro o solicitar al usuario
    if url:
        if not validate_url(url):
            print(f"{Colors.RED}[!] Error: URL inválida. Debe incluir http:// o https://{Colors.RESET}")
            return
        base_url = url
    else:
        base_url = get_user_input()
    
    print(f"\n{Colors.CYAN}[*] Iniciando crawling de: {base_url}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Workers concurrentes: {num_workers}{Colors.RESET}")
    if max_urls:
        print(f"{Colors.CYAN}[*] Límite de URLs: {max_urls}{Colors.RESET}")
    if ignore_ssl:
        print(f"{Colors.YELLOW}[!] ADVERTENCIA: Verificación SSL desactivada{Colors.RESET}")
    print()
    
    urls_found = set()
    queue = deque([base_url])
    semaphore = asyncio.Semaphore(num_workers)
    stats = {'found': 1, 'processed': 0, 'errors': 0}
    urls_found.add(base_url)
    
    start_time = time.time()
    
    # Configurar SSL
    ssl_context = None
    if ignore_ssl:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context if ignore_ssl else True)
    
    async with ClientSession(connector=connector) as session:
        workers = [
            worker(base_url, urls_found, session, queue, semaphore, stats, max_urls) 
            for _ in range(num_workers)
        ]
        await asyncio.gather(*workers)
    
    print_statistics(stats, start_time)
    
    if output_file:
        save_results(urls_found, output_file)


if __name__ == "__main__":
    banner()
    
    parser = argparse.ArgumentParser(
        description='SCARLET - Web Crawler para descubrimiento de URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-u', '--url',
        type=str,
        default=None,
        help='URL base a crawlear (por defecto: solicitar interactivamente)'
    )
    
    parser.add_argument(
        '-m', '--max-urls',
        type=int,
        default=None,
        help='Límite máximo de URLs a procesar (por defecto: sin límite)'
    )
    
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=10,
        help='Número de workers concurrentes (por defecto: 10)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Archivo de salida para guardar resultados en JSON (por defecto: no guardar)'
    )
    
    parser.add_argument(
        '-k', '--insecure',
        action='store_true',
        help='Ignorar errores de certificado SSL (no recomendado, solo para testing)'
    )
    
    args = parser.parse_args()
    
    asyncio.run(main(url=args.url, max_urls=args.max_urls, num_workers=args.workers, output_file=args.output, ignore_ssl=args.insecure))

