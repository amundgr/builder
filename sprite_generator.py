import numpy as np
import cv2

def generate_light(radius, inner_radius, number_of_steps=10):
    board = np.zeros((radius*2, radius*2))
    center = radius-1
    radius_diff = radius - inner_radius
    for x in range(radius*2-1):
        for y in range(radius*2-1):
            distance = np.sqrt((center - x)**2 + (center - y)**2)
            if distance > inner_radius:
                board[x,y] = (distance - inner_radius + 1) / radius_diff
            else:
                board[x,y] = 0
    board *= number_of_steps
    board = np.round(board)
    board *= 255 / number_of_steps
    board = np.round(board)
    board = np.where(board < 0, 0, board)
    board = np.where(board > 255, 255, board)
    cv2.imwrite("img.png", board)
    return np.round(board, 1)

if __name__ == "__main__":
    generate_light(32, 10)