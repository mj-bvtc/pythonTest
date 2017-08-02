import rhinoscriptsyntax as rs
import ghpythonlib.parallel
import math
import time
import Rhino
import scriptcontext

#####  General Matrix Functions  #####
def AbsMatrix(Matrix):
    """
    Solve for the absolute value of every entry in a matrix.
    
    Input Parameter:
        Matrix - [MxN] Matrix of values.
    
    Returns:
        NewMatrix - [MxN] Matrix of absolute values.
        (All positive)
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        for j in range(len(Matrix[i])):
            NewRow.append(abs(Matrix[i][j]))
        NewMatrix.append(NewRow)
    return NewMatrix

def ColumnAverage(Matrix):
    """
    Solve for the Average of each column of a NxM Matrix
    
    Input Parameters:
        Matrix - [MxN] Matrix  to solve average for each column.
    
    Returns:
        NewMatrix [M] List containing column averages.
    """
    Mt=TransposeMatrix(Matrix)
    AvgVector=[]
    for i in range(len(Mt)):
        AvgVector.append(sum(Mt[i])/len(Mt[i]))
    return AvgVector

def DataTranslate(Matrix,Location):
    """
    Translates a matrix of points from a location to the origin. 
    Reducing error in calculations.
    
    Input Parameters:
        Matrix - [MxN] matrix of points to be translated
        Location - [x,y,z] point descriping the location of the matrix.  (Typically Centroid of Points)
    
    Returns:
        NewMatrix - [MxN] Matrix of points located around origin
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        for j in range(len(Matrix[i])):
            NewRow.append(Matrix[i][j]-Location[j])
        NewMatrix.append(NewRow)
    return NewMatrix

def DotProduct(Matrix0,Matrix1):
    """
    Solve for the Dot Product of a two square matricies.
    
    Input Parameters:
        Matrix0 - [NxN] Matrix for dot product.
        Matrix1 - [NxN] Matrix for dot product.
    
    Return:
        NewMatrix - [N] Sumation of each matrix row item multiplied together.
    """
    M0_Cols=len(Matrix0[0])
    M0_Rows=len(Matrix0)
    M1_Cols=len(Matrix1[0])
    M1_Rows=len(Matrix1)
    
    NewMatrix=[]
    if M0_Cols==M1_Cols and M1_Rows==M0_Rows:
        for i in range(M0_Rows):
            Items=[]
            NewRow=[]
            for j in range(M0_Cols):
                Items.append(Matrix0[i][j]*Matrix1[i][j])
            NewRow.append(sum(Items))
            NewMatrix.append(NewRow)
    return NewMatrix

def MatrixToPoints(Matrix):
    """
    Convert a [3xN] Matrix of points into a list of rhino guids.
    
    Input Parameters:
        Matrix - [3xN] Matrix of points.
    
    Returns:
        Points - List of Point guids.
    """
    Points=[]
    for Pt in Matrix:
        if len(Pt)==3:
            Points.append(rs.coerce3dpoint(Pt))
    return Points

