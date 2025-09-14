# PRD - Mappa Flotilla

## Obiettivo

Creare una mappa online per visualizzare l'ultima posizione dei vascelli della Flotilla con funzionalità avanzate di interazione e controllo.

## Requisiti Funzionali

1.  **Fonte Dati**:
    *   I dati sui vascelli devono essere estratti in tempo reale dalla seguente fonte JSON: `https://flotilla-orpin.vercel.app/api/vessels`
    *   Timestamp di ultimo aggiornamento visualizzato nel controllo Source

2.  **Visualizzazione Mappa**:
    *   Tutta la visualizzazione deve essere realizzata con **MapLibre GL JS** (no Leaflet, no Folium, no Python)
    *   Ogni vascello deve essere rappresentato da un marker sulla mappa
    *   La posizione del marker deve corrispondere all'ultima posizione geografica registrata del vascello
    *   **Clustering intelligente**: I marker devono essere raggruppati in cluster quando la mappa è zoomata out
    *   **Zoom automatico**: La mappa deve adattarsi automaticamente per mostrare tutti i vascelli all'apertura

3.  **Interazione Popup**:
    *   Al click su un marker, deve comparire un popup che mostra:
        - Nome del vascello
        - Timestamp dell'ultimo aggiornamento (formato leggibile)
        - Status del vascello (es. "sailing")
        - Tipo di imbarcazione (es. "vessel")
    *   I popup devono attivarsi solo al click (non al mouseover)
    *   I popup devono rimanere aperti finché non vengono chiusi manualmente

4.  **Lista Vascelli Interattiva**:
    *   Bottone "Vessel List" per aprire una modale con lista completa dei vascelli
    *   Lista ordinata alfabeticamente per nome
    *   Campo di ricerca per filtrare i vascelli in tempo reale
    *   **Click su vascello**: zoom automatico alla posizione + apertura popup automatica
    *   Chiusura modale al click esterno o su pulsante X

5.  **Controlli Mappa Avanzati**:
    *   **Zoom controls**: Pulsanti + e - standard
    *   **Zoom to Fit**: Bottone per adattare la vista a tutti i vascelli
    *   **MiniMap**: Mini-mappa di navigazione nell'angolo
    *   **Measure Control**: Strumento per misurare distanze sulla mappa
    *   **Source Link**: Link alla fonte originale con timestamp aggiornamento

6.  **Gestione URL e Stato**:
    *   **Hash URL**: Salvataggio automatico di zoom e posizione nell'URL
    *   **Bookmark**: Possibilità di condividere link con posizione specifica
    *   **Restore State**: Ripristino automatico della posizione all'apertura

7.  **Architettura**:
    *   **Soluzione interamente client-side**: Tutto il rendering e la logica devono essere implementati in JavaScript puro, senza dipendenze Python.
    *   **MapLibre GL JS** come unica libreria di mapping.
    *   **Tailwind CSS** per tutto lo styling e la UI.
    *   Estrazione e elaborazione dati a runtime nel browser.

## Implementazioni Disponibili

### Implementazione
- Tutta la logica e la UI devono essere implementate in JavaScript puro, usando MapLibre GL JS per la mappa e Tailwind CSS per lo stile.
- Non sono ammessi componenti Python, Folium o Leaflet.

## Specifiche Tecniche

### Clustering e Popup Management
- **Estrazione temporanea dal cluster**: Quando si apre un popup da vessel list, il marker viene temporaneamente estratto dal cluster
- **Reinserimento automatico**: Il marker torna nel cluster quando il popup viene chiuso
- **Tracking stato**: Sistema di tracciamento per marker estratti vs. marker in cluster

### Layout e UX
- **Posizionamento controlli**:
  - Vessel List: Alto sinistra (sotto zoom controls)
  - Zoom controls: Alto sinistra (standard)
  - Measure: Alto destra
  - MiniMap: Basso destra
  - Source: Basso sinistra
- **Responsive design**: Adattamento automatico a dispositivi mobili
- **Z-index management**: Gestione sovrapposizioni per evitare conflitti UI

### Performance e Ottimizzazione
- **Lazy initialization**: Inizializzazione ritardata dei riferimenti mappa
- **Event delegation**: Gestione efficiente degli eventi per vessel list
- **Memory management**: Cleanup automatico dei marker estratti

## Requisiti Non Funzionali

*   **Performance**: Gestione fluida di 30+ vascelli con clustering intelligente
*   **Usabilità**: Interfaccia intuitiva con controlli standardizzati
*   **Accessibilità**: Keyboard navigation e screen reader compatible
*   **Responsive**: Funzionamento ottimale su desktop e mobile
*   **Manutenibilità**: Codice modulare e documentato per entrambe le versioni

## Stack Tecnologico
### Stack Tecnologico Unico
*   **Libreria Mappe**: MapLibre GL JS (ultima versione stabile)
*   **Clustering**: clustering nativo MapLibre o plugin compatibile
*   **Styling**: Tailwind CSS (CDN)
*   **JavaScript**: Vanilla ES6+

## File Structure

```
sumud_flotilla/
├── index.html              # Mappa principale (MapLibre)
├── script.js               # Logica JavaScript
├── style.css               # Stili CSS (Tailwind)
├── vessels.json            # Cache dati vessel
├── last_updated.txt        # Timestamp ultimo aggiornamento
├── PRD.md                  # Questo documento
```
