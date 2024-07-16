namespace RAM_Bomber
{
    internal class Program
    {
        static void Main(string[] args)
        {
            for (int i = 0; i <= 100; i++)
            {
                new Thread(() => {
                    while (true)
                    {
                        try
                        {
                            long[] t = new long[10000000];
                        }
                        catch { }
                    }
                }).Start();
            }
            for (int i = 0; i <= 10; i++)
            {
                new Thread(() => {
                    int a = 0;
                    while (true)
                    {
                        for (int i = 1; i <= 1000000000; i++)
                        {
                            a += 1;
                        }
                        Console.WriteLine(a);
                    }
                }).Start();
            }
            int closeTime = 5;
            if (args.Length > 0)
            {
                closeTime = int.Parse(args[0]);
            }
            Thread.Sleep(closeTime * 1000);
            Environment.Exit(0);
        }
    }
}
