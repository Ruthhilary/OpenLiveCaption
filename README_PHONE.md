How to use from your phone

1. On your PC, run the server:

```powershell
C:\Users\acer\AppData\Local\Programs\Python\Python313\python.exe server.py
```

2. Find your PC's local IP address (in PowerShell):

```powershell
ipconfig
```

Look for the IPv4 address under the network adapter you use (e.g., 192.168.1.42).

3. On your phone (connected to the same Wi‑Fi), open a browser and visit:

http://<PC_IP>:5000/

4. Press "Start Recording", speak, then press "Stop Recording". The page will upload and display the transcription.

Notes:
- Whisper models are CPU-heavy. Running on a modern CPU will be slow but works.
- If you want to use `python` directly in terminal without full path, add Python to your PATH or use the existing `run.bat`.
