"""
Use this module to define the racing tracks available in the game, or to create new ones.
"""
import track as track
from math import pi

# TRACK1 BEGINS

# Specifies binary image, mask image, and track name
track1 = track.Track('assets/track.png', 'assets/track_textura.png', 'track1')

# Specifies episode length and timeout
track1.episode_length = 500
track1.timeout = 30

# Determines both cars' positions and initial angles/orientations (in radians)
track1.car1_position = (100,100)
track1.car2_position = (140, 100)
track1.angle_of_cars = 8.14

# Adds checkpoints, in the order they must be crossed
track1.add_checkpoint([(96, 346), (181, 374)])
track1.add_checkpoint([(226, 648), (225, 549)])
track1.add_checkpoint([(510, 375), (509, 466)])
track1.add_checkpoint([(937, 391), (853, 339)])
track1.add_checkpoint([(859, 90), (831, 181)])
track1.add_checkpoint([(524, 171), (486, 258)])
track1.add_checkpoint([(278, 68), (284, 162)])

# Specifies parked cars positions and angles/orientations
track1.add_parked_bot((120, 500), -pi/2)
track1.add_parked_bot((250, 620), 0)
track1.add_parked_bot((500, 390), 0)
track1.add_parked_bot((720, 470), 0)
track1.add_parked_bot((880, 430), -pi/4)
track1.add_parked_bot((950, 250), -2*pi/4)

# TRACK1 ENDS

# TRACK2 BEGINS

track2 = track.Track('assets/track_2.png', 'assets/track_2_textura.png', 'track2')

track2.episode_length = 500
track2.timeout = 30
track2.car1_position = (80, 150)
track2.car2_position = (120, 150)
track2.angle_of_cars = pi/2


track2.add_checkpoint([(180, 351), (280, 370)])
track2.add_checkpoint([(46, 429), (146, 484)])
track2.add_checkpoint([(142, 615), (150, 520)])
track2.add_checkpoint([(457, 692), (459, 594)])
track2.add_checkpoint([(643., 523), (633, 432)])
track2.add_checkpoint([(802, 503), (871, 571)])
track2.add_checkpoint([(835, 342), (740, 334)])
track2.add_checkpoint([(883, 149), (980, 112)])
track2.add_checkpoint([(611, 186), (692, 252)])
track2.add_checkpoint([(427, 328), (349, 392)])
track2.add_checkpoint([(543, 177), (438, 172)])
track2.add_checkpoint([(278, 68), (284, 162)])

track2.add_parked_bot((120, 500), -pi/2)
track2.add_parked_bot((250, 575), -pi/8)
track2.add_parked_bot((500, 590), -pi/4)
track2.add_parked_bot((720, 555), pi/4)
track2.add_parked_bot((870, 430), pi/2 - pi/8)
track2.add_parked_bot((590, 250), -pi/4)

# TRACK2 ENDS

# TRACK3 BEGINS

track3 = track.Track('assets/track_3.png', 'assets/track_3_textura.png', 'track3')

track3.episode_length = 500
track3.timeout = 30
track3.car1_position = (80, 150)
track3.car2_position = (120, 150)
track3.angle_of_cars = pi/2

track3.add_checkpoint([(96, 346), (181, 374)])
track3.add_checkpoint([(226, 648), (225, 549)])
track3.add_checkpoint([(702, 452), (703, 552)])
track3.add_checkpoint([(937, 391), (853, 339)])
track3.add_checkpoint([(859, 90), (831, 181)])
track3.add_checkpoint([(524, 171), (486, 258)])
track3.add_checkpoint([(278, 68), (284, 162)])

track3.add_parked_bot((110, 500), -pi/2)
track3.add_parked_bot((250, 620), -pi/8)
track3.add_parked_bot((500, 410), 0)
track3.add_parked_bot((500, 630), 0)
track3.add_parked_bot((720, 470), 0)
track3.add_parked_bot((880, 430), -pi/4)
track3.add_parked_bot((950, 250), -2*pi/4)

# TRACK3 ENDS

