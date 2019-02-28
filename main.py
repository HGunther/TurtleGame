import arcade
import os
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Awesome Game!"

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Setup game
        self.score = 0

        # Set up the player
        self.player_sprite = arcade.Sprite("images/turtle.png",
                                           0.2)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)

        for i in range(10):
            self.add_new_coin()

        # -- Set up the walls
        for x in range(173, 650, 64):
            wall = arcade.Sprite("images/crate.png", 0.3)
            wall.center_x = x
            wall.center_y = 200
            self.wall_list.append(wall)
        for y in range(273, 500, 64):
            wall = arcade.Sprite("images/crate.png", 0.3)
            wall.center_x = 465
            wall.center_y = y
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def add_new_coin(self):
        coin = arcade.Sprite("images/coin.png", 0.1)

        # Position the coin
        coin.center_x = random.randrange(SCREEN_WIDTH)
        coin.center_y = random.randrange(SCREEN_HEIGHT)

        # Add the coin to the lists
        self.coin_list.append(coin)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        if self.player_sprite.right >= SCREEN_WIDTH and self.player_sprite.change_x > 0:
            self.player_sprite.change_x = 0
        elif self.player_sprite.left <= 0 and self.player_sprite.change_x < 0:
            self.player_sprite.change_x = 0
        if self.player_sprite.top >= SCREEN_HEIGHT and self.player_sprite.change_y > 0:
            self.player_sprite.change_y = 0
        if self.player_sprite.bottom <= 0 and self.player_sprite.change_y < 0:
            self.player_sprite.change_y = 0

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        coins_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.kill()
            self.add_new_coin()
            self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
