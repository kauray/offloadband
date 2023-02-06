Python 3.6.9 (default, Dec  8 2021, 21:08:43) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> from pandas import read_csv
from matplotlib import pyplot
series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
series.plot()
pyplot.show()
SyntaxError: multiple statements found while compiling a single statement
>>> from pandas import read_csv
>>> from matplotlib import pyplot
>>> series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
>>> series.plot()
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8c43c54a8>
>>> pyplot.show()
>>> series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_row=0, squeeze=True)
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_row=0, squeeze=True)
TypeError: parser_f() got an unexpected keyword argument 'index_row'
>>> series.boxplot()
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b07fac88>
>>> pyplot.show()
>>> series.bar()
Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    series.bar()
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/generic.py", line 5274, in __getattr__
    return object.__getattribute__(self, name)
AttributeError: 'DataFrame' object has no attribute 'bar'
>>> series.plot.bar()
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b058b400>
>>> pyplot.show()
>>> pyplot.box()
>>> pyplot.show()
>>> series.boxplot()
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a67a9438>
>>> pyplot.show()
>>> series.boxplot('gD')
Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
    series.boxplot('gD')
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/plotting/_core.py", line 447, in boxplot_frame
    **kwargs,
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/plotting/_matplotlib/boxplot.py", line 375, in boxplot_frame
    **kwds,
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/plotting/_matplotlib/boxplot.py", line 341, in boxplot
    data = data[columns]
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/frame.py", line 2806, in __getitem__
    indexer = self.loc._get_listlike_indexer(key, axis=1, raise_missing=True)[1]
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1553, in _get_listlike_indexer
    keyarr, indexer, o._get_axis_number(axis), raise_missing=raise_missing
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/indexing.py", line 1640, in _validate_read_indexer
    raise KeyError(f"None of [{key}] are in the [{axis_name}]")
KeyError: "None of [Index(['gD'], dtype='object')] are in the [columns]"
>>> plt.setp(bp['D + P'], color='red', marker='+')
Traceback (most recent call last):
  File "<pyshell#17>", line 1, in <module>
    plt.setp(bp['D + P'], color='red', marker='+')
NameError: name 'plt' is not defined
>>> pyplot.setp(bp['D + P'], color='red', marker='+')
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    pyplot.setp(bp['D + P'], color='red', marker='+')
NameError: name 'bp' is not defined
>>> pyplot.setp(series['D + P'], color='red', marker='+')
Traceback (most recent call last):
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/indexes/base.py", line 2646, in get_loc
    return self._engine.get_loc(key)
  File "pandas/_libs/index.pyx", line 111, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 1619, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 1627, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'D + P'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    pyplot.setp(series['D + P'], color='red', marker='+')
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/frame.py", line 2800, in __getitem__
    indexer = self.columns.get_loc(key)
  File "/home/kauray/.local/lib/python3.6/site-packages/pandas/core/indexes/base.py", line 2648, in get_loc
    return self._engine.get_loc(self._maybe_cast_indexer(key))
  File "pandas/_libs/index.pyx", line 111, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 1619, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 1627, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'D + P'
>>> color=dict(boxes='r', whiskers='r', medians='r', caps='r')
>>> color=dict('D + P'='r')
SyntaxError: keyword can't be an expression
>>> series.boxplot(patch_artist = True)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a5e85128>
>>> pyplot.show()
>>> pyplot.setup(series['D + P'], color='red', marker='+')
Traceback (most recent call last):
  File "<pyshell#24>", line 1, in <module>
    pyplot.setup(series['D + P'], color='red', marker='+')
AttributeError: module 'matplotlib.pyplot' has no attribute 'setup'
>>> pyplot.boxplot.setup(series['D + P'], color='red', marker='+')
Traceback (most recent call last):
  File "<pyshell#25>", line 1, in <module>
    pyplot.boxplot.setup(series['D + P'], color='red', marker='+')
AttributeError: 'function' object has no attribute 'setup'
>>> series.boxplot()
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a3c10f60>
>>> pyplot.show()
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a3b34630>
>>> pyplot.show()
>>> series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_row=0, squeeze=True)
Traceback (most recent call last):
  File "<pyshell#30>", line 1, in <module>
    series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_row=0, squeeze=True)
TypeError: parser_f() got an unexpected keyword argument 'index_row'
>>> series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_col=0, squeeze=True)
>>> series.boxplot()
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b09a2668>
>>> pyplot.show()
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a3d26630>
>>> pyplot.show()
>>> pyplot.grid(False)
>>> pyplot.show()
>>> pyplot.grid(True)
>>> pyplot.show()
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a39ae5f8>
>>> pyplot.show()
>>> pyplot.xlabel('Combination Of Applications')
Text(0.5, 0, 'Combination Of Applications')
>>> pyplot.ylabel('Average Task Runtime (in seconds)')
Text(0, 0.5, 'Average Task Runtime (in seconds)')
>>> pyplot.show()
>>> pyplot.show()
>>> pyplot.show()
>>> pyplot.ylabel('Average Task Runtime (in seconds)')
Text(0, 0.5, 'Average Task Runtime (in seconds)')
>>> pyplot.xlabel('Combination Of Applications')
Text(0.5, 0, 'Combination Of Applications')
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b05e8240>
>>> pyplot.show()
>>> pyplot.grid(False)
>>> pyplot.show()
>>> pyplot.xlabel('Combination Of Applications')
Text(0.5, 0, 'Combination Of Applications')
>>> pyplot.ylabel('Average Task Runtime (in seconds)')
Text(0, 0.5, 'Average Task Runtime (in seconds)')
>>> pyplot.grid(False)
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b0557ef0>
>>> pyplot.show()
>>> series = read_csv('/home/kauray/Desktop/data.csv', header=0, index_col=0, squeeze=True)
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b05574e0>
>>> pyplot.show()
>>> series = read_csv('/home/kauray/Desktop/data.csv', header=0, squeeze=True)
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8b05cc710>
>>> pyplot.show()
>>> series = read_csv('/home/kauray/Desktop/data2.csv', header=0, squeeze=True)
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a6160b00>
>>> pyplot.show()
>>> series = read_csv('/home/kauray/Desktop/data3.csv', header=0, squeeze=True)
>>> series.boxplot(showfliers=False)
<matplotlib.axes._subplots.AxesSubplot object at 0x7fa8a608da90>
>>> pyplot.show()
>>> 
