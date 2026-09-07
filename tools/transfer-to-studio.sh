#!/usr/bin/env bash
# Trasferisce i materiali pesanti del progetto sulla macchina Ubuntu Studio.
# Non cancella nulla sull'origine: la rimozione resta una decisione manuale,
# da prendere dopo che il confronto delle impronte SHA-256 e' andato a buon fine.
#
# Uso:
#   bash tools/transfer-to-studio.sh --verifica    solo controlli preliminari
#   bash tools/transfer-to-studio.sh               trasferimento completo
#
# L'host e la destinazione si possono sovrascrivere da ambiente:
#   STUDIO_HOST=alesop95@192.168.10.204 STUDIO_BASE=~/electroacoustics bash tools/transfer-to-studio.sh

set -euo pipefail

STUDIO_HOST="${STUDIO_HOST:-alesop95@192.168.10.204}"
STUDIO_BASE="${STUDIO_BASE:-electroacoustics}"

# Chiave dedicata all'host. Serve perche' su questa postazione non esiste una voce in
# ~/.ssh/config per la macchina, quindi ssh proverebbe solo i nomi di chiave predefiniti,
# che non esistono: le chiavi si chiamano _personal, _corp e _studio. Si sovrascrive con
# STUDIO_KEY, oppure si svuota se si e' aggiunta una voce di configurazione con un alias.
STUDIO_KEY="${STUDIO_KEY-$HOME/.ssh/id_ed25519_studio}"
if [ -n "$STUDIO_KEY" ] && [ -f "$STUDIO_KEY" ]; then
  SSH_OPZ=(-o IdentitiesOnly=yes -i "$STUDIO_KEY")
else
  SSH_OPZ=()
fi
SOLO_VERIFICA=0
SOLO_IMPRONTE=0
[ "${1:-}" = "--verifica" ] && SOLO_VERIFICA=1
[ "${1:-}" = "--impronte" ] && SOLO_IMPRONTE=1

RADICE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MATERIALI="$RADICE/Akabak + VACS"

# Mappa origine -> sottocartella di destinazione. Una riga per file.
MAPPA=(
  "AKABAK_Pro_v324b126.exe|installers"
  "VACS_64_v213b33.exe|installers"
  "VACS_32_v213b33.exe|installers"
  "AKABAK-Examples.zip|examples"
  "Gmail - Akabak 3 license.pdf|licenze"
  "update AKABAK (Joerg Panzer)_2026-03-19_10-18-32.jpg|licenze"
  "randteam.url|licenze"
)
DOCX="_notes/full_electroacoustics.docx"

# Corredo "Progetto stanza": alberi di cartelle, non file singoli. Sono il sottoinsieme
# legittimo e utile del corredo sul Desktop della postazione, selezionato in
# docs/10-ambiente/wine-corredo-progetto-stanza.md. Le voci con protezione rimossa non
# sono qui di proposito, e nemmeno EASE Focus 3.0.18, superata dalla 3.1.260.
CORREDO="${CORREDO:-/c/Users/Utente/Desktop/Progetto stanza (software)}"
MAPPA_DIR=(
  "DIY Loudspeaker Pack Softwares/Arta|progetto-stanza/diy"
  "Room acoustics/EEASE Focus/EASE_Focus_v3.1.260|progetto-stanza/room"
  "Room acoustics/EEASE Focus/EASE_Focus_3_GLL_Database_2016_10_11|progetto-stanza/room"
  "Room acoustics/Ramsete27b - room acoustics|progetto-stanza/room"
  "Room acoustics/EEASE Focus/EASE_Focus_v3.0.18|progetto-stanza/archivio"
)
MAPPA_CORREDO_FILE=(
  "DIY Loudspeaker Pack Softwares/VituixCAD_setup.exe|progetto-stanza/diy"
)

nota()  { printf '  %s\n' "$*"; }
titolo(){ printf '\n== %s ==\n' "$*"; }
errore(){ printf 'ERRORE: %s\n' "$*" >&2; }

titolo "Controlli preliminari"

mancanti=0
for strumento in ssh sha256sum; do
  if command -v "$strumento" >/dev/null 2>&1; then
    nota "$strumento presente"
  else
    errore "$strumento non trovato sul PATH"
    mancanti=1
  fi
done
[ "$mancanti" -eq 0 ] || { errore "installare gli strumenti mancanti e rilanciare"; exit 1; }

# rsync e' preferibile perche' riprende un trasferimento interrotto, ma su Git Bash
# per Windows non c'e'. In sua assenza si usa scp, che copia sempre da capo.
if command -v rsync >/dev/null 2>&1; then
  COPIA=rsync
  nota "rsync presente: trasferimento riprendibile"
else
  COPIA=scp
  if command -v scp >/dev/null 2>&1; then
    nota "rsync assente, si usa scp: un'interruzione richiede di ricopiare il file da capo"
  else
    errore "ne' rsync ne' scp trovati sul PATH"
    exit 1
  fi
fi

if [ ! -d "$MATERIALI" ]; then
  errore "cartella dei materiali non trovata: $MATERIALI"
  exit 1
