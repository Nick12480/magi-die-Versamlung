import pygame
import os


def einstellungen(fenster, breite, hoehe, config):
    schrift = pygame.font.SysFont("Comic Sans MS", 22)
    schrift_titel = pygame.font.SysFont("Comic Sans MS", 35)

    spieleranzahl = config.get("spieleranzahl", 2)
    mono_deck = config.get("mono_deck", False)
    namen = list(config.get("namen", ["", "", "", ""]))

    color_keys = ["RED", "BLUE", "BLACK", "WHITE", "GREEN"]
    color_vals = [str(config.get(k, "0")) for k in color_keys]

    # Icons laden - Dateiname zu Farbe zuordnen
    icon_dateien = {
        "RED": "rad.png",
        "BLUE": "blue.png",
        "BLACK": "black.png",
        "WHITE": "white.png",
        "GREEN": "green.png",
    }
    icons = {}
    for key, datei in icon_dateien.items():
        try:
            img = pygame.image.load(datei)
            icons[key] = pygame.transform.scale(img, (45, 45))
        except Exception:
            icons[key] = None

    master_val = ""
    active_field = None

    run = True
    while run:
        fenster.fill((25, 25, 30))
        maus = pygame.mouse.get_pos()

        # Titel
        titel = schrift_titel.render(
            "Spieler & Decks Setup", True, (255, 255, 255)
        )
        fenster.blit(titel, (breite // 2 - titel.get_width() // 2, 20))

        # --- MASTER FELD ---
        master_lbl = schrift.render(
            "Alle Farben setzen:", True, (255, 215, 0)
        )
        fenster.blit(master_lbl, (breite // 2 - 160, 75))
        master_rect = pygame.Rect(breite // 2 + 20, 70, 100, 40)
        master_col = (250, 200, 0) if active_field == "master" else (120, 100, 0)
        pygame.draw.rect(fenster, master_col, master_rect, border_radius=5)
        pygame.draw.rect(
            fenster, (255, 215, 0), master_rect, 2, border_radius=5
        )
        master_txt = schrift.render(
            master_val if master_val else "0-100", True, (255, 255, 255)
        )
        fenster.blit(master_txt, (
            master_rect.centerx - master_txt.get_width() // 2,
            master_rect.y + 8
        ))

        pygame.draw.line(
            fenster, (80, 80, 80), (30, 125), (breite - 30, 125), 1
        )

        # --- Spieleranzahl ---
        lbl_anzahl = schrift.render(
            "Anzahl Spieler:", True, (255, 255, 255)
        )
        fenster.blit(lbl_anzahl, (50, 145))

        anzahl_buttons = []
        for i, num in enumerate([2, 3, 4]):
            btn_rect = pygame.Rect(200 + i * 60, 140, 50, 40)
            anzahl_buttons.append((btn_rect, num))
            btn_col = (0, 200, 0) if spieleranzahl == num else (100, 100, 100)
            if btn_rect.collidepoint(maus):
                btn_col = (0, 255, 0) if spieleranzahl == num else (150, 150, 150)
            pygame.draw.rect(fenster, btn_col, btn_rect, border_radius=5)
            txt_num = schrift.render(str(num), True, (255, 255, 255))
            fenster.blit(txt_num, (
                btn_rect.centerx - txt_num.get_width() // 2,
                btn_rect.centery - txt_num.get_height() // 2
            ))

        # --- Spieler Namen ---
        name_rects = []
        for i in range(spieleranzahl):
            rect = pygame.Rect(50, 220 + i * 60, 250, 40)
            name_rects.append(rect)
            col = (100, 100, 250) if active_field == ("name", i) else (60, 60, 80)
            pygame.draw.rect(fenster, col, rect, border_radius=5)
            txt_val = (namen[i] if namen[i]
                       else "Name Spieler " + str(i + 1) + "...")
            txt_col = (255, 255, 255) if namen[i] else (160, 160, 160)
            txt_surf = schrift.render(txt_val, True, txt_col)
            fenster.blit(txt_surf, (rect.x + 10, rect.y + 5))

        # --- Farben mit Icons ---
        color_rects = []
        icon_groesse = 45
        icon_abstand = 10
        feld_x = breite - 180
        for i, k in enumerate(color_keys):
            y = 190 + i * 65

            # Icon links neben dem Feld
            if icons.get(k):
                fenster.blit(
                    icons[k],
                    (feld_x - icon_groesse - icon_abstand, y)
                )

            # Farbfeld
            rect = pygame.Rect(feld_x, y, 80, 45)
            color_rects.append(rect)
            col = (250, 100, 100) if active_field == ("color", i) else (80, 60, 60)
            pygame.draw.rect(fenster, col, rect, border_radius=5)
            pygame.draw.rect(
                fenster, (180, 180, 180), rect, 1, border_radius=5
            )

            val_surf = schrift.render(color_vals[i], True, (255, 255, 255))
            fenster.blit(val_surf, (
                rect.centerx - val_surf.get_width() // 2,
                rect.y + 10
            ))

        # --- Checkbox & Start ---
        check_rect = pygame.Rect(breite // 2 - 100, hoehe - 150, 30, 30)
        pygame.draw.rect(fenster, (255, 255, 255), check_rect, 2)
        if mono_deck:
            pygame.draw.rect(
                fenster, (0, 255, 0), check_rect.inflate(-12, -12)
            )
        fenster.blit(
            schrift.render("Mono Deck Modus", True, (255, 255, 255)),
            (check_rect.right + 15, check_rect.y + 2)
        )

        start_btn = pygame.Rect(breite // 2 - 100, hoehe - 80, 200, 55)
        start_col = (0, 150, 0) if start_btn.collidepoint(maus) else (0, 100, 0)
        pygame.draw.rect(fenster, start_col, start_btn, border_radius=10)
        start_txt = schrift.render("SPIEL STARTEN", True, (255, 255, 255))
        fenster.blit(start_txt, (
            start_btn.centerx - start_txt.get_width() // 2,
            start_btn.centery - start_txt.get_height() // 2
        ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                active_field = None

                if master_rect.collidepoint(event.pos):
                    active_field = "master"

                for btn_rect, val in anzahl_buttons:
                    if btn_rect.collidepoint(event.pos):
                        spieleranzahl = val

                for i, r in enumerate(name_rects):
                    if r.collidepoint(event.pos):
                        active_field = ("name", i)

                for i, r in enumerate(color_rects):
                    if r.collidepoint(event.pos):
                        active_field = ("color", i)

                if check_rect.collidepoint(event.pos):
                    mono_deck = not mono_deck

                if start_btn.collidepoint(event.pos):
                    config.update({
                        "spieleranzahl": spieleranzahl,
                        "mono_deck": mono_deck,
                        "namen": namen
                    })
                    for i, k in enumerate(color_keys):
                        config[k] = color_vals[i]
                    return config

            if event.type == pygame.KEYDOWN and active_field:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == "master":
                        master_val = master_val[:-1]
                    elif active_field[0] == "name":
                        namen[active_field[1]] = namen[active_field[1]][:-1]
                    else:
                        color_vals[active_field[1]] = (
                            color_vals[active_field[1]][:-1]
                        )
                elif event.key == pygame.K_RETURN:
                    if active_field == "master" and master_val:
                        try:
                            val = max(0, min(100, int(master_val)))
                            color_vals = [str(val)] * 5
                        except ValueError:
                            pass
                    active_field = None
                else:
                    char = event.unicode
                    if active_field == "master":
                        if char.isnumeric() and len(master_val) < 3:
                            master_val += char
                            try:
                                val = max(0, min(100, int(master_val)))
                                color_vals = [str(val)] * 5
                            except ValueError:
                                pass
                    elif active_field[0] == "name":
                        if len(namen[active_field[1]]) < 15:
                            namen[active_field[1]] += char
                    elif active_field[0] == "color":
                        if (char.isnumeric() and
                                len(color_vals[active_field[1]]) < 3):
                            color_vals[active_field[1]] += char

        pygame.display.flip()
