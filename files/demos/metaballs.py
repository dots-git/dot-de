from de.windows import *
import random

class Metaball(object):
    def __init__(self, x, y, r, x_vel, y_vel):
        self.x = x
        self.y = y
        self.r = r
        self.x_vel = x_vel
        self.y_vel = y_vel

class MetaballWindow(Window):
    def update_array_templates(self):
        EMPTY_ARRAY1: np.ndarray = np.array([[0 for _ in range(height())] for _ in range(width())], dtype=np.float64)
        self.EMPTY_ARRAY = EMPTY_ARRAY1

        ARRAY_X1: np.ndarray = np.array([[i for _ in range(height())] for i in range(width())], dtype=np.float64)
        self.ARRAY_X = ARRAY_X1

        ARRAY_Y1: np.ndarray = np.array([[i for i in range(height())] for _ in range(width())], dtype=np.float64)
        self.ARRAY_Y = ARRAY_Y1

    def init(self):
        self.set_size(100, 100, True)
        self.set_pos(400, 200, True)
        self.start_time = time.time()

        self.size_last_frame = (0, 0)
        balls1: list[Metaball] = []
        self.balls = balls1
        self.color = (0, 0, 0)

        self.balls.append(Metaball(0, 0, 10, random.random() * 160 - 80, random.random() * 160 - 80))
        self.balls.append(Metaball(0, 0, 10, random.random() * 160 - 80, random.random() * 160 - 80))

    def tick(self, delta):
        if time.time() - self.start_time > 2:
            # mouse_x, mouse_y = pygame.mouse.get_pos()
            # balls[0].x = mouse_x
            # balls[0].y = mouse_y

            for ball in self.balls:
                ball.x += ball.x_vel * delta
                ball.y += ball.y_vel * delta

                if ball.x > self.width() or ball.x < 0:
                    ball.x_vel *= -1
                if ball.y > self.height() or ball.y < 0:
                    ball.y_vel *= -1
            if self.size_last_frame != size():
                self.update_array_templates()
                self.size_last_frame = size()

    def draw(self):
        if time.time() - self.start_time > 2:
            inv_distance_sum: np.ndarray = self.EMPTY_ARRAY.copy()
            for ball in self.balls:
                x = ball.x
                y = ball.y

                inv_distance_map = ball.r / np.sqrt(np.power(x - self.ARRAY_X, 2) + np.power(y - self.ARRAY_Y, 2))
                inv_distance_sum += inv_distance_map
            
            for x in range(width()):
                for y in range(height()):
                    if inv_distance_sum[x][y] > 1:
                        set_at(x, y, self.color)

Window.open(MetaballWindow)