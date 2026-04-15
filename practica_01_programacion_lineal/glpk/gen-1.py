#!/usr/bin/env python3
# Parte 2.1 – Minimización del impacto de averías
# Script simplificado tipo tutorial GLPK

import sys
import subprocess
import re

def leer_entrada(path):
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    n, m = map(int, lines[0].split())
    kd, kp = map(float, lines[1].split())
    d = list(map(float, lines[2].split()))
    p = list(map(float, lines[3].split()))
    if len(d) != m or len(p) != m:
        raise ValueError("Las longitudes de d o p no coinciden con m")
    return n, m, kd, kp, d, p

def escribir_dat(path, n, m, kd, kp, d, p):
    with open(path, "w", encoding="utf-8") as f:
        f.write("set I := " + " ".join(map(str, range(1, m+1))) + ";\n")
        f.write("set S := " + " ".join(map(str, range(1, n+1))) + ";\n")
        f.write(f"param kd := {kd};\nparam kp := {kp};\n")
        f.write("param d := " + " ".join(f"[{i}] {d[i-1]}" for i in range(1, m+1)) + ";\n")
        f.write("param p := " + " ".join(f"[{i}] {p[i-1]}" for i in range(1, m+1)) + ";\nend;\n")

def ejecutar_glpk(mod, dat, sol):
    cmd = ["glpsol", "-m", mod, "-d", dat, "-o", sol]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout + result.stderr)
        sys.exit(result.returncode)

def leer_sol(path):
    asign = {}
    pat = re.compile(r'x\[(\d+),(\d+)\]\s+\*\s+1')
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = pat.search(line)
            if m:
                i, s = map(int, m.groups())
                asign[i] = s
    return asign

def calcular_coste(asig, kd, kp, d, p, n, m):
    total = 0
    for i in range(1, m+1):
        if i in asig:
            total += kd * d[i-1]
        else:
            total += kp * p[i-1]
    return total

def main():
    if len(sys.argv) < 3:
        print("Uso: ./gen-1.py entrada.in salida.dat")
        sys.exit(1)

    ruta_in, ruta_dat = sys.argv[1], sys.argv[2]
    ruta_mod = "parte-2-1.mod"
    ruta_sol = "solution.txt"

    n, m, kd, kp, d, p = leer_entrada(ruta_in)
    escribir_dat(ruta_dat, n, m, kd, kp, d, p)
    ejecutar_glpk(ruta_mod, ruta_dat, ruta_sol)
    asign = leer_sol(ruta_sol)

    total = calcular_coste(asign, kd, kp, d, p, n, m)
    print(f"{total:.6f} {m*n} {m+n}")
    for i in range(1, m+1):
        if i in asign:
            print(f"bus {i} -> franja {asign[i]}")
        else:
            print(f"bus {i} -> SIN_ASIGNACION")

if __name__ == "__main__":
    main()
