import math

def sign(x):
    if x == 0:
        return 0
    if x < 0:
        return -1
    return 1

def approx(a, b, variance):
    return a < b + variance and a > b - variance

class AnimatedValue:
    def __init__(self, value, acceleration, acceleration_modifier, drag):
        self.s_value = value
        self.change_rate = 0
        self.value = value

        self.acceleration = acceleration
        self.acceleration_modifier = acceleration_modifier
        self.drag = 1 / (drag + 1)

        self.was_changed = False
    
    def animate(self, delta):
        bef = self.get()
        self.change_rate = circular_exponential(self.value, self.change_rate, self.s_value, self.acceleration, self.acceleration_modifier, self.drag, delta)
        self.value += self.change_rate * delta
        self.was_changed = False
        return int(self.value) != int(bef) or self.was_changed

    def set(self, value):
        self.s_value = value
    
    def inc(self, value):
        self.s_value += value
    
    def set_no_animation(self, value):
        if value != self.value:
            self.was_changed = True

        self.value = value
        self.s_value = value
        self.change_rate = 0
    
    def get(self):
        return self.value

    def __str__(self):
        return '%f animating towards %f' % (self.value, self.s_value)


# Animate with quadratic growth, then exponential decay
def quadratic_exponential(value, change_rate, target, acceleration, drag, delta_time):
    moving_twd = value - change_rate / math.log(drag)
    
    # Accelerate if change_rate is too small
    if moving_twd < target - 0.001:
        change_rate += acceleration * delta_time
        moving_twd = value - change_rate / math.log(drag)

    # Cap change_rate if it is too big
    if moving_twd > target + 0.001:
        change_rate = (value - target) * math.log(drag)
        moving_twd = value - change_rate / math.log(drag)

    # Slow down if that way you reach target precisely
    if approx(moving_twd, target, 0.001):
        change_rate *= pow(drag, delta_time)
    
    return change_rate

# animate with circular growth, then exponential decay
def circular_exponential(value, change_rate, target, acceleration, acceleration_modifier, drag, delta_time):
    moving_twd = value - change_rate / math.log(drag)
    
    # Accelerate if change_rate is too small
    if moving_twd < target - 0.01:
        if math.atan(change_rate / acceleration_modifier) + acceleration * delta_time < math.pi/2:
            change_rate = acceleration_modifier * math.tan(math.atan(change_rate / acceleration_modifier) + acceleration * delta_time)
        else:
            change_rate += change_rate - acceleration_modifier * math.tan(math.atan(change_rate / acceleration_modifier) - acceleration * delta_time)
            if change_rate < 0:
                change_rate = (value - target) * math.log(drag)
        moving_twd = value - change_rate / math.log(drag)
    
    # Cap change_rate if it is too big
    if moving_twd > target + 0.01:
        change_rate = (value - target) * math.log(drag)
        moving_twd = value - change_rate / math.log(drag)

    # Slow down if that way you reach target precisely
    if approx(moving_twd, target, 0.01):
        change_rate *= pow(drag, delta_time)
        change_rate = ((value + change_rate * delta_time) - target) * math.log(drag)
    
    if value + change_rate * delta_time > target:
        change_rate = (target - value) / delta_time
    
    return change_rate