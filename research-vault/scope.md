# Scope della ricerca

> Prodotto dalla skill `research-scoping` il 2026-10-02 (MS-185). È il documento che `literature-search`, `citation-tracker` e le altre skill del pacchetto `academic-researcher` leggono per sapere come operare in questo progetto, invece di riproporre le stesse domande. Tracciato.

## Domanda di ricerca

Come si progetta, si realizza e si verifica una coppia di monitor da studio a due vie attivi, con il crossover in un processore digitale, ottimizzati per un punto di ascolto noto in una stanza domestica non trattabile, partendo dalla stanza e non dal diffusore (ADR-002, ADR-033), e con quale fondamento teorico ogni scelta si dimostra.

Il progetto diventa una tesi (ADR-034): la letteratura serve a fondare le derivazioni matematiche dei capitoli e delle appendici, non soltanto a citare lo stato dell'arte.

## Filoni

Sette filoni, ciascuno con il proprio lotto di materiale locale nel piano `_notes/fonti-studio/piano-lotti.md`, che è locale per ADR-028.

Il primo è il modello dell'altoparlante e del cabinet: parametri di Thiele e Small, cassa chiusa e ventilata, induttanza della bobina, diffrazione del pannello. Il secondo è il crossover digitale: Linkwitz-Riley e famiglie a fase lineare, FIR e IIR, allineamento temporale dei centri acustici, lobi verticali. Il terzo è la correzione nella stanza: equalizzazione dei modi, inversione della risposta, livellamento in frazione di ottava, robustezza fuori dal punto di misura. Il quarto è la percezione: udibilità della fase e del ritardo di gruppo, preferenza di ascolto e sue misure oggettive, campo riverberante in una stanza piccola. Il quinto è la misura: sweep esponenziale, sequenze di massima lunghezza, misure quasi anecoiche, campo vicino. Il sesto è l'amplificazione: classe D e alimentazione per un canale per via. Il settimo è l'implementazione: strutture dei biquad, quantizzazione dei coefficienti, frequenza di campionamento.

## Risposte alle domande di gate

| Domanda | Risposta | Data |
|---|---|---|
| Dominio disciplinare | Elettroacustica, acustica degli ambienti, elaborazione numerica del segnale audio, psicoacustica; database privilegiati AES E-Library, IEEE Xplore, ASA (JASA) e fonti open access | 2026-10-02 |
| Tipo di revisione | Narrativa e mirata al progetto, non sistematica: ogni fonte entra perché fonda una derivazione o una scelta | 2026-10-02 |
| Orizzonte temporale | Nessun limite per i lavori fondativi (dal 1950 in poi); per lo stato dell'arte sulla correzione digitale, preferenza agli ultimi vent'anni | 2026-10-02 |
| Lingue | Inglese e italiano | 2026-10-02 |
| Libreria bibliografica | Da zero, solo `.bib`: `research-vault/bibliography.bib`, validato a mano in JabRef prima di ogni consegna; nessun server MCP, coerente con ADR-031 | 2026-10-02 |
| Formato di uscita | LaTeX, con `biber`, nel progetto `report/` che diventa la tesi | 2026-10-02 |
| Autonomia | Propongo, l'utente conferma: ogni lotto di candidati si presenta e si procede solo dopo il sì | 2026-10-02 |
| Abbonamenti istituzionali | AES E-Library, IEEE Xplore, ASA (JASA), più l'open access | 2026-10-02 |
| Dove stanno i PDF | `research-vault/papers/`, ignorata da git perché molti testi sono sotto diritti dell'editore e il repository è pubblico; li scarica l'utente con i propri accessi | 2026-10-02 |

## Convenzione per i PDF

Il nome del file è la chiave bibliografica della voce, per esempio `mueller2001transfer.pdf`, così che il legame fra il PDF, la voce del `.bib` e la riga di `tracked-sources.md` sia meccanico e non affidato alla memoria. Una fonte passa da da verificare a verificata soltanto dopo che il suo PDF, o la pagina dell'editore con il DOI, è stato letto, secondo la norma `.claude/skills/citation-tracker/RIFERIMENTO.md`.
