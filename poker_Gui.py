import math
import pyglet
from playerHand import *
from pokerEngine import start_hand
from PIL import Image

WINDOW_SIZE_X, WINDOW_SIZE_Y = 1000, 750

# Open the background image
backgroundImage = Image.open('bgimage.jpg')

# Resize the background image
resized_backgroundImage = backgroundImage.resize((WINDOW_SIZE_X, WINDOW_SIZE_Y))

# Create a Pyglet window with the specified size
new_window = pyglet.window.Window(width=WINDOW_SIZE_X, height=WINDOW_SIZE_Y)

# Define the number of players and empty lists for positions and sprites

player_Count = 6
SMALL_BLIND = 5
BIG_BLIND = 10


position_list = []
button_position_list = []
player_sprites = []

# Calculate the desired size of the player icon based on the window size and player count
PLAYER_ICON_SIZE_X = WINDOW_SIZE_X / 17
PLAYER_ICON_SIZE_Y = WINDOW_SIZE_Y / 17

BOARD_CARD_SIZE_X = PLAYER_ICON_SIZE_X * 1.2
BOARD_CARD_SIZE_Y = PLAYER_ICON_SIZE_Y * 1.2

# Create a Pyglet sprite from the resized background image
pokerTable_Sprite = pyglet.sprite.Sprite(pyglet.image.ImageData(
    WINDOW_SIZE_X, WINDOW_SIZE_Y, 'RGB', resized_backgroundImage.tobytes()))

# Load the player icon image
pokerPlayerIcon = pyglet.image.load('playerIcon.png')
pokerPlayerIcon_Sprite = pyglet.sprite.Sprite(pokerPlayerIcon)

# Load the dealer button icon image
dealerButton = pyglet.image.load('dealerButton.png')
dealerButton_Sprite = pyglet.sprite.Sprite(dealerButton)
dealerButton_Sprite.update(scale_x=PLAYER_ICON_SIZE_X / dealerButton.width, scale_y=PLAYER_ICON_SIZE_Y / dealerButton.height)