def ProjectToPlane(Matrix,Normal):
    """
    Project a [3xN] Matrix of points to a plane passing through the
    origin perpendicular to the Normal.
    
    Input Parameters:
        Matrix - [3xN] Matrix of points to be projected onto a single plane.
        Normal - [a,b,c] Vector describing the normal of the plane.
        
    Returns:
        NewMatrix - [3xN] Matrix of points projected to a plane normal to 
        input vector passing through the origin.
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        DP=DotProduct([Matrix[i]],[Normal])[0][0]
        Vector=[Normal[0]*DP,Normal[1]*DP,Normal[2]*DP]
        for j in range(len(Matrix[i])):
            NewRow.append(Matrix[i][j]-Vector[j])
        NewMatrix.append(NewRow)
    return NewMatrix

def PointsToMatrix(PtList):
    """
    Convert a list of Point guid's to a matrix of position vectors.
    For faster processing.
    
    Input Parameters:
        PtList - (List) of points to be converted to a Matrix.
            ***Will not work with data trees.***
        
        Returns:
            [Matrix] 3xN Matrix of position vectors.
    """
    NewMatrix=[]
    for Pt in PtList:
        if Pt!=None:
            if rs.IsPoint(Pt)==True:
                Pt=rs.coerce3dpoint(Pt)
                NewPt=[Pt.X,Pt.Y,Pt.Z]
                NewMatrix.append(NewPt)
            else:
                print Pt
    return NewMatrix

def PointsToPlane(Points):
    """
    Solve for a best fit plane for a list of Points, and project all points to best fit plane.
    (Points should probably be in guid form to be passed into definition.)
    
    Input Parameters:
        Points - List of Points to fit to Plane.
        
    Returns:
        PtsOnPlane - [3xN] Matrix of Points projected onto the best fit plane.
        Plane - Plane of best fit onto which points are projected.
    """
    PtsOnPlane=[]
    Plane=rs.PlaneFitFromPoints(Points)
    EQ=rs.PlaneEquation(Plane)
    for Pt in Points:
        NewRow=[]
        if rs.IsPoint(Pt)==True:
            Pt=rs.PointCoordinates(Pt)
        t=(-Pt[0]*EQ[0]-Pt[1]*EQ[1]-Pt[2]*EQ[2]-EQ[3])/((EQ[0]**2)+(EQ[1]**2)+(EQ[2]**2))
        PtOnPlane=[Pt[0]+t*EQ[0],Pt[1]+t*EQ[1],Pt[2]+t*EQ[2]]
        PtsOnPlane.append(PtOnPlane)
    return PtsOnPlane,Plane

def PtsTo2D(Points):
    """
    Convert Points to 2D Projected then Translated to the XY Plane 
    with the Centroid at the Origin.
    
    Input Parameters:
        Points - List of Point guids (Probably has to be Guids)
    
    Returns:
        XY - The [X,Y] points projected to a plane then translated.
        Normal - Vector normal to the best fit plane for the input points.
        Centroid - Centroid of point cloud lies on best fit plane.
        U1 - Rotation Matrix about X-Axis to align Normal with YZ Plane.
        U2 - Rotation Matrix about Y-Axis to align Normal with XZ Plane
    """
    
    Matrix,Plane=PointsToPlane(Points)
    
    Centroid=ColumnAverage(Matrix)
    EQ=rs.PlaneEquation(Plane)
    Normal=[EQ[0],EQ[1],EQ[2]]
    
    Points=DataTranslate(Matrix,Centroid)
    
    Points,U1,U2=RotatePoints(Points,Normal)
    XY=RemoveZ(Points)
    return XY,Normal,Centroid,U1,U2

def RotateAboutX(Vector):
    """
    Defines a [3x3] Rotation Matrix around the X-Axis.
    
    Input Parameters:
        Vector - [a,b,c] to Rotate to align with ZY Plane.
    
    Returns:
        NewMatrix - [3x3] Rotation Matrix for the given Vector
        
        [  1    0    0  ]
        [  0   Cos  Sin ]
        [  0   Sin  Cos ]
    """
    a=Vector[0]
    b=Vector[1]
    c=Vector[2]
    NewMatrix=[]
    if Vector[1]!=0:
        NewMatrix.append([1,0,0])
        NewMatrix.append([0,c/math.sqrt(b**2+c**2),-b/math.sqrt(b**2+c**2)])
        NewMatrix.append([0,b/math.sqrt(b**2+c**2),c/math.sqrt(b**2+c**2)])
    else:
        NewMatrix.append([1,0,0])
        NewMatrix.append([0,1,0])
        NewMatrix.append([0,0,1])
    return NewMatrix

def RotateAboutY(Vector):
    """
    Defines a [3x3] Rotation Matrix around the Y-Axis.
    
    Input Parameters:
        Vector - [a,b,c] to Rotate to align with XZ Plane.
    
    Returns:
        NewMatrix - [3x3] Rotation Matrix for the given Vector
        
        [ Cos   0   Sin ]
        [  0    1    0  ]
        [-Cos   0   Cos ]
    """
    a=Vector[0]
    b=Vector[1]
    c=Vector[2]
    NewMatrix=[]
    if Vector[0]!=0:
        NewMatrix.append([math.sqrt(b**2+c**2)/math.sqrt(a**2+b**2+c**2),0,-(a)/math.sqrt(a**2+b**2+c**2)])
        NewMatrix.append([0,1,0])
        NewMatrix.append([(a)/math.sqrt(a**2+b**2+c**2),0,(math.sqrt(b**2+c**2))/math.sqrt(a**2+b**2+c**2)])
    else:
        NewMatrix.append([1,0,0])
        NewMatrix.append([0,1,0])
        NewMatrix.append([0,0,1])
    return NewMatrix

def SolveLinearEquations(M_Input,M_Solution):
    """
    Solves System of Linear Equations
    (Solve by zeroing variables before pivot then back solving.)
    (Definition will crash if the number under a pivot is a 0)
    
    Input Parameters:
        M_Input - [NxN] Matrix containing system of equations to be solved.
        M_Solution - [1xN] Matrix of solutions for the System of Equations.
    
    Returns:
        M_Solution - [1xN] Solution set for variables of system of equations.
    """
    ###Combine Matricies###
    if len(M_Input)==len(M_Solution):
        if len(M_Solution[0])==1:
            Matrix=[]
            for i in range(len(M_Input)):
                NewRow=[]
                for j in range(len(M_Input[i])):
                    NewRow.append(M_Input[i][j])
                NewRow.append(M_Solution[i][0])
                Matrix.append(NewRow)
            
            M_Cols=len(Matrix[0])
            M_Rows=len(Matrix)
            ###Reduced Row Form###
            for i in range(M_Rows):
                for j in range(M_Cols):
                    if  i>j:
                        Factor=Matrix[i][j]/Matrix[j][j]
                        NewRow=[]
                        for k in range(M_Cols):
                            NewRow.append(Matrix[i][k]-(Factor*Matrix[j][k]))
                        Matrix[i]=NewRow
            
            ###Solve for Variables###
            Solved=[]
            for i in range(M_Rows):
                Pivot=M_Rows-i-1
                Solution=Matrix[Pivot][M_Cols-1]
                if Solved!=[]:
                    for j in range(1,len(Solved)+1):
                        Solution=Solution-(Solved[j-1]*Matrix[Pivot][Pivot+j])
                Solved.insert(0,(Solution/Matrix[Pivot][Pivot]))
            return Solved

def TransposeMatrix(Matrix):
    """
    Flip Matrix Columns and Rows
    
    Input Parameters:
        Matrix - [MxN] Matrix in array of lists form.
    
    Returns:
        NewMatrix - [MxN] Flipped Matrix
    """
    NewMatrix=[]
    for i in range(len(Matrix[0])):
        NewRow=[]
        for j in range(len(Matrix)):
            NewRow.append(Matrix[j][i])
        NewMatrix.append(NewRow)
    return NewMatrix

def TranslateTo3D(XY,Vector,U1,U2):
    """
    Translate 2D Points into 3D space given (2) Rotation Matricies and a Translation Vector
    
    Input Parameters:
        XY - Matrix[NxM] of XY points
        Vector - Translation Vector
        U1 - First Rotation Matrix [3x3]
        U2 - Second Rotation Matrix [3x3]
    
    Returns:
        FinalPoints - Matrix of Points in 3D rotated and translated into position.
    """
    
    Points=[]
    for i in range(len(XY)):
        NewRow=[]
        for j in range(len(XY[i])):
            NewRow.append(XY[i][j])
        NewRow.append(0)
        Points.append(NewRow)
    
    Pt=TransposeMatrix(Points)
    U1t=TransposeMatrix(U1)
    U2t=TransposeMatrix(U2)
    
    Pt2=MatrixMultiply(U2t,Pt)
    Pt1=MatrixMultiply(U1t,Pt2)
    NewPoints=TransposeMatrix(Pt1)
    
    FinalPoints=[]
    for i in range(len(NewPoints)):
        NewRow=[]
        for j in range(len(NewPoints[i])):
            NewRow.append(NewPoints[i][j]+Vector[j])
        FinalPoints.append(NewRow)
    
    return FinalPoints

def VectorUnitize(Vector):
    """
    Unitize a Position vector so its total length is 1.
    
    Input Parameters:
        Vector - 3D position vector in R3. ([x,y,z])
    
    Returns:
        Unitized - Vector in same direction with a magnitude of 1.
    """
    NewVector=[]
    V_Length=math.sqrt(Vector[0]**2+Vector[1]**2+Vector[2]**2)
    for i in range(3):
        NewVector.append(Vector[i]/V_Length)
    return NewVector

def MatrixMultiply(Matrix0,Matrix1):
    """
    Preform Matrix Multiplication.
    N11= A11*B11+A12*B21+...+A1M*BN1 ect.
    
    Input Parameters:
        Matrix0 - [MxN] Matrix array of lists.
        Matrix1 - [MxN] Matris array of lists.
    
    ***Important Matrix0[M] must equal Matrix1[N]***
    
    Returns:
        NewMatrix - [MxN] Product of two input Matricies.
    """
    NewMatrix=[]
    
    M0_Cols=len(Matrix0[0])
    M0_Rows=len(Matrix0)
    M1_Cols=len(Matrix1[0])
    M1_Rows=len(Matrix1)
    
    if M0_Cols==M1_Rows:
        for i in range(M0_Rows):
            NewRow=[]
            for j in range(M1_Cols):
                Numbers=[]
                for k in range(M0_Cols):
                    Numbers.append(Matrix0[i][k]*Matrix1[k][j])
                NewRow.append(sum(Numbers))
            NewMatrix.append(NewRow)
        return NewMatrix

def RemoveZ(Matrix):
    """
    Remove the all but the first two columns of a Matrix.
    (Used for converting a Matrix to [X,Y] points after being tranformed to the XY Plane)
    
    Input Parameters:
        Matrix - [MxN] Matrix containing columns to be removed.
        
    Returns:
        NewMatrix - [2xN] Matrix containing X,Y Points.
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        for j in range(2):
            NewRow.append(Matrix[i][j])
        NewMatrix.append(NewRow)
    return NewMatrix

