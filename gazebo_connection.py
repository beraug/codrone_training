{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/usr/bin/env python\n",
    "\n",
    "import rospy\n",
    "from std_srvs.srv import Empty\n",
    "\n",
    "class GazeboConnection():\n",
    "    \n",
    "    def __init__(self):\n",
    "        \n",
    "        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)\n",
    "        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)\n",
    "        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)\n",
    "    \n",
    "    def pauseSim(self):\n",
    "        rospy.wait_for_service('/gazebo/pause_physics')\n",
    "        try:\n",
    "            self.pause()\n",
    "        except rospy.ServiceException, e:\n",
    "            print (\"/gazebo/pause_physics service call failed\")\n",
    "        \n",
    "    def unpauseSim(self):\n",
    "        rospy.wait_for_service('/gazebo/unpause_physics')\n",
    "        try:\n",
    "            self.unpause()\n",
    "        except rospy.ServiceException, e:\n",
    "            print (\"/gazebo/unpause_physics service call failed\")\n",
    "        \n",
    "    def resetSim(self):\n",
    "        rospy.wait_for_service('/gazebo/reset_simulation')\n",
    "        try:\n",
    "            self.reset_proxy()\n",
    "        except rospy.ServiceException, e:\n",
    "            print (\"/gazebo/reset_simulation service call failed\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
