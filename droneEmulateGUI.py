import tkinter as tk
from tkinter import ttk
import drone

labelRoll = None
labelPitch = None
labelYaw = None
labelAlt = None
labelBattery = None
labelLat = None
labelLng = None
labelmCount = None

def update_roll(value):
    drone.roll = int(float(value))
    labelRoll.config(text=f"{drone.roll}")

def update_pitch(value):
    drone.pitch = int(float(value))
    labelPitch.config(text=f"{drone.pitch}")

def update_yaw(value):
    drone.yaw = int(float(value))
    labelYaw.config(text=f"{drone.yaw}")

def update_alt(value):
    drone.relativeALT = int(float(value))
    labelAlt.config(text=f"{drone.relativeALT}")

def update_battery(value):
    drone.batteryRemain = int(float(value))
    labelBattery.config(text=f"{drone.batteryRemain}")

def update_lat():
    currentlat = entrylat.get()
    drone.lat = currentlat
    labelLat.config(text=f"{drone.lat}")

def update_lng():
    currentlng = entrylng.get()
    drone.lng = currentlng
    labelLng.config(text=f"{drone.lng}")

def update_mCount():
    currentmCount = entrymCount.get()
    drone.mCount = currentmCount
    entrymCount.config(text=f"{drone.mCount}")

def update_mode(value):
    drone.flightMode = value

def update_flight_ready():
    # 체크박스 상태에 따라 drone.FlightReady 업데이트
    drone.flightReady = flight_ready_var.get()
    print(f"FlightReady 상태: {drone.flightReady}")


def setGUI():
    global labelRoll, labelPitch, labelYaw, labelAlt, labelBattery, labelLat, labelLng, entrylat, entrylng, flight_ready_var, entrymCount
    root = tk.Tk()
    root.title("DRONE GUI")
    root.geometry("300x1000")

    # Roll
    labelRollText = tk.Label(root, text="Roll")
    labelRollText.pack(pady=1)
    labelRoll = tk.Label(root, text=f"{drone.roll}")
    labelRoll.pack(pady=1)
    sliderRoll = ttk.Scale(root, from_=0, to=360, orient="horizontal", length=250, command=update_roll)
    sliderRoll.pack(pady=2)

    # Pitch
    labelPitchText = tk.Label(root, text="Pitch")
    labelPitchText.pack(pady=1)
    labelPitch = tk.Label(root, text=f"{drone.pitch}")
    labelPitch.pack(pady=1)
    sliderPitch = ttk.Scale(root, from_=0, to=360, orient="horizontal", length=250, command=update_pitch)
    sliderPitch.pack(pady=2)

    # Yaw
    labelYawText = tk.Label(root, text="Yaw")
    labelYawText.pack(pady=1)
    labelYaw = tk.Label(root, text=f"{drone.yaw}")
    labelYaw.pack(pady=1)
    sliderYaw = ttk.Scale(root, from_=0, to=360, orient="horizontal", length=250, command=update_yaw)
    sliderYaw.pack(pady=2)

    # Altitude
    labelAltText = tk.Label(root, text="Altitude")
    labelAltText.pack(pady=1)
    labelAlt = tk.Label(root, text=f"{drone.relativeALT}")
    labelAlt.pack(pady=1)
    sliderAlt = ttk.Scale(root, from_=0, to=1000, orient="horizontal", length=250, command=update_alt)
    sliderAlt.pack(pady=2)

    # Battery
    labelBatteryText = tk.Label(root, text="Battery")
    labelBatteryText.pack(pady=1)
    labelBattery = tk.Label(root, text=f"{drone.batteryRemain}")
    labelBattery.pack(pady=1)
    sliderBattery = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=250, command=update_battery)
    sliderBattery.pack(pady=2)

    # Latitude
    entrylat = ttk.Entry(root)
    entrylat.pack(pady=1)
    labelLatText = ttk.Label(root, text="Latitude")
    labelLatText.pack(pady=1)
    labelLat = ttk.Label(root, text=f"{drone.lat}")
    labelLat.pack(pady=1)
    buttonlat = tk.Button(root, text="Set Latitude", command=update_lat)
    buttonlat.pack(pady=1)

    # Longitude
    entrylng = ttk.Entry(root)
    entrylng.pack(pady=1)
    labelLngText = ttk.Label(root, text="Longitude")
    labelLngText.pack(pady=1)
    labelLng = ttk.Label(root, text=f"{drone.lng}")
    labelLng.pack(pady=1)
    buttonlng = tk.Button(root, text="Set Longitude", command=update_lng)
    buttonlng.pack(pady=1)

    # Flight Mode
    labelModeText = tk.Label(root, text="Flight Mode")
    labelModeText.pack(pady=1)
    options = ["Stabilized", "Offboard", "Manual"]
    selected_option = tk.StringVar()
    selected_option.set(options[0])
    option_menu = tk.OptionMenu(root, selected_option, *options, command=update_mode)
    option_menu.pack(pady=2)

    flight_ready_var = tk.BooleanVar(value=drone.flightReady)
    flight_ready_checkbox = tk.Checkbutton(root, text="Flight Ready", variable=flight_ready_var, command=update_flight_ready)
    flight_ready_checkbox.pack(pady=2)

    entrymCount = ttk.Entry(root)
    entrymCount.pack(pady=1)
    labelmCountText = ttk.Label(root, text="mCount")
    labelmCountText.pack(pady=1)
    labelmCount = ttk.Label(root, text=f"{drone.mCount}")
    labelmCount.pack(pady=1)
    buttonmCount = tk.Button(root, text="Set mCount", command=update_mCount)
    buttonmCount.pack(pady=1)


    root.mainloop()
