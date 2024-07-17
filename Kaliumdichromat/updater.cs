using System.Diagnostics;
using System.IO.Compression;
using System.Net;
using System.Text;
using System.Text.Json;

namespace Updater
{
    public class packRuntimeInformation
    {
        public string? version { get; set; }
        public string? exe { get; set; }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            string bootAddr = "", packDownloadSite = "";
            using (StreamReader r = new StreamReader("config.txt"))
            {
                int column = 1;
                string line = "";
                while ((line = r.ReadLine()) != null)
                {
                    if (column == 4)
                    {
                        packDownloadSite = line;
                    }
                    else if (column == 5)
                    {
                        bootAddr = line;
                    }
                    column++;
                }
            }
            using (WebClient wb = new WebClient())
            {
                wb.DownloadFile(bootAddr, "download-boot.txt");
            }
            string createEnd = "create-end---Prevent-Explosion-Field---create-end";
            using (StreamReader reader = new StreamReader("download-boot.txt"))
            {
                string line = "";
                while ((line = reader.ReadLine()) != null)
                {
                    string[] splited = line.Split(' ');
                    if (splited.Length > 0)
                    {
                        if (splited[0] == "update" || splited[0] == "download")
                        {
                            if (splited.Length == 3)
                            {
                                try
                                {
                                    using (WebClient wb = new WebClient())
                                    {
                                        wb.DownloadFile(splited[2], "tmpfile.tmp");
                                    }
                                    try
                                    {
                                        File.Delete(splited[1]);
                                    }
                                    catch { }
                                    File.Move("tmpfile.tmp", splited[1]);
                                }
                                catch { continue; }
                            }
                        }
                        else if (splited[0] == "create" || splited[0] == "modify")
                        {
                            if (splited.Length < 2) continue;
                            using (FileStream fs = File.Create(splited[1]))
                            {
                                string contentToWrite = "";
                                while ((contentToWrite = reader.ReadLine()) != null)
                                {
                                    if (contentToWrite != null)
                                    {
                                        if (contentToWrite == createEnd)
                                        {
                                            break;
                                        }
                                        else
                                        {
                                            byte[] c = Encoding.UTF8.GetBytes(contentToWrite + "\n");
                                            fs.Write(c, 0, c.Length);
                                        }
                                    }
                                }
                            }
                        }
                        else if (splited[0] == "getpack")
                        {
                            if (splited.Length < 2) continue;
                            packRuntimeInformation packInfo = new packRuntimeInformation();
                            if (!Directory.Exists("sidepacks"))
                            {
                                Directory.CreateDirectory("sidepacks");
                            }
                            string packName = splited[1];
                            Console.WriteLine(packName);
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
                                        catch (Exception e) { Console.WriteLine(e); continue; }
                                        ZipFile.ExtractToDirectory(Path.Combine("sidepacks", packName, packName + ".zip"), Path.Combine("sidepacks", packName, packName), Encoding.GetEncoding("gb18030"));
                                    }
                                }
                                catch
                                {
                                    Directory.Delete(Path.Combine("sidepacks", packName), true);
                                    continue;
                                }
                            }
                        }
                        else if (splited[0] == "run")
                        {
                            if (splited.Length < 2) continue;
                            string exePath = "";
                            for (int i = 1; i < splited.Length; i++)
                            {
                                exePath += splited[i] + " ";
                            }
                            Process p = new Process();
                            p.StartInfo.WorkingDirectory = Path.GetDirectoryName(exePath);
                            p.StartInfo.FileName = Path.GetFileName(exePath);
                            p.StartInfo.UseShellExecute = true;
                            p.StartInfo.CreateNoWindow = false;
                            p.Start();
                        }
                        else if (splited[0] == "runpack")
                        {
                            if (splited.Length < 2) continue;
                            string packName = splited[1];
                            if (!File.Exists(Path.Combine("sidepacks", packName, "config.txt"))) continue;
                            string arg = "";
                            if (splited.Length > 2)
                            {
                                for (int i = 2; i < splited.Length; i++)
                                {
                                    arg += splited[i];
                                    arg += " ";
                                }
                            }
                            packRuntimeInformation packInfo = JsonSerializer.Deserialize<packRuntimeInformation>(File.ReadAllText(Path.Combine("sidepacks", packName, "config.txt")));
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
                            catch { }
                        }
                        else if (splited[0] == "setline")
                        {
                            if (splited.Length < 4) continue;
                            string fileToSet = splited[1];
                            if (!File.Exists(fileToSet)) continue;
                            int lineToSet = int.Parse(splited[2]);
                            string newLine = "";
                            for (int i = 3; i < splited.Length; i++)
                            {
                                newLine += splited[i] + " ";
                            }
                            string[] lines = File.ReadAllLines(fileToSet);
                            if (lines.Length >= lineToSet)
                            {
                                lines[lineToSet - 1] = newLine;
                                Console.WriteLine(lines[lineToSet - 1]);
                                File.WriteAllLines(fileToSet, lines);
                            }
                            else
                            {
                                string[] tmp = new string[lineToSet];
                                Array.Copy(lines, tmp, lines.Length);
                                tmp[lineToSet - 1] = newLine;
                                Console.WriteLine(tmp[lineToSet - 1]);
                                File.WriteAllLines(fileToSet, tmp);
                            }

                        }
                        else if (splited[0] == "unzip")
                        {
                            if (splited.Length < 2) continue;
                            if (!File.Exists(splited[1])) continue;
                            if (Directory.Exists(Path.GetFileNameWithoutExtension(splited[1]))) Directory.Delete(Path.GetFileNameWithoutExtension(splited[1]), true);
                            Directory.CreateDirectory(Path.GetFileNameWithoutExtension(splited[1]));
                            ZipFile.ExtractToDirectory(splited[1], Path.Combine(Path.GetDirectoryName(splited[1]), Path.GetFileNameWithoutExtension(splited[1])), Encoding.GetEncoding("gb18030"));
                        }
                    }
                }
            }
        }
    }
}
