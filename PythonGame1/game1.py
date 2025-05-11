import pygame
import random
import time
from datetime import datetime
import os

#1. 게임 초기화
pygame.init()

#2. 게임창 옵션 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "My Game"
pygame.display.set_caption(title)

#3. 게임 내 필요한 설정
clock = pygame.time.Clock()
# 이미지 폴더 경로 설정
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        if address [-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
            self.sx, self.sy = self.img.get_size()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()
    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img,(sx, sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x, self.y))

def crash(a, b):
    return(a.x - b.sx <= b.x <= a.x + a.sx) and (a.y - b.sy <= b.y <= a.y + a.sy)

#이미지 파일 경로 설정
jet_image = os.path.join(image_path, "jet.png")
missile_image = os.path.join(image_path, "mis.png")
enemy_image = os.path.join(image_path, "enemy.png")

#폰트 설정 (시스템 폰트 대신 pygame 기본 폰트 사용)
font_path = pygame.font.get_default_font()

# 게임 시작 함수 정의
def game_start():
    global ss, left_go, right_go, space_go, m_list, a_list, k, kill, loss, GO, CLEAR

    ss = obj()
    ss.put_img(jet_image)
    ss.change_size(50, 80)
    ss.x = round(size[0]/2 - ss.sx/2)
    ss.y = size[1]-ss.sy - 15
    ss.move = 5

    left_go = False
    right_go = False
    space_go = False

    m_list = []
    a_list = []
    k = 0

    kill = 0
    loss = 0
    GO = 0
    CLEAR = 0

#게임 변수 초기화
game_start()

white = (255, 255, 255)
black = (0, 0, 0)

# 게임 메인 루프
running = True
while running:
    # 4-0. 게임 시작 대기 화면
    SB = 0
    while SB == 0 and running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SB = 1
        screen.fill(white)
        font = pygame.font.Font(font_path, 15)
        text = font.render("PRESS SPACE KEY TO START THE GAME", True, black)
        screen.blit(text, (40, round(size[1]/2)-50))
        pygame.display.flip()
    
    if not running:
        break
        
    # 게임 시작 시간 초기화
    start_time = datetime.now()

    # 4. 메인 게임 루프
    while running and SB == 1 and GO == 0 and CLEAR == 0:
        # 4-1. FPS 설정
        clock.tick(60)

        # 4-2. 각종 입력 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_go = True
                elif event.key == pygame.K_RIGHT:
                    right_go = True
                elif event.key == pygame.K_SPACE:
                    space_go = True
                    k = 0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_go = False
                elif event.key == pygame.K_RIGHT:
                    right_go = False
                elif event.key == pygame.K_SPACE:
                    space_go = False

        # 4-3. 입력, 시간에 따른 변화
        now_time = datetime.now()
        delta_time = round((now_time - start_time).total_seconds())

        if left_go:
            ss.x -= ss.move
            if ss.x <= 0:
                ss.x = 0
        elif right_go:
            ss.x += ss.move
            if ss.x >= size[0] - ss.sx:
                ss.x = size[0] - ss.sx
           
        if space_go and k % 6 == 0:
            mm = obj()
            mm.put_img(missile_image)
            mm.change_size(10, 20)
            mm.x = round(ss.x + ss.sx/2 - mm.sx/2)
            mm.y = ss.y - mm.sy - 10
            mm.move = 15
            m_list.append(mm)
        k += 1

        # 미사일 이동 및 화면 밖으로 나간 미사일 제거
        d_list = []
        for i in range(len(m_list)):
            m = m_list[i]
            m.y -= m.move
            if m.y < -m.sy:
                d_list.append(i)

        d_list.sort(reverse=True)
        for d in d_list:
            del m_list[d]

        # 적의 속도를 점수에 따라 증가시키기
        enemy_speed = min(3 + (kill // 10), 10)
        
        # 적 생성
        if random.random() > 0.98:
            aa = obj()
            aa.put_img(enemy_image)
            aa.change_size(40, 40)
            aa.x = random.randrange(0, size[0]-aa.sx-round(ss.sx/2))
            aa.y = 10
            aa.move = enemy_speed
            a_list.append(aa)
            
        # 적 이동 및 화면 밖으로 나간 적 처리
        d_list = []
        for i in range(len(a_list)):
            a = a_list[i]
            a.y += a.move
            if a.y >= size[1]:
                d_list.append(i)

        d_list.sort(reverse=True)
        for d in d_list:
            del a_list[d]
            loss += 1

        # 500점 달성 시 게임 클리어
        if kill >= 300:
            CLEAR = 1
            break
        
        if loss >= 10:
            GO = 1
            break
            
        # 미사일과 적 충돌 처리
        dm_list = []
        da_list = []
        for i in range(len(m_list)):
            for j in range(len(a_list)):
                m = m_list[i]
                a = a_list[j]
                if crash(m, a):
                    dm_list.append(i)
                    da_list.append(j)
                    break

        dm_list = list(set(dm_list))
        da_list = list(set(da_list))

        dm_list.sort(reverse=True)
        da_list.sort(reverse=True)
        for dm in dm_list:
            if dm < len(m_list):
                del m_list[dm]
        
        for da in da_list:
            if da < len(a_list):
                del a_list[da]
                kill += 1

        # 플레이어와 적 충돌 처리
        for a in a_list:
            if crash(a, ss):
                GO = 1
                break

        # 4-4. 그리기
        screen.fill(white)
        ss.show()
        for m in m_list:
            m.show()
        for a in a_list:
            a.show()    
               
        # 점수 및 정보 표시
        font = pygame.font.Font(font_path, 20)
        text_kill = font.render("killed : {} loss : {}".format(kill, loss), True, (0, 0, 255))
        screen.blit(text_kill, (10, 5))

        text_time = font.render("time:{}".format(delta_time), True, (0, 0, 255))
        screen.blit(text_time, (size[0]-100, 5))

        # 현재 적 속도 표시
        text_speed = font.render("Enemy Speed: {}".format(enemy_speed), True, (0, 0, 255))
        screen.blit(text_speed, (10, 30))

        # 4-5. 업데이트
        pygame.display.flip()

    # 5. 게임 종료 또는 클리어 화면
    # 게임 클리어 화면
    while CLEAR == 1 and running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    CLEAR = 0
                    game_start()  # 게임 변수 초기화
                    
        screen.fill(white)
        font = pygame.font.Font(font_path, 40)
        text = font.render("CONGRATULATION", True, (0, 255, 0))
        screen.blit(text, (80, round(size[1]/2)-100))

        font_small = pygame.font.Font(font_path, 20)
        score_text = font_small.render("Killed: {} | Lost: {}".format(kill, loss), True, (0, 0, 255))
        screen.blit(score_text, (120, round(size[1]/2)-40))

        restart_text = font_small.render("PRESS SPACE TO RESTART GAME", True, black)
        screen.blit(restart_text, (40, round(size[1]/2)+20))

        pygame.display.flip()

    # 게임 오버 화면
    while GO == 1 and running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GO = 0
                    game_start()  # 게임 변수 초기화
                    
        screen.fill(white)
        font = pygame.font.Font(font_path, 40)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (80, round(size[1]/2)-100))

        font_small = pygame.font.Font(font_path, 20)
        score_text = font_small.render("Killed: {} | Lost: {}".format(kill, loss), True, (255, 0, 0))
        screen.blit(score_text, (120, round(size[1]/2)-40))

        restart_text = font_small.render("PRESS SPACE TO RESTART GAME", True, black)
        screen.blit(restart_text, (40, round(size[1]/2)+20))
        
        pygame.display.flip()
                        
pygame.quit()