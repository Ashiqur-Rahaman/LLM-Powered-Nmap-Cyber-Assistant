# 🛡️ LLM-Powered Nmap Cyber Assistant

This project is a **local AI-powered command-line assistant** that learns how to generate, run, and analyze Nmap scans using natural language. It combines the power of a local LLM (e.g., Mistral via Ollama) with the capabilities of `nmap` to automate common security reconnaissance tasks.

---

## 🚀 Features

✅ Ask in plain English (e.g. "Scan 10.23.64.227 to detect OS and run basic vulnerability checks")  
✅ Automatically generates optimized `nmap` commands  
✅ Supports common modes: Quick scan, Full scan, Script-based scans, Custom goals  
✅ Parses and summarizes scan results from XML output  
✅ Runs completely locally — no OpenAI or cloud services required  
✅ Uses Ollama with Mistral or other supported models (LLaMA, Mixtral, etc.)

---

## 📸 Demo

🛡️ Local Nmap Cyber Assistant (powered by Mistral + Ollama)

Choose scan mode:
[1] Quick scan (common ports + versions)
[2] Full scan (all ports, OS, aggressive)
[3] Scripted scan (e.g., vuln/http)
[4] Custom natural-language goal
Enter choice [1-4]: 4
Enter your scan goal (natural language): Scan 10.23.64.227 to detect the OS and run vulnerability scripts
🚀 Running: nmap -sS -sV -O --script=vuln -oX scan_output.xml 10.23.64.227

✅ Scan complete. Parsing results...

Host: 10.23.64.227, Port: 22/tcp, State: open, Service: ssh
Host: 10.23.64.227, Port: 80/tcp, State: open, Service: http


---

## 🧠 How It Works

1. Accepts user input (via menu or natural language)
2. Extracts target IP/domain from input
3. Uses local LLM (via [Ollama](https://ollama.com/)) to generate an appropriate `nmap` command
4. Fixes/adds extra options using rules
5. Runs the scan and saves XML output
6. Parses and prints key results (open ports, services, etc.)

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) with Mistral, LLaMA, etc.
- `nmap` installed and available in `$PATH`

---

## 🔧 Installation

### 1. Install `nmap`

```bash
sudo apt install nmap   # Debian/Ubuntu
# or
brew install nmap       # macOS
```
### 2. Install `Ollama` and pull a model

Install Ollama (https://ollama.com)
Then pull a supported model:
ollama pull mistral

# Install Ollama (Mistral model)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral


### 3. ▶️ Run the Assistant 
python3 assistant.py


🧑‍🎓 Ethical Use

This project was developed as a Self-learning research tool to explore:

    Local language model reasoning for security automation

    Nmap command learning and generalization

    Natural language interface for cybersecurity tools

Feel free to fork and build upon this work!


🤝 Acknowledgements

    Nmap

    Ollama

    Mistral

    Python, XML, and all the open-source tools that made this possible.
