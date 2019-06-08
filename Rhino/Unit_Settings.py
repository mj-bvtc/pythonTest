import rhinoscriptsyntax as rs

if rs.UnitSystem() == 2:
    # Current unit is mm, Switch to in
    rs.UnitSystem(8, False, True)
else:
    # Current unit is inches, no change
    rs.UnitSystem(8, False, True)

rs.DimStyleTextHeight("synch template", 0.125)

rs.CurrentDimStyle ("synch template")