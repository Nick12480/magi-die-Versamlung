import pygame

def einstellungen(fenster, breite, hoehe, config):
    schrift = pygame.font.SysFont("Comic Sans MS", 22)
    schrift_titel = pygame.font.SysFont("Comic Sans MS", 35)
    
    # Werte aus der bestehenden Config laden
    spieleranzahl = config.get("spieleranzahl", 2)
    mono_deck = config.get("mono_deck", False)
    namen = list(config.get("namen", ["", "", "", ""]))
    
    color_keys = ["ROT", "BLUE", "BLACK", "WHITE", "GREEN"]
    color_vals = [str(config.get(k, "0")) for k in color_keys]
    
    active_field = None # ("name", index) oder ("color", index)
    
    run = True
    while run:
        fenster.fill((25, 25, 30))
        maus = pygame.mouse.get_pos()
        
        # Titel
        titel = schrift_titel.render("Spieler & Decks Setup", True, (255, 255, 255))
        fenster.blit(titel, (breite//2 - titel.get_width()//2, 20))

        # --- Spieleranzahl Auswahl (2, 3, 4) ---
        lbl_anzahl = schrift.render("Anzahl Spieler:", True, (255, 255, 255))
        fenster.blit(lbl_anzahl, (50, 100))
        
        anzahl_buttons = []
        for i, num in enumerate([2, 3, 4]):
            btn_rect = pygame.Rect(200 + i*60, 95, 50, 40)
            anzahl_buttons.append((btn_rect, num))
            # Highlight wenn ausgewählt oder Maus drüber
            btn_col = (0, 200, 0) if spieleranzahl == num else (100, 100, 100)
            if btn_rect.collidepoint(maus): btn_col = (150, 150, 150) if spieleranzahl != num else (0, 255, 0)
            
            pygame.draw.rect(fenster, btn_col, btn_rect, border_radius=5)
            txt_num = schrift.render(str(num), True, (255, 255, 255))
            fenster.blit(txt_num, (btn_rect.centerx - txt_num.get_width()//2, btn_rect.centery - txt_num.get_height()//2))

        # --- Spieler Namen Sektion (passt sich der Anzahl an) ---
        name_rects = []
        for i in range(spieleranzahl):
            rect = pygame.Rect(50, 180 + i*60, 250, 40)
            name_rects.append(rect)
            col = (100, 100, 250) if active_field == ("name", i) else (60, 60, 80)
            pygame.draw.rect(fenster, col, rect, border_radius=5)
            
            # Platzhalter oder Name anzeigen
            txt_val = namen[i] if namen[i] else f"Name Spieler {i+1}..."
            txt_col = (255, 255, 255) if namen[i] else (160, 160, 160)
            txt_surf = schrift.render(txt_val, True, txt_col)
            fenster.blit(txt_surf, (rect.x + 10, rect.y + 5))

        # --- Farben Sektion (Pools) ---
        color_rects = []
        for i, k in enumerate(color_keys):
            rect = pygame.Rect(breite - 180, 150 + i*60, 80, 40)
            color_rects.append(rect)
            col = (250, 100, 100) if active_field == ("color", i) else (80, 60, 60)
            pygame.draw.rect(fenster, col, rect, border_radius=5)
            lbl = schrift.render(k + ":", True, (255, 255, 255))
            fenster.blit(lbl, (rect.x - 100, rect.y + 5))
            val_surf = schrift.render(color_vals[i], True, (255, 255, 255))
            fenster.blit(val_surf, (rect.centerx - val_surf.get_width()//2, rect.y + 5))

        # --- Checkbox & Start ---
        check_rect = pygame.Rect(breite//2 - 100, hoehe - 150, 30, 30)
        pygame.draw.rect(fenster, (255, 255, 255), check_rect, 2)
        if mono_deck: pygame.draw.rect(fenster, (0, 255, 0), check_rect.inflate(-12, -12))
        fenster.blit(schrift.render("Mono Deck Modus", True, (255, 255, 255)), (check_rect.right + 15, check_rect.y + 2))

        start_btn = pygame.Rect(breite//2 - 100, hoehe - 80, 200, 55)
        pygame.draw.rect(fenster, (0, 150, 0) if start_btn.collidepoint(maus) else (0, 100, 0), start_btn, border_radius=10)
        start_txt = schrift.render("SPIEL STARTEN", True, (255, 255, 255))
        fenster.blit(start_txt, (start_btn.centerx - start_txt.get_width()//2, start_btn.centery - start_txt.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_field = None
                # Spieleranzahl ändern
                for btn_rect, val in anzahl_buttons:
                    if btn_rect.collidepoint(event.pos):
                        spieleranzahl = val
                # Name-Feld aktivieren
                for i, r in enumerate(name_rects):
                    if r.collidepoint(event.pos): active_field = ("name", i)
                # Farbe-Feld aktivieren
                for i, r in enumerate(color_rects):
                    if r.collidepoint(event.pos): active_field = ("color", i)
                # Checkbox
                if check_rect.collidepoint(event.pos): mono_deck = not mono_deck
                # Start
                if start_btn.collidepoint(event.pos):
                    # Alles in die Config speichern
                    config.update({
                        "spieleranzahl": spieleranzahl,
                        "mono_deck": mono_deck,
                        "namen": namen
                    })
                    for i, k in enumerate(color_keys): config[k] = color_vals[i]
                    return config

            if event.type == pygame.KEYDOWN and active_field:
                if event.key == pygame.K_BACKSPACE:
                    if active_field[0] == "name": namen[active_field[1]] = namen[active_field[1]][:-1]
                    else: color_vals[active_field[1]] = color_vals[active_field[1]][:-1]
                elif event.key == pygame.K_RETURN:
                    active_field = None
                else:
                    char = event.unicode
                    if active_field[0] == "name" and len(namen[active_field[1]]) < 15:
                        namen[active_field[1]] += char
                    elif active_field[0] == "color" and char.isnumeric() and len(color_vals[active_field[1]]) < 3:
                        color_vals[active_field[1]] += char

        pygame.display.flip()
