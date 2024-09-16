import pygame
import random
import sys
import os

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize PyGame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Quiz Challenge')

# Load images
student_img = pygame.image.load('student.png')
student_img = pygame.transform.scale(student_img, (40, 40))

question_bubble_img = pygame.image.load('question_bubble.png')
question_bubble_img = pygame.transform.scale(question_bubble_img, (40, 40))

book_of_knowledge_img = pygame.image.load('book_of_knowledge.png')
book_of_knowledge_img = pygame.transform.scale(book_of_knowledge_img, (40, 40))

# Define colors
BLACK = (0, 0, 0)
RETRO_GREEN = (0, 255, 0)
RETRO_RED = (255, 0, 0)
RETRO_YELLOW = (255, 255, 0)
RETRO_BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Set up fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = student_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5  # Adjust as needed for 'move quickly'

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        # Keep player on the screen
        self.rect.clamp_ip(window.get_rect())

# Define QuestionBubble class
class QuestionBubble(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = question_bubble_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(0, HEIGHT - 40)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def update(self, *args):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Bounce off the walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy *= -1

# Define BookOfKnowledge class
class BookOfKnowledge(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = book_of_knowledge_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(0, HEIGHT - 40)

    def update(self, *args):
        pass  # The book doesn't move

# Sample questions
questions = [
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What color do you get when you mix red and white?", "answer": "Pink"},
    {"question": "Who wrote 'Hamlet'?", "answer": "Shakespeare"},
    {"question": "What is the chemical symbol for water?", "answer": "H2O"},
    # Add more questions as needed
]

# Game variables
score = 0
lives = 3
max_score = 10  # Score needed to win
game_over = False

# Sprite groups
all_sprites = pygame.sprite.Group()
question_bubbles = pygame.sprite.Group()
books_of_knowledge = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Spawn initial question bubbles
for _ in range(5):
    bubble = QuestionBubble()
    all_sprites.add(bubble)
    question_bubbles.add(bubble)

# Timers
book_spawn_time = pygame.time.get_ticks()
book_interval = 15000  # Book appears every 15 seconds

clock = pygame.time.Clock()

# Game states
INTRO = 'intro'
PLAYING = 'playing'
QUESTION = 'question'
GAME_OVER = 'game_over'

state = INTRO

# Input buffer for answering questions
input_text = ''

# Main game loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == INTRO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = PLAYING
        elif state == QUESTION:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check the answer
                    if input_text.strip().lower() == current_question['answer'].lower():
                        score += 1
                    else:
                        lives -= 1
                    input_text = ''
                    state = PLAYING
                    if lives <= 0 or score >= max_score:
                        state = GAME_OVER
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        elif state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset the game
                    score = 0
                    lives = 3
                    # Reset player position
                    player.rect.center = (WIDTH // 2, HEIGHT // 2)
                    # Remove all question bubbles and books
                    question_bubbles.empty()
                    books_of_knowledge.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    # Spawn initial question bubbles
                    for _ in range(5):
                        bubble = QuestionBubble()
                        all_sprites.add(bubble)
                        question_bubbles.add(bubble)
                    state = PLAYING

    if state == PLAYING:
        all_sprites.update(keys_pressed)
        # Check for collisions with question bubbles
        bubble_hit_list = pygame.sprite.spritecollide(player, question_bubbles, True)
        for bubble in bubble_hit_list:
            if questions:
                current_question = random.choice(questions)
                state = QUESTION
            else:
                # No questions left
                state = GAME_OVER
        # Check for collisions with books of knowledge
        book_hit_list = pygame.sprite.spritecollide(player, books_of_knowledge, True)
        for book in book_hit_list:
            score += 2
            lives += 1

        # Spawn books of knowledge at intervals
        if pygame.time.get_ticks() - book_spawn_time > book_interval:
            book = BookOfKnowledge()
            all_sprites.add(book)
            books_of_knowledge.add(book)
            book_spawn_time = pygame.time.get_ticks()

    # Drawing
    window.fill(BLACK)

    if state == INTRO:
        # Display instructions
        intro_text1 = font.render("Welcome to Quiz Challenge!", True, RETRO_GREEN)
        intro_text2 = small_font.render("Use the arrow keys to move.", True, WHITE)
        intro_text3 = small_font.render("Collect question bubbles and answer questions.", True, WHITE)
        intro_text4 = small_font.render("Collect the Book of Knowledge for extra points and lives.", True, WHITE)
        intro_text5 = small_font.render("Press SPACE to start.", True, RETRO_YELLOW)
        window.blit(intro_text1, (WIDTH//2 - intro_text1.get_width()//2, HEIGHT//2 - 100))
        window.blit(intro_text2, (WIDTH//2 - intro_text2.get_width()//2, HEIGHT//2 - 50))
        window.blit(intro_text3, (WIDTH//2 - intro_text3.get_width()//2, HEIGHT//2 - 20))
        window.blit(intro_text4, (WIDTH//2 - intro_text4.get_width()//2, HEIGHT//2 + 10))
        window.blit(intro_text5, (WIDTH//2 - intro_text5.get_width()//2, HEIGHT//2 + 60))
    elif state == PLAYING:
        all_sprites.draw(window)
        # Display 'Education', score, and lives
        title_text = font.render("Education", True, RETRO_BLUE)
        window.blit(title_text, (10, 10))
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        lives_text = small_font.render(f"Lives: {lives}", True, WHITE)
        window.blit(score_text, (WIDTH - 150, 10))
        window.blit(lives_text, (WIDTH - 150, 40))
    elif state == QUESTION:
        # Display the question and input field
        question_text = font.render(current_question['question'], True, RETRO_GREEN)
        input_box = font.render(input_text, True, RETRO_YELLOW)
        window.blit(question_text, (WIDTH//2 - question_text.get_width()//2, HEIGHT//2 - 50))
        window.blit(input_box, (WIDTH//2 - input_box.get_width()//2, HEIGHT//2))
    elif state == GAME_OVER:
        # Display Game Over screen
        if lives <= 0:
            game_over_text = font.render("Game Over!", True, RETRO_RED)
        else:
            game_over_text = font.render("You Win!", True, RETRO_GREEN)
        final_score_text = small_font.render(f"Final Score: {score}", True, WHITE)
        restart_text = small_font.render("Press SPACE to restart.", True, RETRO_YELLOW)
        window.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        window.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
        window.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
