import pygame
from win_screen import win_screen


def draw_commander_gradient(surface, rect, colors, ist_raus):
    if ist_raus:
        pygame.draw.rect(surface, (30, 30, 30), rect, border_radius=12)
        pygame.draw.rect(surface, (70, 70, 70), rect, 8, border_radius=12)
        return

    if not colors:
        pygame.draw.rect(surface, (50, 50, 50), rect, border_radius=12)
        pygame.draw.rect(surface, (255, 255, 255), rect, 3, border_radius=12)
        return

    # Gradient aus bis zu 4 Farben
    display = list(colors)
    while len(display) < 4:
        display.append(display[0])

    tiny = pygame.Surface((2, 2))
    tiny.set_at((0, 0), display[0])
    tiny.set_at((1, 0), display[1])
    tiny.set_at((0, 1), display[2])
    tiny.set_at((1, 1), display[3])
    grad = pygame.transform.smoothscale(tiny, (rect.width, rect.height))
    surface.blit(grad, (rect.x, rect.y))
    pygame.draw.rect(surface, (255, 255, 255), rect, 3, border_radius=12)


def zeichne_knopf(fenster, rect, symbol, schrift, maus):
    hover = rect.collidepoint(maus)
    farbe = (100, 100, 100) if hover else (50, 50, 50)
    pygame.draw.rect(fenster, farbe, rect, border_radius=6)
    pygame.draw.rect(fenster, (255, 255, 255), rect, 2, border_radius=6)
    txt = schrift.render(symbol, True, (255, 255, 255))
    fenster.blit(txt, (
        rect.centerx - txt.get_width() // 2,
        rect.centery - txt.get_height() // 2
    ))


