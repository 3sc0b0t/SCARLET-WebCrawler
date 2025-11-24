# SCARLET - Web Crawler

## 🔍 Descripción
SCARLET es un web crawler asíncrono diseñado para descubrir URLs dentro de un mismo dominio. Utiliza `asyncio` y `aiohttp` para realizar peticiones concurrentes de manera eficiente.

## ✨ Características

- ✅ **Crawling asíncrono**: Utiliza async/await para máxima eficiencia
- ✅ **Control de concurrencia**: Semáforos para limitar peticiones simultáneas
- ✅ **Detección de subdominios**: Identifica y marca URLs de subdominios
- ✅ **Manejo robusto de errores**: Timeout, reintentos y validación de URLs
- ✅ **Estadísticas detalladas**: Muestra métricas al finalizar el proceso
- ✅ **Exportación a JSON**: Guarda resultados en formato estructurado
- ✅ **Argumentos CLI**: Configuración flexible desde línea de comandos

## 📋 Requisitos

```bash
pip install aiohttp beautifulsoup4
```

## 🚀 Uso

### Uso básico (interactivo)
```bash
python scarlet_v2.py
```
El programa te pedirá ingresar la URL.

### Con URL directa
```bash
python scarlet_v2.py --url https://ejemplo.com
```

### Con límite de URLs
```bash
python scarlet_v2.py -u https://ejemplo.com --max-urls 100
```

### Configurar workers concurrentes
```bash
python scarlet_v2.py -u https://ejemplo.com --workers 20
```

### Guardar resultados en JSON
```bash
python scarlet_v2.py -u https://ejemplo.com --output resultados.json
```

### Combinando opciones
```bash
python scarlet_v2.py -u https://ejemplo.com -m 500 -w 15 -o sitio.json
```

### Con sitios que tienen problemas de certificado SSL
```bash
python scarlet_v2.py -u https://sitio-con-ssl-invalido.com -k
```
⚠️ **Advertencia**: Solo usa `-k` para testing. No es recomendado en producción.

## 🔧 Parámetros

| Parámetro | Abreviatura | Descripción | Por defecto |
|-----------|-------------|-------------|-------------|
| `--url` | `-u` | URL base a crawlear | Solicitar interactivamente |
| `--max-urls` | `-m` | Límite máximo de URLs a procesar | Sin límite |
| `--workers` | `-w` | Número de workers concurrentes | 10 |
| `--output` | `-o` | Archivo de salida JSON | No guardar |
| `--insecure` | `-k` | Ignorar errores SSL (solo testing) | Verificar SSL |

## 📊 Salida

El programa muestra en tiempo real:
- URLs encontradas (en amarillo para mismo dominio, azul para subdominios)
- Estado de cada URL (✔ accesible, X error)
- Estadísticas finales:
  - Total de URLs encontradas
  - URLs procesadas
  - Errores encontrados
  - Tiempo total de ejecución

## 📁 Formato de salida JSON

```json
{
  "timestamp": "2025-11-04T10:30:00",
  "total_urls": 150,
  "urls": [
    "https://ejemplo.com",
    "https://ejemplo.com/about",
    "https://ejemplo.com/contact"
  ]
}
```

## 🎨 Códigos de color

- 🟢 Verde: URL accesible correctamente
- 🔴 Rojo: Error al acceder a la URL
- 🟡 Amarillo: URL del mismo dominio
- 🔵 Azul: URL de subdominio

## ⚙️ Mejoras implementadas

1. **Validación de URLs**: Verifica formato antes de iniciar
2. **Timeout configurable**: Evita peticiones colgadas (10 segundos)
3. **Semáforos para concurrencia**: Control real de peticiones simultáneas
4. **Manejo de localhost**: Soporte para dominios sin TLD
5. **Eliminación de fragmentos**: Evita duplicados por anchors (#)
6. **Estadísticas en tiempo real**: Monitoreo del proceso
7. **Exportación de datos**: Resultados en formato JSON
8. **CLI con argparse**: Configuración flexible
9. **Docstrings completos**: Documentación en cada función
10. **Banner optimizado**: Sin delay innecesario

## 🐛 Solución de problemas

### Error de importación
```bash
pip install --upgrade aiohttp beautifulsoup4
```

### Error de certificado SSL
Si encuentras errores como `SSL: CERTIFICATE_VERIFY_FAILED`, puedes usar:
```bash
python scarlet_v2.py -u https://sitio.com -k
```
⚠️ **Nota**: Esto desactiva la verificación SSL. Úsalo solo para testing o sitios confiables.

### Demasiados errores de timeout
Reduce el número de workers:
```bash
python scarlet_v2.py --workers 5
```

### Proceso muy lento
Aumenta el número de workers (con precaución):
```bash
python scarlet_v2.py --workers 20
```

## 📝 Notas

- El crawler respeta el mismo dominio base para evitar salir del sitio objetivo
- Los fragmentos de URL (#section) son ignorados para evitar duplicados
- Solo se procesan páginas HTML, otros tipos de contenido son omitidos
- El timeout por defecto es de 10 segundos por petición

## 👤 Autor

**3SC0B0T**

---

⚡ Desarrollado con Python + AsyncIO + aiohttp

