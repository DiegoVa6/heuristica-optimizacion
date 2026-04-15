# Parte 2.2.2 — Minimización del impacto: coincidencias EN LA MISMA FRANJA
# z_iks = 1 si los autobuses i y k están en la misma franja s (en cualquier taller)

set I;                 # Autobuses {1..m}
set S;                 # Franjas {1..n}
set U;                 # Talleres {1..u}

param C{i in I, k in I} >= 0;     # Pasajeros comunes entre buses i,k (C[i,i]=0; suele ser simétrica)
param O{u in U, s in S} binary;   # Disponibilidad de franja s en taller u

var x{i in I, s in S, u in U} binary;                 # 1 si bus i -> (s,u)
var z{i in I, k in I, s in S: i < k} binary;          # 1 si buses i y k coinciden en la MISMA franja s

# Objetivo: minimizar pasajeros afectados por coincidencias de franja
minimize total_overlap:
    sum{i in I, k in I, s in S: i < k} C[i,k] * z[i,k,s];

# (1) Asignación única por autobús (exactamente una franja en un único taller)
s.t. assign_one{i in I}:
    sum{s in S, u in U} x[i,s,u] = 1;

# (2) Capacidad por (franja,taller): a lo sumo un bus
s.t. cap_one{s in S, u in U}:
    sum{i in I} x[i,s,u] <= 1;

# (3) Disponibilidad
s.t. availability{i in I, s in S, u in U}:
    x[i,s,u] <= O[u,s];

# (4) Definición de z: z_iks = AND(  sum_u x[i,s,u] , sum_u x[k,s,u]  )
s.t. z_le_i{i in I, k in I, s in S: i < k}:
    z[i,k,s] <= sum{u in U} x[i,s,u];

s.t. z_le_k{i in I, k in I, s in S: i < k}:
    z[i,k,s] <= sum{u in U} x[k,s,u];

s.t. z_ge_both{i in I, k in I, s in S: i < k}:
    z[i,k,s] >= sum{u in U} x[i,s,u] + sum{u in U} x[k,s,u] - 1;

end;
