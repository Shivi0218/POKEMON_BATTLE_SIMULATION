# Pokémon Battle Simulation

![Deployment](https://img.shields.io/badge/Deployment-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Frameworks](https://img.shields.io/badge/Frameworks-FastAPI%20%7C%20Streamlit-orange)

A full-stack application that simulates Pokémon battles and provides detailed Pokémon information. The backend is built with FastAPI and deployed on Render, while the interactive frontend is built with Streamlit and deployed on Streamlit Community Cloud.



## Live Demo

You can access the live, deployed application here:

-   **Frontend Application (Streamlit):** **https://poke-battle-sim.streamlit.app/**
-   **Backend API (Render):** **https://pokemon-battle-simulation.onrender.com**

---

## Features

-   **Pokémon Information Lookup**
    -   Detailed Pokémon stats (HP, Attack, Defense, etc.)
    -   Type information and badges
    -   Abilities and move sets
    -   Evolution chains
-   **Battle Simulation**
    -   Pit any two Pokémon from the database against each other.
    -   View a turn-by-turn battle log with styled outcomes.
    -   Winner determination based on a weighted calculation of stats and types.

---

## Technology Stack

-   **Backend**: **FastAPI**
-   **Frontend**: **Streamlit**
-   **Language**: **Python 3.7+**
-   **Database**: **SQLite** (for local data caching)
-   **Data Source**: **PokeAPI**
-   **Deployment**:
    -   **Backend**: **Render**
    -   **Frontend**: **Streamlit Community Cloud**

---

## Architecture & Data Flow

The application follows a decoupled frontend-backend architecture.

**Deployed Data Flow:**
`User` → `Streamlit Cloud Frontend` → `Render Backend API` → `Response to User`

---

## Local Development Setup

Follow these instructions to run the project on your local machine for development purposes.

### Prerequisites

-   Python 3.7 or higher
-   pip (Python package manager)
-   A virtual environment tool (e.g., `venv`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Shivi0218/POKEMON_BATTLE_SIMULATION.git](https://github.com/Shivi0218/POKEMON_BATTLE_SIMULATION.git)
    cd POKEMON_BATTLE_SIMULATION
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the local database:**
    The backend uses a local SQLite database for performance. This command fetches data from PokeAPI and populates the database.
    ```bash
    python src/data/seed_data.py
    ```

### Running Locally

You need to run the backend and frontend in two separate terminals.

1.  **Start the FastAPI backend server (Terminal 1):**
    ```bash
    uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload
    ```

2.  **Start the Streamlit frontend (Terminal 2):**
    ```bash
    streamlit run frontend.py
    ```

3.  **Access the local applications:**
    -   **Frontend:** `http://localhost:8501`
    -   **API Docs:** `http://localhost:8000/docs`

---

## API Endpoints

The backend exposes the following endpoints:

-   `GET /api/pokemon/{identifier}`: Get detailed information for a specific Pokémon by name or ID.
-   `POST /api/battle`: Simulate a battle between two Pokémon.
    -   Request Body: `{"pokemon1": "name", "pokemon2": "name"}`

---

## Project Structure

```
POKEMON_BATTLE_SIMULATION/
├── src/
│   ├── data/
│   │   ├── pokemon.db        # SQLite database file
│   │   └── seed_data.py      # Database seeder using PokeAPI
│   ├── models/
│   │   ├── pokemon.py        # Pydantic model for Pokémon
│   │   └── battle.py         # Pydantic model for battles
│   ├── resources/
│   │   ├── pokemon_resource.py  # GET /api/pokemon
│   │   └── battle_resource.py   # POST /api/battle
│   ├── tools/
│   │   └── battle_tool.py    # Battle simulation logic
│   └── server.py             # FastAPI app entrypoint
├── frontend.py              # Streamlit UI
├── requirements.txt         # Python dependencies
├── run.sh                   # Backend startup script
└── README.md                # Project documentation
```

---

## Notes

-   The battle simulation currently includes the first 151 Pokémon (Generation 1).
-   Pokémon data is fetched from PokeAPI and stored locally for better performance.
-   Evolution chains are fetched and stored during database initialization.

---

## Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## Author

-   **NAME**: SHIVI PARASHAR
-   **EMAIL**: shiviparashar18@gmail.com

---

## Acknowledgments

-   [PokeAPI](https://pokeapi.co/) for providing the comprehensive Pokémon data.
-   The teams behind FastAPI, Streamlit, and Render for their incredible tools.