fi
nota "cartella dei materiali trovata"

assenti=0
for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  if [ ! -f "$MATERIALI/$nome" ]; then
    errore "file di origine assente: $nome"
    assenti=1
  fi
done
[ -f "$RADICE/$DOCX" ] || nota "avviso: $DOCX non presente, verra' saltato"

if [ -d "$CORREDO" ]; then
  nota "corredo Progetto stanza trovato"
  for voce in "${MAPPA_DIR[@]}" "${MAPPA_CORREDO_FILE[@]}"; do
    nome="${voce%%|*}"
    [ -e "$CORREDO/$nome" ] || { errore "voce del corredo assente: $nome"; assenti=1; }
  done
else
  nota "avviso: corredo non trovato in $CORREDO, verra' saltato interamente"
fi
[ "$assenti" -eq 0 ] || { errore "manifest e disco non coincidono, controllare prima di trasferire"; exit 1; }
nota "tutti i file del manifest sono presenti"

byte_totali=0
for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  byte_totali=$(( byte_totali + $(stat -c%s "$MATERIALI/$nome") ))
done
[ -f "$RADICE/$DOCX" ] && byte_totali=$(( byte_totali + $(stat -c%s "$RADICE/$DOCX") ))
voci_corredo=0
if [ -d "$CORREDO" ]; then
  for voce in "${MAPPA_DIR[@]}" "${MAPPA_CORREDO_FILE[@]}"; do
    nome="${voce%%|*}"
    if [ -e "$CORREDO/$nome" ]; then
      byte_totali=$(( byte_totali + $(du -sb "$CORREDO/$nome" | cut -f1) ))
      voci_corredo=$(( voci_corredo + 1 ))
    fi
  done
fi
nota "da trasferire: $(( byte_totali / 1048576 )) MiB, $(( ${#MAPPA[@]} + 1 )) file piu' $voci_corredo voci del corredo"

titolo "Raggiungibilita' dell'host"

if ssh "${SSH_OPZ[@]}" -o BatchMode=yes -o ConnectTimeout=10 "$STUDIO_HOST" "echo raggiungibile" >/dev/null 2>&1; then
  nota "$STUDIO_HOST risponde"
else
  errore "$STUDIO_HOST non risponde"
  errore "verificare che la macchina sia accesa, sullo stesso segmento di rete, e con sshd attivo"
  errore "diagnostica: ping dell'indirizzo, presenza in tabella ARP, ascolto sulla porta 22"
  exit 2
fi

spazio_kib="$(ssh "${SSH_OPZ[@]}" -o BatchMode=yes "$STUDIO_HOST" "df -Pk \"\$HOME\" | awk 'NR==2 {print \$4}'")"
nota "spazio disponibile in home sulla destinazione: $(( spazio_kib / 1024 )) MiB"
if [ "$(( spazio_kib * 1024 ))" -lt "$(( byte_totali * 2 ))" ]; then
  errore "spazio insufficiente: serve almeno il doppio dei byte da trasferire per lavorare con margine"
  exit 3
fi

if [ "$SOLO_VERIFICA" -eq 1 ]; then
  titolo "Solo verifica: nessun file copiato"
  exit 0
fi

if [ "$SOLO_IMPRONTE" -eq 0 ]; then
titolo "Creazione dell'albero di destinazione"
ssh "${SSH_OPZ[@]}" -o BatchMode=yes "$STUDIO_HOST" "mkdir -p \"\$HOME/$STUDIO_BASE\"/{installers,examples,licenze,sorgenti,progetto-stanza/diy,progetto-stanza/room,progetto-stanza/archivio}"
nota "albero creato sotto \$HOME/$STUDIO_BASE"

# Nota sui percorsi remoti: qui non si usa "$HOME/..." ma un percorso relativo, perche'
# scp da OpenSSH 9 in avanti trasferisce via SFTP, che non esegue una shell sul lato
# remoto e quindi non espande le variabili: "$HOME" arriverebbe letterale e la copia
# fallirebbe con "dest open: No such file or directory". Un percorso relativo viene
# risolto dalla home dell'utente, che e' la directory iniziale di una sessione SFTP.
copia_uno() {
  origine="$1"
  sotto="$2"
  if [ "$COPIA" = rsync ]; then
    rsync -e "ssh ${SSH_OPZ[*]}" -h --partial --progress --times "$origine" "$STUDIO_HOST:$STUDIO_BASE/$sotto/"
  else
    scp "${SSH_OPZ[@]}" -p "$origine" "$STUDIO_HOST:$STUDIO_BASE/$sotto/"
  fi || { errore "copia fallita: $(basename "$origine")"; return 1; }
}

titolo "Trasferimento con $COPIA"
for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  sotto="${voce##*|}"
  nota "$nome -> $sotto/"
  copia_uno "$MATERIALI/$nome" "$sotto"
done
if [ -f "$RADICE/$DOCX" ]; then
  nota "$(basename "$DOCX") -> sorgenti/"
  copia_uno "$RADICE/$DOCX" "sorgenti"
