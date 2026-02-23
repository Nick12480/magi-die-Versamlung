import pygame
import random
from intro import intro, hauptmenu
from einstellungen import einstellungen
from ball_pl_counter import fenster_mit_knopf

def verteile_decks(config):
    pools = {}
    for c in ["ROT", "BLUE", "BLACK", "WHITE", "GREEN"]:
        try: val = int(config.get(c, "0"))
        except: val = 0
        pools[c] = list(range(1, val + 1))
        
    spieler_daten = []
    farben_rgb = {
        "ROT": (200, 0, 0), "BLUE": (0, 0, 200), "BLACK": (30, 30, 30),
        "WHITE": (220, 220, 220), "GREEN": (0, 150, 0)
    }
    
    # Tracking, wie oft eine Farbe gewählt wurde
    farb_nutzung = {c: 0 for c in pools}

    for i in range(config["spieleranzahl"]):
        decks = []
        name = config["namen"][i] if config["namen"][i] != "" else f"Spieler {i+1}"
        
        for _ in range(2): # Wir ziehen zwei Decks nacheinander
            available = [c for c, nums in pools.items() if len(nums) > 0]
            if not available: break
            
            # Gewichtung: 1 / (Nutzung + 1) -> Je öfter genutzt, desto geringer die Priorität
            gewichte = [1.0 / (farb_nutzung[c] + 1) for c in available]
            wahl_farbe = random.choices(available, weights=gewichte, k=1)[0]
            
            # Ziffer ziehen und aus Pool entfernen
            ziffer = random.choice(pools[wahl_farbe])
            pools[wahl_farbe].remove(ziffer)
            farb_nutzung[wahl_farbe] += 1
            decks.append((wahl_farbe, ziffer))

        # Formatierung für die UI
        if len(decks) == 2:
            deck_str = f"{decks[0][0]} {decks[0][1]} & {decks[1][0]} {decks[1][1]}"
            f1, f2 = farben_rgb[decks[0][0]], farben_rgb[decks[1][0]]
        else:
            deck_str = "Keine Decks"
            f1, f2 = (50, 50, 50), (80, 80, 80)
            
        spieler_daten.append({"name": name, "decks": deck_str, "gradient": (f1, f2)})
        
    return spieler_daten


def main():
    pygame.init()
    breite, hoehe = 1000, 800
    fenster = pygame.display.set_mode((breite, hoehe), pygame.RESIZABLE)
    pygame.display.set_caption("Cheffkoch Nicki")

    config = {
        "spieleranzahl": 2, "mono_deck": False,
        "ROT": "0", "BLUE": "0", "BLACK": "0", "WHITE": "0", "GREEN": "0",
        "namen": ["", "", "", ""]
    }

    if not intro(fenster, breite, hoehe): return

    while True:
        auswahl = hauptmenu(fenster, fenster.get_width(), fenster.get_height())
        if auswahl is None: break
        if auswahl == "Spiel Starten":
            neue_config = einstellungen(fenster, fenster.get_width(), fenster.get_height(), config)
            if neue_config:
                config = neue_config
                daten = verteile_decks(config)
                fenster_mit_knopf(fenster, daten, config["spieleranzahl"])
    pygame.quit()


if __name__ == "__main__":
    main()
