# Documento de Requisitos de Producto (PRD) & Brief del Proyecto
## Módulo Móvil: Impresión y Procesamiento de Facturas / Documentos

---

### 1. Resumen Ejecutivo (Executive Summary)
**Nombre del Proyecto:** Impresión Rápida de Facturas y Documentos (FacturaPrint Mobile)  
**Propósito:** Proporcionar una experiencia móvil sumamente intuitiva, rápida y sin fricción técnica para cargar imágenes/documentos de facturación, revisar visualmente cuáles se desean enviar a procesar/imprimir y monitorear el estado de impresión en tiempo real.

---

### 2. Objetivos del Producto
- **Simplicidad Absoluta:** Reducir la sobrecarga cognitiva eliminando barras de navegación complejas, metadatos innecesarios y controles superfluos.
- **Eficiencia en la Carga:** Permitir seleccionar imágenes/facturas en 1-2 toques desde el dispositivo.
- **Control de Selección:** Inspección rápida con marcado/desmarcado táctil de fotos/facturas a imprimir.
- **Visibilidad del Estado:** Loader claro y reconfortante que informe el progreso del envío a impresión sin tecnicismos confusos.

---

### 3. Audiencia Objetivo y Casos de Uso
- **Público Objetivo:** Usuarios de administración, pequeñas empresas, contadores y clientes finales que necesitan imprimir comprobantes o recibos desde sus teléfonos móviles.
- **Principales Casos de Uso:**
  1. Capturar o subir fotografías de facturas y tickets desde la galería o almacenamiento del teléfono.
  2. Filtrar o descartar aquellas fotos borrosas o no pertinentes antes de enviarlas al centro de impresión.
  3. Enviar a imprimir por lotes con confirmación visual de progreso.

---

### 4. Arquitectura de Información y Flujo de Pantallas

El flujo consta de 3 pantallas clave en formato móvil (Mobile Stack):

```
[Pantalla 1: Carga Central] 
          │ (Archivos seleccionados)
          ▼
[Pantalla 2: Revisión & Selección] 
          │ (Acción: Imprimir)
          ▼
[Pantalla 3: Procesando / Loader]
```

#### Pantalla 1: Carga de Facturas / Imágenes (`Cargar Facturas`)
- **Tipo de Shell:** Mobile Header simple (sin barra de pestañas/tabs inferiores).
- **Encabezado:** Título "Impresión de facturas" con icono de documento/recibo.
- **Zona Central (Dropzone Hero):**
  - Contenedor táctil centralizado con icono ilustrativo.
  - Formatos admitidos: JPG, PNG, PDF (hasta 25 MB por archivo).
  - Botón de acción principal (CTA): *"Elegir facturas"* / *"Explorar archivos"*.
- **Criterio de Aceptación:** No debe haber navegación inferior ni listas residuales que distraigan del llamado a la acción principal.

#### Pantalla 2: Revisión y Selección (`Revisión y Selección`)
- **Visualización:** Cuadrícula táctil de 2 columnas optimizada para móviles.
- **Interacción:**
  - Toque para alternar estado: Seleccionada (Check azul activo con borde destacado) vs Omitida (opacidad atenuada).
  - Opción rápida en cabecera: *"Deseleccionar todas"* / *"Seleccionar todas"*.
- **Barra de Acción Fija:**
  - Contador en tiempo real: *"X facturas seleccionadas"*.
  - Botón primario: *"Imprimir (X)"* con icono de impresora.

#### Pantalla 3: Procesando Impresión (`Loader / Progreso`)
- **Indicador Visual:** Anillo de carga circular minimalista con porcentaje centralizado en tiempo real (ej. 67% / 100%).
- **Mensajes de Estado:**
  - Titular: *"Enviando a imprimir..."*
  - Subtítulo descriptivo: *"Preparando tus documentos en alta resolución"*.
- **Control de Escape:** Botón discreto *"Cancelar"* para abortar la operación si el usuario lo requiere.

---

### 5. Requisitos Funcionales (FR)
- **FR-01 (Formatos):** El componente de subida debe restringir las extensiones exclusivamente a formatos de imagen (JPG, PNG, HEIC) y documentos compatibles (PDF).
- **FR-02 (Selección Múltiple):** El selector del sistema debe soportar selección múltiple simultánea.
- **FR-03 (Toggle de Inclusión):** Cada ítem en la cuadrícula debe alternar su inclusión en el lote con un solo tap.
- **FR-04 (Estado de Envío):** Al pulsar "Imprimir", se bloquea la interfaz y se transiciona a la pantalla del loader, mostrando progreso incremental simulado o conectado al backend de impresión.
- **FR-05 (Cancelación):** Si el usuario cancela en la pantalla de loader, regresa a la pantalla de revisión manteniendo su selección intacta.

---

### 6. Requisitos No Funcionales (NFR)
- **Rendimiento:** Carga inicial de miniaturas en la cuadrícula inferior a 300ms por imagen.
- **Accesibilidad (a11y):** Contraste de colores acorde a WCAG AA en botones primarios (azul índigo `#4f46e5` sobre fondo claro).
- **Diseño Responsivo:** Diseñado nativamente para pantallas táctiles móviles de 390px a 430px de ancho.
- **Feedback Háptico / Visual:** Micro-animaciones fluidas al marcar/desmarcar elementos y durante el giro del loader circular.

---

### 7. Sistema de Diseño & Identidad Visual
- **Tema:** Luminous Print (Modo Claro).
- **Color Primario:** Azul / Índigo corporativo (`#4f46e5`).
- **Fondos:** Superficies claras y limpias (`#f8f9ff`, `#ffffff`) con bordes sutiles redondeados (`rounded-xl` / `rounded-2xl`).
- **Tipografía:** *Plus Jakarta Sans* con jerarquía limpia (títulos Bold/SemiBold y textos auxiliares legibles).

---

### 8. Próximos Pasos & Extensiones Futuras
1. Integración con servicios de impresión en la nube (Cloud Print / AirPrint / Mopria).
2. Pantalla de confirmación de éxito con resumen de ticket o código QR de recogida.
3. Ajustes opcionales de impresión (tamaño de papel A4/Carta, color vs blanco y negro).
