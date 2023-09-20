import cv2
import numpy as np

def make_white_background():
    shape = (256, 256, 3) # y, x, RGB
    output = np.full(shape, 255).astype(np.uint8)
    return output

def draw_grid(input):
    height = len(input)
    for x in np.linspace(20, height-20, 11):
        x = round(x)
        start_point = (x, 20)
        end_point = (x, height-20)
        color = (0, 0, 0) # brack
        thickness = 3 # 寬度
        input = cv2.line(input, start_point, end_point, color, thickness) 
        start_point = (20, x)
        end_point = (height-20, x)
        input = cv2.line(input, start_point, end_point, color, thickness) 
    output = input
    return output

def draw_start_end_point(input, start_point, end_point):
    height = len(input)
    criteria = np.linspace(20, height-20, 11).astype(np.uint8)
    gap = (height-40)/20
    gap = round(gap)
    point_size = 4
    x = criteria[start_point[1]] + gap
    y = criteria[start_point[0]] + gap
    point_color = (0, 0, 255) # red
    thickness = -1
    point = (x, y)
    cv2.circle(input, point, point_size, point_color, thickness)

    x = criteria[end_point[1]] + gap
    y = criteria[end_point[0]] + gap
    point_color = (0, 255, 0) # green
    point = (x, y)
    cv2.circle(input, point, point_size, point_color, thickness)
    output = input
    return output

def draw_block(input, maze):
    height = len(input)
    criteria = np.linspace(20, height-20, 11).astype(np.uint8)
    gap = (height-40)/10
    gap = round(gap)
    for i in range(10):
        for j in range(10):
            if maze[i][j] == 1:
                x = criteria[j]+ gap
                y = criteria[i]+ gap
                point = (x, y)
                cv2.rectangle(input, (criteria[j], criteria[i]), point, (0,0,0), -1) 
    output = input
    return output

def draw_color_cost(input, closed_list):
    height = len(input)
    criteria = np.linspace(20, height-20, 11).astype(np.uint8)
    gap = (height-40)/10
    gap = round(gap)
    for state in closed_list:
        if state == Node(None, (0, 0)):
            continue
        x = criteria[state.position[1]] + gap
        y = criteria[state.position[0]] + gap
        point = (x-2, y-2)
        color = (state.f)*255/160 #/18
        color_bat = np.full((1,1), color).astype(np.uint8)
        color_bat = cv2.applyColorMap(color_bat, cv2.COLORMAP_RAINBOW)
        color_bat = np.squeeze(color_bat)
        color = tuple ([int(x) for x in color_bat])  
        print(state.f, color)
        cv2.rectangle(input, (criteria[state.position[1]]+2, criteria[state.position[0]]+2), point, color, -1) 
    output = input
    return output

def draw_path(input, path):
    height = len(input)
    criteria = np.linspace(20, height-20, 11).astype(np.uint8)
    gap = (height-40)/20
    gap = round(gap)
    for pth in range(len(path)-1):
        a_x = criteria[path[pth][1]] + gap
        a_y = criteria[path[pth][0]] + gap
        b_x = criteria[path[pth+1][1]] + gap
        b_y = criteria[path[pth+1][0]] + gap
        if pth < len(path)-2:
            cv2.circle(input, (b_x,b_y), 4, (0,0,255), -1)
        cv2.line(input,(a_x,a_y),(b_x,b_y),(0,0,255),2)
    output = input
    return output

def draw_ref(input):
    shape = (256, 64, 3) # y, x, RGB
    output = np.zeros(shape).astype(np.uint8)
    for i in range(256):
        for j in range(64):
            output[255-i][j][0] = i
            output[255-i][j][1] = i
            output[255-i][j][2] = i
    output = cv2.applyColorMap(output, cv2.COLORMAP_RAINBOW)
    output = np.concatenate((input, output), axis=1)
    return output

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, img):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    count = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        img = draw_color_cost(img, closed_list)
        cv2.imwrite(f'./video/My Maze_result_{count}.png', img)
        count += 1
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], closed_list # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for idx, child in enumerate(children):
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    children[idx] = Node(None, start)
            
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)) #** 0.5
            child.f = child.g + child.h
            """# over-estimate
            if child.position == (0, 1):
                child.f = child.f + 10000
            print(child.position, child.f)"""

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    children[idx] = Node(None, start)
        # print(children)
        for child in children:
            if child != Node(None, start):
                # Add the child to the open list
                open_list.append(child)
            

def main():

    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (9, 9)
    img = make_white_background()
    img = draw_grid(img)
    img = draw_start_end_point(img, start, end)
    img = draw_block(img, maze)
    cv2.imwrite('My Maze.png', img)
    cv2.imshow('My Maze', img)
    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    path, closed_list = astar(maze, start, end, img)
    print(path)

    img = draw_color_cost(img, closed_list)
    img = draw_start_end_point(img, start, end)
    img = draw_path(img, path)
    cv2.imwrite('./video/My Maze_result_190.png', img)
    img = draw_ref(img)
    cv2.imwrite('My Maze_result.png', img)
    cv2.imshow('My Maze', img)
    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()