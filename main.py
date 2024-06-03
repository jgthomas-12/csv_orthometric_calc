# Project Name
# Emlid CSV Orthometric Calculator

# Description:
# ------------
# This project will take a CSV file (data file from an Emlid with ellipsoidal height)
# will calculate the orthometric height in meters based off the ellipsoid height
# will return the geoid height and the orthometric height in meters and feet
# will make a new column in the CSV file for geoid height (Geoid Height (m)), ortho height in meters
# (Orthometric Height (m)) and ortho height in feet (Orthometric Height (ft))

# Dependencies:
# -------------
# To run this script, you'll need the following dependencies:

# - Python 3.9
# - pandas
# - pygeodesy
# - wxpython

# Installation Instructions:
# --------------------------
# 1. Make sure you have Python 3.9 installed on your machine. You can download it from the official Python website: https://www.python.org/downloads/

# 2. Install the required Python packages using pip. Open your terminal or command prompt and run the following commands:

#    ```sh
#    pip install pandas pygeodesy wxpython

# Usage:
# -----
# When this is properly installed, running the script should bring up a GUI to upload
# a file. Use this GUI to locate the file and you're trying to update and give it a new
# extension name in the space provided.
# FOR THIS TO WORK CORRECTLY each CSV file MUST HAVE columns labled "Latitude" "Longitude" and "Ellipsoidal height (m)"
# FOR THIS TO WORK CORRECTLY each CSV file MUST HAVE columns labled "Latitude" "Longitude" and "Ellipsoidal height (m)"

import wx
import pandas as pd
import pygeodesy
from pygeodesy.ellipsoidalKarney import LatLon

class FileProcessor(wx.Frame):
  def __init__(self, parent, title):
    super(FileProcessor, self).__init__(parent, title="Emlid Ortho File Processor", size=(600,200))
    panel = wx.Panel(self)

    vbox = wx.BoxSizer(wx.VERTICAL)
    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    hbox3 = wx.BoxSizer(wx.HORIZONTAL)

    self.label = wx.StaticText(panel, label="Select a CSV file:")
    hbox1.Add(self.label, flag=wx.RIGHT, border=8)

    self.file_picker = wx.FilePickerCtrl(panel, wildcard="CSV files (*.csv)|*.csv", style=wx.FLP_OPEN | wx.FLP_USE_TEXTCTRL)
    hbox1.Add(self.file_picker, proportion=1)

    vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
    vbox.Add((-1, 10))

    self.ext_label = wx.StaticText(panel, label="Enter new path name separated by underscores:")
    hbox2.Add(self.ext_label, flag=wx.RIGHT, border=8)

    self.ext_text = wx.TextCtrl(panel)
    hbox2.Add(self.ext_text, proportion=1)

    vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
    vbox.Add(-1, 10)

    self.process_button = wx.Button(panel, label="Process File", size=(100, 30))
    self.process_button.Bind(wx.EVT_BUTTON, self.process_file)
    hbox3.Add(self.process_button, proportion=1, flag=wx.ALL, border=10)

    vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
    vbox.Add((-1, 10))

    panel.SetSizer(vbox)
    self.Centre()

  def process_file(self, event):
    file_path = self.file_picker.GetPath()
    if file_path:

      ginterpolator = pygeodesy.GeoidKarney("./geoids/egm2008-5.pgm")

      data = pd.read_csv(file_path)

      csv_data = data[["Latitude", "Longitude", "Ellipsoidal height (m)"]]

      geoid_heights = []
      orthometric_heights_meters = []
      orthometric_heights_feet = []

      for index, row in csv_data.iterrows():
        lat = row["Latitude"]
        lon = row["Longitude"]
        ellipsoidal_height = row["Ellipsoidal height (m)"]
        single_position = LatLon(lat, lon)
        geoid_height = ginterpolator(single_position)
        orthometric_height_meters = ellipsoidal_height - geoid_height
        geoid_heights.append(geoid_height)
        orthometric_heights_meters.append(orthometric_height_meters)

        orthometric_height_feet = orthometric_height_meters * 3.28084
        orthometric_heights_feet.append(orthometric_height_feet)

      data.insert(data.columns.get_loc("Ellipsoidal height (m)") + 1, "Geoid Height (m)", geoid_heights)
      data.insert(data.columns.get_loc("Geoid Height (m)") + 1, "Orthometric Height (m)", orthometric_heights_meters)
      data.insert(data.columns.get_loc("Orthometric Height (m)") + 1, "Orthometric Height (ft)", orthometric_heights_feet)

      output_extension = self.ext_text.GetValue()

      output_csv_path = file_path.replace(".csv", "_{}.csv".format(output_extension))
      data.to_csv(output_csv_path, index=False)
      wx.MessageBox("Processing complete. Output file saved as:\n{}".format(output_csv_path), "Success", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
  app = wx.App(False)
  frame = FileProcessor(None, "File Processor")
  frame.Show()
  app.MainLoop()