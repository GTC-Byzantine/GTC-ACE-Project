namespace ilidilid
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Runtime.InteropServices;
    using System.Security.Cryptography;
    using System.Text;

    class Program
    {
        [DllImport("User32.dll", CharSet = CharSet.Auto)]
        public static extern int GetWindowThreadProcessId(IntPtr hwnd, out int ID);
        delegate bool WndEnumProc(IntPtr hWnd, int lParam);
        [DllImport("user32")]
        static extern bool EnumWindows(WndEnumProc lpEnumFunc, nint lParam);

        [DllImport("user32.dll", EntryPoint = "FindWindow", CharSet = CharSet.Auto)]
        extern static IntPtr FindWindow(string? lpClassName, string lpWindowName);
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        static extern int PostMessage(IntPtr hwnd, int msg, IntPtr wParam, IntPtr lParam);
        const int WM_CLOSE = 0x10;
        [DllImport("user32.dll")]
        static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);

        const int WM_GETTEXT = 0x000D;
        const int WM_GETTEXTLENGTH = 0x000E;

        [DllImport("User32.dll", EntryPoint = "SendMessage")]
        public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);

        [DllImport("user32.dll", EntryPoint = "SendMessage")]
        public static extern int SendMessage(int hwnd, int wMsg, int wParam, Byte[] lParam);
        public static extern bool IsWindowVisible(IntPtr hWnd);

        public static IntPtr FindWindowExByDimStrIntoWindow(string dimStr)
        {
            IntPtr iResult = IntPtr.Zero;

            string controlTitle = ""; //控件完全标题

            // 枚举子窗体，查找控件句柄
            bool i = EnumWindows(
            (h, l) =>
            {
                int cTxtLen;
                if (true)
                {
                    //对每一个枚举窗口的处理
                    cTxtLen = SendMessage(h, WM_GETTEXTLENGTH, 0, 0); //获取内容长度
                    Byte[] byt = new Byte[cTxtLen];
                    SendMessage((int)h, WM_GETTEXT, cTxtLen + 1, byt); //获取内容
                    string str = Encoding.Default.GetString(byt);
                    if (str.ToString().Contains(dimStr))
                    {
                        iResult = h;
                        controlTitle = str.ToString();
                        return false;
                    }
                    else
                        return true;
                }

            },
            0);

            // 返回查找结果
            return iResult;
        }
        static void Main()
        {
            nint hwnd = FindWindowExByDimStrIntoWindow("bilibili");
            int calcID;
            GetWindowThreadProcessId(hwnd, out calcID);
            Console.WriteLine(calcID);
            Console.WriteLine(hwnd);
            // PostMessage(hwnd, WM_CLOSE, IntPtr.Zero, IntPtr.Zero);
            keybd_event(0x11, 0, 0, 0);

            // 发送 W 键按下
            keybd_event(0x57, 0, 0, 0);

            // 发送 W 键释放
            keybd_event(0x57, 0, 2, 0);

            // 发送 Ctrl 键释放
            keybd_event(0x11, 0, 2, 0);
        }

        public delegate bool EnumWindowsProc(IntPtr hwnd, IntPtr lParam);

        [DllImport("user32.dll")]
        static extern int GetWindowTextLength(IntPtr hWnd);

        [DllImport("user32.dll")]
        static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

        [DllImport("user32.dll")]
        static extern int GetProcessId(IntPtr hWnd);
    }
}
