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


def zeichne_knopf(fenster, rect, symbol, schrift, maus):
    """Zeichnet einen + oder - Knopf."""
    hover = rect.collidepoint(maus)
    # Hintergrund
    farbe = (80, 80, 80) if hover else (40, 40, 40)
    pygame.draw.rect(fenster, farbe, rect, border_radius=8)
    # Rahmen
    pygame.draw.rect(fenster, (255, 255, 255), rect, 2, border_radius=8)
    # Symbol
    txt = schrift.render(symbol, True, (255, 255, 255))
    fenster.blit(txt, (
        rect.centerx - txt.get_width() // 2,
        rect.centery - txt.get_height() // 2
    ))


def fenster_mit_knopf(fenster, spieler_daten, anzahl):
    counter = [20] * anzahl
    null_zeiten = [None] * anzahl
    start_zeit = pygame.time.get_ticks()

    running = True
    while running:
        breite, hoehe = fenster.get_size()
        zeit = (pygame.time.get_ticks() - start_zeit) / 1000.0
        maus = pygame.mouse.get_pos()

        # Schriften
        schrift = pygame.font.SysFont("Comic Sans MS", max(18, breite // 50))
        schrift_gross = pygame.font.SysFont(
            "Comic Sans MS", max(60, breite // 12)
        )
        schrift_btn = pygame.font.SysFont(
            "Comic Sans MS", max(30, breite // 25)
        )

        # ESC Knopf
        esc_knopf = pygame.Rect(breite - 110, 20, 90, 45)

        # Layout
        rand = 20
        if anzahl == 2:
            w = breite - rand * 2
            h = (hoehe - rand * 3) // 2
            pos = [(rand, rand), (rand, h + rand * 2)]
        else:
            w = (breite - rand * 3) // 2
            h = (hoehe - rand * 3) // 2
            pos = [
                (rand, rand), (rand, h + rand * 2),
                (w + rand * 2, rand), (w + rand * 2, h + rand * 2)
            ]

        # Knopf Größe
        btn_w = max(60, w // 5)
        btn_h = max(50, h // 4)

        # Knopf Rects berechnen
        knopf_rects = []
        for i in range(anzahl):
            r = pygame.Rect(pos[i][0], pos[i][1], w, h)
            btn_y = r.centery - btn_h // 2
            minus = pygame.Rect(r.x + 15, btn_y, btn_w, btn_h)
            plus = pygame.Rect(r.right - btn_w - 15, btn_y, btn_w, btn_h)
            knopf_rects.append((minus, plus))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if esc_knopf.collidepoint(event.pos):
                    running = False
                    continue

                for i in range(anzahl):
                    minus, plus = knopf_rects[i]
                    if minus.collidepoint(event.pos):
                        if counter[i] > 0:
                            counter[i] -= 1
                        if counter[i] == 0 and null_zeiten[i] is None:
                            null_zeiten[i] = zeit
                    if plus.collidepoint(event.pos):
                        counter[i] += 1
                        null_zeiten[i] = None

        # --- ZEICHNEN ---
        fenster.fill((20, 20, 25))

        for i in range(anzahl):
            r = pygame.Rect(pos[i][0], pos[i][1], w, h)
            c1, c2 = spieler_daten[i]["gradient"]
            draw_horizontal_gradient(fenster, r, c1, c2)
            pygame.draw.rect(fenster, (255, 255, 255), r, 2, border_radius=10)

            # Name & Deck
            name_t = schrift.render(
                spieler_daten[i]["name"], True, (255, 255, 255)
            )
            deck_t = schrift.render(
                "Deck: " + spieler_daten[i]["decks"], True, (230, 230, 230)
            )
            fenster.blit(name_t, (
                r.centerx - name_t.get_width() // 2, r.y + 15
            ))
            fenster.blit(deck_t, (
                r.centerx - deck_t.get_width() // 2, r.y + 45
            ))

            # Große Zahl
            count_t = schrift_gross.render(
                str(counter[i]), True, (255, 255, 255)
            )
            fenster.blit(count_t, (
                r.centerx - count_t.get_width() // 2,
                r.centery - count_t.get_height() // 2
            ))

            # + und - Knöpfe zeichnen
            minus, plus = knopf_rects[i]
            zeichne_knopf(fenster, minus, "-", schrift_btn, maus)
            zeichne_knopf(fenster, plus, "+", schrift_btn, maus)

        # ESC Knopf
        btn_farbe = (180, 50, 50) if esc_knopf.collidepoint(maus) else (130, 30, 30)
        pygame.draw.rect(fenster, btn_farbe, esc_knopf, border_radius=8)
        pygame.draw.rect(fenster, (255, 255, 255), esc_knopf, 2, border_radius=8)
        esc_t = schrift.render("ESC", True, (255, 255, 255))
        fenster.blit(esc_t, (
            esc_knopf.centerx - esc_t.get_width() // 2,
            esc_knopf.centery - esc_t.get_height() // 2
        ))

        # Gewinner prüfen
        fertige = sum(1 for c in counter if c == 0)
        if (anzahl == 2 and fertige >= 1) or (anzahl > 2 and fertige >= anzahl - 1):
            plaetzierung = sorted(
                range(anzahl),
                key=lambda x: (counter[x], null_zeiten[x] or 99999),
                reverse=True
            )
            win_screen(fenster, plaetzierung, [d["name"] for d in spieler_daten])
            running = False

        pygame.display.flip()
