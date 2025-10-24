Perfecto ✅ Aquí tienes **todo el contenido del README completo** en **un solo bloque**, listo para copiar y pegar directamente en tu archivo `README.md` sin cortes:

---

# 🧠 Analizador Léxico y Sintáctico — Tarea 3

Este repositorio contiene el código fuente correspondiente a la **Tarea 3** de la asignatura **Teoría de la Computación**, Semestre II-2025.

---

## 👨‍🏫 Profesor

**M. Lévano**

## 👥 Integrantes

* Daniel Cotal
* Bryan Zapata
* Sebastián Riquelme

---

## 📜 Descripción del Proyecto

El objetivo de este proyecto es el **diseño e implementación de un analizador léxico y sintáctico** para un subconjunto del lenguaje **FORTRAN77**.

El proyecto está desarrollado en **Python** y aplica conceptos de **Gramáticas Libres de Contexto (GLC)** para validar la estructura del código fuente.

El **analizador sintáctico** está implementado mediante un **Parser de Descenso Recursivo**, compatible con el enfoque **LL(1)**.

---

## ✨ Características Principales

* **Analizador Léxico (`Lexer`):**
  Implementado con el módulo `re` de Python. Convierte el código fuente en una lista de tokens reconocibles.

* **Analizador Sintáctico (`Parser`):**
  Valida la secuencia de tokens según una gramática definida.

* **Detección de Errores:**
  El sistema reporta tanto **errores léxicos** (caracteres no reconocidos) como **errores sintácticos** (secuencias de tokens inválidas), indicando el número de línea del problema.

* **Traza de Derivación:**
  Durante el análisis sintáctico, el parser imprime cada token consumido, mostrando el proceso de derivación paso a paso.

* **Manejo de Comentarios:**
  Los comentarios (definidos como `-- ...`) son ignorados por el analizador.

* **Insensible a Mayúsculas:**
  Todo el código se convierte internamente a mayúsculas para facilitar un análisis uniforme.

---

## 📖 Gramática Soportada

El analizador reconoce la siguiente estructura gramatical, correspondiente a un subconjunto de **FORTRAN77**:

* **Programa:**

  ```fortran
  PROGRAM [NOMBRE]
  ...
  END
  ```

* **Declaración:**

  ```fortran
  INTEGER [VAR]
  REAL [VAR]
  ```

* **Asignación:**

  ```fortran
  [VAR] = [NUMERO]
  [VAR] = [VAR]
  ```

* **Impresión:**

  ```fortran
  PRINT *, [VAR]
  ```

* **Condicional:**

  ```fortran
  IF ([VAR]) THEN
      [SENTENCIA]
  END IF
  ```

---

## 🚀 Cómo Ejecutar

El script es **autocontenido** y no requiere librerías externas adicionales a las estándar de Python.

1. **Clonar el repositorio:**

   ```bash
   git clone [URL-DE-TU-REPO]
   ```

2. **Entrar al directorio del proyecto:**

   ```bash
   cd nombre-del-repositorio
   ```

3. **Ejecutar el programa:**

   ```bash
   python tu_archivo.py
   ```

---

## 🧪 Casos de Prueba

El script incluye **tres casos de prueba** integrados para validar el funcionamiento del analizador:

### 1️⃣ `codigo_correcto`

Un programa válido que debe analizarse sin errores.

**Resultado esperado:**
✅ Mensaje: *“¡La sintaxis del programa es correcta!”*

---

### 2️⃣ `codigo_error_sintaxis`

Un programa con error sintáctico (por ejemplo, falta la palabra clave `THEN`).

**Resultado esperado:**
❌ Lanza un `RuntimeError` indicando el **error de sintaxis** y la **línea afectada**.

---

### 3️⃣ `codigo_error_lexico`

Un programa con error léxico (por ejemplo, contiene el carácter inválido `@`).

**Resultado esperado:**
❌ Lanza un `RuntimeError` indicando el **error léxico** y la **línea afectada**.

---

