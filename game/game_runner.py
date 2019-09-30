"""Pygame renderer for the game logic."""

import logging
import pygame as pg
import pygame.freetype as ft
from .game import Game
from . import constants as c

LOG = logging.getLogger(__name__)

class GameRunner: # pylint: disable=too-few-public-methods
    """Pygame renderer for the game logic."""

    size = width, height = c.SCREEN_WIDTH, c.SCREEN_HEIGHT
    clock = pg.time.Clock()

    def __init__(self, game=Game(height=c.SCREEN_HEIGHT)):
        LOG.info("Initializing GameRunner with display size %sx%s", self.width, self.height)
        self.game = game
        pg.init()
        pg.display.set_caption(c.GAME_TITLE)
        self.font = ft.Font(None, 24)
        self.screen = pg.display.set_mode(self.size)
        self.player_pos_y = self.height - c.PLAYER_SPRITE_HOVER
        self.player_height = c.PLAYER_SPRITE_HEIGHT

    def _handle_event(self, event):
        LOG.debug("Handling event type %s", event.type)
        if event.type == pg.QUIT:
            ft.quit()
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.game.move_player_left()
            elif event.key == pg.K_RIGHT:
                self.game.move_player_right()
            elif event.key == pg.K_r:
                self.game.reset()
            elif event.key == pg.K_p:
                self.game.toggle_pause()

    def _render_frame(self):
        delta_time = self.clock.tick(c.TARGET_FRAMERATE)
        LOG.debug("Rendering frame %d ms since last frame", delta_time)
        self.game.advance_time(delta_time)
        if self.game.collision:
            fill_color = c.OBSTACLE_SPRITE_COLOR
            obs_color = c.SCREEN_FILL_COLOR
            score_color = c.PLAYER_SPRITE_COLOR
        else:
            fill_color = c.SCREEN_FILL_COLOR
            obs_color = c.OBSTACLE_SPRITE_COLOR
            score_color = c.SCORE_COLOR
        self.screen.fill(fill_color)

        # calculate player position and draw
        rect = self._get_rect(self.game.player_lane, self.player_pos_y)
        pg.draw.rect(self.screen, c.PLAYER_SPRITE_COLOR, rect)

        # draw obstacles
        for obs in self.game.obstacles:
            rect = self._get_rect(obs.lane, obs.pos)
            pg.draw.rect(self.screen, obs_color, rect)

        # draw score
        self.font.render_to(self.screen, c.SCORE_POSITION, str(self.game.score), score_color)

        # flip frame
        pg.display.flip()

    def _get_rect(self, lane, pos_y):
        area_width = self.width / self.game.lane_count
        pos_x = area_width * lane + c.PLAYER_SPRITE_PADDING
        width = area_width - (c.PLAYER_SPRITE_PADDING * 2)
        return (pos_x, pos_y, width, self.player_height)

    def run(self):
        """Run the game until the player exits."""
        while 1:
            for event in pg.event.get():
                self._handle_event(event)
            self._render_frame()
