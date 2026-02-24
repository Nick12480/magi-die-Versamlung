import pygame


def spielmodus_auswahl(fenster, breite, hoehe):
    """
    Zeigt die Spielmodus-Auswahl zwischen Hauptmenü und Config.
    Gibt den gewählten Modus als String zurück oder None bei Abbruch.
    """
    schrift = pygame.font.SysFont("Comic Sans MS", max(30, breite // 30))
    schrift_titel = pygame.font.SysFont("Comic Sans MS", max(40, breite // 20))

    modi = ["Jumpstart", "Commander (EDH)"]

    while True:
        fenster.fill((30, 30, 35))
        maus = pygame.mouse.get_pos()

        # Titel
        titel = schrift_titel.render(
            "Spielmodus wählen", True, (255, 215, 0)
        )
        fenster.blit(titel, (
            breite // 2 - titel.get_width() // 2,
            hoehe // 4
        ))

        knöpfe = []
        for i, modus in enumerate(modi):
            knopf = pygame.Rect(
                breite // 2 - 180,
                hoehe // 2 - 30 + i * 110,
                360, 70
            )
            knöpfe.append(knopf)

            if knopf.collidepoint(maus):
                pygame.draw.rect(
                    fenster, (255, 255, 255), knopf,
                    border_radius=10, width=2
                )
                farbe = (255, 255, 255)
            else:
                pygame.draw.rect(
                    fenster, (150, 150, 150), knopf,
                    border_radius=10, width=2
                )
                farbe = (150, 150, 150)

            text = schrift.render(modus, True, farbe)
            fenster.blit(text, (
                knopf.centerx - text.get_width() // 2,
                knopf.centery - text.get_height() // 2
            ))

        # Zurück Knopf
        zurueck = pygame.Rect(20, hoehe - 60, 120, 40)
        z_farbe = (255, 255, 255) if zurueck.collidepoint(maus) else (150, 150, 150)
        pygame.draw.rect(fenster, z_farbe, zurueck, border_radius=8, width=2)
        z_txt = schrift.render("< Zurück", True, z_farbe)
        fenster.blit(z_txt, (
            zurueck.centerx - z_txt.get_width() // 2,
            zurueck.centery - z_txt.get_height() // 2
        ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if zurueck.collidepoint(event.pos):
                    return None
                for i, knopf in enumerate(knöpfe):
                    if knopf.collidepoint(event.pos):
                        return modi[i]

        pygame.display.flip()
