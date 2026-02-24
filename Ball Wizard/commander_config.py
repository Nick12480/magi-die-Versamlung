import pygame

def commander_config(fenster, breite, hoehe, config):
    schrift = pygame.font.SysFont("Comic Sans MS", 22)
    schrift_titel = pygame.font.SysFont("Comic Sans MS", 35)
    
    # Werte aus der Config laden
    anzahl = config.get("spieleranzahl", 2)
    namen = list(config.get("namen", ["", "", "", ""]))
    spieler_farben = config.get("commander_farben", [[] for _ in range(4)])
    
    farb_optionen = ["RED", "BLUE", "BLACK", "WHITE", "GREEN"]
    # Zuordnung der Dateinamen (müssen in deinem Ordner liegen)
    icon_dateien = {
        "RED": "rad.png",
        "BLUE": "blue.png",
        "BLACK": "black.png",
        "WHITE": "white.png",
        "GREEN": "green.png"
    }
    
    farb_rgb = {
        "RED": (200, 0, 0), "BLUE": (0, 0, 200), "BLACK": (30, 30, 30),
        "WHITE": (220, 220, 220), "GREEN": (0, 150, 0)
    }

    # Icons laden und skalieren
    icons = {}
    for key, datei in icon_dateien.items():
        try:
            img = pygame.image.load(datei)
            icons[key] = pygame.transform.scale(img, (50, 50))
        except:
            icons[key] = None

    active_name_idx = None
    run = True
    while run:
        fenster.fill((25, 25, 30))
        maus = pygame.mouse.get_pos()
        
        # Titel
        t_img = schrift_titel.render("Commander Setup", True, (255, 215, 0))
        fenster.blit(t_img, (breite // 2 - t_img.get_width() // 2, 30))

        # --- Spieleranzahl Auswahl ---
        for i in range(2, 5):
            rect = pygame.Rect(100 + (i-2)*120, 100, 100, 40)
            farbe = (100, 255, 100) if anzahl == i else (80, 80, 80)
            pygame.draw.rect(fenster, farbe, rect, border_radius=5)
            txt = schrift.render(f"{i} Spieler", True, (255, 255, 255))
            fenster.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

        # --- Symbole über den Spalten zeichnen ---
        start_x_farben = 350
        for f_idx, f_name in enumerate(farb_optionen):
            x = start_x_farben + f_idx * 80
            if icons[f_name]:
                # Symbol mittig über der Checkbox-Spalte
                fenster.blit(icons[f_name], (x - 5, 160))
            else:
                # Falls Bild fehlt, zeige Text
                f_txt = schrift.render(f_name[0], True, (255,255,255))
                fenster.blit(f_txt, (x + 15, 170))

        # --- Spieler Zeilen ---
        for i in range(anzahl):
            y_pos = 230 + i * 90
            
            # Name Eingabefeld
            name_rect = pygame.Rect(50, y_pos, 250, 45)
            border_col = (255, 215, 0) if active_name_idx == i else (100, 100, 100)
            pygame.draw.rect(fenster, (40, 40, 45), name_rect, border_radius=5)
            pygame.draw.rect(fenster, border_col, name_rect, 2, border_radius=5)
            
            display_name = namen[i] if namen[i] else f"Name Spieler {i+1}..."
            n_txt = schrift.render(display_name, True, (255, 255, 255) if namen[i] else (150, 150, 150))
            fenster.blit(n_txt, (name_rect.x + 10, name_rect.centery - n_txt.get_height()//2))

            # Checkboxen für Farben
            for f_idx, f_name in enumerate(farb_optionen):
                cb_rect = pygame.Rect(start_x_farben + f_idx * 80, y_pos, 45, 45)
                is_selected = f_name in spieler_farben[i]
                
                # Checkbox Hintergrund
                pygame.draw.rect(fenster, (50, 50, 55), cb_rect, border_radius=5)
                
                # Wenn ausgewählt: Füllen mit der Mana-Farbe
                if is_selected:
                    pygame.draw.rect(fenster, farb_rgb[f_name], cb_rect.inflate(-10, -10), border_radius=3)
                
                # Rahmen
                pygame.draw.rect(fenster, (200, 200, 200), cb_rect, 2, border_radius=5)

        # --- Start Button ---
        start_btn = pygame.Rect(breite // 2 - 125, hoehe - 100, 250, 60)
        s_col = (0, 180, 0) if start_btn.collidepoint(maus) else (0, 120, 0)
        pygame.draw.rect(fenster, s_col, start_btn, border_radius=12)
        pygame.draw.rect(fenster, (255, 255, 255), start_btn, 2, border_radius=12)
        s_txt = schrift.render("BATTLE STARTEN", True, (255, 255, 255))
        fenster.blit(s_txt, (start_btn.centerx - s_txt.get_width()//2, start_btn.centery - s_txt.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Spieleranzahl Buttons
                for i in range(2, 5):
                    if pygame.Rect(100 + (i-2)*120, 100, 100, 40).collidepoint(event.pos):
                        anzahl = i
                
                # Namen Feld aktivieren
                active_name_idx = None
                for i in range(anzahl):
                    if pygame.Rect(50, 230 + i * 90, 250, 45).collidepoint(event.pos):
                        active_name_idx = i
                
                # Checkboxen klicken
                for i in range(anzahl):
                    for f_idx, f_name in enumerate(farb_optionen):
                        cb_rect = pygame.Rect(start_x_farben + f_idx * 80, 230 + i * 90, 45, 45)
                        if cb_rect.collidepoint(event.pos):
                            if f_name in spieler_farben[i]:
                                spieler_farben[i].remove(f_name)
                            else:
                                spieler_farben[i].append(f_name)
                
                # Start
                if start_btn.collidepoint(event.pos):
                    config.update({
                        "spieleranzahl": anzahl,
                        "namen": namen,
                        "commander_farben": spieler_farben
                    })
                    return config

            if event.type == pygame.KEYDOWN and active_name_idx is not None:
                if event.key == pygame.K_BACKSPACE:
                    namen[active_name_idx] = namen[active_name_idx][:-1]
                elif event.key == pygame.K_RETURN:
                    active_name_idx = None
                else:
                    if len(namen[active_name_idx]) < 15:
                        namen[active_name_idx] += event.unicode

        pygame.display.flip()
