using Microsoft.Win32;

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
            Console.WriteLine("向服务器发出请求");
            try
            {
                Directory.CreateDirectory(Path.Combine(dirveLetter, ".dir"));
                Directory.CreateDirectory(Path.Combine(dirveLetter, ".ace"));
                new DirectoryInfo(Path.Combine(dirveLetter, ".ace")).Attributes |= FileAttributes.Hidden;
            }
            catch { }
            using (HttpClient client = new HttpClient())
            {
                var content = new FormUrlEncodedContent(new Dictionary<string, string> { { "Req", "New_Class_Register" }, { "Cont", className } });
                client.DefaultRequestHeaders.UserAgent.ParseAdd("GTC Software Studio - ACE_Project (priority:00A) && Kaliumdichromat_Project (sub of ACE_Project)");
                HttpResponseMessage response = client.PostAsync("https://ace.gtc.tdom.cn/processer.php", content).Result;
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }
            /*
            RegistryKey r = Registry.CurrentUser;
            RegistryKey rr = r.OpenSubKey("Software\\Microsoft\\Windows\\CurrentVersion\\Run", true);
            rr.SetValue("test", "value");
            */
        }
    }
}
