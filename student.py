import pigo
import time  # import just in case students need
import random
import datetime

# setup logs
import logging

LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        #
        self.start_time = datetime.datetime.utcnow()
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 100
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 100
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        self.TIME_PER_DEGREE = 0.00466667
        self.TURN_MODIFIER = 0
        while True:
            self.stop()
            self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now),
                "o": ("Obstacle Count", self.obstacle_count),
                "t": ("Restore Header Test", self.test_restore_heading)}
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE

        if self.safety_check():
            self.to_the_right()
            self.to_the_left()
            self.now_kick()
            self.walk_it_by_yourself()
            self.carlton()
            self.whip()
            self.running_man()
            self.moonwalk()
            self.ballroom()
            self.dab()

    def safety_check(self):

        self.servo(self.MIDPOINT)
        for loop in range(4):
            if not self.is_clear():
                print("i aint dancin' vro")
                return False
            self.encR(8)
        print("i dont dance i make money moves")
        return True

    def to_the_right(self):
        """subroutine of dance method"""
        self.encR(10)
        for x in range(4):
            self.encF(3)
        self.encL(10)

    def to_the_left(self):
        """subroutine of dance method"""
        self.encL(10)
        for x in range(4):
            self.encF(3)
        self.encR(10)

    def now_kick(self):
        """subroutine of dance method"""
        for x in range(2):
            self.encF(5)
            self.servo(40)
            self.encR(20)
            self.encF(5)
            self.servo(150)
            self.encR(20)
            self.servo(94)

    def walk_it_by_yourself(self):
        """subroutine of dance method"""
        for x in range(4):
            self.encR(3)
            self.servo_shake()
            self.encL(6)

    def servo_shake(self):
        """subroutine of walk_it_by_yourself method"""
        for x in range(2):
            self.servo(74)
            self.servo(114)

    def carlton(self):
        """subroutine of dance method"""
        for x in range(4):
            self.servo(40)
            self.encR(10)
            self.servo(150)
            self.encL(10)

    def whip(self):
        """subroutine of dance method"""
        for x in range(2):
            self.servo(150)
            self.encR(8)
            time.sleep(.4)
            self.servo(40)
            self.encL(8)
            time.sleep(.4)
            self.servo(150)
            self.servo(94)

    def running_man(self):
        """subroutine of dance method"""
        for x in range(2):
            self.encF(25)
            self.encR(18)
            self.encF(25)
            self.encR(18)

    def moonwalk(self):
        """subroutine of dance method"""
        for x in range(4):
            self.encR(2)
            self.encB(3)
            self.encL(4)
            self.encB(3)

    def ballroom(self):
        """subroutine of dance method"""
        for x in range(3):
            self.spin()
            self.encF(8)


    def spin(self):
        """subroutine of ballroom method"""
        for x in range(2):
            self.encR(24)

    def dab(self):
        for x in range(6):
            self.encF(2)
            self.encB(2)











    def restore_heading(self):
        """uses turn track to reorient original heading"""
        print("RESTORING HEADING")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))


    def test_restore_heading(self):
        """turnst robot around to test self.restore_heading"""
        self.encR(5)
        self.encL(14)
        self.encL(4)
        self.encR(3)
        self.encL(9)
        self.restore_heading()







    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        """drives foward until sees object"""
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print("It took you %d seconds to run this" % difference)
        while True:
            if self.is_clear():
                self.cruise()
            """stops driving and finds the best path"""
            else:
                #stops the robot and looks for a new path
                self.stop()
                self.best_path()


    def best_path(self):
        """find the best possible route"""
        safe_count = 0
        path_lists = []
        for x in range(self.MIDPOINT - 40, self.MIDPOINT + 40, 2):
            #^^^ looks around looking for safe distances
            self.servo(x)
            time.sleep(.1)
            self.scan[x] = self.dist()
            if self.scan[x] > self.SAFE_STOP_DIST:
                safe_count += 1
            else:
                #if 12 or more safe distances are found in a row it is a best path
                safe_count = 0
            if safe_count > 12:
                print("\n -----Found a path----- \n" + str(
                    (x + x - 16) / 2))
                safe_count = 0
                path_lists.append((x + x - 16) / 2)
        print(str(path_lists[1:100]))

    def smooth_turn(self):
        self.right_rot()
        while True:
            if  self.dist() > 100:
                self.stop()
                print("aye i think i see a path imma full send")
            elif datetime.datetime.utcnow() - start > datetime.timedelta(seconds=10):
                self.stop()
                print("man this stuff is hard bruh im calling it quits")
            time.sleep(,2)

    def turn_nav(self):
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print("It took you %d seconds to run this" % difference)
        while True:
            if self.is_clear():  # no obstacles are detected by the robot
                print("I am going to move forward!")
                self.cruise()  # moves robot forward due to clear path
            else:  # obstacle is detected
                print("Ut oh! Something is blocking my path!")
                self.encB(8)  # backs up
                self.encR(8)  # turns right
                if self.is_clear():  # clear path found to the right
                    self.cruise()  # robot moves forward in clear direction
                else:
                    self.encL(8)  # turns left to find clear path if no clear path to the right
                    if self.is_clear():  # path is clear
                        self.cruise()  # robot moves forward in clear direction
            self.restore_heading()  # reorients robot to original heading





def cruise(self):
        """Robots drives straight while path is clear"""
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.5)
        self.stop()

    def obstacle_count(self):
        """scans and counts the number of obstacles in sight"""

        for x in range(4):
            self.wide_scan()
            found_something = False
            counter = 0
            for distance in self.scan:
                if distance and distance < 60 and not found_something:
                    found_something = True
                    counter += 1
                    print("object # %d found, I think" % counter)
                if distance and distance > 60 and found_something:
                    found_something = False
            print("\n------I see %d objects------\n" % counter)
            self.encR(7)


    def turnR(self, deg):
        """turns to a degree (right) instead of an encoder"""
        self.turn_track += deg
        print("The exit is " + str(self.turn_track) + "degrees away.")
        self.set_speed(self.LEFT_SPEED * self.TURN_MODIFIER, self.RIGHT_SPEED * self.TURN_MODIFIER)
        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)

    def turnL(self, deg):
        """turns to a degree(left) instead of an encoder"""
        self.turn_track -= deg
        print("The exit is " + str(self.turn_track) + "degrees away.")
        self.set_speed(self.LEFT_SPEED * self.TURN_MODIFIER, self.RIGHT_SPEED * self.TURN_MODIFIER)
        left_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)












####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit


##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
