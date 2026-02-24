import pygame
from intro import intro, hauptmenu
from einstellungen import einstellungen
from ball_pl_counter import fenster_mit_knopf
from ball_pl_counter_commander import counter_commander
from deck_verteilung import verteile_decks, FARBEN_RGB
from spielmodus import spielmodus_auswahl
from commander_config import commander_config

def main():
    pygame.init()
    # Große Standardauflösung, aber anpassbar
    breite, hoehe = 1500, 1000
    fenster = pygame.display.set_mode((breite, hoehe), pygame.RESIZABLE)
    pygame.display.set_caption("Cheffkoch Nicki - Magic Manager")

    # Grundkonfiguration für den Speicher
    config = {
        "spieleranzahl": 2,
        "mono_deck": False,
        "RED": "0",
        "BLUE": "0",
        "BLACK": "0",
        "WHITE": "0",
        "GREEN": "0",
        "namen": ["", "", "", ""],
        "commander_farben": [[] for _ in range(4)]
    }

    # 1. Intro starten
    if not intro(fenster, breite, hoehe):
        pygame.quit()
        return

    while True:
        breite, hoehe = fenster.get_size()

        # 2. Hauptmenü
        auswahl = hauptmenu(fenster, breite, hoehe)
        if auswahl is None:
            break

        if auswahl == "Spiel Starten":
            # 3. Spielmodus wählen (Jumpstart oder Commander)
            modus = spielmodus_auswahl(fenster, breite, hoehe)
            if modus is None:
                continue

            config["modus"] = modus

            # --- PFAD: COMMANDER ---
            if modus == "Commander (EDH)":
                neue_config = commander_config(fenster, breite, hoehe, config)
                if neue_config:
                    config = neue_config
                    spieler_daten = []
                    for i in range(config["spieleranzahl"]):
                        f_namen = config["commander_farben"][i]
                        # Umwandlung der Namen (RED, BLUE...) in RGB-Werte für den Counter
                        rgb_liste = [FARBEN_RGB[f] for f in f_namen]
                        
                        spieler_daten.append({
                            "name": config["namen"][i] or f"Spieler {i+1}",
                            "decks": " / ".join(f_namen) if f_namen else "Colorless",
                            "rgb_farben": rgb_liste
                        })
                    
                    # Aufruf des speziellen Commander-Counters (4-Wege-Gradient)
                    counter_commander(fenster, spieler_daten, config["spieleranzahl"])

            # --- PFAD: JUMPSTART ---
            else:
                neue_config = einstellungen(fenster, breite, hoehe, config)
                if neue_config:
                    config = neue_config
                    # Nutzt das Prioritäten-System zur Zufallsverteilung
                    spieler_daten = verteile_decks(config)
                    # Aufruf des normalen Counters (Horizontaler Gradient)
                    fenster_mit_knopf(fenster, spieler_daten, config["spieleranzahl"])

    pygame.quit()

if __name__ == "__main__":
    main()

