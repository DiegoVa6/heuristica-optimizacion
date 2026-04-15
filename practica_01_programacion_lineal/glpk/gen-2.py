#!/usr/bin/env python3
# Parte 2.2.2 – Maximización de la satisfacción (min impacto por coincidencias en MISMA FRANJA)
# Lee: <n m u>, matriz C (m x m) y matriz O (u x n)
# Genera .dat, ejecuta GLPK y muestra:
#   <valor_objetivo> <num_variables> <num_restricciones>
#   bus i -> taller u, franja s

import sys
import subprocess
import itertools
import re

def leer_entrada(path):
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    try:
        n, m, u = map(int, lines[0].split())
    except Exception:
        raise ValueError("Primera línea debe ser: <n> <m> <u>")

    C, idx = [], 1
    for _ in range(m):
        fila = list(map(int, lines[idx].split()))
        if len(fila) != m:
            raise ValueError("Fila de C con longitud distinta de m")
        C.append(fila); idx += 1

    O = []
    for _ in range(u):
        fila = list(map(int, lines[idx].split()))
        if len(fila) != n:
            raise ValueError("Fila de O con longitud distinta de n")
        O.append(fila); idx += 1

    return n, m, u, C, O

def escribir_dat(path, n, m, u, C, O):
    with open(path, "w", encoding="utf-8") as f:
        f.write("set I := " + " ".join(str(i) for i in range(1, m+1)) + ";\n")
        f.write("set S := " + " ".join(str(s) for s in range(1, n+1)) + ";\n")
        f.write("set U := " + " ".join(str(t) for t in range(1, u+1)) + ";\n")

        f.write("param C : " + " ".join(str(k) for k in range(1, m+1)) + " :=\n")
        for i in range(1, m+1):
            f.write(f"{i} " + " ".join(str(C[i-1][k-1]) for k in range(1, m+1)) + "\n")
        f.write(";\n")

        # O[u,s] → filas talleres (U) x columnas franjas (S)
        f.write("param O : " + " ".join(str(s) for s in range(1, n+1)) + " :=\n")
        for t in range(1, u+1):
            f.write(f"{t} " + " ".join(str(O[t-1][s-1]) for s in range(1, n+1)) + "\n")
        f.write(";\nend;\n")

def ejecutar_glpk(mod, dat, sol):
    cmd = ["glpsol", "-m", mod, "-d", dat, "-o", sol]  # sin --quiet (GLPK 5.0)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stdout + res.stderr)
        sys.exit(res.returncode)

def leer_asignaciones(path_sol):
    # Busca líneas tipo: x[ i , s , u ] * 1
    asig = {}
    pat = re.compile(r"x\[(\d+),(\d+),(\d+)\]\s+(?:\*\s+)?1\b")
    with open(path_sol, encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = pat.search(line)
            if m:
                i, s, u = map(int, m.groups())
                asig[i] = (s, u)
    return asig

def valor_objetivo(C, asign):
    # Suma C[i-1][k-1] por cada par (i,k) que comparte la MISMA franja s (independientemente del taller)
    total = 0
    buses = sorted(asign.keys())
    for i, k in itertools.combinations(buses, 2):
        s_i, _ = asign[i]
        s_k, _ = asign[k]
        if s_i == s_k:
            total += C[i-1][k-1]
    return total

def contadores(n, m, u):
    num_x = m * n * u
    num_z = (m * (m - 1) // 2) * n
    num_vars = num_x + num_z

    # m (assign_one) + n*u (cap_one) + m*n*u (availability) + 3*comb(m,2)*n (z-links)
    num_cons = m + (n * u) + (m * n * u) + 3 * (m * (m - 1) // 2) * n
    return num_vars, num_cons

def main():
    if len(sys.argv) < 3:
        print("Uso: ./gen-2.py <fichero-entrada.in> <fichero-salida.dat>")
        sys.exit(1)

    ruta_in, ruta_dat = sys.argv[1], sys.argv[2]
    ruta_mod = "parte-2-2.mod"
    ruta_sol = "solution_2_2.txt"

    n, m, u, C, O = leer_entrada(ruta_in)
    escribir_dat(ruta_dat, n, m, u, C, O)
    ejecutar_glpk(ruta_mod, ruta_dat, ruta_sol)

    asign = leer_asignaciones(ruta_sol)
    if len(asign) != m:
        sys.stderr.write("Aviso: no se han encontrado todas las asignaciones en la salida de GLPK.\n")

    z = valor_objetivo(C, asign)
    num_vars, num_cons = contadores(n, m, u)

    print(f"{z} {num_vars} {num_cons}")
    for i in range(1, m+1):
        if i in asign:
            s, t = asign[i]
            print(f"bus {i} -> taller {t}, franja {s}")
        else:
            print(f"bus {i} -> SIN_ASIGNACION")

if __name__ == "__main__":
    main()
