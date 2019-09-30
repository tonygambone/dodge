"""Implementation of the game logic."""

import random
from . import constants as c

class Game: # pylint: disable=too-many-instance-attributes
    """Game logic instance."""
    obstacles_per_second = c.DEFAULT_OBSTACLES_PER_SECOND

    def __init__(self, height=c.SCREEN_HEIGHT):
        self._height = height
        self._score = None
        self._player_lane = None
        self._lane_count = None
        self._seconds_since_last_obstacle = None
        self._obstacles = None
        self._collision = None
        self._paused = None
        self.reset()

    def move_player_left(self):
        """Move the player left one lane, if a lane is available."""
        if self._collision:
            return
        if self._player_lane != 0:
            self._player_lane = self._player_lane - 1

    def move_player_right(self):
        """Move the player right one lane, if a lane is available."""
        if self._collision:
            return
        if self._player_lane < self._lane_count - 1:
            self._player_lane = self._player_lane + 1

    def _update_obstacles(self, milliseconds):
        # update obstacle position
        for obs in self._obstacles:
            obs.pos = obs.pos + (obs.speed * milliseconds / 1000)

        # remove offscreen obstacles and update score
        obs_count = len(self._obstacles)
        self._obstacles = [obs for obs in self._obstacles if obs.pos < self._height + 200]
        self._score = self._score + obs_count - len(self._obstacles)

        # add new obstacle
        self._seconds_since_last_obstacle = \
            self._seconds_since_last_obstacle + (milliseconds / 1000)
        if self._seconds_since_last_obstacle > self.obstacles_per_second:
            lane = random.randrange(0, self._lane_count)
            speed = random.randrange(c.OBSTACLE_MIN_SPEED, c.OBSTACLE_MAX_SPEED)
            self._obstacles.append(Obstacle(lane, speed))
            self._seconds_since_last_obstacle = 0

    def _detect_collision(self):
        """Detect if there's a collision with an obstacle."""
        obs_min_y = c.SCREEN_HEIGHT - c.PLAYER_SPRITE_HOVER - c.PLAYER_SPRITE_HEIGHT
        obs_max_y = c.SCREEN_HEIGHT - c.PLAYER_SPRITE_HOVER + c.PLAYER_SPRITE_HEIGHT
        self._collision = len([obs for obs in self._obstacles if
                               obs.lane == self._player_lane
                               and obs.pos >= obs_min_y
                               and obs.pos <= obs_max_y]) > 0

    def advance_time(self, milliseconds):
        """Advance the game time by a certain number of milliseconds."""
        if self._collision or self._paused:
            return
        self._update_obstacles(milliseconds)
        self._detect_collision()

    def reset(self):
        """Resets the game to its original state."""
        self._score = 0
        self._player_lane = c.DEFAULT_LANE_COUNT // 2
        self._lane_count = c.DEFAULT_LANE_COUNT
        self._seconds_since_last_obstacle = 0
        self._obstacles = []
        self._collision = False
        self._paused = False

    def toggle_pause(self):
        """Pauses or unpauses the game."""
        self._paused = not self._paused

    @property
    def collision(self):
        """Whether the game is in a collision state (encountered obstacle)"""
        return self._collision

    @property
    def player_lane(self):
        """The current player lane index"""
        return self._player_lane

    @property
    def lane_count(self):
        """The current total lane count"""
        return self._lane_count

    @property
    def obstacles(self):
        """The current obstacle list"""
        return self._obstacles

    @property
    def score(self):
        """The current score"""
        return self._score

class Obstacle: # pylint: disable=too-few-public-methods
    """Represents one obstacle in the game."""
    def __init__(self, lane, speed=200, pos=0):
        self.lane = lane
        self.speed = speed
        self.pos = pos
