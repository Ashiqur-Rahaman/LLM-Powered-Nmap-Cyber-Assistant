import subprocess
import xml.etree.ElementTree as ET
import re

def extract_ip_or_domain(goal: str) -> str:
    """Extract the first valid IP or domain from the natural language goal."""
    ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", goal)
    if ip_match:
        return ip_match.group(0)
    
    # Fallback: look for domain-like text
    domain_match = re.search(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", goal)
    if domain_match:
        return domain_match.group(0)

    return None
def ask_local_llm(prompt: str, model: str = "mistral") -> str:
    """Ask the local Ollama LLM (Mistral) to generate a response."""
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    response = result.stdout.decode().strip()
    return response

def suggest_nmap_command(goal, target):
    prompt = f"""
You are a cybersecurity assistant that generates correct and efficient Nmap commands based on user goals.

Here are useful Nmap options:
- -sS: TCP SYN scan (stealth)
- -sV: Detect service versions
- -sU: UDP scan
- -O: Detect OS
- -A: Aggressive mode (OS + services + scripts)
- -T0 to -T5: Timing (0=slowest, 5=fastest)
- -p-: Scan all 65535 ports
- --top-ports 100: Scan top 100 common ports
- --script=http-*,vuln: Use NSE scripts
- -Pn: No ping (skip host discovery)
- -oX scan_output.xml: Save output as XML

Your goal is: \"{goal}\"
The target is: {target}

Generate a complete Nmap command using the best options. Only return the command. No explanation.
"""
    return ask_local_llm(prompt)

def fix_command(command, goal, target):
    """Patch LLM mistakes and add defaults."""
    if "-oX" not in command:
        command += " -oX scan_output.xml"

    if "os" in goal.lower() and "-O" not in command:
        command += " -O"

    if "all ports" in goal.lower() and "-p-" not in command:
        command += " -p-"

    if "http" in goal.lower() and "--script=http-" not in command:
        command += " --script=http-*"

    if "vuln" in goal.lower() and "--script=vuln" not in command:
        command += " --script=vuln"

    if "udp" in goal.lower() and "-sU" not in command:
        command += " -sU"

    if target not in command:
        command += f" {target}"

    return command.strip()

def run_nmap(command):
    """Run the Nmap command and return results."""
    print(f"\n🚀 Running: {command}\n")
    subprocess.run(command, shell=True)
    print("\n✅ Scan complete. Parsing results...\n")
    return "scan_output.xml"

def parse_nmap_output(xml_file):
    """Parse XML and display basic info."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for host in root.findall("host"):
        addr = host.find("address").attrib.get("addr")
        for port in host.findall(".//port"):
            port_id = port.attrib.get("portid")
            proto = port.attrib.get("protocol")
            state = port.find("state").attrib.get("state")
            service = port.find("service").attrib.get("name", "unknown")
            print(f"Host: {addr}, Port: {port_id}/{proto}, State: {state}, Service: {service}")

# -------------------- CLI Assistant --------------------

def main():
    print("🛡️  Local Nmap Cyber Assistant (powered by Mistral + Ollama)\n")
    print("Choose scan mode:")
    print("[1] Quick scan (common ports + versions)")
    print("[2] Full scan (all ports, OS, aggressive)")
    print("[3] Scripted scan (e.g., vuln/http)")
    print("[4] Custom natural-language goal")

    mode = input("Enter choice [1-4]: ").strip()
    if mode == "1":
        goal = "Find open common ports and detect service versions quickly"
        target = input("Enter target IP or domain: ").strip()
    elif mode == "2":
        goal = "Perform full scan on all ports and detect OS and services"
        target = input("Enter target IP or domain: ").strip()
    elif mode == "3":
        category = input("Enter script category (e.g., vuln, http, ftp, dns): ").strip()
        goal = f"Scan using NSE script category {category}"
        target = input("Enter target IP or domain: ").strip()
    elif mode == "4":
        goal = input("Enter your scan goal (natural language): ").strip()
        target = extract_ip_or_domain(goal)
        if not target:
            target = input("Enter target IP or domain: ").strip()
    else:
        print("Invalid choice.")
        return

    # ✅ Don't overwrite the extracted target!
    # target = input("Enter target IP or domain: ").strip()  ← delete this

    raw_command = suggest_nmap_command(goal, target)
    final_command = fix_command(raw_command, goal, target)
    xml_file = run_nmap(final_command)
    parse_nmap_output(xml_file)


if __name__ == "__main__":
    main()
