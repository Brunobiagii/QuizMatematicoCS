import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (127, 0, 255)

# Initialize the Pygame display before loading images
pygame.display.set_mode((800, 600))  # Set your initial screen size here

selected_answer = None

# Function to set screen size based on an image
def set_screen_size(image_path):
    image = pygame.image.load(os.path.join(image_path)).convert()
    return image.get_width(), image.get_height()

# Dictionary of operations and their descriptions
operations = {'+': 'Adição', '-': 'Subtração', '*': 'Multiplicação', '/': 'Divisão'}

# Global variables
selected_operation = None
current_question = None
balloons = None
pontos = 0
arrow = None
arrowbox = None
base_button = pygame.image.load("botao.png")

button_size = 104
button_spacing = 40

# Dictionary of background images for different operations
background_images = {'+': 'ad.jpg', '-': 'sub.jpg', '*': 'mul.jpg', '/': 'div.jpg', 'ini': 'ini.jpeg'}
background_image = None

# Initial screen size based on the image "ini.jpeg"
WIDTH, HEIGHT = set_screen_size(background_images['ini'])
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Perguntas e Respostas")

# Sound setup
sound = pygame.mixer.Sound("music.mp3")
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

# Font setup
font = pygame.font.Font("font1.ttf", 50)
font1 = pygame.font.Font("font1.ttf", 75)

# Dictionary of operation images
operation_images = {'+': 'mais.png', '-': 'menos.png', '*': 'mul.png', '/': 'div.png'}
button_images = {operation: pygame.transform.scale(pygame.image.load(os.path.join("botao", filename)).convert_alpha(), (button_size, button_size)) for operation, filename in operation_images.items()}

# Function to generate a random question based on the operation
def generate_question(operation):
    if operation == '/':
        num2 = random.randint(1, 10)
        mult = random.randint(1, 10)
        num1 = num2 * mult
        question_text = f"{num1} {operation} {num2} = ?"
        
        answer = eval(f"{num1}{operation}{num2}")
        answer = int(answer)
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        question_text = f"{num1} {operation} {num2} = ?"
        
        answer = eval(f"{num1}{operation}{num2}")

    return num1, operation, num2, answer, question_text




