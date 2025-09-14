# PRD - Flotilla Map (English)

## Objective

Create an online map to visualize the latest position of Flotilla vessels with advanced interaction and control functionalities.

**Map Orientation**: The map should be displayed **upside down (180° rotated)** as a symbolic gesture of hope to turn the current situation upside down for justice and peace.

## Functional Requirements

1.  **Data Source**:
    *   Vessel data must be extracted in real-time from the following JSON source: `https://flotilla-orpin.vercel.app/api/vessels`
    *   Last update timestamp displayed in the Source control

2.  **Map Visualization**:
    *   All visualization must be implemented with **MapLibre GL JS** (no Leaflet, no Folium, no Python)
    *   Each vessel must be represented by a marker on the map
    *   The marker position must correspond to the last recorded geographical position of the vessel
    *   **Intelligent clustering**: Markers must be grouped in clusters when the map is zoomed out
    *   **Automatic zoom**: The map must automatically adapt to show all vessels on opening
    *   **180° rotation**: The map must be rotated 180° (upside down) by default using the `bearing: 180` option

3.  **Popup Interaction**:
    *   Clicking on a marker should display a popup showing:
        - Vessel name
        - Last update timestamp (readable format)
        - Vessel status (e.g., "sailing")
        - Vessel type (e.g., "vessel")
    *   Popups must activate only on click (not on mouseover)
    *   Popups must remain open until manually closed

4.  **Interactive Vessel List**:
    *   "Vessel List" button to open a modal with complete vessel list
    *   List sorted alphabetically by name
    *   Search field to filter vessels in real-time
    *   **Click on vessel**: automatic zoom to position + automatic popup opening
    *   Modal closure on external click or X button

5.  **Advanced Map Controls**:
    *   **Zoom controls**: Standard + and - buttons
    *   **Zoom to Fit**: Button to adapt view to all vessels
    *   **MiniMap**: Navigation mini-map in corner
    *   **Measure Control**: Tool to measure distances on the map
    *   **Source Link**: Link to original source with update timestamp

6.  **URL and State Management**:
    *   **Hash URL**: Automatic saving of zoom, position, and bearing in URL
    *   **Bookmark**: Ability to share links with specific position and orientation
    *   **Restore State**: Automatic position and bearing restoration on opening

7.  **Architecture**:
    *   **Entirely client-side solution**: All rendering and logic must be implemented in pure JavaScript, without Python dependencies.
    *   **MapLibre GL JS** as the only mapping library.
    *   **Tailwind CSS** for all styling and UI.
    *   Data extraction and processing at runtime in the browser.

## Available Implementations

### Implementation
- All logic and UI must be implemented in pure JavaScript, using MapLibre GL JS for the map and Tailwind CSS for styling.
- Python components, Folium, or Leaflet are not allowed.

## Technical Specifications

### Map Rotation and State Management
- **Default bearing**: Set `bearing: 180` in MapLibre configuration for upside-down orientation
- **URL hash preservation**: Include bearing in URL hash format: `#zoom/lat/lng/bearing`
- **State restoration**: Preserve 180° rotation when restoring from URL hash
- **FitBounds with bearing**: Maintain rotation during zoom-to-fit operations

### Clustering and Popup Management
- **Temporary extraction from cluster**: When opening a popup from vessel list, the marker is temporarily extracted from cluster
- **Automatic reinsertion**: The marker returns to cluster when popup is closed
- **State tracking**: Tracking system for extracted vs. clustered markers

### Layout and UX
- **Control positioning**:
  - Vessel List: Top right (below zoom controls)
  - Zoom controls: Top left (standard)
  - Measure: Top right
  - MiniMap: Bottom right
  - Source: Bottom left
- **Responsive design**: Automatic adaptation to mobile devices
- **Z-index management**: Overlap management to avoid UI conflicts

### Performance and Optimization
- **Lazy initialization**: Delayed initialization of map references
- **Event delegation**: Efficient event handling for vessel list
- **Memory management**: Automatic cleanup of extracted markers

## Non-Functional Requirements

*   **Performance**: Smooth handling of 30+ vessels with intelligent clustering
*   **Usability**: Intuitive interface with standardized controls
*   **Accessibility**: Keyboard navigation and screen reader compatible
*   **Responsive**: Optimal functionality on desktop and mobile
*   **Maintainability**: Modular and documented code for both versions

## Technology Stack
### Unified Technology Stack
*   **Map Library**: MapLibre GL JS (latest stable version)
*   **Clustering**: Native MapLibre clustering or compatible plugin
*   **Styling**: Tailwind CSS (CDN)
*   **JavaScript**: Vanilla ES6+

## File Structure

```
sumud_flotilla/
├── index.html              # Main map (MapLibre)
├── script.js               # JavaScript logic
├── style.css               # CSS styles (Tailwind)
├── vessels.json            # Vessel data cache
├── last_updated.txt        # Last update timestamp
├── PRD.md                  # Original document (Italian)
├── PRD_EN.md               # This document (English)
```

## Symbolic Meaning

The upside-down map orientation serves as a powerful visual metaphor and statement of hope. Just as the map is intentionally inverted from its conventional north-up orientation, it represents the aspiration to turn the current unjust situation upside down, bringing about positive change and justice for the Palestinian people. This design choice transforms a technical interface into a symbol of resistance and hope for transformation.