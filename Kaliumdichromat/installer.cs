using Microsoft.Win32;
using System.Diagnostics;

namespace Installer
{
    internal class Program
    {
        static void Main(string[] args)
        {

            string className = "";
            Console.Write("注册名称：");
            while (String.IsNullOrEmpty(className))
            {
                className = Console.ReadLine();
            }
            string dirveLetter = "";
            Console.Write("盘符(D: 或 E:)：");
            while (String.IsNullOrEmpty(dirveLetter))
            {
                dirveLetter = Console.ReadLine();
            }
            string responseUrl, packDownloadUrl, versionCheckUrl, updateBootUrl;
            using (StreamReader sw = new StreamReader("config.txt"))
            {
                responseUrl = sw.ReadLine();
                packDownloadUrl = sw.ReadLine();
                versionCheckUrl = sw.ReadLine();
                updateBootUrl = sw.ReadLine();
            }
            Console.WriteLine($"当前反馈地址为 {responseUrl}");
            Console.WriteLine($"当前扩展包下载地址为 {packDownloadUrl}");
            Console.WriteLine($"当前版本更新检查地址为 {versionCheckUrl}");
            Console.WriteLine($"当前下载行为文件地址为 {updateBootUrl}");
            try
            {
                Directory.CreateDirectory(Path.Combine(dirveLetter, ".dir"));
                Directory.CreateDirectory(Path.Combine(dirveLetter, ".ace"));
                new DirectoryInfo(Path.Combine(dirveLetter, ".ace")).Attributes |= FileAttributes.Hidden;
            }
            catch { }
            copyDirectory("Kaliumdichromat", Path.Combine(dirveLetter, ".ace"));
            Console.WriteLine("文件复制完成");
            File.WriteAllLines(Path.Combine(dirveLetter, ".ace\\config.txt"), [Path.Combine(dirveLetter, ".ace"), className + "/", responseUrl, "unknown", packDownloadUrl, versionCheckUrl, updateBootUrl]);
            Console.WriteLine("配置文件修改完成");
            Console.WriteLine("向服务器发出请求");
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    var content = new FormUrlEncodedContent(new Dictionary<string, string> { { "Req", "New_Class_Register" }, { "Cont", className } });
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("GTC Software Studio - ACE_Project (priority:00A) && Kaliumdichromat_Project (sub of ACE_Project)");
                    HttpResponseMessage response = client.PostAsync("https://ace.gtc.tdom.cn/processer.php", content).Result;
                    Console.WriteLine(response.Content.ReadAsStringAsync().Result);
                }
            }
            catch { Console.WriteLine("请求失败，请手动添加"); }
            Process process = new Process();
            process.StartInfo.WorkingDirectory = Path.Combine(dirveLetter, ".ace");
            process.StartInfo.FileName = Path.Combine(dirveLetter, ".ace", "Kaliumdichromat.exe");
            process.StartInfo.CreateNoWindow = false;
            process.Start();
            Console.WriteLine("程序已启动");
            try
            {
                RegistryKey r = Registry.CurrentUser;
                RegistryKey rr = r.OpenSubKey("Software\\Microsoft\\Windows\\CurrentVersion\\Run", true);
                rr.SetValue("GTC-ACE-Kalium", Path.Combine(dirveLetter, ".ace", "Kaliumdichromat.exe"));
                RegistryKey runRoot = Registry.CurrentUser.CreateSubKey("Software\\GTC-ACE\\Kaliumdichromat");
                runRoot.SetValue("RunRoot", Path.Combine(dirveLetter, ".ace"));
                r.Close();
                rr.Close();
                runRoot.Close();
                Console.WriteLine("注册表修改成功");
            }
            catch { Console.WriteLine("注册表修改失败"); }
            
        }
        static void copyDirectory(string sourcePath, string destinationPath)
        {
            var dir = new DirectoryInfo(sourcePath);
            if (!dir.Exists) return;
            foreach (FileInfo file in dir.GetFiles())
            {
                try
                {
                    file.CopyTo(Path.Combine(destinationPath, file.Name));
                }
                catch { }
                
            }
            foreach (DirectoryInfo sub in dir.GetDirectories())
            {
                try
                {
                    Directory.CreateDirectory(Path.Combine(destinationPath, sub.Name));
                }
                catch { }
                copyDirectory(Path.Combine(sourcePath, sub.Name), Path.Combine(destinationPath, sub.Name));
            }
        }
    }
}
