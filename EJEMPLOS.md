# Ejemplos de Uso - SCARLET

## Ejemplo 1: Uso básico interactivo
```bash
python scarlet_v2.py
```
El programa te pedirá ingresar una URL:
```
Ingrese la URL: https://ejemplo.com
```

## Ejemplo 2: Con URL directa
```bash
python scarlet_v2.py --url https://ejemplo.com
```
o usando la forma corta:
```bash
python scarlet_v2.py -u https://ejemplo.com
```

## Ejemplo 3: Limitar a 50 URLs
```bash
python scarlet_v2.py -u https://ejemplo.com --max-urls 50
```
Procesa máximo 50 URLs y luego se detiene.

## Ejemplo 4: Aumentar concurrencia
```bash
python scarlet_v2.py -u https://ejemplo.com --workers 20
```
Usa 20 workers concurrentes para procesamiento más rápido.

## Ejemplo 5: Guardar resultados
```bash
python scarlet_v2.py -u https://ejemplo.com --output resultados.json
```
Guarda todas las URLs encontradas en un archivo JSON.

## Ejemplo 6: Configuración completa
```bash
python scarlet_v2.py -u https://ejemplo.com -m 200 -w 15 -o sitio_web.json
```
- URL: https://ejemplo.com
- Procesa máximo 200 URLs
- Usa 15 workers concurrentes
- Guarda resultados en sitio_web.json

## Ejemplo 7: Sitio con problemas de certificado SSL
```bash
python scarlet_v2.py -u https://sitio-ssl-invalido.com -k -o resultado.json
```
⚠️ **Advertencia**: `-k` desactiva la verificación SSL. Úsalo solo para testing.

## Ejemplo 8: Crawling rápido sin SSL
```bash
python scarlet_v2.py -u https://on.pe/empresas/ -w 20 -m 100 -k
```
Para sitios con certificados problemáticos pero confiables.

## Salida esperada

Durante la ejecución verás algo como:
```
    ███████╗ ██████╗ █████╗ ██████╗ ██╗     ███████╗████████╗
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██║     ██╔════╝╚══██╔══╝
    ███████╗██║     ███████║██████╔╝██║     █████╗     ██║   
    ╚════██║██║     ██╔══██║██╔══██╗██║     ██╔══╝     ██║   
    ███████║╚██████╗██║  ██║██║  ██║███████╗███████╗   ██║   
    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   
                                                         	
                Create by: Eddu escobedo

Ingrese la URL: https://ejemplo.com

[*] Iniciando crawling de: https://ejemplo.com
[*] Workers concurrentes: 10

https://ejemplo.com/about - ✔
https://ejemplo.com/contact - ✔
https://ejemplo.com/blog - ✔
https://ejemplo.com/services - ✔
...

============================================================
ESTADÍSTICAS FINALES
============================================================
URLs encontradas: 47
URLs procesadas: 47
Errores: 3
Tiempo total: 12.34 segundos
============================================================

[✓] Resultados guardados en: resultados.json
```

## Interpretación de colores

- **Amarillo**: URL del mismo dominio principal
- **Azul**: URL de un subdominio (ej: blog.ejemplo.com)
- **Verde (✔)**: URL accesible correctamente
- **Rojo (X)**: Error al acceder (404, timeout, etc.)

## Archivo JSON resultante

```json
{
  "timestamp": "2025-11-04T15:30:45.123456",
  "total_urls": 47,
  "urls": [
    "https://ejemplo.com",
    "https://ejemplo.com/about",
    "https://ejemplo.com/blog",
    "https://ejemplo.com/contact",
    "https://ejemplo.com/services"
  ]
}
```

## Casos de uso comunes

### Auditoría de sitio web
```bash
python scarlet_v2.py -u https://misitio.com -o auditoria.json
```

### Crawling rápido de vista previa
```bash
python scarlet_v2.py -u https://ejemplo.com -m 20 -w 5
```

### Crawling profundo y completo
```bash
python scarlet_v2.py -u https://ejemplo.com -w 25 -o crawl_completo.json
```

### Testing local
```bash
python scarlet_v2.py -u http://localhost:3000 -m 50
```

### Automatización con scripts
```bash
# En un script bash/PowerShell
python scarlet_v2.py -u https://sitio1.com -o sitio1.json
python scarlet_v2.py -u https://sitio2.com -o sitio2.json
python scarlet_v2.py -u https://sitio3.com -o sitio3.json
```

## Tips y recomendaciones

1. **Sitios pequeños**: Usa pocos workers (5-10)
   ```bash
   python scarlet_v2.py -u https://blog-personal.com -w 5
   ```

2. **Sitios grandes**: Aumenta workers (15-25)
   ```bash
   python scarlet_v2.py -u https://sitio-grande.com -w 25
   ```

3. **Conexión lenta**: Reduce workers (3-5)
   ```bash
   python scarlet_v2.py -u https://ejemplo.com -w 3
   ```

4. **Exportar siempre**: Usa `-o` para no perder resultados
   ```bash
   python scarlet_v2.py -u https://ejemplo.com -o backup.json
   ```

5. **Limitar primero**: Usa `-m` cuando explores sitios nuevos
   ```bash
   python scarlet_v2.py -u https://sitio-nuevo.com -m 50
   ```

6. **Modo automatizado**: Úsalo en scripts sin interacción
   ```bash
   python scarlet_v2.py -u https://ejemplo.com -m 100 -o resultado.json
   ```
