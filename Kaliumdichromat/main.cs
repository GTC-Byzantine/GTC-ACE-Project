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
String localSaveRoot = "";

void scanDirectory(string path)
{
    DirectoryInfo currentDir = new DirectoryInfo(path);
    FileInfo[] files = currentDir.GetFiles();
    DirectoryInfo[] dirs = currentDir.GetDirectories();
    foreach (DirectoryInfo dir in dirs)
    {
        Console.WriteLine(dir.FullName.Substring(3));
        Directory.CreateDirectory(localSaveRoot + dir.FullName.Substring(3));
        scanDirectory(dir.FullName);
    }
    foreach (FileInfo file in files)
    {
        fileCnt += 1;
        copyRoot[fileCnt, 0] = file.FullName;
        copyRoot[fileCnt, 1] = localSaveRoot + file.FullName.Substring(3);
    }
}
/*
localSaveRoot = $"D:\\.dir\\[{(uint)(DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0)).TotalSeconds}]\\";
Directory.CreateDirectory(localSaveRoot);
scanDirectory("G:\\Otvratitelniy (C++ Reconstruct)");
for (int i = 1; i <= fileCnt; i++)
{
    Console.WriteLine("from " + copyRoot[i, 0] + " to " + copyRoot[i, 1]);
}
*/
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
            String saveDirName = SaveRoot + $"[{(uint)(DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0)).TotalSeconds}] from [{utf8.GetString(gb)}]\\";
            Console.WriteLine(saveDirName);
            fileCnt = 0;
            localSaveRoot  = saveDirName;
            Directory.CreateDirectory(localSaveRoot);
            scanDirectory(utf8.GetString(gb));
for (int i = 1; i <= fileCnt; i++)
{
    Console.WriteLine("from " + copyRoot[i, 0] + " to " + copyRoot[i, 1]);
}
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

