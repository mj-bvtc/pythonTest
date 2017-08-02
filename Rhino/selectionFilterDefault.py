import rhinoscriptsyntax as rs


rs.Command("""-_SelectionFilter 
                ShowDialog=Yes  
                Curves=Yes  
                Surfaces=Yes  
                Polysurfaces=Yes  
                Meshes=Yes  
                Annotations=Yes  
                Lights=Yes  
                Blocks=Yes  
                Points=Yes  
                ControlPoints=Yes  
                PointClouds=Yes  
                Hatches=Yes  
                Others=Yes  
                DisableFilter=No _enter""")


op
opop