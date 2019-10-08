from donkeycar.parts.actuator import TwoWheelSteeringThrottle, Mini_HBridge_DC_Motor_PWM

#DC_TWO_WHEEL - with two wheels as drive, left and right.
#these GPIO pinouts are only used for the DRIVE_TRAIN_TYPE=DC_TWO_WHEEL
# HBRIDGE_PIN_LEFT_FWD = 18
# HBRIDGE_PIN_LEFT_BWD = 16
# HBRIDGE_PIN_RIGHT_FWD = 15
# HBRIDGE_PIN_RIGHT_BWD = 13

LEFT_PID_DIR1 = 11
LEFT_PID_DIR2 = 13
LEFT_PWM = 15
RIGHT_PID_DIR1 = 12
RIGHT_PID_DIR2 = 16
RIGHT_PWM = 18
# speed
left = 0
right = 0


def change_speed(left, right, delta_l, delta_r):
    left += delta_l
    right += delta_r
    if left > 1:
        left = 1
    elif left < -1:
        left = -1

    if right > 1:
        right = 1
    elif right < -1:
        right = -1

    return left, right


left_motor = Mini_HBridge_DC_Motor_PWM(LEFT_PID_DIR1, LEFT_PID_DIR2, LEFT_PWM)
right_motor = Mini_HBridge_DC_Motor_PWM(RIGHT_PID_DIR1, RIGHT_PID_DIR2, RIGHT_PWM)
#two_wheel_control = TwoWheelSteeringThrottle()

while True:
    a = input ("please input direction among 'w s a d', quit for 'q'\r\n")
    if len(a) != 1:
        print('input error, try again')
        continue

    elif a == 'q':
        print('quit')
        left_motor.shutdown()
        right_motor.shutdown()
        break
    elif a == 'w':
        left, right = change_speed(left, right, 0.1, 0.1)
    elif a == 's':
        left, right = change_speed(left, right, -0.1, -0.1)
    elif a == 'a':
        left, right = change_speed(left, right, -0.1, 0.1)
    elif a == 'd':
        left, right = change_speed(left, right, 0.1, -0.1)
    print(left, right)
    left_motor.run(left)
    right_motor.run(right)
