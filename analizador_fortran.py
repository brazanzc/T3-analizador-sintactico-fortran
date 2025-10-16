import re

# --- PASO 1: EL ANALIZADOR LÉXICO (MÁS SIMPLE) ---

# Tupla para guardar la información de cada Token de forma sencilla
# (Tipo, Valor, Número de Línea) -> El número de línea es clave para los errores.
class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        # Esta función ayuda a que se vea bonito si imprimimos un token.
        return f"({self.type}, '{self.value}', Línea {self.line})"

def lexer(codigo_fuente):
    """
    Función que toma el código fuente y lo convierte en una lista de Tokens.
    """
    # Convertimos todo a mayúsculas para que sea insensible (PROGRAM = program)
    codigo_fuente = codigo_fuente.upper()
    
    # Definimos los "planos" de nuestros tokens con expresiones regulares.
    # El orden es importante: las palabras clave van antes que los identificadores.
    especificaciones_token = [
        ('COMENTARIO', r'--.*'),           # Ignorar comentarios (de -- hasta el final de la línea)
        ('ESPACIO',    r'[ \t\n]+'),         # Ignorar espacios, tabs y saltos de línea
        ('NUMERO',     r'\d+(\.\d*)?'),     # 123 o 45.67
        ('ASIGNACION', r'='),               # =
        ('OPERADOR',   r'[+\-*/()]'),       # +, -, *, /, (, )
        ('PRINT',      r'PRINT'),           # La palabra clave PRINT
        ('PROGRAM',    r'PROGRAM'),
        ('INTEGER',    r'INTEGER'),
        ('REAL',       r'REAL'),
        ('IF',         r'IF'),
        ('THEN',       r'THEN'),
        ('END',        r'END'),
        ('COMA',       r','),
        ('IDENTIFICADOR', r'[A-Z][A-Z0-9_]*'), # Nombres de variables: VAR, MI_PROG, X1
        ('ERROR',      r'.'),               # Cualquier otro caracter es un error léxico
    ]
    
    # Unimos todas las expresiones regulares en una sola.
    regex_tokens = '|'.join('(?P<%s>%s)' % pair for pair in especificaciones_token)
    
    tokens = []
    line_num = 1
    
    # Recorremos el código buscando coincidencias con nuestra gran regex.
    for match in re.finditer(regex_tokens, codigo_fuente):
        tipo = match.lastgroup
        valor = match.group()
        
        # Si es un espacio o comentario, lo ignoramos y contamos las líneas.
        if tipo == 'ESPACIO':
            line_num += valor.count('\n')
        elif tipo == 'COMENTARIO':
            continue
        # Si es un token válido, lo agregamos a nuestra lista.
        elif tipo != 'ERROR':
            tokens.append(Token(tipo, valor, line_num))
        # Si encontramos un caracter no reconocido, lanzamos un error claro.
        else:
            raise RuntimeError(f"Error Léxico en la línea {line_num}: Caracter inesperado '{valor}'")
            
    tokens.append(Token('EOF', None, line_num)) # "End Of File" Token para marcar el final.
    return tokens


# --- PASO 2: EL ANALIZADOR SINTÁCTICO (MÁS CLARO) ---

