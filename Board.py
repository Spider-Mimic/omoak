# 바둑판 크기 설정 15x15
BOARD_SIZE = 15

def print_board(board):
    # 열 번호 출력 (가독성을 위해 0~14 표시)
    print("   " + " ".join([f"{i:2}" for i in range(BOARD_SIZE)]))
    
    for i in range(BOARD_SIZE):
        row_str = f"{i:2} "  # 행 번호 출력
        for j in range(BOARD_SIZE):
            # 1. 돌이 놓인 경우 (흑돌 또는 백돌)
            if board[i][j] == 1:
                row_str += "●  "  # 흑돌
            elif board[i][j] == 2:
                row_str += "○  "  # 백돌
            
            # 2. 돌이 없는 경우 (테두리 및 교차점 그리기)
            else:
                # 네 모서리
                if i == 0 and j == 0:
                    row_str += "┌  "
                elif i == 0 and j == BOARD_SIZE - 1:
                    row_str += "┐  "
                elif i == BOARD_SIZE - 1 and j == 0:
                    row_str += "└  "
                elif i == BOARD_SIZE - 1 and j == BOARD_SIZE - 1:
                    row_str += "┘  "
                
                # 상하좌우 테두리
                elif i == 0:
                    row_str += "┬  "
                elif i == BOARD_SIZE - 1:
                    row_str += "┴  "
                elif j == 0:
                    row_str += "├  "
                elif j == BOARD_SIZE - 1:
                    row_str += "┤  "
                
                # 내부 교차점
                else:
                    row_str += "┼  "
                    
        print(row_str)


def get_user_input(board, current_player):
    while True:
        try:
            # 현재 턴이 누구인지 표시
            player_name = "흑돌(●)" if current_player == 1 else "백돌(○)"
            
            # 입력받기 (예: "7 7")
            user_input = input(f"{player_name} 차례. 행과 열을 띄어쓰기 입력 (0~14): ")
            row, col = map(int, user_input.split())
            
            # 1. 바둑판 범위를 벗어났는지 검사
            if 0 <= row < 15 and 0 <= col < 15:
                # 2. 이미 돌이 놓인 위치인지 검사
                if board[row][col] == 0:
                    return row, col # 정상적인 입력이므로 좌표 반환
                else:
                    print("돌이 놓인 위치. 다른 곳 선택.")
            else:
                print("바둑판 범위(0~14)초과. 다시 입력.")
                
        except ValueError:
            # 숫자가 아닌 문자 등을 입력했을 때의 예외 처리
            print("숫자 두 개를 띄어쓰기로 구분해서 입력 (예: 7 7)")


def check_win(board, row, col, player):
    # 4가지 탐색 방향: (가로, 세로, 우하향 대각선, 우상향 대각선)
    # 한 방향의 양쪽(+, -)을 모두 탐색하기 위해 기준 방향만 설정
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # 방금 놓은 돌 본인을 포함하므로 1부터 시작
        
        # 1. 정방향(+dr, +dc) 탐색
        r, c = row + dr, col + dc
        while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == player:
            count += 1
            r += dr
            c += dc
            
        # 2. 역방향(-dr, -dc) 탐색
        r, c = row - dr, col - dc
        while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
            
        # 3. 연속된 돌이 5개 이상이면 승리 (오목 규칙에 따라 5개 이상 승리 처리)
        if count >= 5:
            return True
            
    return False

#바둑판 꽉차면 종료
def is_board_full(board):
    for row in board:
        if 0 in row:  # 빈 공간(0)이 하나라도 있으면 아직 덜 찬 거
            return False
    return True  # 0이 하나도 없으면 꽉 찬 거


def play_game():
    # 1. 빈 바둑판 생성
    my_board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # 2. 흑돌(1)부터 시작
    current_player = 1
    
    print("오목 게임 테스트 시작(종료 Ctrl+C)")
    print_board(my_board)
    
    # 테스트
    while True:
        print("\n" + "="*40)
        
        #  만든 함수로 입력받기
        row, col = get_user_input(my_board, current_player)
        
        #  바둑판에 돌 놓기
        my_board[row][col] = current_player
        
        #  결과 출력하기
        print(f"\n {row}, {col}")
        print_board(my_board)

        # 승리 조건 체크
        if check_win(my_board, row, col, current_player):
             winner = "흑돌(●)" if current_player == 1 else "백돌(○)"
             print(f"{winner} 승리 ")
             break

        if is_board_full(my_board):
            print("\n바둑판 꽉차서 무승부")
            break
        
        # 6. 턴 넘기기 (1이면 2로, 2면 1로)
        current_player = 2 if current_player == 1 else 1
        
    print("\n테스트 종료")
