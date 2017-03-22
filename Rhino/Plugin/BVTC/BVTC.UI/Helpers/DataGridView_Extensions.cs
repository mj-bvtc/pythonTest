using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data;

namespace BVTC.UI.Helpers
{
    public static class DataGridView_Extensions
    {
        public static void ColumnVisible(this DataGridView gridView, int columnIndex, bool visible)
        {
            gridView.Columns[columnIndex].Visible = visible;
        }
        public static void ColumnVisible(this DataGridView gridView, string columnName, bool visible)
        {
            for (int i = 0; i < gridView.Columns.Count; i++)
            {
                if (gridView.Columns[i].Name == columnName)
                {
                    gridView.ColumnVisible(i, visible);
                }
            }
        }

        public static DataTable Get_CheckedRows(this DataGridView gridview)
        {
            DataTable dt = new DataTable();
            if (gridview.RowCount == 0) { return dt; }


            int index = -1;
            // find the checkBox column //
            foreach (DataGridViewColumn column in gridview.Columns)
            {
                if (column.GetType() == typeof(DataGridViewCheckBoxColumn))
                {
                    index = column.Index;
                }
                else
                {
                    // add columns to DataGrid //
                    Type type = gridview.Rows[0].Cells[column.Name].Value.GetType();
                    DataColumn col = dt.Columns.Add(column.Name, type);
                }
            }

            // return if no checkbox column was found //
            if (index < 0) { return dt; }

            // add a row for each checked box //
            foreach (DataGridViewRow row in gridview.Rows)
            {
                DataGridViewCheckBoxCell cell = (DataGridViewCheckBoxCell)row.Cells[index];
                DataRow dtRow = dt.NewRow();
                if (cell.Value != null && (bool)cell.Value == true)
                {
                    int rowCount = 0;
                    for (int i = 0; i < gridview.ColumnCount; i++)
                    {
                        if (i != index)
                        {
                            dtRow[rowCount] = row.Cells[i].Value;
                            rowCount++;
                        }
                    }
                    dt.Rows.Add(dtRow);
                }
            }

            return dt;
        }

        public static void ResizeGridView(this DataGridView gridView, int maxHeight = 700)
        
        {
            // calculate prefered width of columns //
            int width = 0;
            foreach (DataGridViewColumn col in gridView.Columns)
            {
                if (col.Visible)
                {
                    width += col.GetPreferredWidth(DataGridViewAutoSizeColumnMode.AllCells, true);
                }
            }
            // account for size of selection column //
            width += 45;

            // set width after calculation //
            gridView.Width = width;

            // set values for row height //
            int height = 0;
            int rowCount = 0;
            // account for space used by heading //
            if (gridView.ColumnHeadersVisible == true)
            {
                height += gridView.ColumnHeadersHeight;
            }

            // add height for each row being shown //
            foreach (DataGridViewRow row in gridView.Rows)
            {
                height += row.GetPreferredHeight(rowCount, DataGridViewAutoSizeRowMode.AllCells, true);
                rowCount++;
            }

            if (height < maxHeight)
            {
                // set total height of gridview //
                gridView.Height = height;
            }
            else
            {
                // add scroll bar //
                gridView.ScrollBars = ScrollBars.Vertical;
                gridView.Width = width + 15;
                gridView.Height = maxHeight;
            }
            

            // make sure first column and row shown //
            if (gridView.ColumnCount > 0)
            {
                for (int i = 0; i < gridView.ColumnCount; i++)
                {
                    if (gridView.Columns[i].Visible)
                    {
                        gridView.FirstDisplayedScrollingColumnIndex = i;
                        break;
                    }
                }
            }
            if (gridView.RowCount > 0)
            {
                gridView.FirstDisplayedScrollingRowIndex = 0;
            }
            
        }

        public static void ReadOnlyColumns(this DataGridView gridView, List<string> readOnlyColumns)
        {
            foreach (DataGridViewColumn dc in gridView.Columns)
            {
                if (readOnlyColumns.Contains(dc.Name))
                {
                    dc.ReadOnly = true;
                }
            }
        }

        public static void AddComboBoxColumn(this DataGridView gridView, int index = 0, string name = "", string headerText = "")
        {
            DataGridViewCheckBoxColumn chk = new DataGridViewCheckBoxColumn();
            gridView.Columns.Add(chk);
            chk.Name = name;
            chk.HeaderText = headerText;
            chk.DisplayIndex = index;
        }
    }
}
