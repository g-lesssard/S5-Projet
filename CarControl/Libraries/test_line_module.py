from SunFounder_Line_Follower import Line_Follower
import time

lf = Line_Follower.Line_Follower(references=[20,20,20,20,20])
while True:
	print(lf.read_analog())
	print(lf.read_digital())
	print('')
	time.sleep(0.5)