def VectorScale(Vector,Scale):
    NewVector=[]
    for i in range(len(Vector)):
        NewVector.append(Vector[i]*Scale)
    return NewVector

#####  Least Squares Circle  #####
def CircleA(Matrix):
    """
    
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        for j in range(len(Matrix[i])):
            NewRow.append(Matrix[i][j]*2)
        NewRow.append(-1)
        NewMatrix.append(NewRow)
    return NewMatrix

def CircleB(Matrix):
    """
    
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        NewRow.append(Matrix[i][0]**2+Matrix[i][1]**2)
        NewMatrix.append(NewRow)
    return NewMatrix

def CircleJacobian(Matrix,C_E,R_E):
    """
    Construct the  Jacobian Matrix of partial derivitives for a best fit circle approximation.
    
    Input Parameters:
        Matrix - Matrix to be approximated with a best fir circle.
        C_E - Center estimate for geometry. [X,Y]
        R_E - Radius estimate for geometry. [X,Y]
        
    Returns:
        NewMatrix - Jacobian Matrix of partial derivitives.
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        NewRow.append(-(Matrix[i][0]-C_E[0])/R_E)
        NewRow.append(-(Matrix[i][1]-C_E[1])/R_E)
        NewRow.append(-1)
        NewMatrix.append(NewRow)
    return NewMatrix

def CircleD(Matrix,C_E,R_E):
    """
    Construct a [1xN] Matrix of the distance from each [x,y] point to best fit circle.
    
    Input Parameters:
        Matrix - [2xN] Matrix of points to be compaired against best fit geometry.
        C_E - Center Estimate [X,Y] point for best fit circle.
        R_E - Radius Estimate for best fit circle.
        
    Returns:
        NewMatrix - [1xN] Matrix of distances from [X,Y] point to best fit Circle
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        Di=math.sqrt((Matrix[i][0]-C_E[0])**2+(Matrix[i][1]-C_E[1])**2)-R_E
        NewRow.append(Di)
        NewMatrix.append(NewRow)
    return NewMatrix

