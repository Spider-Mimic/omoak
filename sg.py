import pygame
import sys

# --- 1. 기본 설정 및 색상 상수 (참고 소스 기반) ---
BOARD_SIZE = 15  # 과제 기준 15x15 [3]
CELL_SIZE = 40   # 15x15 크기가 화면에 다 들어가도록 픽셀 크기 조정 [2], [4]
PADDING = 40     # 바둑판 테두리 여백 [2], [4]

# 화면 전체 크기 계산 
SCREEN_WIDTH = (BOARD_SIZE - 1) * CELL_SIZE + (PADDING * 2)
SCREEN_HEIGHT = (BOARD_SIZE - 1) * CELL_SIZE + (PADDING * 2)

# 참고 소스의 테마 색상 적용 
COLOR_BOARD = (225, 228, 232)  # 라이트 그레이
COLOR_GRID = (165, 170, 175)   # 격자선
COLOR_BLACK = (45, 48, 55)     # 차콜 블랙
COLOR_WHITE = (250, 252, 255)  # 퓨어 오프화이트
COLOR_WHITE_BORDER = (200, 205, 210) # 백돌 테두리 색상

# --- 2. 기존 게임 로직 (수정 없이 재사용) ---
def check_win(board, row, col, player):
    """방금 놓은 돌을 기준으로 5목 완성 여부 확인 [3]"""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # 정방향 탐색
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # 역방향 탐색
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
            
        if count >= 5:
            return True
    return False

def is_board_full(board):
    """바둑판이 꽉 찼는지 확인하여 무승부 판별 [3]"""
    for row in board:
        if 0 in row: 
            return False
    return True

# --- 3. Pygame GUI 그리기 로직 ---
def draw_board(screen):
    """바둑판의 배경과 격자선."""
    screen.fill(COLOR_BOARD) # 바둑판 배경색 채우기
    
    for i in range(BOARD_SIZE):
        # 가로선
        pygame.draw.line(screen, COLOR_GRID, 
                         (PADDING, PADDING + i * CELL_SIZE), 
                         (PADDING + (BOARD_SIZE - 1) * CELL_SIZE, PADDING + i * CELL_SIZE), 2)
        # 세로선
        pygame.draw.line(screen, COLOR_GRID, 
                         (PADDING + i * CELL_SIZE, PADDING), 
                         (PADDING + i * CELL_SIZE, PADDING + (BOARD_SIZE - 1) * CELL_SIZE), 2)

def draw_stones(screen, board):
    """2차원 리스트의 상태에 따라 흑돌과 백돌."""
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            # 돌이 그려질 중심 x, y 좌표 계산
            x = PADDING + c * CELL_SIZE
            y = PADDING + r * CELL_SIZE
            
            if board[r][c] == 1:
                pygame.draw.circle(screen, COLOR_BLACK, (x, y), CELL_SIZE // 2 - 2)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, COLOR_WHITE, (x, y), CELL_SIZE // 2 - 2)
                pygame.draw.circle(screen, COLOR_WHITE_BORDER, (x, y), CELL_SIZE // 2 - 2, 1)

# --- 4. 메인 게임 루프 ---
def main():
    pygame.init() # Pygame 초기화 [6]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 화면 크기 설정 [6]
    pygame.display.set_caption("인간 vs 인간 오목 프로그램 (GUI)")
    
    # 15x15 2차원 리스트 생성 [3], [7]
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 1 # 1: 흑돌, 2: 백돌
    game_over = False
    
    # 게임 루프
    while True:
        for event in pygame.event.get():
            # X 버튼을 누르면 프로그램 종료
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # 마우스 클릭 입력 처리 (기존 input() 함수를 대체)
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                
                # 마우스 좌표(픽셀)를 바둑판의 행/열(인덱스)로 변환
                col = round((mouse_x - PADDING) / CELL_SIZE)
                row = round((mouse_y - PADDING) / CELL_SIZE)
                
                # 1. 클릭된 좌표가 15x15 바둑판 범위 안인지 검사 [1]
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    # 2. 이미 돌이 놓인 곳이 아닌지 검사 [1]
                    if board[row][col] == 0:
                        board[row][col] = current_player
                        
                        # 3. 승리 또는 무승부 판별 [1], [8]
                        if check_win(board, row, col, current_player):
                            winner = "흑돌" if current_player == 1 else "백돌"
                            print(f" {winner} 승리 게임종료")
                            game_over = True
                        elif is_board_full(board):
                            print("무승부")
                            game_over = True
                            
                        # 4. 턴 교체 (1->2, 2->1) [1]
                        current_player = 2 if current_player == 1 else 1

        # 화면 업데이트
        draw_board(screen)
        draw_stones(screen, board)
        pygame.display.update()

if __name__ == "__main__":
    main()