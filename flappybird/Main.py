import pygame,sys,random

from pygame.display import flip;
pygame.init();

#các biến trong game
gravity = 0.5;
bird_movement = 0;
game_active = False;
score = 0;
high_score = 0;


#các hàm trong game
def draw_floor():
    #ve nền đất chạy
    screen.blit(floor,(floor_x_pos,400));
    screen.blit(floor,(floor_x_pos+800,400));
def create_pipe() : #tạo vận cản
    random_pipe_pos = random.choice(pipe_height);
    bottom_pipe = pipe_surface.get_rect(midtop =(800,random_pipe_pos ));
    top_pipe = pipe_surface.get_rect(midtop =(800,random_pipe_pos-380 ));
    return bottom_pipe,top_pipe;
def move_pipe(pipes) : #di chuyển các vật cản
    for pipe in pipes :
        pipe.centerx -= 5;
    return pipes;
def draw_pipe(pipes) : #vẽ các vật cản lên màn hình
    for pipe in pipes:
        if pipe.bottom >= 400:
            screen.blit(pipe_surface,pipe);
        else  : 
            flip_pipe = pygame.transform.flip(pipe_surface,False,True);
            screen.blit(flip_pipe,pipe);
def check_collision(pipes) : #kiểm tra điều kiện thua
    for pipe in pipes:
        if bird_rect.colliderect(pipe) :
            print("Bạn quá non!")
            return False;
    if bird_rect.top <=-90 or bird_rect.top >=375 :
        print("Bạn non quá!");
        return False;
    return True;
def rotate_bird(bird1) : #xoay chim khi bay
    new_bird = pygame.transform.rotozoom(bird1,bird_movement*4,1);
    return new_bird;
def score_display(game_status) : # hiển thị điểm
    if game_status == "main_game" :
        score_surface = game_font.render(str(int(score)),True,(246,57,57));
        score_rect = score_surface.get_rect(center = (730,30 ));
        screen.blit(score_surface,score_rect);
    if game_status == "game_over" :
        score_surface = game_font.render(f'Score:{int(score)}',True,(246,57,57));
        score_rect = score_surface.get_rect(center = (700,30));
        screen.blit(score_surface,score_rect);
    
        high_score_surface = game_font.render(f'High Score:{int(high_score)}',True,(246,57,57));
        high_score_rect = score_surface.get_rect(center = (700,60));
        screen.blit(high_score_surface,high_score_rect);
def update_highScore(score,high_score) : #cập nhật điểm cao
    if score>high_score:
        high_score = score;
    return high_score;


screen = pygame.display.set_mode((800,450)); # tạo màn hình game
clock = pygame.time.Clock();
game_font = pygame.font.Font('04B_19.ttf',20);


#tạo màn hình game
bg = pygame.image.load('assets/background.png');
bg = pygame.transform.scale(bg,(800,450)); #chỉnh lại kích thước background
#mặt đất bên dưới
floor = pygame.image.load('assets/floor.png');
floor = pygame.transform.scale(floor,(800,450)); #chỉnh lại kích thước đất
floor_x_pos =0;

#tạo con chim
bird = pygame.image.load('assets/bird-midflap.png');
bird = pygame.transform.scale(bird,(30,22));
bird_rect = bird.get_rect(center = (100,225));
#tạo vật cản
pipe_surface = pygame.image.load('assets/pipe.png'); 
pipe_list = []
#tạo màn hình kết thúc
game_over_surface = pygame.transform.scale(pygame.image.load('assets/message.png'),(400,225));
game_over_rect = game_over_surface.get_rect(center = (400,225));
#tiếng game
sound = pygame.mixer.Sound("sound/sfx_wing.wav");
#tạo timer
spawnpipe = pygame.USEREVENT;
pygame.time.set_timer(spawnpipe,1200); #thời gian giữa các vật thể xuất hiện
pipe_height = [150,200,250,300,350]; #chiều cao ngẫu nhiên của các vật thể

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit();
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE and game_active :
                bird_movement = 0;
                bird_movement = -9;
                sound.play();
            if event.key == pygame.K_SPACE and not game_active : # thua thì nhấn space để đổi lại
                game_active = True;
                pipe_list.clear();
                bird_rect.center = (100,225);
                bird_movement = 0;
                score = 0;
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()); 
            

    screen.blit(bg,(0,0)); #cài background game
    if game_active :
        #chim
        bird_movement +=gravity;
        rotated_bird = rotate_bird(bird);
        bird_rect.centery +=bird_movement;
        screen.blit(rotated_bird,bird_rect);
        game_active =check_collision(pipe_list);

        #vật cản
        pipe_list = move_pipe(pipe_list);
        draw_pipe(pipe_list);
        score+=0.01;
        score_display('main_game');
    else :
        screen.blit(game_over_surface,game_over_rect);
        screen.blit(bird,bird.get_rect(center = (100,225)));
        high_score = update_highScore(score,high_score);
        score_display('game_over');
    #đất
    floor_x_pos -=1;
    draw_floor();
    if floor_x_pos<=-800:
        floor_x_pos =0;
    pygame.display.update();
    clock.tick(60); #cài đặt fps là 60