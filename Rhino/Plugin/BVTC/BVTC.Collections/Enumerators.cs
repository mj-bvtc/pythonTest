using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BVTC.Collections
{
    // ways to add submittal data to C-Trac //
    public enum SubmittalType { New, Merge, Overwrite };
    // the department the submittal is destined for //
    public enum SubmittalTarget { Client, Moldshop, Pressing, Finishing, Glazing, Sizing, Shipping, PROD_ALL };
    // page orientation for printing //
    public enum PageLayout { Portrait, Landscape};
    // name of the column that pdf data is added to //
    public enum PdfColumn { ClientPDF, ShopPDF};
}