def Fit2DCircle(Pts2D):
    """
    Solve for a least squares circle given [X,Y] points.
    (Solve using initial least squares estimate.)
    (Initial Estimate is looped through Jacobian Matrix.)
    (Loop stops when satifactory convergence has been achieved.)
    
    Input Parameters:
        Pts2D - [2xN] Matrix of points defining points in a 2 demensional plane.
    
    Returns:
        C_E - [X,Y,Z] Center Estimate for best fit circle.
        R_E - Radius Estimate for best fit circle.
    """
    A=CircleA(Pts2D)
    B=CircleB(Pts2D)
    At=TransposeMatrix(A)
    AtA=MatrixMultiply(At,A)
    AtB=MatrixMultiply(At,B)
    S=SolveLinearEquations(AtA,AtB)
    
    C_E=S[0],S[1]
    R_E=math.sqrt(S[0]**2+S[1]**2-S[2])
    
    Last=0
    PercentChange=1
    Times=0
    
    while abs(PercentChange)>.001:
        J=CircleJacobian(Pts2D,C_E,R_E)
        D=CircleD(Pts2D,C_E,R_E)
        Jt=TransposeMatrix(J)
        JtJ=MatrixMultiply(Jt,J)
        JtD=MatrixMultiply(Jt,D)
        
        Values=[]
        for i in D:
            Values.append(abs(i[0]))
        Avg=sum(Values)/len(Values)
        
        PercentChange=(Avg-Last)/Avg
        Last=Avg
        
        S=SolveLinearEquations(JtJ,JtD)
        
        C_E=[C_E[0]-S[0],C_E[1]-S[1]]
        R_E=R_E-S[2]
        
        Times=Times+1
        
        if Times>100:
            break
    
    return C_E,R_E