# Function to create answer balloons
def create_answer_balloons(correct_answer):
    answer_options = [correct_answer]
    while len(answer_options) < 3:
        random_option = random.randint(int(correct_answer) - 3, int(correct_answer) + 3)
        if random_option not in answer_options:
            answer_options.append(random_option)

    random.shuffle(answer_options)

    balloons = []
    wid = WIDTH // 2 - ((button_size + button_spacing) * 3 / 2)
    for option in answer_options:
        balloon_rect = pygame.Rect(wid + (answer_options.index(option)) * (button_size + button_spacing), HEIGHT // 1.5, button_size, button_size)
        balloons.append((option, balloon_rect, option == correct_answer))

    return balloons

# Function to draw operation buttons on the screen
def draw_operation_buttons():
    wid = WIDTH // 2 - ((button_size + button_spacing) * 2)
    for i, (key, value) in enumerate(operations.items()):
        button_rect = pygame.Rect(wid + i * (button_size + button_spacing), HEIGHT // 2, button_size, button_size)
        screen.blit(button_images[key], button_rect)
        operations[key] = button_rect

# Function to draw the score on the screen
def draw_score():
    score_text = font.render(f"Pontos: {pontos}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Function to draw a square box with optional border on the screen
def draw_square_box(surface, rect, color, border_color, border_width):
    border_rect = rect
    #border_rect.topleft(border_rect.x + 5, border_rect+ 5)
    back = pygame.transform.scale(base_button, (rect.width, rect.height))
    pygame.draw.rect(surface, border_color, rect, border_radius=border_width)
    pygame.draw.rect(surface, color, rect)
    #screen.blit(back, (rect.x, rect.y))

# Function to draw the points box on the screen
def draw_points_box():
    points_text = font.render(f"Pontos: {pontos}", True, BLACK)
    points_rect = points_text.get_rect(topleft=(10, 10))
    box_width, box_height = points_rect.width + 40, points_rect.height + 40
    box_rect = pygame.Rect(points_rect.topleft, (box_width, box_height), border=3)
    #draw_square_box(screen, box_rect, PURPLE, BLACK, 5)
    screen.blit(points_text, (points_rect.x + 20, points_rect.y + 20))

# Function to draw the balloons on the screen
def draw_balloons():
    for option, rect, is_correct in balloons:
        x = rect.center[0] - base_button.get_width()/2
        y = rect.center[1] - base_button.get_height()/2
        screen.blit(base_button, (x, y))
        #pygame.draw.rect(screen, BLACK, rect, 2)
        answer_text = font.render(str(option), True, BLACK)
        screen.blit(answer_text, (rect.x + answer_text.get_width()//2, rect.y + answer_text.get_height()//2))

        # Draw purple box around the correct answer only if selected
        if is_correct and selected_answer is not None and selected_answer == option:
            pygame.draw.rect(screen, PURPLE, rect, 2)  # Use PURPLE color for the correct answer
        elif is_correct and selected_answer is not None and selected_answer != option:
            pygame.draw.rect(screen, BLACK, rect, 2)  # Draw black border for correct but not selected answer

# Main function
def main():
    global selected_operation, current_question, balloons, pontos, background_image, WIDTH, HEIGHT, screen, selected_answer  # Declare screen as a global variable

    # Load and display the initial background image
    initial_background = pygame.image.load(os.path.join(background_images['ini'])).convert()
    initial_background = pygame.transform.scale(initial_background, (WIDTH, HEIGHT))  # Redimensiona a imagem
    screen.blit(initial_background, (0, 0))
    pygame.display.flip()

    # Ajuste as coordenadas para o canto superior direito
    arrow = pygame.image.load("Voltar.png").convert_alpha()
    arrowbox = pygame.Rect(0, 0, arrow.get_width(), arrow.get_height())

    # Adiciona uma camada roxa acinzentada semi-transparente
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((127, 50, 255, 128))  # Cor roxa acinzentada semi-transparente

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if selected_operation is None:
                    for operation_key, button_rect in operations.items():
                        if button_rect.collidepoint(event.pos):
                            selected_operation = operation_key
                            current_question = generate_question(selected_operation)
                            balloons = create_answer_balloons(current_question[3])
                            arrowbox.topleft = (WIDTH - arrowbox.width, 0)  # Ajuste para o canto superior direito
                            background_image = pygame.image.load(os.path.join(background_images[selected_operation])).convert()
                            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                            screen.blit(background_image, (0, 0))
                            pygame.display.flip()

                elif current_question is not None and balloons is not None:
                    for option, rect, is_correct in balloons:
                        if rect.collidepoint(event.pos):
                            if is_correct:
                                print("Você selecionou a resposta correta!")
                                pontos += 1  # Incrementa pontos ao acertar
                                selected_answer = option  # Atualiza a resposta selecionada
                            else:
                                print(f"Você selecionou a resposta incorreta. A resposta correta era {current_question[3]}")
                                pontos = 0  # Perde todos os pontos ao errar
                            # Gerar nova pergunta da mesma operação
                            current_question = generate_question(selected_operation)
                            balloons = create_answer_balloons(current_question[3])
                            selected_answer = None  # Reinicia a resposta selecionada
                            break  # Importante: interrompe o loop para evitar desenhar balões múltiplos
                    if arrowbox.collidepoint(event.pos):
                        current_question = None
                        selected_operation = None
                        pontos = 0

        if selected_operation is None:
            screen.blit(initial_background, (0, 0))
            draw_operation_buttons()
        elif current_question is not None and balloons is not None:
            screen.blit(background_image, (0, 0))

            # Adiciona a camada roxa acinzentada semi-transparente apenas na imagem de fundo
            screen.blit(overlay, (0, 0))

            draw_points_box()  # Draw the points box
            question_text = f"{current_question[0]} {current_question[1]} {current_question[2]}"
            question_display = font1.render(question_text, True, BLACK)
            text_rect = question_display.get_rect(center=(WIDTH // 2, HEIGHT // 3))

            # Draw square box around the selected operation
            if selected_operation in operations:
                box_width, box_height = text_rect.width + 40, text_rect.height + 40
                box_rect = pygame.Rect(text_rect.centerx - box_width // 2, text_rect.centery - box_height // 2, box_width, box_height)
                #draw_square_box(screen, box_rect, PURPLE, BLACK, 5)

            draw_balloons()  # Draw the answer balloons
            screen.blit(question_display, text_rect)
            screen.blit(arrow, arrowbox)


        pygame.display.flip()

if __name__ == "__main__":
    main()