fi

copia_albero() {
  origine="$1"
  sotto="$2"
  if [ "$COPIA" = rsync ]; then
    rsync -e "ssh ${SSH_OPZ[*]}" -a -h --partial --progress "$origine" "$STUDIO_HOST:$STUDIO_BASE/$sotto/"
  else
    scp "${SSH_OPZ[@]}" -p -r "$origine" "$STUDIO_HOST:$STUDIO_BASE/$sotto/"
  fi || { errore "copia dell'albero fallita: $(basename "$origine")"; return 1; }
}

if [ -d "$CORREDO" ]; then
  titolo "Trasferimento del corredo Progetto stanza"
  for voce in "${MAPPA_CORREDO_FILE[@]}"; do
    nome="${voce%%|*}"; sotto="${voce##*|}"
    [ -e "$CORREDO/$nome" ] || continue
    nota "$(basename "$nome") -> $sotto/"
    copia_uno "$CORREDO/$nome" "$sotto"
  done
  for voce in "${MAPPA_DIR[@]}"; do
    nome="${voce%%|*}"; sotto="${voce##*|}"
    [ -e "$CORREDO/$nome" ] || continue
    nota "$(basename "$nome")/ -> $sotto/"
    copia_albero "$CORREDO/$nome" "$sotto"
  done
fi

fi

titolo "Verifica delle impronte: i file del manifest"

# I file del manifest sono piatti, uno per sottocartella di destinazione: si confronta
# l'elenco per nome di file. Il corredo, che e' fatto di alberi, si verifica dopo, con
# un confronto separato per ciascuna voce, perche' un solo elenco piatto non basterebbe.

atteso="$(mktemp)"
ottenuto="$(mktemp)"
trap 'rm -f "$atteso" "$ottenuto"' EXIT

for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  sha256sum "$MATERIALI/$nome" | awk -v n="$nome" '{print $1"  "n}'
done | sed 's/ \*/  /' > "$atteso"
if [ -f "$RADICE/$DOCX" ]; then
  sha256sum "$RADICE/$DOCX" | awk -v n="$(basename "$DOCX")" '{print $1"  "n}' >> "$atteso"
fi
sort -k2 -o "$atteso" "$atteso"

ssh "${SSH_OPZ[@]}" -o BatchMode=yes "$STUDIO_HOST" "cd \"\$HOME/$STUDIO_BASE\" && find installers examples licenze sorgenti -maxdepth 1 -type f -exec sha256sum {} + | sed 's#  [^/]*/#  #'" | sort -k2 > "$ottenuto"

differenze=0
if diff -u "$atteso" "$ottenuto"; then
  nota "gli 8 file del manifest coincidono"
else
  errore "le impronte dei file del manifest non coincidono"
  differenze=1
fi

if [ -d "$CORREDO" ]; then
  titolo "Verifica delle impronte: il corredo Progetto stanza"
  for voce in "${MAPPA_CORREDO_FILE[@]}" "${MAPPA_DIR[@]}"; do
    nome="${voce%%|*}"
    sotto="${voce##*|}"
    base="$(basename "$nome")"
    [ -e "$CORREDO/$nome" ] || continue

    loc="$(mktemp)"
    rem="$(mktemp)"

    if [ -f "$CORREDO/$nome" ]; then
      ( cd "$(dirname "$CORREDO/$nome")" && sha256sum "$base" ) | sed 's/ \*/  /' | sort -k2 > "$loc"
      ssh "${SSH_OPZ[@]}" -o BatchMode=yes "$STUDIO_HOST" "cd \"\$HOME/$STUDIO_BASE/$sotto\" && sha256sum \"$base\"" 2>/dev/null | sort -k2 > "$rem"
    else
      ( cd "$CORREDO/$nome" && find . -type f -exec sha256sum {} + ) | sed 's/ \*/  /' | sort -k2 > "$loc"
      ssh "${SSH_OPZ[@]}" -o BatchMode=yes "$STUDIO_HOST" "cd \"\$HOME/$STUDIO_BASE/$sotto/$base\" && find . -type f -exec sha256sum {} +" 2>/dev/null | sort -k2 > "$rem"
    fi

    n_loc="$(wc -l < "$loc")"
    n_rem="$(wc -l < "$rem")"
    if diff -q "$loc" "$rem" >/dev/null 2>&1; then
      nota "ok $base: $n_loc file, impronte identiche"
    else
      errore "$base: origine $n_loc file, destinazione $n_rem file, impronte diverse"
      diff -u "$loc" "$rem" | head -20
      differenze=1
    fi
    rm -f "$loc" "$rem"
  done
fi

if [ "$differenze" -eq 0 ]; then
  titolo "Trasferimento verificato: tutte le impronte coincidono"
  nota "la rimozione dei file dall'origine resta manuale e deliberata"
  nota "sblocca la verifica di PA-001: python tools/check-pending-actions.py"
else
  errore "verifica non superata: non rimuovere nulla dall'origine"
  exit 4
fi