def FitCircle(Matrix):
    """
    Least squares solution to best fit circle.
    
    (Initial Estiate is arrived at for best fit geometry.
    Initial Estiamate is looped through Jacobian matrix.
    Partial derivities are evaluated and the best fit geometry
    is adjusted until the algorithim converges.)
    
    Input Geometry:
        Matrix - [3XN] Matrix of points to be fit with a least squares circle.
    
    Returns:
        R_E - Radius Estimate for least squares circle.
        Normal - [a,b,c] Vector normal to plane the circle lies in.
        Point - [X,Y,Z] Center Point for least squares circle.
    """
    XY,Normal,Centroid,U1,U2=PtsTo2D(Matrix)
    C_E,R_E=Fit2DCircle(XY)
    Point=TranslateTo3D([C_E],Centroid,U1,U2)[0]
    
    return R_E,Normal,Point

def CreateCircle(Point,Normal,Radius):
    """
    Create a circle geometry within the Rhino document.
    
    Input Parameters:
        Point - [X,Y,Z] Point for center of circle.
        Normal - [a,b,c] Vector normal to the plane the circle lies on.
        Radius - Radius for circle.
    
    Return:
        Circle - Circle geometry added to the Rhino document.
    """
    Plane=rs.PlaneFromNormal(Point,Normal)
    Circle=rs.AddCircle(Plane,Radius)
    return Circle

##### Least Squares Sphere  #####
def SphereB(Matrix):
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        NewRow.append(Matrix[i][0]**2+Matrix[i][1]**2+Matrix[i][2]**2)
        NewMatrix.append(NewRow)
    return NewMatrix

def SphereA(Matrix):
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        for j in range(len(Matrix[i])):
            NewRow.append(-2*Matrix[i][j])
        NewRow.append(1)
        NewMatrix.append(NewRow)
    return NewMatrix

def SphereJacobian(Matrix,C_E):
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        Denominator=math.sqrt(((C_E[0]-Matrix[i][0])**2)+((C_E[1]-Matrix[i][1])**2)+((C_E[2]-Matrix[i][2])**2))
        for j in range(len(Matrix[i])):
            NewRow.append(-(Matrix[i][j]-C_E[j])/Denominator)
        NewRow.append(-1)
        NewMatrix.append(NewRow)
    return NewMatrix

def SphereNegD(Matrix,C_E,R_E):
    NewMatrix=[]
    for i in range(len(Matrix)):
        Ri=math.sqrt(((C_E[0]-Matrix[i][0])**2)+((C_E[1]-Matrix[i][1])**2)+((C_E[2]-Matrix[i][2])**2))
        D=Ri-R_E
        NewMatrix.append([-D])
    return NewMatrix

def FitSphere(Points,Convergence=.0001):
    ###Compute Least Squares Matricies###
    Matrix=PtListToMatrix(Points)
    
    B=SphereB(Matrix)
    A=SphereA(Matrix)
    At=TransposeMatrix(A)
    AtA=MatrixMultiply(At,A)
    AtB=MatrixMultiply(At,B)
    
    S=SolveLinearEquations(AtA,AtB)
    
    ###Calculate Radius and Center Estimates###
    R_E=Radius=math.sqrt(abs((S[0]**2+S[1]**2+S[2]**2)-S[3]))
    C_E=[-S[0],-S[1],-S[2]]
    Last=0
    PercentChange=1
    Times=0
    
    while abs(PercentChange)>Convergence:
        J=SphereJacobian(Matrix,C_E)
        NegD=SphereNegD(Matrix,C_E,R_E)
        
        Jt=TransposeMatrix(J)
        JtJ=MatrixMultiply(Jt,J)
        JtD=MatrixMultiply(Jt,NegD)
        
        S=SolveLinearEquations(JtJ,JtD)
        
        R_E=R_E+S[3]
        C_E=[C_E[0]+S[0],C_E[1]+S[1],C_E[2]+S[2]]
        
        Values=[]
        for i in NegD:
            Values.append(abs(i[0]))
        Avg=sum(Values)/len(Values)
        
        PercentChange=(Last-Avg)/Avg
        Last=Avg
        
        Times=Times+1
        if Times>99:
            break
    
    print "Center: "+str(C_E)
    print "Radius: "+str(R_E)
    print str(Times)+" Times Through Jacobian Matrix"
    
    return C_E,R_E

def CreateSphere(Center,Radius):
    """
    Create a sphere in the Rhino document.
    
    Input Parameters:
        Center - [X,Y,Z] point for sphere center.
        Radius - Distance for geometry from center.
    
    Returns:
        Sphere - Geometry object added to the document.
    """
    Sphere=rs.AddSphere(Center,Radius)
    return Sphere

