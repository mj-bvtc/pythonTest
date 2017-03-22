using System;
using Rhino;
using Rhino.Commands;
using System.Collections.Generic;

namespace BVTC.RhinoPlugin.Commands
{
    [System.Runtime.InteropServices.Guid("87813ffd-3dd2-4d71-8f48-d6511d638874")]
    public class UpdateWeight : Command
    {
        static UpdateWeight _instance;
        public UpdateWeight()
        {
            _instance = this;
        }

        ///<summary>The only instance of the UpdateWeight command.</summary>
        public static UpdateWeight Instance
        {
            get { return _instance; }
        }

        public override string EnglishName
        {
            get { return "UpdateWeight"; }
        }

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // get document guid //
            Guid guid = RhinoTools.Document.GetGuid(doc, false);

            // get objects to calculate weight for //
            List<Guid> ids = Interface.GetObjects(doc,"Select Object(s) to measure for weight");
            if (ids == null || ids.Count == 0)
            {
                RhinoApp.Wait();
                return Rhino.Commands.Result.Cancel;
            }

            double firedWeight = RhinoTools.Geometry.MeasureWeight(doc, ids);
            double batchWeight = firedWeight * 1.14;

            // get shipped weight //
            List<string> cutouts = new List<string>() { "Model::Cutout" };
            double shipWeight = RhinoTools.Geometry.MeasureWeight(doc, ids,cutouts);

            // build weight recording UI //
            UI.Weight ui = new UI.Weight(batchWeight, firedWeight, shipWeight);
            Rhino.UI.Dialogs.ShowSemiModal(ui);
            if ((ui.DialogResult == System.Windows.Forms.DialogResult.OK) && 
                (ui.preKilnWeight > 0 || ui.postKilnWeight > 0 || ui.shippedWeight >0))
            {
                new Repositories.CTrac().Insert_Weight(
                    batchWeight, firedWeight, shipWeight, 
                    ui.preKilnWeight, ui.postKilnWeight, ui.shippedWeight, 
                    doc.Path);
                RhinoApp.WriteLine("Weight successfully added to C-Trac");
            }
            else { RhinoApp.WriteLine("UI Aborted"); }            

            return Result.Success;
        }
    }
}
