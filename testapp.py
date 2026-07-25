import backend.fastf1data as f1

print("File:", f1.__file__)
print("Dir:", dir(f1))
print("Has get_races:", hasattr(f1, "get_races"))
print("Has get_drivers:", hasattr(f1, "get_drivers"))