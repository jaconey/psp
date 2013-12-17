import json
import sys

g_node_id = 0

def CheckId(node):
	if "node_id" not in node:
		global g_node_id
		g_node_id += 1
		node["node_id"] = g_node_id
		print '\tnode%d [shape=box, label="%s"]' % (g_node_id, node["func_key"][0])

def walk(caller, callee_list ):
	if len(callee_list) == 0:
		return
	CheckId(caller)

	for info in callee_list:
		CheckId(info)

		if info["inner_count"] > 0:
			print "\tnode%d -> node%d [label=\"%s\"];" %(caller["node_id"], info["node_id"],
				info["inner_count"])
		else:
			print "\tnode%d -> node%d;" %(caller["node_id"], info["node_id"])

		walk(info, info["callee_list"])

def usage():
	print "usage:python %s input_file output_file" % __file__

def main():
	if len(sys.argv) <= 2:
		return usage()

	f = open(sys.argv[1])
	data = json.loads(f.read())

	old_stdout = sys.stdout

	sys.stdout = open(sys.argv[2], "w")
	print "digraph G{"
	walk({"func_key": "____"}, data["call_info"]["callee_list"])
	print "}"

	sys.stdout = old_stdout
	print "done. use 'dot -Tgif %s > %s.gif' to generate the graph"


if __name__ == "__main__":
	main()
