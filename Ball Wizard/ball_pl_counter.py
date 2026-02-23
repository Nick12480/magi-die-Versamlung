import pygame
from win_screen import win_screen


def draw_horizontal_gradient(surface, rect, color1, color2):
    """Zeichnet einen horizontalen Farbverlauf von links nach rechts."""
    for x in range(rect.width):
        ratio = x / rect.width
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (rect.x + x, rect.y), (rect.x + x, rect.bottom))


def fenster_mit_knopf(fenster, spieler_daten, anzahl):
    breite, hoehe = fenster.get_size()
    counter = [20] * anzahl
    null_zeiten = [None] * anzahl
    start_zeit = pygame.time.get_ticks()
    schrift = pygame.font.SysFont("Comic Sans MS", 25)
    schrift_gross = pygame.font.SysFont("Comic Sans MS", 80)

    running = True
    while running:
        zeit = (pygame.time.get_ticks() - start_zeit) / 1000.0
        maus = pygame.mouse.get_pos()
        esc_knopf = pygame.Rect(breite - 90, 10, 80, 45)  # Definition hier für Kollision
        
        # Layout Logik
        rand = 20
        w = (breite - rand*3) // 2 if anzahl > 2 else breite - rand*2
        h = (hoehe - rand*3) // 2
        pos = [(rand, rand), (rand, h+rand*2), (w+rand*2, rand), (w+rand*2, h+rand*2)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ESC Button Check (Priorität 1)
                if esc_knopf.collidepoint(event.pos): 
                    running = False
                    continue
                
                # Counter Check
                for i in range(anzahl):
                    r = pygame.Rect(pos[i][0], pos[i][1], w, h)
                    if r.collidepoint(event.pos):
                        if event.pos[0] < r.centerx:
                            if counter[i] > 0: counter[i] -= 1
                            if counter[i] == 0: null_zeiten[i] = zeit
                        else:
                            counter[i] += 1
                            null_zeiten[i] = None

        # --- ZEICHNEN ---
        fenster.fill((10, 10, 15))
        
        for i in range(anzahl):
            r = pygame.Rect(pos[i][0], pos[i][1], w, h)
            # Hier der horizontale Gradient!
            draw_horizontal_gradient(fenster, r, spieler_daten[i]["gradient"][0], spieler_daten[i]["gradient"][1])
            pygame.draw.rect(fenster, (255, 255, 255), r, 2, border_radius=5)
            
            name_t = schrift.render(spieler_daten[i]["name"], True, (255, 255, 255))
            deck_t = schrift.render(spieler_daten[i]["decks"], True, (200, 200, 200))
            count_t = schrift_gross.render(str(counter[i]), True, (255, 255, 255))
            
            fenster.blit(name_t, (r.centerx - name_t.get_width()//2, r.y + 10))
            fenster.blit(deck_t, (r.centerx - deck_t.get_width()//2, r.y + 45))
            fenster.blit(count_t, (r.centerx - count_t.get_width()//2, r.centery - 20))

        # ESC BUTTON IMMER OBEN
        pygame.draw.rect(fenster, (180, 40, 40), esc_knopf, border_radius=5)
        pygame.draw.rect(fenster, (255, 255, 255), esc_knopf, width=1, border_radius=5)
        esc_txt = schrift.render("ESC", True, (255, 255, 255))
        fenster.blit(esc_txt, (esc_knopf.centerx - esc_txt.get_width()//2, esc_knopf.centery - esc_txt.get_height()//2))

        # Gewinner prüfen
        if sum(1 for c in counter if c == 0) >= (anzahl - 1 if anzahl > 2 else 1):
            res = sorted(range(anzahl), key=lambda x: (counter[x], null_zeiten[x] or 9999))
            win_screen(fenster, res, [d["name"] for d in spieler_daten])
            running = False

        pygame.display.flip()
