using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Data;

namespace BVTC.Repositories
{
    public abstract class database
    {
        // abstract base class for BVTC.Repositories //
        public bool setup { get; set; }

        public database() { setup = false; }
        public database(string server, string db)
        {
            // overloaded initialize with db info //
            this.setup = false;
            this.serverName = server;
            this.databaseName = db;
        }

        // database info //
        public string serverName { get; set; }
        public string serverIP { get; set; }
        public string databaseName { get; set; }
        public string user { get; set; }
        public string password { get; set; }

        // active command objects //
        public string connString { get; set; }
        public string command { get; set; }


        public static string BuildConnectionString(string serverName, string serverIP, string databaseName, string password, string user)
        {
            // build connection string with class properties //
            string connString = "";

            // set the server target //
            if (serverName != null)
            { connString += "Server Name=" + serverName + ";"; }
            else if(serverIP != null)
            { connString += "Server Name=" + serverIP + ";"; }
            else
            {
                connString = null;
                throw new Exceptions.OpenDB("Please specify a server to connect to.");
            }

            // set the data base name //
            if (databaseName != null)
            { connString += string.Format("Database Name ={0};", databaseName); }
            else
            {
                connString = null;
                throw new Exceptions.OpenDB("Please specify a database to connect to.");
            }

            // set username and password //
            if(password != null && user != null)
            {
                connString += string.Format("User ID={0};Password={1};", user, password);
            }

            // return results if any //
            return connString;
        }
        public string BuildConnectionString()
        {
            this.connString = BuildConnectionString(this.serverName, this.serverIP, this.databaseName, this.password, this.user);
            return this.connString;
        }


        // methods to override  when derived //
        // data setup and close functions //
        public abstract void OpenDB();
        public abstract void CloseDB();

        // generic command functions to run //
        public abstract DataTable CommandToDataTable(string cmdStr);
        public abstract List<string> CommandToList(string cmdStr);
        public abstract string CommandToString(string cmdStr);
        public abstract int ExecuteCommand(string cmdStr);

        // funcitons to pull data schemes //
        public abstract List<string> GetColumnNames(string table);
    }

    
}
