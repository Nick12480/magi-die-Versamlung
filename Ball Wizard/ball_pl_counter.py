import pygame
from win_screen import win_screen


def draw_horizontal_gradient(surface, rect, color1, color2):
    for x in range(rect.width):
        ratio = x / rect.width
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(
            surface, (r, g, b),
            (rect.x + x, rect.y),
            (rect.x + x, rect.bottom)
        )


def fenster_mit_knopf(fenster, spieler_daten, anzahl):
    breite, hoehe = fenster.get_size()
    counter = [20] * anzahl
    null_zeiten = [None] * anzahl
    start_zeit = pygame.time.get_ticks()

    running = True
    while running:
        breite, hoehe = fenster.get_size()
        zeit = (pygame.time.get_ticks() - start_zeit) / 1000.0
        maus = pygame.mouse.get_pos()

        # Schriften dynamisch basierend auf Fenstergröße
        schrift = pygame.font.SysFont("Comic Sans MS", max(16, breite // 40))
        schrift_gross = pygame.font.SysFont(
            "Comic Sans MS", max(40, breite // 14)
        )
        schrift_btn = pygame.font.SysFont(
            "Comic Sans MS", max(24, breite // 25)
        )

        # ESC Knopf
        esc_knopf = pygame.Rect(breite - 90, 10, 80, 45)

        # Layout
        rand = 20
        if anzahl <= 2:
            # 2 Spieler: nebeneinander
            w = (breite - rand * 3) // 2
            h = hoehe - rand * 2
            pos = [
                (rand, rand),
                (w + rand * 2, rand),
                (rand, rand),
                (w + rand * 2, rand)
            ]
        elif anzahl == 3:
            # 3 Spieler: 2 oben, 1 unten zentriert
            w = (breite - rand * 3) // 2
            h = (hoehe - rand * 3) // 2
            pos = [
                (rand, rand),
                (w + rand * 2, rand),
                (breite // 2 - w // 2, h + rand * 2),
                (rand, rand)
            ]
        else:
            # 4 Spieler: 2x2 Raster
            w = (breite - rand * 3) // 2
            h = (hoehe - rand * 3) // 2
            pos = [
                (rand, rand),
                (w + rand * 2, rand),
                (rand, h + rand * 2),
                (w + rand * 2, h + rand * 2)
            ]

        # Höhe anpassen für 2 Spieler
        if anzahl <= 2:
            h = hoehe - rand * 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.WINDOWRESIZED:
                breite, hoehe = fenster.get_size()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc_knopf.collidepoint(event.pos):
                    running = False
                    continue

                for i in range(anzahl):
                    r = pygame.Rect(pos[i][0], pos[i][1], w, h)
                    # Linkes Drittel = minus, rechtes Drittel = plus
                    btn_breite = r.width // 4
                    btn_hoehe = max(60, r.height // 4)
                    btn_y = r.centery - btn_hoehe // 2

                    minus_rect = pygame.Rect(
                        r.x + 10, btn_y, btn_breite, btn_hoehe
                    )
                    plus_rect = pygame.Rect(
                        r.right - btn_breite - 10, btn_y,
                        btn_breite, btn_hoehe
                    )

                    if minus_rect.collidepoint(event.pos):
                        if counter[i] > 0:
                            counter[i] -= 1
                        if counter[i] == 0 and null_zeiten[i] is None:
                            null_zeiten[i] = zeit

                    if plus_rect.collidepoint(event.pos):
                        counter[i] += 1
                        null_zeiten[i] = None

        # Zeichnen
        fenster.fill((10, 10, 15))

        for i in range(anzahl):
            r = pygame.Rect(pos[i][0], pos[i][1], w, h)
            draw_horizontal_gradient(
                fenster, r,
                spieler_daten[i]["gradient"][0],
                spieler_daten[i]["gradient"][1]
            )
            pygame.draw.rect(fenster, (255, 255, 255), r, 2, border_radius=5)

            # Name & Deck
            name_t = schrift.render(
                spieler_daten[i]["name"], True, (255, 255, 255)
            )
            deck_t = schrift.render(
                spieler_daten[i]["decks"], True, (200, 200, 200)
            )
            fenster.blit(
                name_t,
                (r.centerx - name_t.get_width() // 2, r.y + 10)
            )
            fenster.blit(
                deck_t,
                (r.centerx - deck_t.get_width() // 2, r.y + 40)
            )

            # Counter
            count_t = schrift_gross.render(
                str(counter[i]), True, (255, 255, 255)
            )
            fenster.blit(
                count_t,
                (r.centerx - count_t.get_width() // 2,
                 r.centery - count_t.get_height() // 2)
            )

            # + und - Knöpfe sichtbar zeichnen
            btn_breite = r.width // 4
            btn_hoehe = max(60, r.height // 4)
            btn_y = r.centery - btn_hoehe // 2

            minus_rect = pygame.Rect(
                r.x + 10, btn_y, btn_breite, btn_hoehe
            )
            plus_rect = pygame.Rect(
                r.right - btn_breite - 10, btn_y,
                btn_breite, btn_hoehe
            )

            # Knopf Hintergrund halbtransparent
            for btn_r, symbol in [(minus_rect, "-"), (plus_rect, "+")]:
                btn_surf = pygame.Surface(
                    (btn_r.width, btn_r.height), pygame.SRCALPHA
                )
                if btn_r.collidepoint(maus):
                    btn_surf.fill((255, 255, 255, 60))
                else:
                    btn_surf.fill((0, 0, 0, 60))
                fenster.blit(btn_surf, (btn_r.x, btn_r.y))
                pygame.draw.rect(
                    fenster, (255, 255, 255), btn_r,
                    border_radius=8, width=2
                )
                sym_t = schrift_btn.render(symbol, True, (255, 255, 255))
                fenster.blit(sym_t, (
                    btn_r.centerx - sym_t.get_width() // 2,
                    btn_r.centery - sym_t.get_height() // 2
                ))

        # ESC Knopf immer oben
        pygame.draw.rect(fenster, (180, 40, 40), esc_knopf, border_radius=5)
        pygame.draw.rect(
            fenster, (255, 255, 255), esc_knopf, width=1, border_radius=5
        )
        esc_schrift = pygame.font.SysFont("Comic Sans MS", 22)
        esc_txt = esc_schrift.render("ESC", True, (255, 255, 255))
        fenster.blit(esc_txt, (
            esc_knopf.centerx - esc_txt.get_width() // 2,
            esc_knopf.centery - esc_txt.get_height() // 2
        ))

        # Gewinner prüfen
        nullen = sum(1 for c in counter if c == 0)
        if nullen >= (anzahl - 1):
            res = sorted(
                range(anzahl),
                key=lambda x: (counter[x], null_zeiten[x] or 9999)
            )
            win_screen(fenster, res, [d["name"] for d in spieler_daten])
            running = False

        pygame.display.flip()
