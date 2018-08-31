{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/usr/bin/env python\n",
    "import sys\n",
    "print sys.path\n",
    "import numpy as np\n",
    "print np.__file__\n",
    "print np.__version__\n",
    "import os\n",
    "import gym\n",
    "\n",
    "import matplotlib\n",
    "import matplotlib.pyplot as plt\n",
    "import itertools\n",
    "import sys\n",
    "import argparse\n",
    "import rospkg\n",
    "\n",
    "from scipy.interpolate import pchip\n",
    "\n",
    "class LivePlot(object):\n",
    "    def __init__(self, outdir, data_key='episode_rewards', line_color='blue'):\n",
    "        \"\"\"\n",
    "        Liveplot renders a graph of either episode_rewards or episode_lengths\n",
    "        Args:\n",
    "            outdir (outdir): Monitor output file location used to populate the graph\n",
    "            data_key (Optional[str]): The key in the json to graph (episode_rewards or episode_lengths).\n",
    "            line_color (Optional[dict]): Color of the plot.\n",
    "        \"\"\"\n",
    "        #data_key can be set to 'episode_lengths'\n",
    "        self.outdir = outdir\n",
    "        self._last_data = None\n",
    "        self.data_key = data_key\n",
    "        self.line_color = line_color\n",
    "\n",
    "        #styling options\n",
    "        matplotlib.rcParams['toolbar'] = 'None'\n",
    "        plt.style.use('ggplot')\n",
    "        plt.xlabel(\"episodes\")\n",
    "        plt.ylabel(\"cumulated episode rewards\")\n",
    "        fig = plt.gcf().canvas.set_window_title('averaged_simulation_graph')\n",
    "        matplotlib.rcParams.update({'font.size': 15})\n",
    "\n",
    "    def plot(self, full=True, dots=False, average=0, interpolated=0):\n",
    "        results = gym.monitoring.load_results(self.outdir)\n",
    "        data =  results[self.data_key]\n",
    "        avg_data = []\n",
    "\n",
    "        if full:\n",
    "            plt.plot(data, color='blue')\n",
    "        if dots:\n",
    "            plt.plot(data, '.', color='black')\n",
    "        if average > 0:\n",
    "            average = int(average)\n",
    "            for i, val in enumerate(data):\n",
    "                if i%average==0:\n",
    "                    if (i+average) < len(data)+average:\n",
    "                        avg =  sum(data[i:i+average])/average\n",
    "                        avg_data.append(avg)\n",
    "            new_data = expand(avg_data,average)\n",
    "            plt.plot(new_data, color='red', linewidth=2.5) \n",
    "        if interpolated > 0:\n",
    "            avg_data = []\n",
    "            avg_data_points = []\n",
    "            n = len(data)/interpolated\n",
    "            if n == 0:\n",
    "                n = 1\n",
    "            data_fix = 0\n",
    "            for i, val in enumerate(data):\n",
    "                if i%n==0:\n",
    "                    if (i+n) <= len(data)+n:\n",
    "                        avg =  sum(data[i:i+n])/n\n",
    "                        avg_data.append(avg)\n",
    "                        avg_data_points.append(i)\n",
    "                if (i+n) == len(data):\n",
    "                    data_fix = n\n",
    "            \n",
    "            x = np.arange(len(avg_data))\n",
    "            y = np.array(avg_data)\n",
    "            #print x\n",
    "            #print y\n",
    "            #print str(len(avg_data)*n)\n",
    "            #print data_fix\n",
    "            interp = pchip(avg_data_points, avg_data)\n",
    "            xx = np.linspace(0, len(data)-data_fix, 1000)\n",
    "            plt.plot(xx, interp(xx), color='green', linewidth=3.5)        \n",
    "\n",
    "        # pause so matplotlib will display\n",
    "        # may want to figure out matplotlib animation or use a different library in the future\n",
    "        # plt.pause(0.000001)\n",
    "\n",
    "def expand(lst, n):\n",
    "    lst = [[i]*n for i in lst]\n",
    "    lst = list(itertools.chain.from_iterable(lst))\n",
    "    return lst\n",
    "\n",
    "def pause():\n",
    "    programPause = raw_input(\"Press the <ENTER> key to finish...\")\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    \n",
    "    rospack = rospkg.RosPack()\n",
    "    pkg_path = rospack.get_path('codrone_training')\n",
    "    outdir = pkg_path + '/training_results'\n",
    "    plotter = LivePlot(outdir)\n",
    "\n",
    "    parser = argparse.ArgumentParser()\n",
    "    parser.add_argument(\"-f\", \"--full\", action='store_true', help=\"print the full data plot with lines\")\n",
    "    parser.add_argument(\"-d\", \"--dots\", action='store_true', help=\"print the full data plot with dots\")\n",
    "    parser.add_argument(\"-a\", \"--average\", type=int, nargs='?', const=50, metavar=\"N\", help=\"plot an averaged graph using N as average size delimiter. Default = 50\")\n",
    "    parser.add_argument(\"-i\", \"--interpolated\", type=int, nargs='?', const=50, metavar=\"M\", help=\"plot an interpolated graph using M as interpolation amount. Default = 50\")\n",
    "    args = parser.parse_args()\n",
    "\n",
    "    if len(sys.argv)==1:\n",
    "        # When no arguments given, plot full data graph\n",
    "        plotter.plot(full=True)\n",
    "    else:\n",
    "        plotter.plot(full=args.full, dots=args.dots, average=args.average, interpolated=args.interpolated)\n",
    "\n",
    "    plt_save_path = outdir + \"/experiment_data_plot.png\"\n",
    "    plt.savefig(plt_save_path)\n",
    "    print (\"Saved plot in \"+plt_save_path)\n",
    "    print \"Opening Plot in Graphic Tools Window\"\n",
    "    plt.show()\n",
    "    # pause()"
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
