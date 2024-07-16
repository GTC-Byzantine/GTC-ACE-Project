namespace xmsx
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] args)
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            ApplicationConfiguration.Initialize();
            void run()
            {
                Form form = new Form1();
                int size = new Random().Next(600, 800);
                form.ClientSize = new Size(size, size);
                Application.Run(form);
            }
            int lastTime = 15000;
            int flipTime = 10;
            if (args.Length > 0)
            {
                try
                {
                    lastTime = int.Parse(args[0]);
                }
                catch { }
            }
            if (args.Length > 1)
            {
                try
                {
                    flipTime = int.Parse(args[1]);
                }
                catch { }
            }
            for (int i = 0; i < flipTime; i++)
            {
                new Thread(run).Start();
            }
            Thread.Sleep(lastTime);
            Environment.Exit(0);
        }
    }
}