
import sensor, image, time, math, ulab, pyb

from Kalman_Filter import Kalman_Filter

kf = Kalman_Filter()
kf.configure("constant_velocity.json")

clock = time.clock()


while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)

    # Circle objects have four values: x, y, r (radius), and magnitude. The
    # magnitude is the strength of the detection of the circle. Higher is
    # better...

    # `threshold` controls how many circles are found. Increase its value
    # to decrease the number of circles detected...

    # `x_margin`, `y_margin`, and `r_margin` control the merging of similar
    # circles in the x, y, and r (radius) directions.

    # r_min, r_max, and r_step control what radiuses of circles are tested.
    # Shrinking the number of tested circle radiuses yields a big performance boost.

    circles = img.find_circles(threshold = 2000, x_margin = 10, y_margin = 10, r_margin = 10, r_min = 2, r_max = 100, r_step = 2)
    if len(circles) > 0:
        c = sorted(circles, key = lambda i: i[3], reverse = True)[0]
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        print(c.x(), c.y(), c.r())

        circle_values = ulab.array([c.x(), c.y(), c.r()])
        filtered_circle = kf.update(circle_values.transpose(), update_Q_Matrix=True)

        print(filtered_circle[0][0], filtered_circle[1][0], filtered_circle[2][0])

        img.draw_circle(int(round(filtered_circle[0][0])), int(round(filtered_circle[1][0])), int(round(filtered_circle[2][0])), color= (0, 255,0))

