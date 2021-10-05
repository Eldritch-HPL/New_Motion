#plotting.py Runs motion_detector.py and produces bokeh plot

from bokeh.io import curdoc
from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S") # Format tooltips output
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height = 100, width = 500,
sizing_mode='scale_width', title = "Motion Graph")
p.yaxis.minor_tick_line_color = None
p.yaxis[0].ticker.desired_num_ticks=1
p.title.align = "center"    # format graph
curdoc().theme = 'dark_minimal'

hover = HoverTool(tooltips = [("Start", "@Start_string"), ("End", "@End_string")])  #Format/add HoverTools
p.add_tools(hover)

# define quadrants
q = p.quad(left = "Start", right = "End", bottom = 0,top = 1, color = "green", source = cds)

output_file("Motion_Graph.html")
show(p)
