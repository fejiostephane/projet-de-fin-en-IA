import pygame
import random

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre et de la carte
tile_size = 30
size = 20
width, height = size * tile_size, size * tile_size
interface_height = 150  # Hauteur supplémentaire pour l'interface

# Couleurs
PASSABLE_COLOR = (200, 200, 200)        # Gris clair pour les cases passables
PLAYER_COLOR = (0, 0, 255)              # Bleu pour le joueur
PLAYER_COLOR_LIGHT = (100, 100, 255)    # Bleu clair pour le joueur capable de bouger
ENEMY_COLOR = (255, 0, 0)               # Rouge pour les ennemis
ENEMY_COLOR_LIGHT = (255, 100, 100)     # Rouge clair pour les ennemis capables de bouger
SELECTED_COLOR = (0, 255, 0)            # Vert pour la sélection
OBJECTIVE_MAJOR_COLOR = (255, 255, 0)   # Jaune pour objectif majeur
OBJECTIVE_MINOR_COLOR = (255, 215, 0)   # Doré pour objectif mineur

# Classe pour les unités
class Unit:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.selected = False
        self.moved = False  # Indicateur de mouvement pour le tour
        self.pv = 2  # Points de Vie
        self.attacked_this_turn = False  # Indicateur d'attaque dans ce tour

    def draw(self, screen, units, objectives):
        """Affiche l'unité sur l'écran."""
        rect = pygame.Rect(self.x * tile_size, self.y * tile_size, tile_size, tile_size)
        if not self.moved:
            color = PLAYER_COLOR_LIGHT if self.color == PLAYER_COLOR else ENEMY_COLOR_LIGHT
        else:
            color = self.color
        pygame.draw.rect(screen, color, rect)

        if self.selected:
            pygame.draw.rect(screen, SELECTED_COLOR, rect, 3)

        font = pygame.font.SysFont(None, 16)
        symbols = self.get_symbols_on_same_tile(units)
        combined_text = font.render(symbols, True, (255, 255, 255))
        text_width = combined_text.get_width()
        text_x = self.x * tile_size + (tile_size - text_width) // 2
        screen.blit(combined_text, (text_x, self.y * tile_size + 5))

        for obj in objectives:
            if self.x == obj['x'] and self.y == obj['y']:
                pygame.draw.rect(screen, (0, 255, 0), rect, 1)

    def can_move(self, x, y):
        """Vérifie si l'unité peut se déplacer vers une case."""
        if 0 <= x < size and 0 <= y < size:
            if abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
                return True
        return False
    
    def move(self, x, y):
        """Déplace l'unité vers une case spécifiée."""
        self.x = x
        self.y = y
        self.moved = True

    def attack(self, target_unit, units, objectives):
        """Attaque une unité ennemie."""
        if self.can_move(target_unit.x, target_unit.y):
            dx = target_unit.x - self.x
            dy = target_unit.y - self.y
            new_x, new_y = target_unit.x + dx, target_unit.y + dy

            if target_unit.attacked_this_turn:
                target_unit.pv -= 1
                target_unit.attacked_this_turn = False
                if target_unit.pv <= 0:
                    units.remove(target_unit)
                    return
                elif 0 <= new_x < size and 0 <= new_y < size:
                    if any(u.x == new_x and u.y == new_y and u.color != target_unit.color for u in units) or any(obj['x'] == new_x and obj['y'] == new_y and obj['type'] == 'MAJOR' for obj in objectives):
                        units.remove(target_unit)
                    else:
                        target_unit.move(new_x, new_y)
            else:
                if 0 <= new_x < size and 0 <= new_y < size:
                    if any(u.x == new_x and u.y == new_y and u.color != target_unit.color for u in units) or any(obj['x'] == new_x and obj['y'] == new_y for obj in objectives):
                        units.remove(target_unit)
                    else:
                        target_unit.move(new_x, new_y)
                        target_unit.attacked_this_turn = True

    def get_symbols_on_same_tile(self, units):
        """Retourne les symboles des unités sur la même case."""
        symbols = [u.get_symbol() for u in units if u.x == self.x and u.y == self.y]
        return ' '.join(symbols)

    def get_symbol(self):
        """Retourne le symbole de l'unité."""
        return "U"

# Générer la carte
def generate_map(size):
    """Génère une carte de taille spécifiée."""
    return [[1 for _ in range(size)] for _ in range(size)]
