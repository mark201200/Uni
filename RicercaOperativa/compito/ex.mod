set 	VariabiliMinZero;
set 	VariabiliMaggZero;
set 	Variabili;
set 	VincoliMinori;
set 	VincoliMaggiori;
set 	Vincoli;

param alpha;

param	b{Vincoli};
param 	c{Variabili};
param 	a{Vincoli, Variabili};

var 	x{Variabili};

minimize z: sum{j in Variabili} c[j]*x[j];

s.t. v0 {i in VincoliMinori}:	sum{j in Variabili} a[i,j]*x[j] <= b[i];
s.t. v1 {i in VincoliMaggiori}: sum{j in Variabili} a[i,j]*x[j] >= b[i] + alpha;

s.t. v3 {j in VariabiliMinZero}: 	x[j] <= 0;
s.t. v4 {j in VariabiliMaggZero}: 	x[j] >= 0;