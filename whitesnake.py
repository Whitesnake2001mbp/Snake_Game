import pygame 
import random

# Initialize the game
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")
# Set up the game clock
clock = pygame.time.Clock()
# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
# Define the frame count
frame_count = 0
# Set up the snake
snake_block_size = 20
snake_speed = 10

# Function to draw the snake
def draw_snake(snake_block_size, snake_list):
    for i, block in enumerate(snake_list):
        if i == len(snake_list) - 1:  # If this is the last block (the head)
            pygame.draw.rect(window, white, [block[0], block[1], snake_block_size, snake_block_size])
            pygame.draw.circle(window, black, (block[0] + snake_block_size // 2, block[1] + snake_block_size // 2), snake_block_size // 3)
        else:
            pygame.draw.rect(window, white, [block[0], block[1], snake_block_size, snake_block_size])

class Fire:
    def __init__(self, window):
        self.x = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
        self.y = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0 
        self.window = window
    
    def draw(self):
        pygame.draw.rect(self.window, red, [self.x, self.y, snake_block_size, snake_block_size])
    
    def reset_position(self):
        self.x = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
        self.y = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0 

# Main game loop
def game_loop():
    global frame_count
    game_over = False
    game_quit = False
    
    # Initial position of the snake
    x1 = window_width / 2
    y1 = window_height / 2
    # Initial movement direction of the snake
    x1_change = 0
    y1_change = 0
    # Create an empty list to store the snake's body parts
    snake_list = []
    snake_length = 1
    # Generate the initial position of the food
    food_x = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0
    # Create a list of fires
    fires = [Fire(window) for _ in range(5)]
    
    while not game_quit:
        window.fill(black)
        font_style = pygame.font.SysFont(None, 40)
        # Print length (left-aligned)
        length_text = "Length: " + str(snake_length)
        length_surface = font_style.render(length_text, True, white)
        window.blit(length_surface, [10, 10])  # 10 pixels from the left edge of the window
        # Print time played (right-aligned)
        time_text = "Time: " + str(pygame.time.get_ticks() // 1000)  # Convert milliseconds to seconds
        time_surface = font_style.render(time_text, True, white)
        time_width, _ = font_style.size(time_text)  # Get the width of the time text
        window.blit(time_surface, [window_width - time_width - 10, 10])  # 10 pixels from the right edge of the window
        # Print commands (centered)
        move_text = "Use <Arrow> Keys to Move!"
        move_surface = font_style.render(move_text, True, white)
        move_width, _ = font_style.size(move_text)  # Get the width of the move text
        window.blit(move_surface, [(window_width - move_width) / 2, 10])  # Centered horizontally
        
        while game_over:
            # Game over screen
            window.fill(black)
            font_style1 = pygame.font.SysFont(None, 80)
            font_style2 = pygame.font.SysFont(None, 30)
            message_text1 = "Game Over!"
            message_text2 = "Press Q-Quit or P-Play Again!"
            message1 = font_style1.render(message_text1, True, red)
            message2 = font_style2.render(message_text2, True, red)
            
            # Get the width of the messages
            message_width1, message_height1 = font_style1.size(message_text1)
            message_width2, message_height2 = font_style2.size(message_text2)
            
            # Calculate the position to center the messages
            pos_x1 = window_width/2 - message_width1/2 
            pos_y1 = window_height/2 - message_height1
            pos_x2 = window_width/2 - message_width2/2
            pos_y2 = window_height/2 
            
            # Display the Game Over messages
            window.blit(message1, [pos_x1, pos_y1])
            window.blit(message2, [pos_x2, pos_y2])
            pygame.display.update()
            
            # Event handling for game over screen
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_quit = True
                        game_over = False
                    if event.key == pygame.K_p:
                        game_loop()
        
        # Event handling snake movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user clicks the close button
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block_size
                    x1_change = 0
        
        # Check for collision with the boundaries of the window and return to the oposite side
        if x1 >= window_width:
            x1 = 0
        elif x1 < 0:
            x1 = window_width - snake_block_size
        if y1 >= window_height:
            y1 = 0
        elif y1 < 0:
            y1 = window_height - snake_block_size  
        
        #FOOD    
        # Draw the food
        pygame.draw.rect(window, green, [food_x, food_y, snake_block_size, snake_block_size])    
        # Check for collision with the food
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0
            snake_length += 1
        
        #SNAKE
        # Update the position of the snake
        x1 += x1_change
        y1 += y1_change    
        # Update the snake's body
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length: # If the snake's length is greater than the snake_length 
            del snake_list[0]    # Delete the last block of the snake 
        # Check for collision with the snake's body
        for x in snake_list[:-1]:
            if x == snake_head: # If the snake's head collides with its body Game Over
                game_over = True
        # Draw the snake
        draw_snake(snake_block_size, snake_list)
        
        #FIRE
        # Reset fire positions every 30 frames
        if frame_count % (30 * snake_speed) == 0: # Every 30 frames all the fires will change position
            for fire in fires:
                fire.reset_position()
        frame_count += 1
        # Draw the fires
        for fire in fires:
            fire.draw()
        # Check for collision with the fire
        for fire in fires:   
            if x1 == fire.x and y1 == fire.y:
                # Reset the position of the fire
                fire.x = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
                fire.y = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0
                fire.reset_position()
                if snake_length > 1: # If the snake has more than one block 
                    snake_length -= 1
                    del snake_list[0] # Delete the last block 
                else:
                    game_over = True # If the snake has only one block Game Over
        # Update the display
        pygame.display.update()
        # Set the game speed
        clock.tick(snake_speed)
    # Quit the game
    pygame.quit()
# Start the game loop
game_loop()