#####  Lease Squares Cylinder  #####
def CylinderVectorEstimate(Points):
    """
    Solve for an axis estimate for cylinder fitting.
    Solve for a unitized best fit vector for a set of points.
    
    Input Parameters:
        Points - List of Points. (Must be a list of guids (Probably))
    
    Returns:
        V - Unitized Vector for the best fit line to the set of Points.
    """
    Line=rs.LineFitFromPoints(Points)
    Vector=rs.VectorCreate(Line.From,Line.To)
    Vector=rs.VectorUnitize(Vector)
    V=[]
    V.append(Vector[0])
    V.append(Vector[1])
    V.append(Vector[2])
    return V

def RotatePoints(Matrix,Vector):
    """
    Rotate a [3xN] Matrix of Points from any arbitrary vector to align on the Z-Axis.
    In order to Rotate the Matrix to align with the Z-Axis a rotatation matricies 
    about the x and y axies are applied one after the other.
    
    Input Parameters:
        Matrix - [3xN] Matrix of points align to Z-Axis.
        Vector - Reference direction basis for transformation matrix.
        
    Returns:
        FinalPoints - [3xN] Matrix of Points rotated to align with Z-Axis.
        RotX - [3x3] Rotation Matrix describing rotation about X-Axis to lie on YZ Plane.
        RotY - [3x3] Rotation Matrix describing rotation about Y-Axis to lie on ZY Plane.
    """
    
    RotX=RotateAboutX(Vector)
    RotY=RotateAboutY(Vector)
    
    Pt=TransposeMatrix(Matrix)
    
    PtRx=MatrixMultiply(RotX,Pt)
    PtRy=MatrixMultiply(RotY,PtRx)
    FinalPoints=TransposeMatrix(PtRy)
    
    Vt=TransposeMatrix([Vector])
    Vtx=MatrixMultiply(RotX,Vt)
    Vty=MatrixMultiply(RotY,Vtx)
    NewVector=TransposeMatrix(Vty)
    
    return FinalPoints,RotX,RotY

def CylinderRadius(Matrix,V_E,P_E):
    """
    Calculate distances from Axis to matrix of Points.
    
    Input Parameters:
        Matrix - [3xN] Matrix of points to measure radius from.
        V_E - [a,b,c] Vector estimate axis for best fit cylinder.
        P_E - [X,Y,Z] Point estimate for base of best fit cylinder.
    
    Returns:
        NewMatrix - [1xN] Matrix of radius from points to axis.
    """
    NewMatrix=[]
    
    a=V_E[0]
    b=V_E[1]
    c=V_E[2]
    
    for i in range(len(Matrix)):
        NewRow=[]
        U=(c*(Matrix[i][1]-P_E[1])-b*(Matrix[i][2]-P_E[2]))
        V=(a*(Matrix[i][2]-P_E[2])-c*(Matrix[i][0]-P_E[0]))
        W=(b*(Matrix[i][0]-P_E[0])-a*(Matrix[i][1]-P_E[1]))
        
        top=math.sqrt(U**2+V**2+W**2)
        bottom=math.sqrt(a**2+b**2+c**2)
        R=top/bottom
        NewRow.append(R)
        NewMatrix.append(NewRow)
    return NewMatrix

def CylinderNegD(R,R_E):
    """
    Solve for the distance from best fit geometry to each point on the sample Matrix.
    
    Input Parameters:
        R - [1xN] Matrix of actual radiuses from each point to the cylinder axis.
        R_E - Estimate radius for cylinder.
    
    Returns:
        NewMatrix - [1xN] Matrix of negitive distances from point to estimate cylinder.
    """
    NewMatrix=[]
    for i in range(len(R)):
        NewRow=[]
        D=R[i][0]-R_E
        NegD=-D
        NewRow.append(NegD)
        NewMatrix.append(NewRow)
    return NewMatrix

def CylinderJacobian(Matrix,R):
    """
    Construct a Jacobian Matrix of partial derivities for a cylinder
    whose axis is aligned to Z-Axis.
    
    Input Parameters:
        Matrix - [3xN] Matrix of [X,Y,Z] points to be fitted with a least squares goemetry.
        R - [1xN] Matrix of radius distance from Z-Axis to Point.
    
    Returns:
        NewMatrix - [5xN] Matris of partial derivities for least squares approximation.
    """
    NewMatrix=[]
    for i in range(len(Matrix)):
        NewRow=[]
        NewRow.append(-Matrix[i][0]/R[i][0])
        NewRow.append(-Matrix[i][1]/R[i][0])
        NewRow.append(-Matrix[i][0]*Matrix[i][2]/R[i][0])
        NewRow.append(-Matrix[i][1]*Matrix[i][2]/R[i][0])
        NewRow.append(-1)
        NewMatrix.append(NewRow)
    return NewMatrix

