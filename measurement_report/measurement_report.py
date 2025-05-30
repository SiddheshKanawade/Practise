import matplotlib.pyplot as plt
import mpld3
import numpy as np

plt.figure()
plt.plot(range(10), [i*np.sin(i) for i in range(10)])

html_string = mpld3.fig_to_html(plt.gcf())

with open("./output.html", "w") as f:
   f.write(html_string)
