#!/usr/bin/python
#-*- coding: utf-8 -*-

"""A periodic sampling profiler."""

import json
import signal
import sys

class SampleNode(object):
	def __init__(self):
		self.func_key = ('', '', 0)
		self.inner_count = 0
		self.callee_dict = {}

	def to_dict(self):
		dd = {'func_key': self.func_key, 'inner_count': self.inner_count}
		callee_list = []
		for callee in self.callee_dict.values():
			callee_list.append(callee.to_dict())
		dd['callee_list'] = callee_list
		return dd

class SampleCollector(object):
	def __init__(self, interval = 0.01, mode = 'virtual', filename = ""):
		if hasattr(signal, 'setitimer'):
			self.MODES = {
			'prof': (signal.ITIMER_PROF, signal.SIGPROF),
			'virtual': (signal.ITIMER_VIRTUAL, signal.SIGVTALRM),
			'real': (signal.ITIMER_REAL, signal.SIGALRM),
			}
		self._interval = interval
		if mode not in self.MODES:
			mode = 'virtual'
		self._mode = mode
		self._root_node = SampleNode()
		self._root_node.func_key = ('root', 'root', 0)
		self._stopped = False
		self._samples_taken = 0
		self._filename = filename
		self._max_depth = 100
		self._stop_cb = None

	def start(self, duration = 30.0, callback = None):
		self._stopped = False
		self._stop_cb = callback

		timer, sig = self.MODES[self._mode]
		signal.signal(sig, self.handler)
		signal.setitimer(timer, self._interval, self._interval)

	def stop(self):
		timer, sig = self.MODES[self._mode]
		signal.signal(sig, signal.SIG_IGN)
		signal.setitimer(timer, 0)

		if self._filename != "":
			with open(self._filename, "w") as f:
				output = dict()
				output["total_samples"] = self._samples_taken
				output["call_info"] = self._root_node.to_dict()
				f.write(json.dumps(output, sort_keys=True, indent=4))

		if self._stop_cb is not None:
			self._stop_cb()

		self._stopped = True

	def handler(self, sig, current_frame):
		if self._stopped:
			return

		for tid, frame in sys._current_frames().iteritems():
			func_list = []
			while frame is not None:
				code = frame.f_code
				if code.co_name != "handler" and code.co_filename != __file__:
					func_list.append((code.co_name, code.co_filename, code.co_firstlineno))
				frame = frame.f_back

			node = self._root_node
			for func_key in reversed(func_list):
				sub_node = node.callee_dict.get(func_key)
				if not sub_node:
					sub_node = SampleNode()
					sub_node.func_key = func_key
					node.callee_dict[func_key] = sub_node
				node = sub_node
			node.inner_count += 1
		self._samples_taken += 1

g_collector = None
def Start(filename, time_long = 1000):
	global g_collector
	if g_collector is not None:
		return False

	g_collector = SampleCollector(mode = "real", filename = filename)
	g_collector.start(time_long, StopCallback)
	return True

def StopCallback():
	global g_collector
	g_collector = None

def Stop():
	global g_collector
	if g_collector is None:
		return False
	g_collector.stop()
	g_collector = None
	return True