class Parser:
    """
    El inspector que verifica que la secuencia de tokens siga las reglas gramaticales.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 # Nuestra posición actual en la lista de tokens.

    def token_actual(self):
        """Devuelve el token que estamos mirando ahora, sin avanzar."""
        return self.tokens[self.pos]

    def error_sintactico(self, tipo_esperado):
        """Función mejorada para reportar errores de forma clara."""
        token = self.token_actual()
        # ¡Este es el mensaje de error mejorado!
        raise RuntimeError(
            f"Error de Sintaxis en la línea {token.line}: \n"
            f"Se esperaba un token de tipo '{tipo_esperado}', "
            f"pero se encontró un '{token.value}' (tipo: {token.type})."
        )

    def consumir(self, tipo_esperado):
        """
        Consume el token actual SI Y SÓLO SI es del tipo esperado.
        Si no lo es, lanza un error. Si lo es, avanza a la siguiente posición.
        """
        token = self.token_actual()
        if token.type == tipo_esperado:
            print(f"Consumido: {token}") # Traza para ver qué está haciendo el parser
            self.pos += 1
            return token
        else:
            self.error_sintactico(tipo_esperado)

    # --- Reglas de la Gramática ---
    # Cada función representa una regla: ¿qué estructura esperamos ver?

    def programa(self):
        """Regla: PROGRAM IDENTIFICADOR ... sentencias ... END"""
        self.consumir('PROGRAM')
        self.consumir('IDENTIFICADOR')
        self.sentencias()
        self.consumir('END')
        print("\nAnálisis finalizado: ¡La sintaxis del programa es correcta! ✅")
    
    def sentencias(self):
        """Una o más sentencias hasta que encontremos 'END'."""
        while self.token_actual().type not in ['END', 'EOF']:
            self.sentencia()

    def sentencia(self):
        """Decide qué tipo de sentencia es (asignación, if, print, etc.)."""
        tipo_token = self.token_actual().type
        if tipo_token in ['INTEGER', 'REAL']:
            self.declaracion_var()
        elif tipo_token == 'IDENTIFICADOR':
            self.asignacion()
        elif tipo_token == 'PRINT':
            self.impresion()
        elif tipo_token == 'IF':
            self.condicional()
        else:
            raise RuntimeError(f"Error de Sintaxis en línea {self.token_actual().line}: "
                               f"No se esperaba el inicio de una sentencia con '{self.token_actual().value}'.")

    def declaracion_var(self):
        """Regla: (INTEGER | REAL) IDENTIFICADOR"""
        if self.token_actual().type == 'INTEGER':
            self.consumir('INTEGER')
        else:
            self.consumir('REAL')
        self.consumir('IDENTIFICADOR')

    def asignacion(self):
        """Regla: IDENTIFICADOR = expresion"""
        self.consumir('IDENTIFICADOR')
        self.consumir('ASIGNACION')
        # Aquí iría la lógica para analizar una expresión completa.
        # Por simplicidad, solo consumimos un número o variable.
        if self.token_actual().type == 'NUMERO':
            self.consumir('NUMERO')
        else:
            self.consumir('IDENTIFICADOR')

    def impresion(self):
        """Regla: PRINT *, IDENTIFICADOR"""
        self.consumir('PRINT')
        self.consumir('OPERADOR') # El asterisco
        self.consumir('COMA')
        self.consumir('IDENTIFICADOR')

    def condicional(self):
        """Regla: IF (IDENTIFICADOR) THEN sentencia END IF"""
        self.consumir('IF')
        self.consumir('OPERADOR') # Paréntesis (
        self.consumir('IDENTIFICADOR')
        self.consumir('OPERADOR') # Paréntesis )
        self.consumir('THEN')
        self.sentencia() # Puede haber una o más sentencias dentro del IF
        self.consumir('END')
        self.consumir('IF')

# --- PASO 3: PRUEBAS (MÁS FÁCILES DE ENTENDER) ---

# CASO 1: Un código perfectamente válido
codigo_correcto = """
PROGRAM MI_TEST
  -- Declaraciones de variables
  INTEGER VAR1
  REAL TOTAL
  
  -- Asignaciones
  VAR1 = 100
  TOTAL = VAR1
  
  -- Condicional
  IF (VAR1) THEN
    PRINT *, TOTAL
  END IF
  
END
"""

# CASO 2: Un error de sintaxis obvio (falta el 'THEN')
codigo_error_sintaxis = """
PROGRAM PRUEBA_ERROR
  INTEGER A
  
  -- Aquí falta la palabra THEN después de la condición
  IF (A)
    A = 10
  END IF
  
END
"""

# CASO 3: Un error léxico (un símbolo que no existe en nuestro lenguaje)
codigo_error_lexico = """
PROGRAM PRUEBA_LEXICO
  INTEGER B
  
  -- El símbolo @ no está definido en nuestro lenguaje
  B = @
END
"""

def analizar_codigo(nombre_prueba, codigo):
    """Función para ejecutar una prueba y mostrar el resultado de forma clara."""
    print(f"\n--- INICIANDO PRUEBA: '{nombre_prueba}' ---")
    try:
        # 1. Obtener la lista de tokens
        tokens = lexer(codigo)
        print("Tokens generados:")
        # for t in tokens: print(t) # Descomenta esta línea si quieres ver la lista de tokens
        
        # 2. Crear el parser con los tokens
        parser = Parser(tokens)
        
        # 3. Iniciar el análisis desde la regla principal 'programa'
        parser.programa()
        
    except RuntimeError as e:
        # Si algo falla (léxico o sintáctico), mostramos el error claro.
        print(f"\n❌ ERROR DETECTADO en '{nombre_prueba}':")
        print(e)
    print("--------------------------------------")


# --- Ejecutamos las pruebas ---
analizar_codigo("1", codigo_correcto)
analizar_codigo("2", codigo_error_sintaxis)
analizar_codigo("3", codigo_error_lexico)