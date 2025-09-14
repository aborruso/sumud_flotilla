# PRD - Mappa Flotilla

## Obiettivo

Creare una mappa online per visualizzare l'ultima posizione dei vascelli della Flotilla con funzionalità avanzate di interazione e controllo.

## Requisiti Funzionali

1.  **Fonte Dati**:
    *   I dati sui vascelli devono essere estratti in tempo reale dalla seguente fonte JSON: `https://flotilla-orpin.vercel.app/api/vessels`
    *   Timestamp di ultimo aggiornamento visualizzato nel controllo Source

2.  **Visualizzazione Mappa**:
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
    *   **Versione JavaScript**: Soluzione client-side pura con Leaflet.js
    *   **Versione Python**: Generazione statica con folium e funzionalità JavaScript integrate
    *   Estrazione e elaborazione dati a runtime nel browser

## Implementazioni Disponibili

### 1. Versione JavaScript Originale (`index.html` + `script.js`)
- **Tecnologie**: Leaflet.js, MarkerCluster, Tailwind CSS
- **Caratteristiche**:
  - Aggiornamento dinamico in tempo reale
  - Gestione URL hash per bookmark
  - Controlli Leaflet nativi

### 2. Versione Python Folium (`leafmap_version/`)
- **Tecnologie**: Python folium, MarkerCluster, MiniMap, MeasureControl
- **Caratteristiche**:
  - Generazione statica con `generate_map.py`
  - JavaScript custom integrato per vessel list
  - Controlli folium avanzati (MiniMap, Measure)
  - Gestione intelligente dei cluster per popup

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

### Versione JavaScript
*   **Libreria Mappe**: Leaflet.js 1.9.4
*   **Clustering**: Leaflet.markercluster 1.4.1
*   **Styling**: Tailwind CSS (CDN)
*   **JavaScript**: Vanilla ES6+

### Versione Python
*   **Generazione Mappa**: Python folium
*   **Plugins**: MarkerCluster, MiniMap, MeasureControl
*   **Templating**: Branca MacroElement per componenti custom
*   **JavaScript Runtime**: Custom JS integrato per vessel list

## File Structure

```
sumud_flotilla/
├── index.html              # Mappa JavaScript principale
├── script.js               # Logica JavaScript
├── style.css               # Stili CSS
├── vessels.json            # Cache dati vessel
├── last_updated.txt        # Timestamp ultimo aggiornamento
├── PRD.md                  # Questo documento
└── leafmap_version/        # Versione Python
    ├── generate_map.py     # Script generazione mappa
    └── map.html           # Mappa folium generata
```