def counter_commander(fenster, spieler_daten, anzahl):
    life = [40] * anzahl
    # cd_matrix[i][g] = Commander Damage den Spieler i von Spieler g bekommen hat
    cd_matrix = [[0] * anzahl for _ in range(anzahl)]
    spieler_raus = [False] * anzahl

    schrift_hp = pygame.font.SysFont("Comic Sans MS", 70, bold=True)
    schrift_name = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
    schrift_cd = pygame.font.SysFont("Comic Sans MS", 24)
    schrift_btn = pygame.font.SysFont("Comic Sans MS", 28)
    schrift_klein = pygame.font.SysFont("Comic Sans MS", 20)

    clock = pygame.time.Clock()
    running = True

    while running:
        breite, hoehe = fenster.get_size()
        maus = pygame.mouse.get_pos()

        rand = 15
        w = (breite - rand * 3) // 2
        h = (hoehe - rand * 3) // 2

        # Positionen für bis zu 4 Spieler
        positionen = [
            (rand, rand),
            (w + rand * 2, rand),
            (rand, h + rand * 2),
            (w + rand * 2, h + rand * 2)
        ]

        # Knopf Rects für alle Spieler vorberechnen
        # Struktur: alle_knopf_rects[i] = {"hp_m", "hp_p", "cd": [(m,p), ...]}
        alle_rects = []
        for i in range(anzahl):
            x, y = positionen[i]
            r = pygame.Rect(x, y, w, h)
            btn_w = max(50, w // 6)
            btn_h = max(40, h // 8)

            hp_m = pygame.Rect(r.x + 10, r.y + 60, btn_w, btn_h)
            hp_p = pygame.Rect(r.right - btn_w - 10, r.y + 60, btn_w, btn_h)

            cd_knopfe = []
            gegner_idx = [g for g in range(anzahl) if g != i]
            for j, g in enumerate(gegner_idx):
                row_y = r.y + 165 + j * 60
                cd_m = pygame.Rect(r.right - 100, row_y, 42, 36)
                cd_p = pygame.Rect(r.right - 50, row_y, 42, 36)
                cd_knopfe.append((g, cd_m, cd_p))

            alle_rects.append({
                "rect": r,
                "hp_m": hp_m,
                "hp_p": hp_p,
                "cd": cd_knopfe
            })

        # ESC Knopf
        esc_knopf = pygame.Rect(breite - 110, 20, 90, 45)

        # --- EVENTS (einmal pro Frame, außerhalb der Zeichenschleife) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # ESC
                if esc_knopf.collidepoint(event.pos):
                    running = False
                    break

                for i in range(anzahl):
                    if spieler_raus[i]:
                        continue
                    rects = alle_rects[i]

                    # HP Knöpfe
                    if rects["hp_m"].collidepoint(event.pos):
                        life[i] -= 1
                        if life[i] <= 0:
                            spieler_raus[i] = True

                    if rects["hp_p"].collidepoint(event.pos):
                        life[i] += 1
                        if life[i] > 0:
                            spieler_raus[i] = False

                    # Commander Damage Knöpfe
                    for (g, cd_m, cd_p) in rects["cd"]:
                        if cd_m.collidepoint(event.pos):
                            if cd_matrix[i][g] > 0:
                                cd_matrix[i][g] -= 1
                        if cd_p.collidepoint(event.pos):
                            cd_matrix[i][g] += 1
                            if cd_matrix[i][g] >= 21:
                                spieler_raus[i] = True

        # --- ZEICHNEN ---
        fenster.fill((10, 10, 15))

        for i in range(anzahl):
            x, y = positionen[i]
            r = pygame.Rect(x, y, w, h)
            rects = alle_rects[i]

            draw_commander_gradient(
                fenster, r,
                spieler_daten[i]["rgb_farben"],
                spieler_raus[i]
            )

            # Name
            name_t = schrift_name.render(
                spieler_daten[i]["name"], True, (255, 255, 255)
            )
            fenster.blit(name_t, (
                r.centerx - name_t.get_width() // 2, r.y + 12
            ))

            if spieler_raus[i]:
                raus_t = schrift_hp.render("RAUS", True, (255, 50, 50))
                fenster.blit(raus_t, (
                    r.centerx - raus_t.get_width() // 2,
                    r.centery - raus_t.get_height() // 2
                ))
            else:
                # Leben
                hp_t = schrift_hp.render(str(life[i]), True, (255, 255, 255))
                fenster.blit(hp_t, (
                    r.centerx - hp_t.get_width() // 2, r.y + 40
                ))

                # HP Knöpfe
                zeichne_knopf(fenster, rects["hp_m"], "-", schrift_btn, maus)
                zeichne_knopf(fenster, rects["hp_p"], "+", schrift_btn, maus)

                # Commander Damage Sektion
                cd_titel = schrift_cd.render(
                    "CMD Damage:", True, (220, 220, 220)
                )
                fenster.blit(cd_titel, (r.x + 10, r.y + 148))
                pygame.draw.line(
                    fenster, (150, 150, 150),
                    (r.x + 10, r.y + 162),
                    (r.right - 10, r.y + 162), 1
                )

                for (g, cd_m, cd_p) in rects["cd"]:
                    j = rects["cd"].index((g, cd_m, cd_p))
                    row_y = r.y + 165 + j * 60
                    gegner_name = spieler_daten[g]["name"]
                    schaden = cd_matrix[i][g]
                    farbe = (255, 80, 80) if schaden >= 15 else (255, 255, 255)
                    cd_txt = schrift_cd.render(
                        gegner_name + ": " + str(schaden), True, farbe
                    )
                    fenster.blit(cd_txt, (r.x + 10, row_y + 5))
                    zeichne_knopf(fenster, cd_m, "-", schrift_cd, maus)
                    zeichne_knopf(fenster, cd_p, "+", schrift_cd, maus)

        # ESC Knopf
        esc_farbe = (180, 50, 50) if esc_knopf.collidepoint(maus) else (130, 30, 30)
        pygame.draw.rect(fenster, esc_farbe, esc_knopf, border_radius=8)
        pygame.draw.rect(fenster, (255, 255, 255), esc_knopf, 2, border_radius=8)
        esc_schrift = pygame.font.SysFont("Comic Sans MS", 22)
        esc_t = esc_schrift.render("ESC", True, (255, 255, 255))
        fenster.blit(esc_t, (
            esc_knopf.centerx - esc_t.get_width() // 2,
            esc_knopf.centery - esc_t.get_height() // 2
        ))

        # Gewinner prüfen
        noch_im_spiel = [i for i in range(anzahl) if not spieler_raus[i]]
        if len(noch_im_spiel) == 1:
            # Gewinner = letzter übriggebliebener
            plaetzierung = [noch_im_spiel[0]]
            raus_reihenfolge = [
                i for i in range(anzahl) if spieler_raus[i]
            ]
            plaetzierung += raus_reihenfolge[::-1]
            win_screen(fenster, plaetzierung,
                       [d["name"] for d in spieler_daten])
            running = False

        pygame.display.flip()
        clock.tick(60)
