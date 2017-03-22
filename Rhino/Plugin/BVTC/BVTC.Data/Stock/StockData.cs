using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Data.Stock
{
    public class StockData : data
    {
        public string ProjectNumber { get; set; }
        public string ProjectName { get; set; }
        public string Part { get; set; }
        public string UseMold { get; set; }
        public string Method { get; set; }
        public string GUID { get; set; }
        public string ModelPath { get; set; }
        public bool IsSculpture { get; set; }
        public bool IsCncSculpture { get; set; } //not implemented in CTrac yet
        public bool Delivery { get; set; }
        public int StockCut { get; set; }
        public int WireCutTraditional { get; set; } //input as integer 0 or 1, returns true or false in CTrac
        public float Shrinkage { get; set; }
        public int Quantity { get; set; }
        public int StockLength { get; set; }
        public int StockWidth { get; set; }
        public int StockHeight { get; set; }
        public int EMT { get; set; }
        public int PartRun { get; set; }
        public string StockDate { get; set; }
        public string PgmDate { get; set; }
        public string VerifyDate { get; set; }
        public string PartStartDate { get; set; }
        public int PartStartTime { get; set; }
        public int PartEndTime { get; set; }
        public string PartEndDate { get; set; }
        public string PartCompleteDate { get; set; }
        public string Drawings { get; set; } //comma separated string of drawings
        public string NotUsed { get; set; }//empty field in CTrac
        public string Stock { get; set; }
        public string Stand { get; set; }
        public string PartPDF { get; set; } //new field for ?????





    }
}
