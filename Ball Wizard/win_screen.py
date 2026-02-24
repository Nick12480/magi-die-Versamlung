import pygame

def win_screen(fenster, plaetzierung, namen):
    breite, hoehe = fenster.get_size()
    schrift_titel = pygame.font.SysFont("Comic Sans MS", max(40, breite // 20))
    schrift_gross = pygame.font.SysFont("Comic Sans MS", max(28, breite // 35))
    schrift_klein = pygame.font.SysFont("Comic Sans MS", max(20, breite // 50))

    farben_podium = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (100, 100, 120)]
    podium_hoehen = [200, 150, 100, 50]
    podium_breite = breite // 6
    podium_y_basis = hoehe - 150
    
    podium_positionen = [
        breite // 2 - podium_breite // 2,
        breite // 2 - podium_breite * 2,
        breite // 2 + podium_breite,
        breite // 2 + podium_breite * 2 + 20
    ]

    running = True
    while running:
        fenster.fill((20, 20, 25))
        maus = pygame.mouse.get_pos()

        titel = schrift_titel.render("Spiel Beendet!", True, (255, 255, 255))
        fenster.blit(titel, (breite // 2 - titel.get_width() // 2, 50))

        for i in range(len(plaetzierung)):
            spieler_idx = plaetzierung[i]
            x_pos = podium_positionen[i]
            p_hoehe = podium_hoehen[i]
            
            rect = pygame.Rect(x_pos, podium_y_basis - p_hoehe, podium_breite, p_hoehe)
            pygame.draw.rect(fenster, farben_podium[i], rect)
            pygame.draw.rect(fenster, (255, 255, 255), rect, width=2)

            zahl = schrift_gross.render(str(i + 1), True, (0, 0, 0))
            fenster.blit(zahl, (rect.centerx - zahl.get_width() // 2, rect.y + 10))

            name_txt = schrift_klein.render(namen[spieler_idx], True, (255, 255, 255))
            fenster.blit(name_txt, (rect.centerx - name_txt.get_width() // 2, rect.y - 35))

        zurueck_knopf = pygame.Rect(breite // 2 - 150, hoehe - 70, 300, 50)
        z_farbe = (255, 255, 255) if zurueck_knopf.collidepoint(maus) else (150, 150, 150)
        pygame.draw.rect(fenster, z_farbe, zurueck_knopf, border_radius=8, width=2)
        
        z_text = schrift_klein.render("Zurück zum Hauptmenü", True, z_farbe)
        fenster.blit(z_text, (zurueck_knopf.centerx - z_text.get_width() // 2, zurueck_knopf.centery - z_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if zurueck_knopf.collidepoint(event.pos):
                    running = False

        pygame.display.flip()