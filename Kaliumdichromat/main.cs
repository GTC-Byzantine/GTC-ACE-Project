// See https://aka.ms/new-console-template for more information

using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

/*
DirectoryInfo d = new DirectoryInfo("D:\\beseige_2");
FileInfo[] files = d.GetFiles();
DirectoryInfo[] directories = d.GetDirectories();
foreach (FileInfo file in files)
{
    Console.WriteLine(file.FullName);
}
foreach (DirectoryInfo directory in directories)
{
    Console.WriteLine(directory.Name);
}
*/
String SaveRoot = "D:\\.dir\\";
String[, ] copyRoot = new string[600000, 2];
bool[] registeredDrive = new bool[26];
int fileCnt = 0;
/*
StringBuilder volumename = new StringBuilder(256);
StringBuilder fstype = new StringBuilder(256);
uint serialNum, serialNumLength, flags;
GetVolumeInformationW("F:\\", volumename,
    (uint)volumename.Capacity - 1, out serialNum, out serialNumLength,
    out flags, fstype, (uint)fstype.Capacity - 1);
Console.WriteLine(volumename.ToString());
*/
void scanDirectory(string path)
{
    DirectoryInfo currentDir = new DirectoryInfo(path);
    FileInfo[] files = currentDir.GetFiles();
    DirectoryInfo[] dirs = currentDir.GetDirectories();
}
DriveInfo[] allDrivesG = DriveInfo.GetDrives();
Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
Console.OutputEncoding = System.Text.Encoding.Unicode;

foreach (DriveInfo item in allDrivesG)
{
    if (item.IsReady)
    {
        Encoding gbk = Encoding.GetEncoding("gb18030");
        Encoding utf8 = Encoding.GetEncoding("utf-8");
        byte[] gb = gbk.GetBytes(item.VolumeLabel);
        gb = Encoding.Convert(gbk, utf8, gb);
        Console.WriteLine(utf8.GetString(gb));
    }
    
    registeredDrive[item.Name[0] - 'A'] = true;
}

foreach (bool n in registeredDrive)
{ Console.WriteLine(n); }
while (true)
{
    DriveInfo[] allDrives = DriveInfo.GetDrives();
    bool[] visited = new bool[26];
    foreach (DriveInfo item in allDrives)
    {
        visited[item.Name[0] - 'A'] = true;
        if (!registeredDrive[item.Name[0] - 'A'])
        {
            if (!item.IsReady) continue;
            registeredDrive[item.Name[0] - 'A'] = true;
            Encoding gbk = Encoding.GetEncoding("gb18030");
            Encoding utf8 = Encoding.GetEncoding("utf-8");
            byte[] gb = gbk.GetBytes(item.VolumeLabel);
            gb = Encoding.Convert(gbk, utf8, gb);
            String saveDirName = SaveRoot + $"[{(uint)(DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0)).TotalSeconds}] from [{utf8.GetString(gb)}]";
            Console.WriteLine(saveDirName);
        }
    }
    for (int i = 0; i < 26; i++)
    {
        if (!visited[i] && registeredDrive[i])
        {
            registeredDrive[i] = false;
        }
    }
    Thread.Sleep(1000);
}

