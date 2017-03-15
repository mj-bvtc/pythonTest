import rhinoscriptsyntax as rs
import Rhino



def addArcLeader():
    """
    Automatically calculates and annotates the length of a curve object,
    used primarily for arc length
    
    Input parameters: None    
    
    Returns: Guid if successful
             None if failure    
    """

    try:
        #assign empty variables
        points = []
        leader = None
        
        #get curve
        crv = rs.GetCurveObject("Select curve object")    
        crvLen = rs.CurveLength(crv[0])  #get curve's length  

        #get points
        pts = rs.GetPoints("AddPoints, press enter when done")     
        points = rs.AddPoints(pts)    

        #make leader
        leader = rs.AddLeader(points, text="ArcLength: " + str(round(crvLen, 3)))
        return leader

    except Exception:
        pass

    finally:
        if points:
            rs.DeleteObjects(points)  #points will be deleted even upon exception
        return leader

def main():
    leader = addArcLeader()
    print leader

if __name__ == "__main__":
    main()