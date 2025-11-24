# Test básico de funciones de SCARLET

import sys
from scarlet_v2 import validate_url, is_same_domain, Colors

def test_validate_url():
    """Prueba la función de validación de URLs"""
    print(f"{Colors.CYAN}Testing validate_url...{Colors.RESET}")
    
    # URLs válidas
    assert validate_url("https://www.google.com") == True
    assert validate_url("http://localhost:3000") == True
    assert validate_url("https://ejemplo.com/path") == True
    
    # URLs inválidas
    assert validate_url("www.google.com") == False
    assert validate_url("ftp://archivo.com") == False
    assert validate_url("") == False
    assert validate_url("not-a-url") == False
    
    print(f"{Colors.GREEN}✓ validate_url: PASS{Colors.RESET}")

def test_is_same_domain():
    """Prueba la función de comparación de dominios"""
    print(f"{Colors.CYAN}Testing is_same_domain...{Colors.RESET}")
    
    # Mismo dominio
    assert is_same_domain("https://ejemplo.com", "https://ejemplo.com/about") == True
    assert is_same_domain("https://ejemplo.com", "https://www.ejemplo.com") == True
    
    # Diferente dominio
    assert is_same_domain("https://ejemplo.com", "https://otro.com") == False
    
    # Localhost
    assert is_same_domain("http://localhost:3000", "http://localhost:3000/path") == True
    
    print(f"{Colors.GREEN}✓ is_same_domain: PASS{Colors.RESET}")

if __name__ == "__main__":
    try:
        print(f"\n{Colors.MAGENTA}{'='*50}{Colors.RESET}")
        print(f"{Colors.MAGENTA}SCARLET - Test Suite{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*50}{Colors.RESET}\n")
        
        test_validate_url()
        test_is_same_domain()
        
        print(f"\n{Colors.GREEN}{'='*50}{Colors.RESET}")
        print(f"{Colors.GREEN}Todos los tests pasaron correctamente ✓{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*50}{Colors.RESET}\n")
        
        sys.exit(0)
    except AssertionError as e:
        print(f"\n{Colors.RED}✗ Test falló: {e}{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}✗ Error inesperado: {e}{Colors.RESET}\n")
        sys.exit(1)
