import pygame

def intro(fenster, breite, hoehe):
    schrift = pygame.font.SysFont("Comic Sans MS", max(30, breite // 20))
    text = schrift.render("presented by Chefkoch Nicki", True, (255, 255, 255))
    text_x = breite // 2 - text.get_width() // 2
    text_y = hoehe // 2 - text.get_height() // 2

    try:
        hintergrund = pygame.image.load("BW.jpg")
        hintergrund = pygame.transform.scale(hintergrund, (breite, hoehe))
    except:
        hintergrund = pygame.Surface((breite, hoehe))
        hintergrund.fill((20, 20, 20))

    # Fade In
    for alpha in range(0, 256, 4):
        fenster.blit(hintergrund, (0, 0))
        text.set_alpha(alpha)
        fenster.blit(text, (text_x, text_y))
        pygame.display.flip()
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]: return True

    pygame.time.delay(1000)

    # Fade Out
    for alpha in range(255, -1, -4):
        fenster.blit(hintergrund, (0, 0))
        text.set_alpha(alpha)
        fenster.blit(text, (text_x, text_y))
        pygame.display.flip()
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]: break

    return True

def hauptmenu(fenster, breite, hoehe):
    schrift = pygame.font.SysFont("Comic Sans MS", max(30, breite // 30))
    # Der Optionen-Knopf ist verschwunden!
    optionen = ["Spiel Starten", "Beenden"]
    
    while True:
        fenster.fill((30, 30, 35))
        maus = pygame.mouse.get_pos()
        knöpfe = []

        for i, option in enumerate(optionen):
            # Zentriert bei 2 Knöpfen
            knopf = pygame.Rect(breite // 2 - 150, hoehe // 2 - 50 + i * 100, 300, 60)
            knöpfe.append(knopf)

            if knopf.collidepoint(maus):
                pygame.draw.rect(fenster, (255, 255, 255), knopf, border_radius=10, width=2)
                farbe = (255, 255, 255)
            else:
                pygame.draw.rect(fenster, (150, 150, 150), knopf, border_radius=10, width=2)
                farbe = (150, 150, 150)

            text = schrift.render(option, True, farbe)
            fenster.blit(text, (knopf.centerx - text.get_width() // 2, knopf.centery - text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, knopf in enumerate(knöpfe):
                    if knopf.collidepoint(event.pos):
                        if optionen[i] == "Beenden":
                            return None
                        if optionen[i] == "Spiel Starten":
                            return "Spiel Starten"

        pygame.display.flip()
