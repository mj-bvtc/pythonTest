import rhinoscriptsyntax as rs


rs.Command("""-_SelectionFilter 
                ShowDialog=Yes  
                Curves=No  
                Surfaces=No   
                Polysurfaces=No   
                Meshes=No   
                Annotations=No   
                Lights=No   
                Blocks=No   
                Points=No   
                ControlPoints=No   
                PointClouds=No   
                Hatches=No   
                Others=No   
                DisableFilter=No _enter """)
