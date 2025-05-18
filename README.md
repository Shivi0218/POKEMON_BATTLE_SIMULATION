# 🎮 Pokemon Battle Simulation

A full-stack application that simulates Pokemon battles and provides detailed Pokemon information using FastAPI and Streamlit. The application uses the PokeAPI to fetch Pokemon data and implements a battle simulation system.

## 🌟 Features

- **Pokemon Information Lookup**
  - Detailed Pokemon stats (HP, Attack, Defense, etc.)
  - Type information
  - Abilities list
  - Move sets
  - Evolution chains
  
- **Battle Simulation**
  - Real-time, turn-based battles
  - Type- and stat-based outcome logic
  - Winner determination based on Pokemon stats and types

## 🔧 Technology Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: SQLite
- **External API**: PokeAPI
- **Language**: Python 3.7+

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Shivi0218/POKEMON_BATTLE_SIMULATION.git
cd POKEMON_BATTLE_SIMULATION
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the Pokemon database:
```bash
python src/data/seed_data.py
```

## 🎯 Running the Application

1. Start the FastAPI backend server:
```bash
./run.sh
# Or alternatively:
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run frontend.py
```

3. Access the applications:
   - Frontend: http://localhost:8501
   - API Documentation: http://localhost:8000/docs
   - API Base URL: http://localhost:8000/api

## 📚 API Endpoints

### Pokemon Information
- `GET /api/pokemon/{identifier}`
  - Get detailed information about a specific Pokemon
  - `identifier` can be Pokemon name or ID

### Battle Simulation
- `POST /api/battle`
  - Simulate a battle between two Pokemon
  - Request body:
    ```json
    {
        "pokemon1": "pokemon_name",
        "pokemon2": "pokemon_name"
    }
    ```

## 🎮 Using the Application

1. **Pokemon Search**
   - Enter a Pokemon name in the search box
   - View detailed information including stats, types, abilities, and evolution chain

2. **Battle Simulation**
   - Enter names of two Pokemon
   - Click "Start Battle" to simulate the battle
   - View turn-by-turn battle progression and final result

## 🗄️ Project Structure

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

## 🔄 Data Updates

The Pokemon database can be refreshed at any time:
```bash
rm src/data/pokemon.db  # Remove existing database
python src/data/seed_data.py  # Recreate database with fresh data
```
## 📊 Data Flow
Initial SetupPokeAPI → seed_data.py → SQLite database
Pokémon SearchUser → Streamlit → FastAPI → SQLite → UI display
Battle SimulationUser → Streamlit → FastAPI → Battle logic → Logs & result → UI

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 Notes

- The battle simulation currently includes the first 151 Pokemon (Generation 1)
- Pokemon data is fetched from PokeAPI and stored locally for better performance
- Evolution chains are fetched and stored during database initialization

## 🔐 License

[Add your license information here]

## 👥 Author

- NAME: SHIVI PARASHAR
- EMAIL: shiviparashar18@gmail.com

## 🙏 Acknowledgments

- [PokeAPI](https://pokeapi.co/) for providing Pokemon data
- FastAPI and Streamlit communities for excellent documentation and tools 