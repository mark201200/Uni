set VariabiliMinZero;
set VariabiliMaggZero;
set Variabili;
set VincoliMinZero;
set VincoliMagZero;
set Vincoli;

param b{Vincoli};
param c{Variabili};
param a{Vincoli, Variabili};

var x{Variabili};

minimize z: sum{j in Variabili} c[j]*x[j];

s.t. v0 {i in VincoliMinZero}: sum{j in Variabili} a[i,j]*x[j] <= b[i];
s.t. v1 {i in VincoliMagZero}: sum{j in Variabili} a[i,j]*x[j] >= b[i];
s.t. v2 {j in VariabiliMinZero}: x[j] <= 0;
s.t. v3 {j in VariabiliMaggZero}: x[j] >= 0;