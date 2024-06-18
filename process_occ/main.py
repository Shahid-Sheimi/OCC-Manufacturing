# main.py
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.STEPControl import STEPControl_Reader

def read_stp_file(file_path):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    if status == IFSelect_RetDone:
        step_reader.TransferRoots()
        shape = step_reader.Shape(1)
        return shape
    else:
        raise ValueError("Error: can't read file.")

def get_dimensions_and_volume(shape):
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    a = xmax - xmin
    b = ymax - ymin
    l = zmax - zmin
    w = xmax - xmin  # Use xmax - xmin for width
    h = ymax - ymin  # Use ymax - ymin for height
   
    return a, b, l, w, h

def surface_area(l, w,h):
    surface_area_cal = 2*(l*w+l*h+w*h)*1E-6 
    return surface_area_cal


def calculate_volume(l,w,h):
    finished_volume_mm3 = l * w * h
    return finished_volume_mm3


def calculate_area(l,w):
    finished_area_mm2 = l * w
    return finished_area_mm2

def find_tightest_tolerance(shape):
    # Perform some operations to find the tightest tolerance
    tightest_tolerance = 0.13  # Set to the tightest tolerance found
    return tightest_tolerance

def format_measurements(dimensions_mm, volume_mm3):
    dimensions_in = [mm / 25.4 for mm in dimensions_mm]
    measurements_mm = f"{dimensions_mm[0]:.3f} mm x {dimensions_mm[1]:.3f} mm x {dimensions_mm[2]:.3f} mm"
    measurements_in = f"{dimensions_in[0]:.3f} in x {dimensions_in[1]:.3f} in x {dimensions_in[2]:.3f} in"
    volume_in3 = volume_mm3 / 25.4 ** 3
    return measurements_mm, measurements_in, volume_mm3, volume_in3

def process_stp_file(file_path):
    shapes = read_stp_file(file_path)
    a, b, l, w, h = get_dimensions_and_volume(shapes)
    surface_area_cal = surface_area(l, w,h)
    finished_volume_mm3 = calculate_volume(l, w,h)
    finished_area_mm2 = calculate_area(l,w)
    tightest_tolerance = find_tightest_tolerance(shapes)
    measurements_mm, measurements_in, volume_mm3, volume_in3 = format_measurements((a, b, l), finished_volume_mm3)
    tolerances = tightest_tolerance

    return a, b, l, w, h,surface_area_cal, finished_volume_mm3, finished_area_mm2, measurements_mm, measurements_in, volume_mm3, volume_in3, tolerances



