import os,  inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0,parentdir)

from pybullet_envs.mimic.humanoid import Humanoid
from pybullet_utils.bullet_client import BulletClient
from pybullet_envs.mimic.motion_capture_data import MotionCaptureData
import pybullet_data
import pybullet
import time
import random

bc = BulletClient(connection_mode=pybullet.GUI)
bc.setAdditionalSearchPath(pybullet_data.getDataPath())
bc.configureDebugVisualizer(bc.COV_ENABLE_Y_AXIS_UP,1)
bc.setGravity(0,-9.8,0)
motion=MotionCaptureData()

motionPath = pybullet_data.getDataPath()+"/motions/humanoid3d_walk.txt"#humanoid3d_spinkick.txt"#/motions/humanoid3d_backflip.txt"
motion.Load(motionPath)
print("numFrames = ", motion.NumFrames())
simTimeId= bc.addUserDebugParameter("simTime",0,motion.NumFrames()-1.1,0)

y2zOrn = bc.getQuaternionFromEuler([-1.57,0,0])
bc.loadURDF("plane.urdf",[0,-0.04,0], y2zOrn)

humanoid = Humanoid(bc, motion,[0,0,0])

simTime = 0


keyFrameDuration = motion.KeyFrameDuraction()
print("keyFrameDuration=",keyFrameDuration)
#for i in range (50):
# bc.stepSimulation()

stage = 0





def Reset(humanoid):
	global simTime
	humanoid.Reset()
	simTime = random.randint(0,motion.NumFrames()-2)
	humanoid.SetSimTime(simTime)
	pose = humanoid.InitializePoseFromMotionData()
	humanoid.ApplyPose(pose, True, True)


Reset(humanoid)
bc.stepSimulation()


while (1):
  #simTime = bc.readUserDebugParameter(frameTimeId)
  #print("keyFrameDuration=",keyFrameDuration)
  dt = (1./240.)
  print("------------------------------------------")
  print("dt=",dt)
  
  print("simTime=",simTime)
  print("humanoid.SetSimTime(simTime)")
  humanoid.SetSimTime(simTime)

  #pose = humanoid.InitializePoseFromMotionData()

  #humanoid.ApplyPose(pose, True)#False)#False, False)
  if (humanoid.Terminates()):
  	Reset(humanoid)
  	
  state = humanoid.GetState()
  action = [0]*36
  humanoid.ApplyAction(action)
  for s in range (8):
    print("step:",s)
    bc.stepSimulation()
    simTime += dt   
    time.sleep(1./240.)

