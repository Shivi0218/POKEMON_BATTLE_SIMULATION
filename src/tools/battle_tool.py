from src.models.battle import BattleInput, BattleResult, BattleAction
from src.resources.pokemon_resource import get_pokemon
import random

async def simulate_battle(battle_input: BattleInput) -> BattleResult:
    # Fetch Pokémon data
    pokemon1 = await get_pokemon(battle_input.pokemon1)
    pokemon2 = await get_pokemon(battle_input.pokemon2)

    # Initialize battle state
    hp1, hp2 = pokemon1.stats["hp"], pokemon2.stats["hp"]
    logs = []
    turn = 1

    # Type effectiveness matrix
    type_effectiveness = {
        ("fire", "grass"): 2.0, ("grass", "water"): 2.0, ("water", "fire"): 2.0,
        ("fire", "water"): 0.5, ("water", "grass"): 0.5, ("grass", "fire"): 0.5,
        ("electric", "water"): 2.0, ("water", "electric"): 0.5,
        ("electric", "grass"): 0.5, ("grass", "electric"): 2.0,
        ("poison", "grass"): 2.0, ("grass", "poison"): 0.5,
        ("fire", "fire"): 0.5, ("water", "water"): 0.5, ("grass", "grass"): 0.5,
        ("electric", "electric"): 0.5, ("poison", "poison"): 0.5
    }

    # Move power dictionary
    move_power = {
        "thunderbolt": 90, "quick-attack": 40, "tackle": 40, "vine-whip": 45,
        "razor-leaf": 55, "water-gun": 40, "bubble": 40, "ember": 40, "flamethrower": 90
    }

    # Status effects
    status1 = None
    status2 = None

    while hp1 > 0 and hp2 > 0:
        # Turn order logic
        first = pokemon1 if pokemon1.stats["speed"] >= pokemon2.stats["speed"] else pokemon2
        second = pokemon2 if first == pokemon1 else pokemon1
        hp_first = hp1 if first == pokemon1 else hp2
        hp_second = hp2 if first == pokemon1 else hp1
        status_first = status1 if first == pokemon1 else status2
        status_second = status2 if first == pokemon1 else status1

        # First Pokémon's turn
        if status_first == "paralysis" and random.random() < 0.25:
            logs.append(BattleAction(
                turn=turn,
                action=f"{first.name.capitalize()} is paralyzed",
                outcome="It can't move!"
            ))
        else:
            # Move selection and power
            move = random.choice(first.moves)
            move_pow = move_power.get(move, 40)

            # Damage calculation
            level = 50  # Assume level 50
            base_damage = ((2 * level / 5 + 2) * move_pow * (first.stats["attack"] / second.stats["defense"]) / 50 + 2)
            type_mult = 1.0
            for first_type in first.types:
                for second_type in second.types:
                    type_mult *= type_effectiveness.get((first_type, second_type), 1.0)
            damage = int(base_damage * type_mult * random.uniform(0.85, 1.0))
            hp_second -= damage

            # Effectiveness message
            effectiveness_msg = (
                "It's super effective!" if type_mult > 1
                else "It's not very effective." if type_mult < 1
                else "It's a normal hit."
            )

            logs.append(BattleAction(
                turn=turn,
                action=f"{first.name.capitalize()} uses {move.capitalize()} on {second.name.capitalize()}",
                outcome=f"Deals {damage} damage. {effectiveness_msg} {second.name.capitalize()} has {max(0, hp_second)} HP left."
            ))

            # Status effect application
            if random.random() < 0.2:
                if "electric" in first.types and not status_second:
                    status_second = "paralysis"
                    logs.append(BattleAction(
                        turn=turn,
                        action=f"{second.name.capitalize()} is affected by a status",
                        outcome=f"{second.name.capitalize()} is paralyzed!"
                    ))
                elif "fire" in first.types and not status_second:
                    status_second = "burn"
                    logs.append(BattleAction(
                        turn=turn,
                        action=f"{second.name.capitalize()} is affected by a status",
                        outcome=f"{second.name.capitalize()} is burned!"
                    ))
                elif "poison" in first.types and not status_second:
                    status_second = "poison"
                    logs.append(BattleAction(
                        turn=turn,
                        action=f"{second.name.capitalize()} is affected by a status",
                        outcome=f"{second.name.capitalize()} is poisoned!"
                    ))

            # Burn or poison damage
            if status_second == "burn":
                burn_damage = int(second.stats["hp"] * 0.0625)
                hp_second -= burn_damage
                logs.append(BattleAction(
                    turn=turn,
                    action=f"{second.name.capitalize()} is hurt by its burn",
                    outcome=f"Deals {burn_damage} damage. {second.name.capitalize()} has {max(0, hp_second)} HP left."
                ))
            elif status_second == "poison":
                poison_damage = int(second.stats["hp"] * 0.125)
                hp_second -= poison_damage
                logs.append(BattleAction(
                    turn=turn,
                    action=f"{second.name.capitalize()} is hurt by poison",
                    outcome=f"Deals {poison_damage} damage. {second.name.capitalize()} has {max(0, hp_second)} HP left."
                ))

        # Update HP and status
        if first == pokemon1:
            hp2 = hp_second
            status2 = status_second
        else:
            hp1 = hp_second
            status1 = status_second

        if hp_second <= 0:
            break

        # Second Pokémon's turn
        if status_second == "paralysis" and random.random() < 0.25:
            logs.append(BattleAction(
                turn=turn,
                action=f"{second.name.capitalize()} is paralyzed",
                outcome="It can't move!"
            ))
        else:
            move = random.choice(second.moves)
            move_pow = move_power.get(move, 40)

            base_damage = ((2 * level / 5 + 2) * move_pow * (second.stats["attack"] / first.stats["defense"]) / 50 + 2)
            type_mult = 1.0
            for second_type in second.types:
                for first_type in first.types:
                    type_mult *= type_effectiveness.get((second_type, first_type), 1.0)
            damage = int(base_damage * type_mult * random.uniform(0.85, 1.0))
            hp_first -= damage

            effectiveness_msg = (
                "It's super effective!" if type_mult > 1
                else "It's not very effective." if type_mult < 1
                else "It's a normal hit."
            )

            logs.append(BattleAction(
                turn=turn,
                action=f"{second.name.capitalize()} uses {move.capitalize()} on {first.name.capitalize()}",
                outcome=f"Deals {damage} damage. {effectiveness_msg} {first.name.capitalize()} has {max(0, hp_first)} HP left."
            ))

            if random.random() < 0.2:
                if "electric" in second.types and not status_first:
                    status_first = "paralysis"
                    logs.append(BattleAction(
                        turn=turn,
                        action=f"{first.name.capitalize()} is affected by a status",
                        outcome=f"{first.name.capitalize()} is paralyzed!"
                    ))
                elif "fire" in second.types and not status_first:
                    status_first = "burn"
                    logs.append(BattleAction(
                        turn=turn,
                        action=f"{first.name.capitalize()} is affected by a status",
                        outcome=f"{first.name.capitalize()} is burned!"
                    ))
                elif "poison" in second.types and not status_first:
                    status_first = "poison"
                    logs.append(BattleAction(
                        turn=turn,
                        action=f"{first.name.capitalize()} is affected by a status",
                        outcome=f"{first.name.capitalize()} is poisoned!"
                    ))

            if status_first == "burn":
                burn_damage = int(first.stats["hp"] * 0.0625)
                hp_first -= burn_damage
                logs.append(BattleAction(
                    turn=turn,
                    action=f"{first.name.capitalize()} is hurt by its burn",
                    outcome=f"Deals {burn_damage} damage. {first.name.capitalize()} has {max(0, hp_first)} HP left."
                ))
            elif status_first == "poison":
                poison_damage = int(first.stats["hp"] * 0.125)
                hp_first -= poison_damage
                logs.append(BattleAction(
                    turn=turn,
                    action=f"{first.name.capitalize()} is hurt by poison",
                    outcome=f"Deals {poison_damage} damage. {first.name.capitalize()} has {max(0, hp_first)} HP left."
                ))

        # Update HP and status
        if first == pokemon1:
            hp1 = hp_first
            status1 = status_first
        else:
            hp2 = hp_first
            status2 = status_first

        turn += 1

    winner = pokemon1.name if hp1 > 0 else pokemon2.name
    return BattleResult(winner=winner.capitalize(), logs=logs)
