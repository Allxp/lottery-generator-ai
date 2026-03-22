# 🚀 Guía de Despliegue: Security Review Automático

## 📋 Pasos para Configurar GitHub Actions

### 1. **Crear Repositorio en GitHub**
```bash
# Si aún no tienes el repositorio remoto, créalo en GitHub
# Luego conecta tu repositorio local:
git remote add origin https://github.com/TU_USUARIO/lottery-generator.git
git push -u origin main
```

### 2. **Configurar Secret de Anthropic**
1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**
4. **Name**: `ANTHROPIC_API_KEY`
5. **Value**: Tu clave API de Anthropic (obtén una en https://console.anthropic.com/)

### 3. **Probar el Security Review**
```bash
# Push de la rama de prueba (desde el directorio del proyecto)
git push origin feature/security-test
```

### 4. **Crear Pull Request**
1. Ve a tu repositorio en GitHub
2. Crea un **Pull Request** desde `feature/security-test` hacia `main`
3. El workflow se activará automáticamente
4. Revisa los comentarios del bot en el PR

## 🛡️ Qué Detectará el Security Review

### 🎯 **Vulnerabilidades Incluidas en la Prueba**
- **SQL Injection**: `f"SELECT * FROM table WHERE id = {user_input}"`
- **Secrets Expuestos**: API keys y passwords hardcoded
- **Corrupción LEIDSA**: Manejo incorrecto de datos históricos

### ✅ **Resultado Esperado**
- ❌ **Workflow falla** (debido a vulnerabilidades high severity)
- 💬 **Comentarios detallados** en el PR
- 🔍 **Identificación específica** de cada vulnerabilidad

## 📊 Monitoreo Continuo

### Después de la Configuración Inicial:
- **Cada PR hacia main** activará automáticamente el review
- **Comentarios en tiempo real** sobre vulnerabilidades encontradas
- **Status checks** que bloquean merges inseguros

### Dashboard de Seguridad:
- Revisa la pestaña **Actions** en GitHub para ver ejecuciones
- Los **comentarios del bot** contienen análisis detallados
- **Workflow runs** muestran logs completos del análisis

## 🔧 Troubleshooting

### Si el Workflow no se Activa:
1. Verifica que el archivo esté en `.github/workflows/security.yml`
2. Confirma que el secret `ANTHROPIC_API_KEY` esté configurado
3. Asegúrate de que el PR sea hacia la rama `main`

### Si Falla la Acción:
- Revisa los logs en la pestaña **Actions**
- Verifica que la API key de Anthropic sea válida
- Confirma que tienes permisos para usar Claude Code Security Review

## 🎉 Próximos Pasos

Una vez configurado y probado:
1. **Merge seguro**: Solo código que pase el security review
2. **Monitoreo continuo**: Cada contribución será auditada
3. **Mejora iterativa**: El sistema aprende y mejora con cada análisis

**¡Tu generador de lotería ahora tiene seguridad por diseño integrada!** 🔒✨