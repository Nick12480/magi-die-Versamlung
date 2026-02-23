run:
	python3 main.py

install:
	pip install pygame

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

help:
	@echo "Verfügbare Befehle:"
	@echo "  make run      - Spiel starten"
	@echo "  make install  - pygame installieren"
	@echo "  make clean    - Cache löschen"

.PHONY: run install clean help