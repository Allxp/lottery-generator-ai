# 🧠 Dashboard del Generador Inteligente de Lotería

Interfaz web completa para el sistema de generación inteligente de combinaciones de lotería con memoria Engram persistente.

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.11+
- Flask (`pip install flask`)
- Sistema Engram ya configurado

### Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install flask
   ```

2. **Ejecutar el dashboard:**
   ```bash
   python dashboard.py
   ```

3. **Acceder al dashboard:**
   - Abrir navegador en: http://localhost:5000

## 📱 Funcionalidades

### 🏠 Página Principal (`/`)
- **Estado del sistema** en tiempo real
- **Métricas generales** del sistema Engram
- **Navegación** a todas las secciones
- **Actualización automática** cada 30 segundos

### 🎯 Generación de Combinaciones (`/generate`)
- **Selección de lotería:** LEIDSA, Primitiva, Euromillones, Bonoloto
- **Número de combinaciones** a generar (1-20)
- **Visualización de scores** y probabilidades
- **Resultados en tiempo real** con formato de lotería

### 🧠 Memoria Engram (`/memory`)
- **Visualización de aprendizajes** del sistema
- **Filtros por dominio:** backtesting, arquitectura, estadísticas, data_pipeline
- **Búsqueda en tiempo real** de memorias
- **Estadísticas de confianza** y timestamps
- **Navegación paginada** de memorias

### 📊 Reportes (`/reports`)
- **Métricas de rendimiento** general
- **Estado por lotería** con indicadores visuales
- **Historial de backtests** y precisiones
- **Alertas del sistema** automáticas
- **Acciones de mantenimiento:**
  - Ejecutar backtests para todos los juegos
  - Limpiar datos antiguos
  - Crear backups de la base de datos
  - Exportar reportes

### 🔍 Detalles de Juego (`/reports/{game_id}/details`)
- **Estadísticas específicas** por lotería
- **Historial de backtests** detallado
- **Métricas de rendimiento** individuales
- **Acciones específicas** del juego

## 🔧 API Endpoints

### GET `/api/status`
**Estado del sistema Engram**
```json
{
  "total_memories": 150,
  "domains": {
    "backtesting": 45,
    "architecture": 23,
    "stats": 67
  },
  "timestamp": "2024-01-15T14:30:00",
  "status": "operational"
}
```

### POST `/api/generate`
**Generar combinaciones programáticamente**
```json
// Request
{
  "lottery": "leidsa",
  "count": 5
}

// Response
{
  "lottery": "leidsa",
  "combinations": [
    {
      "numbers": [5, 12, 23, 34, 41, 48],
      "score": 0.85,
      "confidence": 0.92
    }
  ],
  "count": 5
}
```

## 🏗️ Arquitectura

### Componentes Principales
- **`dashboard.py`**: Aplicación Flask principal con rutas y lógica
- **`templates/`**: Plantillas HTML con estilos CSS integrados
  - `index.html`: Página principal
  - `generate.html`: Generación de combinaciones
  - `memory.html`: Visualización de memoria Engram
  - `reports.html`: Dashboard de reportes
  - `game_details.html`: Detalles específicos de lotería

### Integración con Engram
- **Lectura directa** desde `engram_storage.py`
- **Búsqueda FTS** para filtrado eficiente
- **Actualización automática** de métricas
- **Limpieza programada** de datos antiguos

### Seguridad y Rendimiento
- **Validación de entrada** en todos los formularios
- **Manejo de errores** con páginas de error amigables
- **Caché inteligente** para consultas frecuentes
- **Timeouts apropiados** para operaciones largas

## 🎨 Interfaz de Usuario

### Diseño
- **Responsive Design** adaptable a móviles y desktop
- **Paleta de colores** profesional (azul principal)
- **Iconografía consistente** con emojis descriptivos
- **Navegación intuitiva** con breadcrumbs

### Funcionalidades UX
- **Estados de carga** para operaciones asíncronas
- **Feedback visual** para acciones del usuario
- **Validación en tiempo real** de formularios
- **Accesibilidad** con etiquetas y navegación por teclado

## 🔧 Mantenimiento

### Tareas Programadas
```bash
# Ejecutar backtests diarios (desde auto_backtest.py)
python auto_backtest.py

# Limpiar memorias antiguas (desde dashboard)
# Acceder a /reports/clean-old-data
```

### Backup y Recuperación
```bash
# Backup manual desde CLI
python engram_manager.py backup

# Backup desde dashboard
# Acceder a /reports/backup-database
```

### Monitoreo
- **Logs del sistema** en `data/engram.log`
- **Métricas en tiempo real** en página principal
- **Alertas automáticas** en reportes
- **Estado de salud** vía API `/api/status`

## 🚨 Solución de Problemas

### Error 500 en Reportes
- **Causa:** Problemas con consultas a base de datos
- **Solución:** Verificar integridad de `data/engram.db`

### Dashboard No Carga
- **Causa:** Puerto 5000 ocupado o Flask no instalado
- **Solución:**
  ```bash
  pip install flask
  # Cambiar puerto en dashboard.py si es necesario
  ```

### Memoria Engram Vacía
- **Causa:** Sistema aún no ha generado aprendizajes
- **Solución:** Ejecutar backtests para poblar la memoria

## 📈 Métricas y KPIs

### Rendimiento del Sistema
- **Precisión promedio** de predicciones
- **Tasa de éxito** de backtests
- **Cobertura de juegos** activos
- **Frecuencia de aprendizaje** (memorias/día)

### Salud del Sistema
- **Tiempo de respuesta** de endpoints
- **Uso de memoria** del proceso
- **Tamaño de base de datos**
- **Último backup** exitoso

## 🔮 Próximas Funcionalidades

- [ ] **Gráficos interactivos** con Chart.js
- [ ] **Notificaciones push** para eventos importantes
- [ ] **API REST completa** para integraciones externas
- [ ] **Autenticación de usuarios** multi-sesión
- [ ] **Exportación de datos** en múltiples formatos
- [ ] **Dashboard móvil** optimizado

## 📝 Notas de Desarrollo

- **Framework:** Flask con Jinja2 templates
- **Base de datos:** SQLite con FTS5 para búsqueda
- **Estilos:** CSS integrado (sin dependencias externas)
- **JavaScript:** Vanilla JS para interactividad básica
- **Arquitectura:** MVC simplificado con separación clara

---

**Desarrollado con ❤️ para el Sistema Engram de Generación de Lotería**