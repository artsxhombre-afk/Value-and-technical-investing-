# 📈 App de Análisis de Acciones - Guía de Instalación

## 🎯 ¿Qué hace esta app?

Analiza acciones automáticamente y te da recomendaciones de COMPRA/VENTA basadas en:
- Análisis técnico completo (SMA, RSI, MACD, Bollinger Bands)
- Score de 0-100 puntos
- Señales claras y niveles de trading

**Funciona desde tu celular** ✅

---

## 📱 OPCIÓN 1: Usar desde el celular (GRATIS en internet)

### Paso 1: Crear cuenta en GitHub (si no tienes)
1. Ve a https://github.com
2. Click en "Sign up"
3. Crea tu cuenta gratis

### Paso 2: Subir la app a GitHub
1. Ve a https://github.com/new
2. Nombre del repositorio: `stock-analyzer`
3. Selecciona "Public"
4. Click "Create repository"
5. En tu computadora, sube estos archivos:
   - `stock_analyzer_app.py`
   - `requirements.txt`
   
   (Puedes arrastrar y soltar en la página de GitHub)

### Paso 3: Desplegar en Streamlit Cloud
1. Ve a https://streamlit.io/cloud
2. Click "Sign up" y usa tu cuenta de GitHub
3. Click "New app"
4. Selecciona:
   - Repository: `tu-usuario/stock-analyzer`
   - Branch: `main`
   - Main file path: `stock_analyzer_app.py`
5. Click "Deploy"
6. ¡Espera 2-3 minutos y listo!

### Paso 4: Acceder desde tu celular
1. Streamlit te dará una URL como: `https://tu-app.streamlit.app`
2. Guarda esa URL en favoritos de tu celular
3. ¡Ya puedes usar la app desde cualquier lugar!

**IMPORTANTE:** La app estará disponible 24/7 gratis en internet

---

## 💻 OPCIÓN 2: Correr en tu computadora (Local)

### Requisitos
- Python 3.8 o superior instalado
- Conexión a internet

### Instalación

1. **Abre la terminal/cmd y navega a la carpeta con los archivos**
```bash
cd /ruta/donde/guardaste/los/archivos
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

3. **Corre la app**
```bash
streamlit run stock_analyzer_app.py
```

4. **Abre tu navegador**
Se abrirá automáticamente en `http://localhost:8501`

### Para acceder desde tu celular (misma red WiFi):
1. En la terminal verás: `Network URL: http://192.168.X.X:8501`
2. Abre esa URL en el navegador de tu celular
3. ¡Listo!

---

## 🚀 Cómo usar la app

### Modo 1: Análisis Individual
1. Selecciona "🎯 Acción Individual"
2. Ingresa el ticker (ejemplo: `AAPL`, `PNG.V`)
3. Click en "🔍 ANALIZAR"
4. Recibe:
   - Score técnico (0-100)
   - Recomendación clara (COMPRA/VENTA/OBSERVAR)
   - Señales detalladas de todos los indicadores
   - Niveles de entrada/salida sugeridos

### Modo 2: Lista de Acciones
1. Selecciona "📊 Lista de Acciones"
2. Ingresa múltiples tickers (uno por línea):
   ```
   AAPL
   MSFT
   PNG.V
   GOOGL
   ```
3. Click en "🔍 ANALIZAR TODAS"
4. Recibe:
   - Ranking completo ordenado por score
   - Top 3 mejores oportunidades
   - Tabla con todas las recomendaciones
   - Estadísticas de señales

---

## 📊 Indicadores que usa

La app calcula automáticamente:

**Tendencia:**
- SMA 20, 50, 200 días
- Golden Cross / Death Cross

**Momentum:**
- RSI (14 períodos)
- MACD + Signal Line

**Volatilidad:**
- Bollinger Bands (superior, media, inferior)
- % de posición en las bandas

**Volumen:**
- Ratio volumen actual vs promedio 20 días

**Score Final:**
Combina todos los indicadores para dar un puntaje de 0-100:
- **75-100:** 🟢 COMPRA FUERTE
- **60-74:** 🟢 COMPRA
- **45-59:** 🟡 OBSERVAR
- **30-44:** 🟠 PRECAUCIÓN
- **0-29:** 🔴 EVITAR

---

## ⚠️ Notas importantes

### Sobre los datos:
- La app usa Yahoo Finance para datos en tiempo real
- Los datos son gratuitos pero pueden tener ~15 min de retraso
- Para datos en tiempo real necesitarías una API paga

### Limitaciones actuales (versión demo):
- Por restricciones de red, la versión actual usa datos simulados
- Para activar datos reales:
  1. Descomenta la línea con `yfinance` en el código
  2. Comenta la línea de datos demo
  3. Necesitas conexión a internet

### Código para datos reales:
Busca en `stock_analyzer_app.py` línea ~450:
```python
# Cambiar de:
data = get_stock_data_demo(ticker)

# A:
import yfinance as yf
data = yf.download(ticker, period="1y", progress=False)
```

---

## 🔧 Solución de problemas

**La app no se abre:**
- Verifica que Python esté instalado: `python --version`
- Reinstala dependencias: `pip install -r requirements.txt --upgrade`

**Error al descargar datos:**
- Verifica conexión a internet
- Algunos tickers necesitan sufijo (.V para TSX Venture, etc.)
- Ejemplo: Kraken Robotics es `PNG.V` no `PNG`

**La app es lenta:**
- Normal al analizar muchas acciones
- Limita a 10-20 acciones por análisis

**No funciona en el celular:**
- Verifica que estés en la misma red WiFi
- Usa la IP exacta que muestra la terminal
- Algunos routers bloquean acceso local

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que todos los archivos estén en la misma carpeta
2. Revisa que Python 3.8+ esté instalado
3. Asegúrate de tener conexión a internet
4. Reinstala las dependencias

---

## 🎯 Próximos pasos sugeridos

Una vez que la app funcione, puedes:

1. **Agregar análisis fundamental:**
   - P/E ratio, ROE, márgenes
   - Crecimiento de ventas/ganancias
   - Combinar con score técnico

2. **Backtesting:**
   - Probar estrategias históricamente
   - Ver qué habría pasado

3. **Alertas:**
   - Recibir notificaciones cuando haya señales
   - Email o SMS cuando score cambie

4. **Más indicadores:**
   - Fibonacci retracements
   - Ichimoku Cloud
   - Volume Profile

¿Quieres que agregue alguna de estas funcionalidades?

---

## ✅ Checklist de instalación

- [ ] Python instalado
- [ ] Archivos descargados (app.py + requirements.txt)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] App corriendo (`streamlit run stock_analyzer_app.py`)
- [ ] Accesible desde navegador
- [ ] (Opcional) Desplegada en Streamlit Cloud
- [ ] (Opcional) Accesible desde celular

---

¡Listo! Ahora tienes tu propia app de análisis de acciones funcionando 📈
