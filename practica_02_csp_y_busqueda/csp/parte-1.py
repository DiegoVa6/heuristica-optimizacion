import sys

"""---------------------------------------------------------
        FUNCION: leer_instancia(ruta_entrada)
------------------------------------------------------------
Lee el archivo .in y devuelve la rejilla como una lista
de cadenas de longitud n. Comprueba:
   - que no esté vacío
   - que todas las filas tengan la misma longitud
   - que n sea par (condición necesaria del Binairo)
 Esta función NO resuelve nada, solo valida y carga datos.
------------------------------------------------------------
"""
def leer_instancia(ruta_entrada):
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]

    if not lineas:
        raise ValueError("El fichero de entrada está vacío")

    n = len(lineas[0])

    for fila in lineas:
        if len(fila) != n:
            raise ValueError("Todas las filas deben tener la misma longitud")

    if n % 2 != 0:
        raise ValueError("El tamaño del tablero n debe ser par")

    return lineas

"""---------------------------------------------------------
        FUNCION: formatear_tablero(grid)
------------------------------------------------------------
Convierte una rejilla en forma de lista de strings
a un tablero dibujado con bordes.
------------------------------------------------------------
"""
def formatear_tablero(grid, mostrar_puntos_como_vacio=True):
    n = len(grid)
    line_sep = "+---" * n + "+\n"

    def convertir_char(c):
        if mostrar_puntos_como_vacio and c == '.':
            return ' '
        return c

    out = []
    out.append(line_sep)
    for fila in grid:
        celdas = [convertir_char(c) for c in fila]
        out.append("| " + " | ".join(celdas) + " |\n")
        out.append(line_sep)
    return "".join(out)

