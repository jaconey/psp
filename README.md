PSP - Python Statistical Profiler.
===

This package provides a simple statistical profiler for Python.

The idea is inspired by google-perftools which uses SIGPROF signal to halt the proccess, collect the whole stack infomations at current frame and after all provide results based on statistics.

Basic usage
---------------
It's easy to integrate with psp, here is an example :
```python
from psp import profiler
def fun():
    profiler.Start("output_file_name")
    """ your code """
    profiler.Stop()
fun()
```

In ``profiler.Start`` we passed a file name to the function so when we called ``profiler.Stop`` the result woull be written with that file name. 

Data processing
------------------

Since that all data are serialized in JSON format, it is easy to convert them into other representations. 
 
A example script that parse and output the result to DOT format is included in the source code. Some one have been using the result on a website, which is drawed by [D3.js] [1] 
[1]: http://d3js.org/ "D3 Javascript liberary"

Reference
------------------
There are similar projects on github, such as: [bos/statprof.py](https://github.com/bos/statprof.py)

