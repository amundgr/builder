import numpy as np
import cv2

def generate_light(radius, inner_radius, number_of_steps=10):
    diameter = int(2 * radius)
    board = np.zeros((diameter, diameter))
    radius_diff = radius - inner_radius
    for x in range(diameter):
        for y in range(diameter):
            distance = np.sqrt((radius - x - 0.5)**2 + (radius - y - 0.5)**2)
            if distance >= inner_radius:
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
    radius = 11
    inner_radius = 2
    number_of_steps = 6
    res = generate_light(radius=radius, 
                         inner_radius=inner_radius, 
                         number_of_steps=number_of_steps)

    cut_out_radius = 5
    print(res[radius-cut_out_radius:radius+cut_out_radius, 
              radius-cut_out_radius:radius+cut_out_radius])