# Parte 2.1 – Minimización del impacto de averías
# Modelo general compatible con GLPK 5.0

set I;  # Autobuses
set S;  # Franjas disponibles

param kd;  # coste €/km si se asigna
param kp;  # penalización €/pasajero si NO se asigna
param d{i in I};  # distancia (km) de cada autobús al taller
param p{i in I};  # pasajeros afectados

var x{i in I, s in S}, binary;  # 1 si el autobús i se asigna a la franja s

# Función objetivo: minimizar el coste total
# Coste = sum(kd*d[i] * x[i,s]) + sum(kp*p[i] * (1 - sum(x[i,s])))
minimize total_cost:
    sum{i in I, s in S} kd * d[i] * x[i,s]
  + sum{i in I} kp * p[i] * (1 - sum{s in S} x[i,s]);

# Cada autobús puede ocupar a lo sumo una franja
s.t. at_most_one{i in I}:
    sum{s in S} x[i,s] <= 1;

# Cada franja puede asignarse a lo sumo a un autobús
s.t. cap{s in S}:
    sum{i in I} x[i,s] <= 1;

end;
