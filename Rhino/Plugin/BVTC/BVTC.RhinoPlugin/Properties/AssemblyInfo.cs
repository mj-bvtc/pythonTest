using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using Rhino.PlugIns;


// Plug-in Description Attributes - all of these are optional
// These will show in Rhino's option dialog, in the tab Plug-ins
[assembly: PlugInDescription(DescriptionType.Address, "6860 South Abbott Road, Orchard Park, NY, 14127")]
[assembly: PlugInDescription(DescriptionType.Country, " United States")]
[assembly: PlugInDescription(DescriptionType.Email, "peters@bostonvalley.com")]
[assembly: PlugInDescription(DescriptionType.Phone, "(716) 649-7490")]
[assembly: PlugInDescription(DescriptionType.Fax, "-")]
[assembly: PlugInDescription(DescriptionType.Organization, "Boston Valley Terra Cotta")]
[assembly: PlugInDescription(DescriptionType.UpdateUrl, "-")]
[assembly: PlugInDescription(DescriptionType.WebSite, "http://bostonvalley.com/services/innovative-archlab/")]


// General Information about an assembly is controlled through the following 
// set of attributes. Change these attribute values to modify the information
// associated with an assembly.
[assembly: AssemblyTitle("BVTC.RhinoPlugin.Commands")] // Plug-In title is extracted from this
[assembly: AssemblyDescription("Beta Test Release")]
[assembly: AssemblyConfiguration("Git Hosted Solution")]
[assembly: AssemblyCompany("Boston Valley Terra Cotta")]
[assembly: AssemblyProduct("BVTC.RhinoPlugin")]
[assembly: AssemblyCopyright("Copyright ©  2016")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]

// Setting ComVisible to false makes the types in this assembly not visible 
// to COM components.  If you need to access a type in this assembly from 
// COM, set the ComVisible attribute to true on that type.
[assembly: ComVisible(false)]

// The following GUID is for the ID of the typelib if this project is exposed to COM
[assembly: Guid("b763cf8c-cb0a-41c5-859f-25c36421adae")] // This will also be the Guid of the Rhino plug-in

// Version information for an assembly consists of the following four values:
//
//      1 - Major Version
//      0 - Minor Version 
//      1 - Build Number
//      9 - Revision
//
// You can specify all the values or you can default the Build and Revision Numbers 
// by using the '*' as shown below:
// [assembly: AssemblyVersion("1.0.1.9)]
[assembly: AssemblyVersion("1.0.1.9")]
[assembly: AssemblyFileVersion("1.0.1.9")]
