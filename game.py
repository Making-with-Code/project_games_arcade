################################################################################
# your game file
# ------------------
# feel free to take pieces of the example games and adapt them for your game
################################################################################

import arcade

TILE_SCALING = 1
PLAYER_SCALING = 1.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Game Platformer Example"
SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING


# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 20
GRAVITY = 1.1


class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.game_over = False
        self.score = 0
        
     
        """Set up the game and initialize the variables."""

        # Set up the player
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            "assets/sprites/ninja_frog.png",
            PLAYER_SCALING,
        )

        self.player_sprite.center_x = 196
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite)

        # sets up map
        map_name = "assets/map/project_map.tmj"

        layer_options = {
            "Walls": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
            "End": {"use_spatial_hash": True},
            "Background": {"use_spatial_hash": False},
        }

        # read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, layer_options=layer_options, scaling=TILE_SCALING
        )

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # sets wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["Walls"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]
        self.background_list = self.tile_map.sprite_lists["Background"]
        self.end_list = self.tile_map.sprite_lists["End"]

  
        # sets the background color
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)


        # Keep player from running through the wall_list layer
        walls = [self.wall_list, ]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls, gravity_constant=GRAVITY
        )

        # sets up camera 
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # center camera on user
        self.pan_camera_to_user()


    def on_draw(self):
        """
        Render the screen.
        """

        # These commands must happen before we start drawing
        self.camera.use()
        self.clear()

        # draw all the sprites and map
        self.wall_list.draw()
        self.coin_list.draw()
        self.background_list.draw()
        self.end_list.draw()
        self.player_list.draw()

        # draw game over text if condition met
        if self.game_over:
            arcade.draw_text(
                f"Game Over - Score {self.score}",
                self.player_sprite.center_x + 50,
                self.player_sprite.center_y + 100,
                arcade.color.BLACK,
                30,
            )

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Call update on all sprites
        if not self.game_over:
            self.physics_engine.update()

        # if player hits the 'End' map layer, end game
        if arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.end_list
        ):
            self.game_over = True


        # if player hits coins
        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

        # Pan to the user
        self.pan_camera_to_user()

    def pan_camera_to_user(self):
        """ Manage Scrolling """

        panning_fraction = 0.12

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 3)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 3
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)


if __name__ == "__main__":
    window = MyGame()
    arcade.run()