def UpdatePoint(S,U1t,U2t,P_E):
    """
    Update estimate for cylinder base point using solution least squares jacobian matrix.
    
    Input Parameters:
        S - [1x5] Solution set from Jabian matrix least square approximation.
        U1t - [3x3] Transpose of rotation matrix about X-Axis.
        U2t - [3x3] Transpose of rotation matrix about Y-Axis.
        P_E - [X,Y,Z] Point estimate for cylinder base.
        
    Returns:
        Point - Updated estimate for cylinder base point.
    """
    P=[[S[0]],[S[1]],[-S[0]*S[2]-S[0]*S[3]]]
    
    Update=MatrixMultiply(U2t,P)
    
    Update=MatrixMultiply(U1t,Update)
    
    Point=[P_E[0]+Update[0][0],P_E[1]+Update[1][0],P_E[2]+Update[2][0]]
    return Point

def UpdateVector(S,U1t,U2t):
    """
    Update vector estimate based on solution of Jacobian matrix.
    Transform Vector to its origional position by multiplying the transpose of rotation matricies.
    
    Input Parameters:
        S - [1x5] Solution set to jacobian set of partial derivites.
        U1t - [3x3] Transpose of rotation matrix about X-Axis.
        U2t - [3x3] Transpose of rotation matrix about Y-Axis.
        V_E - Vector Estimate (Not Acutally needed.)
    """
    P=VectorUnitize([S[2],S[3],1])
    P=TransposeMatrix([P])
    Update=MatrixMultiply(U2t,P)
    Update=MatrixMultiply(U1t,Update)
    Vector=[Update[0][0],Update[1][0],Update[2][0]]
    Vector=VectorUnitize(Vector)
    return Vector

def FitCylinder(Matrix):
    """
    Preform a best fit algorithm for a least squares cylinder.
    
    Input Parameters:
        (First initial estimates are arrived at for Point, Radius and Axis)
        (Jacobian Matrix is looped through to evaluate partial derivites)
        (Partial derivites move the best fit approximation by small incriments)
        (Solution is finally arrived at when the data has sufficiently converged.)
    
    Returns:
        R_E - Final best fit estimate Radius.
        P_E - Final best fit [X,Y,Z] Point estimate.
        V_E - Final best fit [a,b,c] vector estimate.
        Times - Number of times Jacobian loop was iterated before solution converged.
    """
    V_E=CylinderVectorEstimate(Points)
    Pts=ProjectToPlane(Matrix,V_E)
    R_E,V_E,P_E=FitCircle(Pts)
    
    Last=0
    PercentChange=1
    Times=0
    
    while abs(PercentChange)>.001:
        M_P=DataTranslate(Matrix,P_E)
        
        M_P,U1,U2=RotatePoints(M_P,V_E)
        
        R=CylinderRadius(Matrix,V_E,P_E)
        
        NegD=CylinderNegD(R,R_E)
        AbsD=AbsMatrix(NegD)
        
        J=CylinderJacobian(M_P,R)
        Jt=TransposeMatrix(J)
        JtJ=MatrixMultiply(Jt,J)
        JtD=MatrixMultiply(Jt,NegD)
        
        S=SolveLinearEquations(JtJ,JtD)
        
        U1t=TransposeMatrix(U1)
        U2t=TransposeMatrix(U2)
        
        P_E=UpdatePoint(S,U1t,U2t,P_E)
        V_E=UpdateVector(S,U1t,U2t)
        R_E=S[4]+R_E
        
        Avg=ColumnAverage(AbsD)[0]
        PercentChange=(Last-Avg)/Avg
        Last=Avg
        
        Times=Times+1
        if Times>100:
            break
        
    print "Radius Estimate: "+str(R_E)
    print "Point Estimate: "+str(P_E)
    print "Axis Estimate: "+str(V_E)
    print str(Times)+" Times Through Jacobian Matrix"
    
    return R_E,P_E,V_E,Times

