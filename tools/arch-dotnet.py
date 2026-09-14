"""Dice l'architettura reale di un eseguibile Windows, distinguendo i .NET dai nativi.

Perche' esiste. Per un programma nativo l'architettura si legge dall'intestazione PE e
`file` basta: `PE32` significa 32 bit e `PE32+` significa 64. Per un assembly .NET quella
lettura e' insufficiente e induce in errore, perche' un assembly compilato *AnyCPU* e'
anch'esso `PE32` e gira a 64 bit su una macchina a 64 bit. Chi si fermasse a `file`
concluderebbe che un programma a 64 bit sia a 32, e su questo progetto quella conclusione
avrebbe portato a smontare un prefix corretto: e' il caso di VituixCAD, documentato in
MS-101 del registro dei microstep.

Che cosa legge. L'intestazione del runtime CLI, che e' la voce 14 della tabella delle
directory del PE. Se manca, il file e' nativo e l'architettura e' quella dichiarata dal
formato. Se c'e', decidono tre flag: ILONLY, 32BITREQUIRED e 32BITPREFERRED. Se
32BITREQUIRED e' spento l'assembly e' AnyCPU e gira alla larghezza della macchina; se e'
acceso ed e' spento 32BITPREFERRED l'assembly e' x86 e gira sempre a 32 bit; se sono
accesi entrambi e' AnyCPU con preferenza per i 32 bit, che gira a 32 bit dove puo'.

Uso:
    python tools/arch-dotnet.py <percorso di un .exe o .dll>

Esce con codice 0 se ha potuto decidere, 2 se il file non e' un PE valido. Non apre
connessioni, non scrive nulla, e legge il file una volta sola.
"""
import struct
import sys


def leggi(percorso):
    with open(percorso, "rb") as f:
        return f.read()


def analizza(percorso):
    d = leggi(percorso)
    if len(d) < 0x40 or d[:2] != b"MZ":
        return None, "non e' un eseguibile Windows: manca la firma MZ"

    pe = struct.unpack_from("<I", d, 0x3C)[0]
    if len(d) < pe + 24 or d[pe:pe + 4] != b"PE\x00\x00":
        return None, "non e' un eseguibile Windows: manca la firma PE"

    numero_sezioni = struct.unpack_from("<H", d, pe + 6)[0]
    dimensione_opzionale = struct.unpack_from("<H", d, pe + 20)[0]
    opzionale = pe + 24
    magic = struct.unpack_from("<H", d, opzionale)[0]
    formato = "PE32+" if magic == 0x20B else "PE32"

    base_directory = opzionale + (0x70 if magic == 0x20B else 0x60)
    rva_cli = struct.unpack_from("<I", d, base_directory + 14 * 8)[0]
    if rva_cli == 0:
        nativo = "64 bit" if magic == 0x20B else "32 bit"
        return {"formato": formato, "dotnet": False, "architettura": nativo}, None

    sezioni = pe + 24 + dimensione_opzionale
    offset_cli = None
    for i in range(numero_sezioni):
        s = sezioni + i * 40
        va = struct.unpack_from("<I", d, s + 12)[0]
        dimensione = struct.unpack_from("<I", d, s + 16)[0]
        puntatore = struct.unpack_from("<I", d, s + 20)[0]
        if va <= rva_cli < va + dimensione:
            offset_cli = puntatore + (rva_cli - va)
            break
    if offset_cli is None:
        return None, "intestazione CLI dichiarata ma non trovata in alcuna sezione"

    flag = struct.unpack_from("<I", d, offset_cli + 16)[0]
    richiede32 = bool(flag & 0x2)
    preferisce32 = bool(flag & 0x20000)
    if not richiede32:
        arch = "AnyCPU, gira a 64 bit su una macchina a 64 bit"
    elif preferisce32:
        arch = "AnyCPU con preferenza 32 bit, gira a 32 bit dove puo'"
    else:
        arch = "x86, gira sempre a 32 bit"
    return {"formato": formato, "dotnet": True, "flag": flag,
            "ilonly": bool(flag & 0x1), "richiede32": richiede32,
            "preferisce32": preferisce32, "architettura": arch}, None


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[0])
        print("uso: python tools/arch-dotnet.py <percorso>")
        return 2
    esito, errore = analizza(sys.argv[1])
    if errore:
        print("%s: %s" % (sys.argv[1], errore))
        return 2
    print("file:                  %s" % sys.argv[1])
    print("formato PE:            %s" % esito["formato"])
    if not esito["dotnet"]:
        print("intestazione CLI:      assente, eseguibile nativo")
        print("architettura reale:    %s" % esito["architettura"])
        return 0
    print("intestazione CLI:      presente, assembly .NET")
    print("flag CLI:              0x%08X" % esito["flag"])
    print("  ILONLY:              %s" % esito["ilonly"])
    print("  32BITREQUIRED:       %s" % esito["richiede32"])
    print("  32BITPREFERRED:      %s" % esito["preferisce32"])
    print("architettura reale:    %s" % esito["architettura"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
