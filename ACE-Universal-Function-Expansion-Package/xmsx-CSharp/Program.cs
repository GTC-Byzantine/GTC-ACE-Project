namespace xmsx
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
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
            for (int i = 0; i < 10; i++)
            {
                new Thread(run).Start();
            }
            Thread.Sleep(15000);
            System.Environment.Exit(0);
        }
    }
}