class PlayerSprite(pyglet.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

        #create pokerPlayer sprite with name from position list and initial stack varying in some range
        self.player = pokerPlayer(str(position_list[random.randint(0, len(position_list) - 1)]), random.randrange(800, 2500, 10))
        self.current_position = ''
        self.scale = PLAYER_ICON_SIZE_X / pokerPlayerIcon.width  # Scale the sprite

        self.stack_label = pyglet.text.Label(
            f"${self.player.getStackSize()}",
            font_name='Arial',
            font_size=12,
            x=self.x,
            y=self.y - 20,
            anchor_x='center',
            anchor_y='center'
        )
        self.stack_label_BB = pyglet.text.Label(
            f"{self.player.getStackSize() / BIG_BLIND} BBs",
            font_name='Arial',
            font_size=12,
            x=self.stack_label.x,
            y=self.stack_label.y - 20,
            anchor_x='center',
            anchor_y='center'
        )
        self.test_Label = pyglet.text.Label(
            f"VPIP: {round(self.player.frequencies.get_VPIP() / 100, 2)}",
            font_name='Arial',
            font_size=12,
            x=self.stack_label.x,
            y=self.stack_label_BB.y - 20,
            anchor_x='center',
            anchor_y='center'
        )
      
    def draw(self):
        super().draw()
        self.stack_label.draw()
        self.stack_label_BB.draw()
        self.test_Label.draw()

class CommunityCards():
    def __init__(self):
        self.currentHandCommunity = HandGenerator(player_Count)
        self.preflop = self.currentHandCommunity.dealPreFlop()
        self.flop = self.currentHandCommunity.dealFlop()
        self.turn = self.currentHandCommunity.dealTurn()
        self.river = self.currentHandCommunity.dealRiver()

        # Load card images and determine their sizes
        flop_card1_image = pyglet.image.load(self.flop[0] + '.png')
        flop_card2_image = pyglet.image.load(self.flop[1] + '.png')
        flop_card3_image = pyglet.image.load(self.flop[2] + '.png')
        turn_card_image = pyglet.image.load(str(self.turn[0]) + '.png')
        river_card_image = pyglet.image.load(str(self.river[0]) + '.png')

        self.card_width = flop_card1_image.width / PLAYER_ICON_SIZE_X  # Assuming all cards have the same width
        self.card_height = flop_card1_image.height / PLAYER_ICON_SIZE_Y  # Assuming all cards have the same height

        # Create batches for efficient rendering
        self.flop_batch = pyglet.graphics.Batch()
        self.turn_batch = pyglet.graphics.Batch()
        self.river_batch = pyglet.graphics.Batch()

        # Create sprites for the community cards and position them
        self.flop_card1 = pyglet.sprite.Sprite(flop_card1_image, batch=self.flop_batch)
        self.flop_card1.update(scale_x=BOARD_CARD_SIZE_X / flop_card1_image.width,
                               scale_y=BOARD_CARD_SIZE_X / flop_card1_image.height)

        self.flop_card2 = pyglet.sprite.Sprite(flop_card2_image, batch=self.flop_batch)
        self.flop_card2.update(scale_x=BOARD_CARD_SIZE_X / flop_card2_image.width,
                               scale_y=BOARD_CARD_SIZE_X / flop_card2_image.height)

        self.flop_card3 = pyglet.sprite.Sprite(flop_card3_image, batch=self.flop_batch)
        self.flop_card3.update(scale_x=BOARD_CARD_SIZE_X / flop_card3_image.width,
                               scale_y=BOARD_CARD_SIZE_X / flop_card3_image.height)

        self.turn_card = pyglet.sprite.Sprite(turn_card_image, batch=self.turn_batch)
        self.turn_card.update(scale_x=BOARD_CARD_SIZE_X / turn_card_image.width,
                              scale_y=BOARD_CARD_SIZE_X / turn_card_image.height)

        self.river_card = pyglet.sprite.Sprite(river_card_image, batch=self.river_batch)
        self.river_card.update(scale_x=BOARD_CARD_SIZE_X / river_card_image.width,
                               scale_y=BOARD_CARD_SIZE_X / river_card_image.height)

    def set_window_size(self, window_width, window_height):
        self.calculate_positions(window_width, window_height)

    def calculate_positions(self, window_width, window_height):
        # Calculate the position of the center of the window
        center_x = window_width // 2
        center_y = window_height // 2

        # Update the position of flop cards
        self.flop_card1.x = center_x - window_width / 6
        self.flop_card1.y = center_y

        self.flop_card2.x = self.flop_card1.x + self.flop_card2.width
        self.flop_card2.y = center_y

        self.flop_card3.x = self.flop_card2.x + self.flop_card3.width
        self.flop_card3.y = center_y

        # Update the position of turn card
        self.turn_card.x = self.flop_card3.x + self.turn_card.width
        self.turn_card.y = center_y

        # Update the position of river card
        self.river_card.x = self.turn_card.x + self.river_card.width
        self.river_card.y = center_y
    
    def setPlayer(self, name, firstCard, secondCard):
        return 0

    def get_batches(self):
        return self.flop_batch, self.turn_batch, self.river_batch

    def get_cards(self):
        return [self.flop_card1, self.flop_card2, self.flop_card3, self.turn_card, self.river_card]


# Organize player seat positions geometrically
def seating_position_Generator(total_players):
    ellipse_center = (WINDOW_SIZE_X / 2, WINDOW_SIZE_Y / 2)
    ellipse_radius_x, ellipse_radius_y = WINDOW_SIZE_X / 3, WINDOW_SIZE_Y / 3
    num_divisions = total_players

    for i in range(total_players):
        angle = 2 * math.pi * i / num_divisions
        x = round(ellipse_center[0] + math.cos(angle) * ellipse_radius_x - (PLAYER_ICON_SIZE_X / 2),2)
        button_X = x - PLAYER_ICON_SIZE_X
        y = round(ellipse_center[1] + math.sin(angle) * ellipse_radius_y - (PLAYER_ICON_SIZE_Y / 2), 2)
        button_Y = y +  PLAYER_ICON_SIZE_Y
        position_list.append((x, y))
        button_position_list.append((button_X, button_Y))
    return position_list

def buttonPosition():
    
    for i, j in button_position_list:
        dealerButton_Sprite.update(x = i , y = j , scale_x=PLAYER_ICON_SIZE_X / dealerButton.width,
                                scale_y=PLAYER_ICON_SIZE_Y / dealerButton.height)

seating_position_Generator(player_Count)
# Generate the seating positions and create sprites for each position
for i, position in enumerate(position_list):
    stack_size = 1000  # Set the stack size for the player
    sprite = PlayerSprite(image=pokerPlayerIcon, x=position[0], y=position[1])
    sprite.scale = PLAYER_ICON_SIZE_X / pokerPlayerIcon.width
    player_sprites.append(sprite)

start_hand()

@new_window.event
def on_draw():
    new_window.clear()
    pokerTable_Sprite.draw()
    dealerButton_Sprite.draw()

    for sprite in player_sprites:
        sprite.draw()

# Event handler for mouse press
@new_window.event
def on_mouse_press(x, y, button, modifiers):
    for sprite in player_sprites:
        if sprite.x < x < sprite.x + sprite.width and sprite.y < y < sprite.y + sprite.height:
            sprite.on_button_click(x, y, button, modifiers)

# Start the game
pyglet.app.run()


