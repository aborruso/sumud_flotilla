# PRD - Mappa Flotilla

## Obiettivo

Creare una mappa online per visualizzare l'ultima posizione dei vascelli della Flotilla.

## Requisiti Funzionali

1.  **Fonte Dati**:
    *   I dati sui vascelli devono essere estratti in tempo reale dalla seguente fonte JSON: `https://flotilla-orpin.vercel.app/api/vessels`

2.  **Visualizzazione Mappa**:
    *   Ogni vascello deve essere rappresentato da un pallino sulla mappa.
    *   La posizione del pallino deve corrispondere all'ultima posizione geografica registrata del vascello.

3.  **Interazione Utente**:
    *   Al click su un pallino, deve comparire un popup o un tooltip che mostra il nome del vascello.

4.  **Architettura**:
    *   La soluzione deve essere implementata interamente con tecnologie lato client (*client-side*).
    *   L'estrazione e l'elaborazione dei dati devono avvenire a *runtime* nel browser dell'utente.

## Requisiti Non Funzionali

*   **Performance**: La mappa deve essere fluida e reattiva, anche con un numero significativo di vascelli.
*   **Usabilità**: L'interfaccia deve essere semplice e intuitiva.

## Stack Tecnologico (Proposta)

*   **Libreria Mappe**: Leaflet.js o Mapbox GL JS.
*   **Libreria JavaScript**: Nessuna dipendenza specifica, Vanilla JavaScript è sufficiente.
*   **Styling**: CSS standard.