def CreateCylinder(R_E,P_E,V_E,Points):
    """
    Create Cylinder Geometery from Radius, Point and Vector trim within Points limits.
    
    Input Parameters:
        R_E - Radius [r] Estimate for Cylinder.
        P_E - Point [X,Y,Z] Estimate for Cylinder.
        V_E - Vector [a,b,c] Estimate for Cylinder.
        Points - Describe the extents of the Cylinder.
    
    Returns:
        Cylinder - Created Cylinder Geometry in the Rhino Doc.
    """
    
    Plane=rs.PlaneFromNormal(P_E,V_E)
    BB=rs.BoundingBox(Points,Plane)
    Sides=[]
    Sides.append(rs.AddSrfPt([BB[0],BB[1],BB[2],BB[3]]))
    Sides.append(rs.AddSrfPt([BB[0],BB[1],BB[4],BB[5]]))
    Sides.append(rs.AddSrfPt([BB[1],BB[2],BB[6],BB[5]]))
    Sides.append(rs.AddSrfPt([BB[3],BB[2],BB[6],BB[7]]))
    Sides.append(rs.AddSrfPt([BB[0],BB[3],BB[7],BB[4]]))
    Sides.append(rs.AddSrfPt([BB[4],BB[5],BB[6],BB[7]]))
    
    Planes=[]
    for side in Sides:
        Centroid=rs.SurfaceAreaCentroid(side)[0]
        Param=rs.SurfaceClosestPoint(side,Centroid)
        Normal=rs.SurfaceNormal(side,Param)
        if rs.IsVectorParallelTo(Normal,V_E)!=0:
            Planes.append(rs.PlaneFromNormal(Centroid,Normal))
        rs.DeleteObject(side)
    Line=(P_E,[P_E[0]+V_E[0],P_E[1]+V_E[1],P_E[2]+V_E[2]])
    
    Intersects=[]
    for Plane in Planes:
        Intersects.append(rs.LinePlaneIntersection(Line,Plane))
    
    Base=rs.PlaneFromNormal(Intersects[0],V_E)
    Height=rs.Distance(Intersects[0],Intersects[1])
    Cylinder=rs.AddCylinder(Base,Height,R_E,False)
    return Cylinder

def RemovePoints(Matrix,R_E,P_E,V_E,OnePercent):
    R=CylinderRadius(Matrix,V_E,P_E)
    D=CylinderNegD(R,R_E)
    D=AbsMatrix(D)
    Removed=[]
    for i in range(int(OnePercent)):
        Max=max(D)
        Index=D.index(Max)
        Removed.append(Matrix[Index])
        Matrix.remove(Matrix[Index])
        D.remove(D[Index])
    return Matrix,Removed

def FitPlane(Points,Remove=20,Repeat=5):
    start=time.time()
    ## Threaded Definition ##
    def Threaded_Distance(Point):
        Distances.append(abs(Plane.DistanceTo(Point)))
    
    ## Single Core Calculation ##
    Count=len(Points)
    Remove_Count=int(round(Count*Remove/100/5))
    
    for i in range(Repeat):
        Plane=rs.PlaneFitFromPoints(Points)
        Plane=rs.coerceplane(Plane)
        
        Distances=[]
        ghpythonlib.parallel.run(Threaded_Distance,Points)
        for j in range(Remove_Count):
            Index=Distances.index(max(Distances))
            Distances.pop(Index)
            Points.pop(Index)
    
    Plane=rs.PlaneFitFromPoints(Points)
    Plane=rs.coerceplane(Plane)
    
    end=time.time()
    print end-start
    return Plane

def CreatePlane(Points,Plane):
    BB=rs.BoundingBox(Points)
    BB=rs.coerceboundingbox(BB)
    brep=BB.ToBrep()
    tol=scriptcontext.doc.ModelAbsoluteTolerance
    r,Curves,points=Rhino.Geometry.Intersect.Intersection.BrepPlane(brep,Plane,tol)
    if r==True:
        PlanarSrf=rs.AddPlanarSrf(Curves)

if __name__=="__main__":
    Mesh=rs.GetObject("Select Mesh",32)
    Shape="Cylinder"
    
    if not Shape:
        Shapes=["Circle","Sphere","Cylinder"]
        msg="Select Point Function for Point Analysis"
        Shape=rs.ComboListBox(Shapes,msg,"Select Function")
    
    if Shape:
        Points=rs.MeshVertices(Mesh)
        if Shape=="Cylinder":
            r=FitCylinder(Points)
            if r:
                R_E,P_E,V_E,Times=r
                Geo=CreateCylinder(R_E,P_E,V_E,Points)
        
        if Shape=="Circle":
            R_E,Normal,Point=FitCircle(Points)
            Geo=CreateCircle(Point,Normal,R_E)
        
        if Shape=="Sphere":
            C_E,R_E=FitSphere(Points)
            Geo=CreateSphere(C_E,R_E)
        
        if Shape=="Plane":
            Plane=FitPlane(Points)
            Geo=CreatePlane(Points,Plane)