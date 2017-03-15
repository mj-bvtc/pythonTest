!-_RunScript (
Call WriteIt

Function WriteIt()
	Dim strFileName, TXT, strFilter, objStream, Arrobjs

	strFilter = "Txt File (*.txt)|*.txt|All Files (*.*)|*.*||"
	strFileName = Rhino.SaveFileName("Save File As", strFilter)
	Set TXT = CreateObject("Scripting.FileSystemObject")
	Set objStream = TXT.CreateTextFile(strFileName, True)
	
	objStream.WriteLine("M90")
	objStream.WriteLine("G74")
'	objStream.WriteLine("M58") '9000 Command to change from Router to Wire Tool
	objStream.WriteLine("G91") 'Relative
	'	objStream.WriteLine("G90") 'Absolute
	objStream.WriteLine("M11")

	'	Rhino.Command "_Join"
	Arrobjs = Rhino.getObjects("Select Curves", 4) 
	Rhino.Command "_Dir"
	
	Call rhino.UnselectAllObjects
	Call rhino.Redraw
	Call objs2CODE(Arrobjs, objStream)

	objStream.WriteLine("M21")
	objStream.WriteLine("M02")
	objStream.Close
End Function
'---------------------------------------------------------------------------------------------------------------------------------------
' function that takes a set of objects and calls its CODE conversion function according to the object type
'---------------------------------------------------------------------------------------------------------------------------------------
Function objs2CODE(arrobjs, ByRef objStream)
	Dim strObj, strTemp

	For Each strObj In arrObjs
		If Rhino.IsPolyline(strObj) Then
			Polyline2CODE strObj, objStream
			objs2CODE = 1
		ElseIf Rhino.IsArc(strObj) Then
			Arc2CODE strObj, objStream
			objs2CODE = 1
		ElseIf Rhino.IsLine(strObj)Then
			Line2CODE strObj, objStream
			objs2CODE = 1
		ElseIf Rhino.IsPolyCurve(strObj) Then
			Polycurve2CODE strObj, objStream, 1
			objs2CODE = 1
		Else
			strTemp = Rhino.ConvertCurveToPolyline(strobj)
			Call PolyLine2CODE(strTemp, objStream)
			Call rhino.deleteObject(strTemp)
			objs2CODE = 1
		End If
	Next
End Function
'---------------------------------------------------------------------------------------------------------------------------------------
' function that converts polylines to G-CODE and writes the commands to the filestream
'---------------------------------------------------------------------------------------------------------------------------------------
Function Polyline2CODE(strObj, ByRef objStream)
	Dim arrPts, Bound, i

	arrPts = rhino.PolylineVertices(strObj)
	Bound = UBound(arrPts)
	For i = 1 To bound	
		'	objStream.WriteLine("G01 X" & unit(arrPts(i)(0)) & " Y" & unit(arrPts(i)(1))) 'Absolute Coordinates
		objStream.WriteLine("G01 X" & unit((arrPts(i)(0)) - (arrPts(i - 1)(0))) & " Y" & unit((arrPts(i)(1)) - (arrPts(i - 1)(1)))) 'Relative Coordinates
	Next
End Function

'---------------------------------------------------------------------------------------------------------------------------------------
' function that converts lines to G-CODE and writes the commands to the filestream
'---------------------------------------------------------------------------------------------------------------------------------------
Function Line2CODE(strObj, ByRef objStream)
	Dim StartPt, EndPt

	StartPt = Rhino.CurveStartPoint(strObj)
	EndPt = Rhino.CurveEndPoint(strObj)
	objStream.WriteLine("G01 X" & unit((EndPt(0) - (StartPt(0)))) & " Y" & unit((EndPt(1)) - (StartPt(1)))) 'Relative Testing
	'	objStream.WriteLine("G01 X" & unit(EndPt(0)) & " Y" & unit(EndPt(1))) 'Absolute
End Function
'---------------------------------------------------------------------------------------------------------------------------------------
' function that converts arcs to G-CODE and writes the commands to the filestream
'---------------------------------------------------------------------------------------------------------------------------------------
Function Arc2CODE(strObj, ByRef objStream)
	Dim StartPt, EndPt, Center, R, Alpha, zNorm
	
	StartPt = Rhino.CurveStartPoint(strObj)
	EndPt = Rhino.CurveEndPoint(strObj)
	Center = Rhino.ArcCenterPoint(strObj)
	R = Rhino.ArcRadius(strObj)
	Alpha = Rhino.Angle2(array(Center, StartPt), array(Center, EndPt))(0)
	zNorm = Rhino.CurveNormal(strObj)(2)

	If zNorm > 0 Then
		objStream.WriteLine("G03 X" & Round((EndPt(0) - StartPt(0)), 3) & " Y" & Round((EndPt(1) - StartPt(1)), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Relative Working
		'	objStream.WriteLine("G03 X" & Round((EndPt(0) - StartPt(0)), 3) & " Y" & Round((EndPt(1) - StartPt(1)), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Absolute 
	Else
		'	objStream.WriteLine("G02 X" & Round((EndPt(0) - StartPt(0)), 3) & " Y" & Round((EndPt(1) - StartPt(1)), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Absolute		
		objStream.WriteLine("G02 X" & Round((EndPt(0) - StartPt(0)), 3) & " Y" & Round((EndPt(1) - StartPt(1)), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Relative Working
	End If
End Function

'---------------------------------------------------------------------------------------------------------------------------------------
' function that converts polycurves to G-CODE and writes the commands to the filestream
'---------------------------------------------------------------------------------------------------------------------------------------
Function Polycurve2CODE(strObj, ByRef objStream, up)
	Dim StartPt, Count, Index, Obj, objs, strTemp

	StartPt = Rhino.CurveStartPoint(strObj)
	Count = Rhino.PolyCurveCount(strObj)
	If up = 1 Then
		objStream.WriteLine("G01 X" & unit((StartPt(0)) - (StartPt(0))) & " Y" & unit((StartPt(1)) - (StartPt(1)))) 'Relative Testing
		'objStream.WriteLine("G01 X" & unit(StartPt(0)) & " Y" & unit(StartPt(1)))  'Absolute Working
	Else
		objStream.WriteLine("G01 X" & unit((StartPt(0)) - (StartPt(0))) & " Y" & unit((StartPt(1)) - (StartPt(1)))) 'Relative Testing
		'objStream.WriteLine("G01 X" & unit(StartPt(0)) & " Y" & unit(StartPt(1))) 'Absolute Working
	End If

	Objs = Rhino.ExplodeCurves(strObj)

	For Each obj In objs
		If Rhino.isLine(Obj) Then
			Dim EndPt, StartPt3
			EndPt = Rhino.CurveEndPoint(obj)
			StartPt3 = Rhino.CurveStartPoint(obj)
			objStream.WriteLine("G01 X" & unit((EndPt(0) - (StartPt3(0)))) & " Y" & unit((EndPt(1)) - (StartPt3(1)))) 'Relative Testing
			'			objStream.WriteLine("G01 X" & unit(EndPt(0)) & " Y" & unit(EndPt(1))) 'Absolute Working
		
		ElseIf Rhino.IsArc(Obj) Then
			Dim EndPt2, Center, R, zNorm, Alpha
			StartPt = Rhino.CurveStartPoint(obj)
			EndPt2 = Rhino.CurveEndPoint(obj)
			Center = Rhino.ArcCenterPoint(obj)
			Alpha = Rhino.Angle2(array(Center, StartPt), array(Center, EndPt2))(0)
			zNorm = Rhino.CurveNormal(obj)(2)
			If zNorm > 0 Then
				objStream.WriteLine("G03 X" & Round((EndPt2(0) - StartPt(0)), 3) & " Y" & Round((EndPt2(1) - StartPt(1)), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Relative
				'				objStream.WriteLine("G03 X" & Round((StartPt(0) + (EndPt2(0) - StartPt(0))), 3) & " Y" & Round((StartPt(1) + (EndPt2(1) - StartPt(1))), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Absolute 
			Else
				objStream.WriteLine("G02 X" & Round((EndPt2(0) - StartPt(0)), 3) & " Y" & Round((EndPt2(1) - StartPt(1)), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3)) 'Relative
				'				objStream.WriteLine("G02 X" & Round((StartPt(0) + (EndPt2(0) - StartPt(0))), 3) & " Y" & Round((StartPt(1) + (EndPt2(1) - StartPt(1))), 3) & " I" & Round((Center(0) - StartPt(0)), 3) & " J" & Round((Center(1) - StartPt(1)), 3))  'Absolute
			End If
		ElseIf Rhino.isPolyline(obj) Then
			Dim arrPts, Point, Bound, l
			arrPts = Rhino.PolylineVertices(obj)
			Bound = Ubound(arrPts)
			For l = 1 To Bound
				objStream.WriteLine("G01 X" & unit(arrPts(l)(0)) & " Y" & Unit(arrPts(l)(1)))
			Next
		ElseIf Rhino.isPolyCurve(obj) Then
			Polycurve2CODE strObj, objStream, 0
		Else
			strTemp = Rhino.ConvertCurveToPolyline(obj)
			Dim arrPts1, Boun, j

			arrPts1 = rhino.PolylineVertices(strTemp)
			Boun = UBound(arrPts1)

			Call rhino.deleteobject(strTemp)
		End If
	Next
	Rhino.deleteobjects(objs)

End Function
'---------------------------------------------------------------------------------------------------------------------------------------
' converts the rhino coordinates into correct decimals 
'---------------------------------------------------------------------------------------------------------------------------------------
Function Unit(value)
	unit = Round((Value * 1), 4)
End Function

)