"""
------------------------------------------------------------
        FUNCION: resolver_binairo(grid)
------------------------------------------------------------
 Resuelve el puzzle Binairo por backtracking manual.
 Representa:
   - board[i][j] en {-1 (vacío), 0 (O), 1 (X)}
   - Restricción R1: Cada fila y columna debe tener n/2 unos
   - Restricción R2: No se permiten tres iguales consecutivos
   - Restricción R3: Celdas prefijadas se respetan

 El algoritmo:
   1. Inicializa el tablero con las celdas fijas.
   2. Comprueba si ya es infactible.
   3. Realiza backtracking llenando solo las celdas '.'.
   4. Hace poda incremental: comprueba restricciones
      inmediatamente después de poner un valor.
 Devuelve:
   (número_de_soluciones, primera_solución)
------------------------------------------------------------
"""
def resolver_binairo(grid):
    n = len(grid)
    half = n // 2

    board = [[-1] * n for _ in range(n)]
    row_ones = [0] * n       
    col_ones = [0] * n       
    row_assigned = [0] * n   
    col_assigned = [0] * n   

    # --- FUNCIONES LOCALES DE COMPROBACIÓN (RESTRICCIONES) ---
    # Comprueba si la fila i aún puede alcanzar exactamente n/2 unos

    def ok_row(i):
        ones = row_ones[i]
        assigned = row_assigned[i]
        remaining = n - assigned

        if ones > half:
            return False
        if ones + remaining < half:
            return False
        if assigned == n and ones != half:
            return False
        return True
    
    def ok_col(j):
        ones = col_ones[j]
        assigned = col_assigned[j]
        remaining = n - assigned

        if ones > half:
            return False
        if ones + remaining < half:
            return False
        if assigned == n and ones != half:
            return False
        return True

    # Comprueba la restricción R2 (no triples consecutivos)
    def check_triples(i, j):
        v = board[i][j]
        if v == -1:
            return True

        # Triples en la fila
        for dj in (-2, -1, 0):
            j0 = j + dj
            if 0 <= j0 <= n - 3:
                a, b, c = board[i][j0], board[i][j0 + 1], board[i][j0 + 2]
                if a != -1 and a == b == c:
                    return False

        # Triples en la columna
        for di in (-2, -1, 0):
            i0 = i + di
            if 0 <= i0 <= n - 3:
                a, b, c = board[i0][j], board[i0 + 1][j], board[i0 + 2][j]
                if a != -1 and a == b == c:
                    return False

        return True

    # --- INICIALIZACIÓN CON LAS CELDAS PREFIJADAS (R3) ---
    for i in range(n):
        for j in range(n):
            c = grid[i][j]
            if c in ('X', 'O'): 
                v = 1 if c == 'X' else 0
                board[i][j] = v
                row_assigned[i] += 1
                col_assigned[j] += 1
                if v == 1:
                    row_ones[i] += 1
                    col_ones[j] += 1

                # Si ya viola las restricciones → sin soluciones
                if not ok_row(i) or not ok_col(j) or not check_triples(i, j):
                    return 0, None

    # --- Creamos la lista de variables libres (las '.') ---
    vars_pos = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == '.']

    sol_count = 0
    first_solution = None

    """------------------------------------------------------------
                FUNCION LOCAL: backtrack(idx)
    ------------------------------------------------------------
    Intenta asignar valores a partir de vars_pos[idx].
    Cada asignación comprueba inmediatamente:
       - si la fila puede seguir cumpliéndose
       - si la columna puede seguir cumpliéndose
       - si no se forman triples prohibidos
    Cuando idx == len(vars_pos), significa que el tablero está completo.
    ------------------------------------------------------------
    """
    def backtrack(idx):
        nonlocal sol_count, first_solution

        if idx == len(vars_pos):
            for i in range(n):
                if row_assigned[i] != n or row_ones[i] != half:
                    return
            for j in range(n):
                if col_assigned[j] != n or col_ones[j] != half:
                    return
            sol_count += 1

            # Guardar la primera solución para guardarla en el .out
            if first_solution is None:
                first_solution = [row[:] for row in board]
            return

        i, j = vars_pos[idx]

        # Probar O (0) y luego X (1)
        for v in (0, 1):
            board[i][j] = v
            row_assigned[i] += 1
            col_assigned[j] += 1
            if v == 1:
                row_ones[i] += 1
                col_ones[j] += 1

            # Poda: comprobaciones inmediatas
            if ok_row(i) and ok_col(j) and check_triples(i, j):
                backtrack(idx + 1)

            # Deshacer decisión (backtracking)
            if v == 1:
                row_ones[i] -= 1
                col_ones[j] -= 1
            row_assigned[i] -= 1
            col_assigned[j] -= 1
            board[i][j] = -1

    # Lanzar la búsqueda
    backtrack(0)

    # Si no hay soluciones
    if first_solution is None:
        return sol_count, None

    # Convertimos 0/1 a 'O'/'X' para imprimir
    sol_grid = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append('X' if first_solution[i][j] == 1 else 'O')
        sol_grid.append("".join(fila))

    return sol_count, sol_grid

"""
------------------------------------------------------------
            FUNCION PRINCIPAL (main)
------------------------------------------------------------
Maneja los argumentos:
python3 parte-1.py entrada.in salida.out
Muestra por pantalla la instancia y el número de soluciones,
y escribe en el fichero:
  - instancia original
  - solución (si existe)
------------------------------------------------------------
"""
def main():
    if len(sys.argv) != 3:
        print("Uso: ./parte-1.py fichero-entrada fichero-salida")
        sys.exit(1)

    fichero_entrada = sys.argv[1]
    fichero_salida = sys.argv[2]

    # --- Leer ---
    grid = leer_instancia(fichero_entrada)

    # --- Resolver ---
    num_soluciones, sol_grid = resolver_binairo(grid)

    # --- Mostrar en pantalla ---
    tablero_instancia = formatear_tablero(grid, mostrar_puntos_como_vacio=True)
    print(tablero_instancia, end="")
    print(f"{num_soluciones} soluciones encontradas")

    # --- Escribir salida ---
    with open(fichero_salida, "w", encoding="utf-8") as f:
        f.write(tablero_instancia)

        if sol_grid is not None:
            tablero_sol = formatear_tablero(sol_grid, mostrar_puntos_como_vacio=False)
            f.write(tablero_sol)


if __name__ == "__main__":
    main()
