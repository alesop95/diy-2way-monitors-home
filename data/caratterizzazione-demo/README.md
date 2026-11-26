# Cinque curve sintetiche per il controllo dei file

Questi dati sono costruiti, non descrivono un driver o una stanza. La griglia è geomspace(50,24000,241) in hertz. Posto x=log2(f/500), i moduli relativi sono:

| Curva | Modulo in dB |
|---|---|
| axial | 0.25 sin(x) |
| h_neg10 | -1 + 0.2 sin(x) |
| h_pos10 | -1.2 + 0.2 cos(x) |
| v_neg10 | -1 + 0.25 cos(x) |
| v_pos10 | -1.2 + 0.15 sin(x) - 2.2 exp(-0.5 (log2(f/2600)/0.4)^2) |

La fase è -360 f 0.0002 gradi, cioè il solo ritardo sintetico di 0,2 ms, per tutte le curve. Non è stata ricavata dai moduli né imposta come fase minima di un modello fisico. I dati sono serializzati con dodici cifre significative.

Il bersaglio è relativo allo stesso riferimento 0 dB, da 60 a 20000 Hz entro ±2 dB. La quinta curva contiene volutamente una valle fuori bersaglio; le altre quattro devono risultare entro i limiti ai campioni controllati. La coerenza non è disponibile in questi FRD; non viene inventata. Banda valida e direzioni sono dichiarazioni della fixture, non evidenze sperimentali.

Il modulo di progetto produce CSV, FRD con fase solo quando presente, copia dei byte originali e manifesto delle impronte. La qualifica hardware rimane falsa. Uso e limiti nella [procedura](../../docs/65-caratterizzazione-aperta-e-dati-di-misura.md).
