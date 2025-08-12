import streamlit as st
import requests
import pandas as pd
import random

# Page config
st.set_page_config(page_title="Pokémon Battle Simulator", page_icon="⚔️", layout="wide")

# CSS Styles including animations, glowing winner, hover zoom, type colors, and enhanced log/moves
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    body {
        background-image: url("https://wallpapercave.com/wp/wp10267235.jpg");
        background-size: cover;
        background-attachment: fixed;
        color: #fff;
        font-family: 'Press Start 2P', cursive;
    }

    .stApp {
        background-color: rgba(0, 0, 0, 0.85); /* Darker overlay for readability */
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5); /* Gold shadow for the main app container */
    }

    .title {
        text-align: center;
        color: #FFD700; /* Gold */
        font-size: 3em;
        text-shadow: 3px 3px 5px black;
        margin-bottom: 1rem;
        animation: pulse 2s infinite; /* Add pulse animation to title */
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    .pokemon-card, .battle-pokemon-card {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        transition: transform 0.3s ease;
        border: 2px solid rgba(255, 215, 0, 0.5); /* Subtle gold border */
    }

    .battle-pokemon-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px #ffcb05; /* Stronger gold shadow on hover */
    }

    /* Improve metric styling */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05); /* Very subtle background */
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid rgba(144, 238, 144, 0.3); /* Light green subtle border */
    }
    .stMetric label {
        color: #ADD8E6 !important; /* Light blue for labels */
        font-size: 0.9em;
    }
     .stMetric div[data-testid="stMetricValue"] {
        color: #90EE90 !important; /* Light green for values */
        font-size: 1.2em;
        font-weight: bold;
    }

    .type-badge {
        display: inline-block;
        margin-right: 10px;
        padding: 5px 10px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.8em;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.3); /* Add a subtle white border */
    }

    /* Pokémon type colors (keep as is, they are good) */
    .type-fire { background-color: #F08030; }
    .type-water { background-color: #6890F0; }
    .type-grass { background-color: #78C850; }
    .type-electric { background-color: #F8D030; color: black; }
    .type-psychic { background-color: #F85888; }
    .type-ice { background-color: #98D8D8; color: black; }
    .type-dragon { background-color: #7038F8; }
    .type-dark { background-color: #705848; }
    .type-fairy { background-color: #EE99AC; color: black; }
    .type-normal { background-color: #A8A878; }
    .type-fighting { background-color: #C03028; }
    .type-flying { background-color: #A890F0; }
    .type-poison { background-color: #A040A0; }
    .type-ground { background-color: #E0C068; color: black; }
    .type-rock { background-color: #B8A038; }
    .type-bug { background-color: #A8B820; }
    .type-ghost { background-color: #705898; }
    .type-steel { background-color: #B8B8D0; color: black; }

    /* Glowing winner animation */
    .winner-glow {
        animation: glow 2s ease-in-out infinite alternate;
        border: 3px solid #FFD700;
        border-radius: 20px;
    }
    @keyframes glow {
        from { box-shadow: 0 0 10px #FFD700; }
        to { box-shadow: 0 0 30px #FFEA00; }
    }

    /* Battle log container style */
    .battle-log-container {
        background: rgba(0,0,0,0.6); /* Slightly more opaque */
        padding: 15px; /* Increased padding */
        border-radius: 12px;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace; /* Monospace for log */
        border: 2px solid #6495ED; /* Solid blue border */
        max-height: 350px; /* Slightly increased height */
        overflow-y: auto; /* Add scroll if needed */
    }

    /* Styling for individual log entries */
    .log-entry {
        margin-bottom: 15px; /* More space between log entries */
        padding-bottom: 15px; /* Padding before border */
        border-bottom: 1px dashed rgba(255,255,255,0.2); /* Dashed separator */
        color: #E0E0E0; /* Light grey for overall log text */
        white-space: pre-wrap; /* Preserve line breaks if any */
        line-height: 1.5; /* Increased line height */
    }
    /* Remove bottom border for the last log entry */
    .battle-log-container .log-entry:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    .log-turn {
        font-weight: bold;
        color: #FFD700; /* Gold for turn number */
        margin-right: 8px; /* More space after turn */
        text-shadow: 1px 1px 2px black; /* Subtle text shadow */
    }

    .log-action {
        font-style: italic;
        color: #ADD8E6; /* Light blue for action */
        margin-right: 8px; /* More space after action */
    }

    .log-separator {
        color: #ffffff; /* White separator */
        margin-right: 8px;
    }

    .log-outcome {
        color: #90EE90; /* Light green for outcome */
    }

    /* Styling for highlighted log outcomes */
    .log-super-effective {
        color: #FFA500; /* Orange */
        font-weight: bold;
    }
    .log-critical-hit {
        color: #DC143C; /* Crimson Red */
        font-weight: bold;
        text-shadow: 0 0 5px rgba(220, 20, 60, 0.7); /* More prominent shadow */
    }
    .log-faint {
        color: #808080; /* Grey */
        font-style: italic;
        text-decoration: line-through;
    }

    /* Styling for Moves List */
    .moves-list-container {
        padding: 10px;
        border: 1px dashed rgba(100, 149, 237, 0.3); /* Subtle blue dashed border */
        border-radius: 8px;
        margin-top: 15px; /* More space above moves */
        background-color: rgba(0, 0, 0, 0.3); /* Darker background for contrast */
    }

    .move-item {
        margin-bottom: 8px; /* Space between move items */
        padding-left: 15px; /* Indent for bullet effect */
        position: relative; /* Needed for custom bullet */
    }
     .move-item::before {
         content: '•'; /* Custom bullet point */
         color: #ADD8E6; /* Light blue bullet */
         font-size: 1.2em;
         position: absolute;
         left: 0;
         top: 0;
     }

    .move-name {
        /* background-color: rgba(100, 149, 237, 0.1); /* Slightly transparent blue background */
        color: #E0E0E0; /* Light grey text */
        padding: 2px 5px; /* Smaller padding */
        /* border-radius: 3px; */
        /* border: 1px solid rgba(100, 149, 237, 0.3); /* Blue border */
        font-size: 1em; /* Standard font size */
        font-weight: normal; /* Standard font weight */
        font-family: 'Press Start 2P', cursive; /* Keep retro font */
    }

    /* Pokeball animated background */
    .pokeball-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: -1;
        background-image: url('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png');
        background-repeat: repeat;
        background-size: 80px 80px;
        animation: moveBg 30s linear infinite;
        opacity: 0.05; /* Reduced opacity */
    }

    @keyframes moveBg {
        from { background-position: 0 0; }
        to { background-position: 1000px 1000px; }
    }

    /* Streamlit widget overrides for better look */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #FFD700;
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        font-family: 'Press Start 2P', cursive;
    }
     .stButton>button {
        background-color: #FFD700; /* Gold button */
        color: #000000; /* Black text */
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s ease;
        font-family: 'Press Start 2P', cursive;
    }
    .stButton>button:hover {
        background-color: #FFEA00; /* Brighter gold on hover */
        color: #000000;
    }
     .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 2px solid #FFD700;
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
         font-family: 'Press Start 2P', cursive;
    }
    .stExpansionContainer {
         background: rgba(255,255,255,0.05);
         border-radius: 10px;
         border: 1px solid rgba(100, 149, 237, 0.5); /* Light blue border */
         margin-top: 15px; /* Add space above expander */
    }
    .stExpansionContainer label {
        color: #ADD8E6; /* Light blue */
         font-family: 'Press Start 2P', cursive;
    }
    /* Style for the expander content area */
    .stExpansionContainer div[data-baseweb="collapse"] > div {
        background-color: rgba(0, 0, 0, 0.4); /* Dark background for expander content */
        padding: 15px;
        border-radius: 0 0 10px 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Add Pokeball background div
st.markdown('<div class="pokeball-bg"></div>', unsafe_allow_html=True)

# === THIS IS THE UPDATED LINE ===
API_BASE_URL = "https://pokemon-battle-simulation.onrender.com/api"
# ================================

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2" # Added PokeAPI base URL

# Function to get sprite (added caching)
@st.cache_data
def get_pokemon_sprite(pokemon_name):
    if not pokemon_name: return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    try:
        response = requests.get(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_name.lower()}")
        if response.status_code == 200:
            data = response.json()
            # Use official artwork if available, fallback to front_default
            official_sprite = data["sprites"]["other"].get("official-artwork", {}).get("front_default")
            return official_sprite or data["sprites"].get("front_default") or "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
        return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png" # Missing sprite
    except Exception as e:
        # st.warning(f"Could not fetch sprite for {pokemon_name}: {e}") # Optional: display sprite errors
        return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png" # Missing sprite

# Title
st.markdown("<div class='title'>⚔️ Pokémon Battle Simulator</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ADD8E6; font-size: 1.1em;'>Unleash the Power Within!</p>", unsafe_allow_html=True)


with st.sidebar:
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/master-ball.png", width=100)
    st.markdown("## About")
    st.info("This application simulates Pokémon battles by interacting with a FastAPI backend. Search for Pokémon details or pit two against each other!")
    st.markdown("---")
    st.markdown("Made with ❤️ for Pokémon fans!")


tab1, tab2 = st.tabs(["🔍 Pokémon Search", "⚔️ Battle Arena"])

# TAB 1: Pokémon Search
with tab1:
    st.subheader("Search a Pokémon")
    pokemon_name = st.text_input("Enter Pokémon Name:", placeholder="e.g. pikachu", key="search_input")

    col_btn, col_rand = st.columns([1, 1])
    with col_btn:
        search_clicked = st.button("Search", key="search_button")
    with col_rand:
         # Add a random button for fun, assuming your backend can handle random search or you have a list
         # This requires a way to get a random pokemon name, which the backend might provide or you need a list
         # For demonstration, let's just use a placeholder button
         # st.button("Random Pokémon", key="random_search_button")
         pass # Removed random search button for simplicity unless backend supports it

    if search_clicked: # Removed random_clicked as it's commented out
        if pokemon_name:
            with st.spinner(f"Searching for {pokemon_name.title()}..."):
                try:
                    res = requests.get(f"{API_BASE_URL}/pokemon/{pokemon_name.lower()}")
                    if res.status_code == 200:
                        data = res.json()
                        col1, col2 = st.columns([2, 1])

                        sprite_url = get_pokemon_sprite(data.get('name', '')) # Use get with default

                        with col1:
                            st.markdown(f"<div class='pokemon-card'><h3>{data.get('name', 'N/A').title()} (#{data.get('id', 'N/A')})</h3>", unsafe_allow_html=True)

                            # Types with colors
                            types_html = ""
                            for t in data.get('types', []): # Use get with default empty list
                                types_html += f"<span class='type-badge type-{t.lower()}'>{t.title()}</span>"
                            st.markdown(types_html, unsafe_allow_html=True)

                            st.subheader("Stats")
                            stats = data.get('stats', {}) # Use get with default empty dict
                            for k, v in stats.items():
                                st.metric(label=k.replace('-', ' ').title(), value=v)
                            st.markdown("</div>", unsafe_allow_html=True)

                        with col2:
                            st.image(sprite_url, width=150)
                            st.markdown("<div class='pokemon-card'>", unsafe_allow_html=True)
                            st.subheader("Abilities")
                            abilities = data.get('abilities', []) # Use get with default empty list
                            if abilities:
                                for ab in abilities:
                                    st.write(f"• {ab.replace('-', ' ').title()}")
                            else:
                                st.write("No abilities listed")

                            st.subheader("Evolutions")
                            evolutions = data.get('evolutions', []) # Use get with default empty list
                            if evolutions:
                                for evo in evolutions:
                                    st.write(f"➡️ {evo.title()}")
                            else:
                                st.write("No further evolutions")
                            st.markdown("</div>", unsafe_allow_html=True)

                        # Moves section updated to be visually appealing
                        with st.expander("🔧 View Moves"):
                            moves = data.get('moves', []) # Use get with default empty list
                            if moves:
                                st.markdown("<div class='moves-list-container'>", unsafe_allow_html=True) # Optional container

                                # Display moves in columns
                                # Calculate number of columns based on number of moves
                                num_moves = len(moves)
                                num_cols = 2 if num_moves > 10 else 1 # Use 2 columns if more than 10 moves
                                cols = st.columns(num_cols)

                                for i, move in enumerate(moves):
                                    col = cols[i % num_cols] # Alternate between columns
                                    # Style each move name
                                    col.markdown(f"<div class='move-item'><span class='move-name'>{move.replace('-', ' ').title()}</span></div>", unsafe_allow_html=True)

                                st.markdown("</div>", unsafe_allow_html=True) # Close container

                            else:
                                st.info("No moves listed for this Pokémon.") # Changed from st.write

                    elif res.status_code == 404:
                         st.error(f"Pokémon '{pokemon_name}' not found. Please check the spelling.")
                    else:
                        st.error(f"Error fetching data for '{pokemon_name}'. Status code: {res.status_code}")
                        st.json(res.json()) # Display error details if available
                except requests.exceptions.ConnectionError:
                     # This error message now reflects a real server issue, not just a local one.
                     st.error("Cannot connect to the API. The backend server may be down or experiencing issues.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a Pokémon name to search!")

# TAB 2: Battle Arena
with tab2:
    st.subheader("Let the battle begin!")
    col1, col2 = st.columns(2)
    with col1:
        pokemon1 = st.text_input("First Pokémon:", placeholder="e.g. bulbasaur", key="battle_pokemon1")
    with col2:
        pokemon2 = st.text_input("Second Pokémon:", placeholder="e.g. charizard", key="battle_pokemon2")

    battle_clicked = st.button("Start Battle!", key="start_battle_button")

    if battle_clicked:
        if pokemon1 and pokemon2:
            with st.spinner("Preparing the battlefield..."):
                try:
                    # Fetch Pokemon data for comparison display before battle
                    res1 = requests.get(f"{API_BASE_URL}/pokemon/{pokemon1.lower()}")
                    res2 = requests.get(f"{API_BASE_URL}/pokemon/{pokemon2.lower()}")

                    poke1_data = res1.json() if res1.status_code == 200 else None
                    poke2_data = res2.json() if res2.status_code == 200 else None

                    if poke1_data and poke2_data:
                        # Show Pokémon before battle starts
                        st.subheader("🥊 Pokemon Face-Off")
                        col_a, col_b = st.columns(2)

                        def display_battle_pokemon_card(col, data, name, is_winner=False):
                            if not data:
                                col.markdown(f"<h4>{name.title()}</h4><p>Data not found</p>", unsafe_allow_html=True)
                                return
                            sprite_url = get_pokemon_sprite(data.get('name', ''))
                            classes = "battle-pokemon-card"
                            if is_winner:
                                classes += " winner-glow"

                            col.markdown(f"<div class='{classes}'><h4>{name.title()}</h4>", unsafe_allow_html=True)
                            col.image(sprite_url, width=150)
                            types_html = ""
                            for t in data.get('types', []):
                                types_html += f"<span class='type-badge type-{t.lower()}'>{t.title()}</span>"
                            col.markdown(types_html, unsafe_allow_html=True)
                             # Display key stats for comparison
                            st.markdown("<h5>Stats:</h5>", unsafe_allow_html=True)
                            stats_to_show = ['hp', 'attack', 'defense', 'speed']
                            stats_data = data.get('stats', {})
                            for stat_key in stats_to_show:
                                value = stats_data.get(stat_key, 'N/A')
                                col.write(f"**{stat_key.replace('-', ' ').title()}:** {value}")

                            col.markdown("</div>", unsafe_allow_html=True)


                        # Display initial face-off (without glow yet)
                        display_battle_pokemon_card(col_a, poke1_data, pokemon1)
                        display_battle_pokemon_card(col_b, poke2_data, pokemon2)


                        # Proceed to battle simulation
                        payload = {"pokemon1": pokemon1.lower(), "pokemon2": pokemon2.lower()}
                        battle_res = requests.post(f"{API_BASE_URL}/battle", json=payload)

                        if battle_res.status_code == 200:
                            result = battle_res.json()

                            st.subheader("🏆 Battle Result 🏆")
                            winner_name = result.get('winner', 'Unknown').lower()

                            # Re-display with winner glow
                            col_a_result, col_b_result = st.columns(2)
                            display_battle_pokemon_card(col_a_result, poke1_data, pokemon1, is_winner=(pokemon1.lower() == winner_name))
                            display_battle_pokemon_card(col_b_result, poke2_data, pokemon2, is_winner=(pokemon2.lower() == winner_name))


                            st.success(f"🎉 The Winner is: {result.get('winner', 'Unknown').title()}! 🎉")
                            # Removed st.balloons()


                            # Battle Log - Handle list of dicts with 'turn', 'action', 'outcome'
                            st.subheader("📜 Battle Log")
                            battle_logs = result.get('logs', []) # Use get with default empty list

                            if battle_logs:
                                # Display logs within the styled container
                                st.markdown("<div class='battle-log-container'>", unsafe_allow_html=True)

                                for log_entry in battle_logs:
                                    # Check if the entry is a dictionary with expected keys
                                    if isinstance(log_entry, dict) and 'turn' in log_entry and 'action' in log_entry and 'outcome' in log_entry:
                                        turn_num = log_entry.get('turn', 'N/A')
                                        action_text = log_entry.get('action', 'No action')
                                        outcome_text = log_entry.get('outcome', 'No outcome')

                                        # Add emojis based on outcome keywords (simple examples)
                                        outcome_emoji = ""
                                        if "fainted" in outcome_text.lower():
                                            outcome_emoji = "💀 "
                                        elif "super effective" in outcome_text.lower():
                                            outcome_emoji = "✨ "
                                        elif "critical hit" in outcome_text.lower():
                                            outcome_emoji = "💥 "
                                        # Add more action-based emojis if needed (can get complex)
                                        # elif "thunderbolt" in action_text.lower(): outcome_emoji = "⚡ "


                                        # Add CSS classes based on outcome for highlighting
                                        outcome_classes = "log-outcome"
                                        if "fainted" in outcome_text.lower():
                                            outcome_classes += " log-faint"
                                        elif "super effective" in outcome_text.lower():
                                            outcome_classes += " log-super-effective"
                                        elif "critical hit" in outcome_text.lower():
                                             outcome_classes += " log-critical-hit"


                                        # Format the dictionary keys into an HTML string for visual appeal
                                        formatted_html_entry = (
                                            f"<div class='log-entry'>"
                                            f"<span class='log-turn'>Turn {turn_num}:</span> "
                                            f"<span class='log-action'>{action_text}</span> "
                                            f"<span class='log-separator'>-</span> "
                                            f"<span class='{outcome_classes}'>{outcome_emoji}{outcome_text}</span>" # Added class and emoji
                                            f"</div>"
                                        )
                                        st.markdown(formatted_html_entry, unsafe_allow_html=True)

                                    elif isinstance(log_entry, str):
                                        # Handle cases where some entries might still be simple strings
                                        st.markdown(f"<div class='log-entry'>{log_entry}</div>", unsafe_allow_html=True)
                                    else:
                                        # Handle any other unexpected formats
                                        st.markdown(f"<div class='log-entry' style='color: red;'>Unexpected log entry format: {log_entry}</div>", unsafe_allow_html=True)

                                st.markdown("</div>", unsafe_allow_html=True) # Close the container div

                            else:
                                st.info("No battle log available.")


                        else:
                            st.error(f"Battle simulation failed. Status code: {battle_res.status_code}")
                            try:
                                error_details = battle_res.json()
                                st.json(error_details) # Display error details if available
                            except:
                                st.write(battle_res.text) # Display raw text if JSON fails


                    else:
                        if not poke1_data:
                            st.error(f"Could not find data for {pokemon1.title()}. Please check the name.")
                        if not poke2_data:
                             st.error(f"Could not find data for {pokemon2.title()}. Please check the name.")
                        # Optional: Display status codes if data fetching failed
                        # if res1.status_code != 200: st.write(f"Debug: Status for {pokemon1} was {res1.status_code}")
                        # if res2.status_code != 200: st.write(f"Debug: Status for {pokemon2} was {res2.status_code}")


                except requests.exceptions.ConnectionError:
                     # This error message now reflects a real server issue, not just a local one.
                     st.error("Cannot connect to the API. The backend server may be down or experiencing issues.")
                except Exception as e:
                    st.error(f"An unexpected error occurred during battle simulation: {e}")
                    # Optionally print traceback for debugging
                    # import traceback
                    # st.text(traceback.format_exc())
        else:
            st.warning("Please enter names for both Pokémon to start a battle!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #ADD8E6;'>Gotta catch 'em all! 🌟</p>", unsafe_allow_html=True)