import rhinoscriptsyntax as rs

if rs.UnitSystem() == 2:
    # Current unit is mm, Switch to m
    rs.UnitSystem(8, False, True)
else:
    # Current unit is m, switch to mm
    rs.UnitSystem(8, False, True)