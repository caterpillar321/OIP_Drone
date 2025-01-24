import tkinter as tk
from tkinter import ttk
import drone  

labelX = None
labelY = None
labelmCount = None

"""
def update_x():
    currentx = entryX.get()
    drone.x = currentx
    labelX.config(text=f"{drone.x}")
    """

def update_x(value):
    drone.x = int(float(value))
    labelX.config(text=f"{drone.x}")

def update_y(value):
    drone.y = int(float(value))
    labelY.config(text=f"{drone.y}")

def update_mCount():
    currentmCount = entrymCount.get()
    drone.mCount = currentmCount
    entrymCount.config(text=f"{drone.mCount}")



def setGUI():
    global labelX, labelY, entrymCount
    root = tk.Tk()
    root.title("DRONE SLAM GUI")
    root.geometry("300x500")

    labelXText = tk.Label(root, text="X")
    labelXText.pack(pady=1)
    labelX = tk.Label(root, text=f"{drone.x}")
    labelX.pack(pady=1)
    sliderRoll = ttk.Scale(root, from_=-5000, to=5000, orient="horizontal", length=250, command=update_x)
    sliderRoll.pack(pady=2)

    labelYText = tk.Label(root, text="Y")
    labelYText.pack(pady=1)
    labelY = tk.Label(root, text=f"{drone.y}")
    labelY.pack(pady=1)
    sliderRoll = ttk.Scale(root, from_=-5000, to=5000, orient="horizontal", length=250, command=update_y)
    sliderRoll.pack(pady=2)

    entrymCount = ttk.Entry(root)
    entrymCount.pack(pady=1)
    labelmCountText = ttk.Label(root, text="mCount")
    labelmCountText.pack(pady=1)
    labelmCount = ttk.Label(root, text=f"{drone.mCount}")
    labelmCount.pack(pady=1)
    buttonmCount = tk.Button(root, text="Set mCount", command=update_mCount)
    buttonmCount.pack(pady=1)


    """
    entryX = ttk.Entry(root)
    entryX.pack(pady=1)
    labelXText = ttk.Label(root, text="drone X Pos")
    labelXText.pack(pady=1)
    labelX = ttk.Label(root, text=f"{drone.x}")
    labelX.pack(pady=1)

    buttonlat = tk.Button(root, text="set lat", command=update_x)
    buttonlat.pack(pady=1)
    """
    root.mainloop()