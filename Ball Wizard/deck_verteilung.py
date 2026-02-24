import random

# Zentrale Farbdefinitionen
FARBEN_RGB = {
    "RED":   (200, 0, 0),
    "BLUE":  (0, 0, 200),
    "BLACK": (30, 30, 30),
    "WHITE": (220, 220, 220),
    "GREEN": (0, 150, 0),
}

def verteile_decks(config):
    # 1. Pools erstellen
    pools = {}
    for farbe in FARBEN_RGB:
        try:
            val = int(config.get(farbe, "0"))
        except (ValueError, TypeError):
            val = 0
        pools[farbe] = list(range(1, val + 1))
        
    spieler_daten = []
    # Tracking: Wie oft wurde eine Farbe insgesamt im ganzen Spiel vergeben?
    farb_nutzung_gesamt = {c: 0 for c in FARBEN_RGB}
    
    mono_deck_modus = config.get("mono_deck", False)
    anzahl_spieler = config.get("spieleranzahl", 2)
    namen = config.get("namen", ["", "", "", ""])

    for i in range(anzahl_spieler):
        name = namen[i] if namen[i] != "" else f"Spieler {i+1}"
        gezogene_decks = [] # Speichert (Farbe, Nummer)
        
        for d_idx in range(2): # Jeder bekommt 2 Decks
            # Welche Farben haben noch Decks im Pool?
            verfuegbar = [c for c, p in pools.items() if len(p) > 0]
            
            # REGEL: Keine doppelte Farbe beim selben Spieler (außer Mono-Modus)
            if not mono_deck_modus and d_idx == 1 and gezogene_decks:
                erste_farbe = gezogene_decks[0][0]
                if erste_farbe in verfuegbar and len(verfuegbar) > 1:
                    verfuegbar.remove(erste_farbe)

            if not verfuegbar:
                break

            # PRIORITÄT: Farben, die seltener genutzt wurden, kriegen höheres Gewicht
            # Formel: 1 / (Nutzung + 1)
            gewichte = [1.0 / (farb_nutzung_gesamt[c] + 1) for c in verfuegbar]
            
            wahl_farbe = random.choices(verfuegbar, weights=gewichte, k=1)[0]
            
            # Nummer ziehen und aus Pool löschen
            ziffer = random.choice(pools[wahl_farbe])
            pools[wahl_farbe].remove(ziffer)
            
            # Nutzung tracken
            farb_nutzung_gesamt[wahl_farbe] += 1
            gezogene_decks.append((wahl_farbe, ziffer))

        # Daten für die UI aufbereiten
        if len(gezogene_decks) == 2:
            d1, d2 = gezogene_decks
            # Wenn Mono-Modus und gleiche Farbe, bleibt d1[0] == d2[0]
            deck_str = f"{d1[0]} {d1[1]} & {d2[0]} {d2[1]}"
            f1, f2 = FARBEN_RGB[d1[0]], FARBEN_RGB[d2[0]]
        elif len(gezogene_decks) == 1:
            d1 = gezogene_decks[0]
            deck_str = f"{d1[0]} {d1[1]}"
            f1 = f2 = FARBEN_RGB[d1[0]]
        else:
            deck_str = "Keine Decks verfugbar"
            f1 = f2 = (50, 50, 50)

        spieler_daten.append({
            "name": name,
            "decks": deck_str,
            "gradient": (f1, f2)
        })

    return spieler_daten

