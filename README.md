# Sumud Flotilla Tracker

**The map is upside down 🤘: may the world turn upside down for justice!**

A real-time interactive map displaying the latest positions of vessels participating in the Global Sumud Flotilla mission, updated every 30 minutes.

## About the Global Sumud Flotilla

[The Global Sumud Flotilla (GSF)](https://globalsumudflotilla.org/) is the largest civilian maritime mission organized to break Israel's illegal siege on Gaza. Coordinated by grassroots organizers, seafarers, doctors, artists, and solidarity activists from over 40 countries, the flotilla is a nonviolent humanitarian mission responding to the ongoing genocide and siege against the Palestinian people.

In August and September 2025, boats of all sizes will set sail from ports around the world, converging toward Gaza to open a humanitarian corridor by sea.

## Symbolic Meaning

The upside-down map orientation serves as a powerful visual metaphor and statement of hope. Just as the map is intentionally inverted from its conventional north-up orientation, it represents the aspiration to turn the current unjust situation upside down, bringing about positive change and justice for the Palestinian people. This design choice transforms a technical interface into a symbol of resistance and hope for transformation.

## Features

### Map Visualization

- **180° Rotation**: Map displayed upside down as a symbolic gesture
- **Real-time Data**: Vessel positions updated every 30 minutes
- **Intelligent Clustering**: Automatic grouping of markers when zoomed out
- **Auto-fit Zoom**: Map automatically adjusts to show all vessels on load

### Interactive Elements

- **Vessel Popups**: Click markers to view vessel details (name, status, type, last update)
- **Vessel List Modal**: Searchable list of all vessels with quick navigation
- **Info Modal**: Background information about the flotilla mission
- **Zoom Controls**: Standard zoom in/out and "zoom to fit" functionality

### Technical Features

- **URL State Management**: Bookmark and share specific map positions
- **Responsive Design**: Optimized for both desktop and mobile devices
- **Real-time Updates**: Automatic data refresh from official sources

## Data Source

This map reads vessel position data from the [official Global Sumud Flotilla tracker](https://globalsumudflotilla.org/tracker/) API:

- **API Endpoint**: `https://flotilla-orpin.vercel.app/api/vessels`
- **Update Frequency**: Every 30 minutes
- **Data Format**: JSON with vessel positions, status, and metadata

## Technology Stack

- **Mapping Library**: [MapLibre GL JS](https://maplibre.org/) v3.6.1
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) (CDN)
- **Base Map**: MapTiler Basic v2
- **Language**: Vanilla JavaScript (ES6+)
- **Architecture**: Entirely client-side, no server dependencies

## Installation & Usage

### Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/aborruso/sumud_flotilla.git
   cd sumud_flotilla
   ```

2. Open `index.html` in a web browser or serve it via a local web server:

   ```bash
   # Using Python
   python -m http.server 8000

   # Using Node.js
   npx serve .
   ```

3. Navigate to `http://localhost:8000` in your browser

### File Structure

```text
sumud_flotilla/
├── index.html              # Main application
├── vessels.json            # Cached vessel data
├── last_updated.txt        # Update timestamp
├── style.css               # Additional styles
├── share.png               # Social media preview image
├── PRD.md                  # Product Requirements Document
└── README.md               # This file
```

## Contributing

This is an open-source project supporting a humanitarian mission. Contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

### Development Guidelines

- Maintain the symbolic 180° map orientation
- Ensure mobile responsiveness
- Follow accessibility best practices
- Keep dependencies minimal (client-side only)
- Document any new features

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **Data Provider**: [Global Sumud Flotilla Organization](https://globalsumudflotilla.org/)
- **Mapping**: Powered by MapLibre GL JS and MapTiler
- **Inspiration**: The brave activists and humanitarian workers of the Global Sumud Flotilla

---

*This project stands in solidarity with the Palestinian people and supports the nonviolent humanitarian mission of the Global Sumud Flotilla.*

## Links

- 🌐 **Live Demo**: [https://aborruso.github.io/sumud_flotilla/](https://aborruso.github.io/sumud_flotilla/)
- 📊 **Official Tracker**: [https://globalsumudflotilla.org/tracker/](https://globalsumudflotilla.org/tracker/)
- 🚢 **Flotilla Website**: [https://globalsumudflotilla.org/](https://globalsumudflotilla.org/)
- 💻 **Source Code**: [https://github.com/aborruso/sumud_flotilla](https://github.com/aborruso/sumud_flotilla)
