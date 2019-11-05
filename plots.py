from bokeh.plotting import figure, output_file, show

# prepare some data
year = [1990, 1995, 2000, 2005, 2006, 2010, 2011, 2015, 2016, 2017, 2018, 2019, 2020]
CO2_real = [2517, 2459, 2471, 2386, 2295, 2116, 2061, 2017, 1981, 1954]
CO2_planned = [2517, 2349.2, 2181.4, 2013.6, 1980.04, 1845.8, 1812.24, 1678, 1644.44, 1610.88, 1577.32, 1543.76, 1510.2]

# output to static HTML file
output_file("index.html")

# create a new plot with a title and axis labels
p = figure(title="Klimaschutz Münster: Pläne und Realität", x_axis_label='Jahr', y_axis_label='CO2 (in tausend Tonnen)', y_range = (0, 2550))

# add a line renderer with legend and line thickness
p.line(year, CO2_real, legend="CO2-Emissionen (in tausend Tonnen)", line_width=2, color="#d95f02")
p.line(year, CO2_planned, legend="CO2-Ziele (in tausend Tonnen)", line_width=2, color="#1b9e77")

p.legend.location = "center_left"

# show the results
show(p)
