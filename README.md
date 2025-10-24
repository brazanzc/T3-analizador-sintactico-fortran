# 🧠 Analizador Léxico y Sintáctico — Tarea 3

Este repositorio contiene el código fuente correspondiente a la **Tarea 3** de la asignatura **Teoría de la Computación**, Semestre II-2025.

---

## 👨‍🏫 Profesor

**M. Lévano**

## 👥 Integrantes

- Daniel Cotal  
- Bryan Zapata  
- Sebastián Riquelme  

---

## 📜 Descripción del Proyecto

El objetivo de este proyecto es el **diseño e implementación de un analizador léxico y sintáctico** para un subconjunto del lenguaje **FORTRAN77**.  

El proyecto está desarrollado en **Python** y aplica conceptos de **Gramáticas Libres de Contexto (GLC)** para validar la estructura del código fuente.  

El **analizador sintáctico** está implementado mediante un **Parser de Descenso Recursivo**, compatible con el enfoque **LL(1)**.

---

## ✨ Características Principales

- **Analizador Léxico (`Lexer`):**  
  Implementado con el módulo `re` de Python. Convierte el código fuente en una lista de tokens reconocibles.

- **Analizador Sintáctico (`Parser`):**  
  Valida la secuencia de tokens según una gramática definida.

- **Detección de Errores:**  
  El sistema reporta tanto **errores léxicos** (caracteres no reconocidos) como **errores sintácticos** (secuencias de tokens inválidas), indicando el número de línea del problema.

- **Traza de Derivación:**  
  Durante el análisis sintáctico, el parser imprime cada token consumido, mostrando el proceso de derivación paso a paso.

- **Manejo de Comentarios:**  
  Los comentarios (definidos como `-- ...`) son ignorados por el analizador.

- **Insensible a Mayúsculas:**  
  Todo el código se convierte internamente a mayúsculas para facilitar un análisis uniforme.

---

## 📖 Gramática Soportada

El analizador reconoce la siguiente estructura gramatical, correspondiente a un subconjunto de **FORTRAN77**:

- **Programa:**  
  ```fortran
  PROGRAM [NOMBRE]
  ...
  END
