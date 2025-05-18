import streamlit as st
import requests
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page config
st.set_page_config(
    page_title="Pokemon Battle Simulator",
    page_icon="⚔️",
    layout="wide"
)

# Title and description
st.title("⚔️ Pokemon Battle Simulator")
st.markdown("Search for Pokemon and simulate battles!")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("A Pokemon battle simulation app using FastAPI and Streamlit")

# Create tabs
tab1, tab2 = st.tabs(["Pokemon Search 🔍", "Battle Arena ⚔️"])

# Pokemon Search Tab
with tab1:
    st.header("Pokemon Search")
    pokemon_name = st.text_input("Enter Pokemon Name:", placeholder="e.g., pikachu")
    
    if st.button("Search Pokemon"):
        if pokemon_name:
            try:
                response = requests.get(f"{API_BASE_URL}/pokemon/{pokemon_name.lower()}")
                
                if response.status_code == 200:
                    pokemon = response.json()
                    
                    # Display basic info
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader(f"{pokemon['name'].title()} (#{pokemon['id']})")
                        st.write("**Types:**", ", ".join(pokemon['types']).title())
                        
                        # Display stats
                        st.subheader("Stats")
                        for stat, value in pokemon['stats'].items():
                            st.metric(stat.replace('-', ' ').title(), value)
                    
                    with col2:
                        st.subheader("Abilities")
                        for ability in pokemon['abilities']:
                            st.write(f"• {ability.replace('-', ' ').title()}")
                        
                        st.subheader("Evolutions")
                        if pokemon['evolutions']:
                            for evolution in pokemon['evolutions']:
                                st.write(f"• {evolution.title()}")
                        else:
                            st.write("No evolutions")
                    
                    # Display moves in an expander
                    with st.expander("View Moves"):
                        moves_df = pd.DataFrame(pokemon['moves'], columns=['Move'])
                        st.dataframe(moves_df)
                
                else:
                    st.error(f"Error: Pokemon '{pokemon_name}' not found!")
            
            except requests.exceptions.ConnectionError:
                st.error("Error: Cannot connect to the API. Make sure the backend server is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a Pokemon name!")

# Battle Arena Tab
with tab2:
    st.header("Battle Arena")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pokemon1 = st.text_input("First Pokemon:", placeholder="e.g., pikachu")
    
    with col2:
        pokemon2 = st.text_input("Second Pokemon:", placeholder="e.g., charmander")
    
    if st.button("Start Battle!"):
        if pokemon1 and pokemon2:
            try:
                battle_data = {
                    "pokemon1": pokemon1.lower(),
                    "pokemon2": pokemon2.lower()
                }
                
                response = requests.post(f"{API_BASE_URL}/battle", json=battle_data)
                
                if response.status_code == 200:
                    battle_result = response.json()
                    
                    # Display winner
                    st.success(f"🏆 Winner: {battle_result['winner'].title()}!")
                    
                    # Display battle log
                    st.subheader("Battle Log")
                    for log in battle_result['logs']:
                        with st.container():
                            st.markdown(f"""
                            **Turn {log['turn']}**  
                            Action: {log['action']}  
                            Outcome: {log['outcome']}
                            ---
                            """)
                else:
                    st.error("Battle simulation failed. Make sure both Pokemon names are correct!")
            
            except requests.exceptions.ConnectionError:
                st.error("Error: Cannot connect to the API. Make sure the backend server is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter both Pokemon names!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using FastAPI and Streamlit")