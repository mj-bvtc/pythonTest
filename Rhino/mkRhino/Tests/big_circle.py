import rhinoscriptsyntax as rs

origin = [0,0,0]
def draw_circle(radius):
    rs.AddCircle(origin, radius)

def zoom_extents():
    rs.ZoomExtents()

def main():
    circle = rs.GetObject("select biggest circle so far", filter=rs.filter.curve)
    radius = rs.CircleRadius(circle)
    for i in range(200):
        radius *= 5
        print radius
        draw_circle(radius)
        zoom_extents()


if __name__ == "__main__":
    main()