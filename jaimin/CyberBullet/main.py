import customtkinter as ctk
import hashlib
import json
import os
import re
import socket
import subprocess
import time
import platform
from pathlib import Path
from urllib.parse import urlparse

from core.network_scanner import scan_network

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CyberBullet(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CYBERBULLET | Premium Security Suite")
        self.geometry("1400x820")
        self.minsize(1150, 720)

        self.scan_count = 0
        self.threat_count = 0
        self.device_count = 0
        self.open_port_count = 0
        self.history = []

        self.configure(fg_color="#05080d")
        self._setup_fonts()
        self.build_sidebar()
        self.build_dashboard()

    def _setup_fonts(self):
        self.font_title = ("Segoe UI", 28, "bold")
        self.font_h2 = ("Segoe UI", 19, "bold")
        self.font_body = ("Segoe UI", 12)
        self.font_small = ("Segoe UI", 10)
        self.font_mono = ("Consolas", 11)
        self.bg = "#05080d"
        self.panel = "#0b121a"
        self.panel2 = "#0e1721"
        self.border = "#17303a"
        self.teal = "#25e0c0"
        self.green = "#38e27b"
        self.muted = "#718295"

    def add_topbar(self, title, subtitle):
        top = ctk.CTkFrame(self.main, fg_color="transparent", height=72)
        top.pack(fill="x", padx=34, pady=(22, 4))
        top.pack_propagate(False)

        left = ctk.CTkFrame(top, fg_color="transparent")
        left.pack(side="left", fill="y")
        ctk.CTkLabel(left, text=title, font=self.font_title,
                     text_color="#f5f7fb").pack(anchor="w")
        ctk.CTkLabel(left, text=subtitle, font=self.font_small,
                     text_color="#778397").pack(anchor="w", pady=(2, 0))

        status = ctk.CTkFrame(top, corner_radius=12, fg_color="#101722",
                              border_width=1, border_color="#1e2a3a")
        status.pack(side="right", pady=10)
        ctk.CTkLabel(status, text="●", text_color="#35d07f",
                     font=("Segoe UI", 12, "bold")).pack(side="left", padx=(12, 4))
        ctk.CTkLabel(status, text="SYSTEM ONLINE", font=("Segoe UI", 10, "bold"),
                     text_color="#cbd5e1").pack(side="left", padx=(0, 12))

    def section_title(self, text):
        ctk.CTkLabel(self.main, text=text, font=self.font_h2,
                     text_color="#f5f7fb").pack(anchor="w", padx=36, pady=(12, 10))

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#0b0f15")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(26, 24))

        ctk.CTkLabel(brand, text="CB", width=44, height=44, corner_radius=12,
                     fg_color="#182231", text_color="#25e0c0",
                     font=("Segoe UI", 18, "bold")).pack(side="left")
        brand_text = ctk.CTkFrame(brand, fg_color="transparent")
        brand_text.pack(side="left", padx=10)
        ctk.CTkLabel(brand_text, text="CYBERBULLET",
                     font=("Segoe UI", 16, "bold"), text_color="#ffffff").pack(anchor="w")
        ctk.CTkLabel(brand_text, text="SECURITY PLATFORM",
                     font=("Segoe UI", 8, "bold"), text_color="#69778b").pack(anchor="w")

        ctk.CTkLabel(self.sidebar, text="WORKSPACE",
                     font=("Segoe UI", 9, "bold"), text_color="#536174").pack(
                         anchor="w", padx=22, pady=(0, 8))

        menu = [
            ("◉", "Dashboard", self.build_dashboard),
            ("⌁", "Network Scanner", self.open_network_scanner),
            ("⌁", "Wi-Fi Scanner", self.open_wifi_scanner),
            ("⌁", "Port Scanner", self.open_port_scanner),
            ("⌁", "IP / Host Info", self.open_host_info),
            ("⌁", "Password Analyzer", self.open_password),
            ("⌁", "Phishing Analyzer", self.open_phishing),
            ("⌁", "File Integrity", self.open_integrity),
            ("⌁", "Log Analyzer", self.open_log),
            ("⌁", "Ransomware Simulator", self.open_ransomware),
            ("⌁", "Scan History", self.open_history),
            ("⌁", "Reports", self.open_reports),
        ]

        for icon, name, command in menu:
            ctk.CTkButton(
                self.sidebar, text=f"{icon}   {name}", command=command,
                height=39, corner_radius=9, fg_color="transparent",
                hover_color="#151e2b", anchor="w",
                font=("Segoe UI", 11), text_color="#b8c3d2"
            ).pack(fill="x", padx=13, pady=2)

        ctk.CTkButton(
            self.sidebar, text="⚙   Settings", command=self.open_settings,
            height=36, corner_radius=8, fg_color="transparent",
            hover_color="#151e2b", anchor="w", font=("Segoe UI", 10),
            text_color="#8996a7"
        ).pack(fill="x", padx=13, pady=(12, 8))

        bottom = ctk.CTkFrame(self.sidebar, corner_radius=12, fg_color="#0f151e")
        bottom.pack(side="bottom", fill="x", padx=14, pady=16)
        ctk.CTkLabel(bottom, text="DEFENSIVE MODE",
                     font=("Segoe UI", 9, "bold"), text_color="#35d07f").pack(
                         anchor="w", padx=12, pady=(10, 0))
        ctk.CTkLabel(bottom, text="Local security operations",
                     font=("Segoe UI", 9), text_color="#667386").pack(
                         anchor="w", padx=12, pady=(2, 10))

    def clear_main(self):
        if hasattr(self, "main"):
            self.main.destroy()
        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="#0a0d12")
        self.main.pack(side="right", fill="both", expand=True)

    def page_header(self, title, subtitle):
        ctk.CTkLabel(self.main, text=title, font=("Arial", 30, "bold"),
                     text_color="#ffffff").pack(anchor="w", padx=38, pady=(30, 2))
        ctk.CTkLabel(self.main, text=subtitle, font=("Arial", 12),
                     text_color="#7f8a9a").pack(anchor="w", padx=40, pady=(0, 22))

    def card(self, parent, title, value, description):
        f = ctk.CTkFrame(parent, corner_radius=15, fg_color="#111720")
        f.pack(side="left", expand=True, fill="both", padx=6)
        ctk.CTkLabel(f, text=title, font=("Arial", 11, "bold"),
                     text_color="#8793a5").pack(pady=(18, 4))
        ctk.CTkLabel(f, text=value, font=("Arial", 28, "bold"),
                     text_color="#ffffff").pack()
        ctk.CTkLabel(f, text=description, font=("Arial", 10),
                     text_color="#667386").pack(pady=(2, 16))
        return f

    def build_dashboard(self):
        self.clear_main()
        self.add_topbar("Dashboard", "Real-time overview of your security environment")

        hero = ctk.CTkFrame(self.main, corner_radius=18, fg_color=self.panel,
                            border_width=1, border_color=self.border)
        hero.pack(fill="x", padx=30, pady=(6, 12))

        score_area = ctk.CTkFrame(hero, width=185, height=175, fg_color="transparent")
        score_area.pack(side="left", padx=(18, 5), pady=14)
        score_area.pack_propagate(False)
        score = max(0, 100 - min(100, self.threat_count * 15))
        ctk.CTkLabel(score_area, text="SECURITY SCORE", font=("Segoe UI", 9, "bold"),
                     text_color=self.muted).pack(pady=(8, 2))
        ctk.CTkLabel(score_area, text=str(score), font=("Segoe UI", 48, "bold"),
                     text_color=self.green).pack()
        ctk.CTkLabel(score_area, text="/ 100", font=("Segoe UI", 10, "bold"),
                     text_color="#93a2b3").pack()

        hero_mid = ctk.CTkFrame(hero, fg_color="transparent")
        hero_mid.pack(side="left", fill="both", expand=True, padx=10, pady=20)
        ctk.CTkLabel(hero_mid,
                     text="Your System is Secure" if self.threat_count == 0 else "Security Review Recommended",
                     font=("Segoe UI", 20, "bold"), text_color="#f5f7fb").pack(anchor="w")
        ctk.CTkLabel(hero_mid,
                     text="No critical threats found" if self.threat_count == 0 else f"{self.threat_count} finding(s) require attention",
                     font=("Segoe UI", 11), text_color=self.muted).pack(anchor="w", pady=(5, 3))
        ctk.CTkLabel(hero_mid,
                     text=f"Last activity: {self.history[-1][1] if self.history else 'No scan yet'}",
                     font=("Segoe UI", 10), text_color="#667789").pack(anchor="w", pady=(0, 15))
        ctk.CTkButton(hero_mid, text="QUICK SCAN", command=self.open_network_scanner,
                      height=38, width=120, corner_radius=9, fg_color="#16a673",
                      hover_color="#10845a", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        feed = ctk.CTkFrame(hero, width=300, height=175, corner_radius=14,
                            fg_color="#080e15", border_width=1, border_color="#14252e")
        feed.pack(side="right", padx=14, pady=14)
        feed.pack_propagate(False)
        ctk.CTkLabel(feed, text="LIVE THREAT FEED", font=("Segoe UI", 10, "bold"),
                     text_color="#dbe6ef").pack(anchor="w", padx=15, pady=(12, 7))
        for msg, col in [
            ("System protection active", self.green),
            ("Network monitoring ready", self.teal),
            ("No critical threats found", self.green),
        ]:
            row = ctk.CTkFrame(feed, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(row, text="●", text_color=col, font=("Segoe UI", 10, "bold")).pack(side="left")
            ctk.CTkLabel(row, text=msg, font=("Segoe UI", 9), text_color="#aab6c4").pack(side="left", padx=7)

        stats = ctk.CTkFrame(self.main, fg_color="transparent")
        stats.pack(fill="x", padx=24, pady=4)
        for title, value, desc in [
            ("NETWORK DEVICES", str(self.device_count), "Online"),
            ("OPEN PORTS", str(self.open_port_count), "Detected"),
            ("THREATS BLOCKED", str(self.threat_count), "Findings"),
            ("SCANS COMPLETED", str(self.scan_count), "This session"),
            ("SYSTEM STATUS", "OK", "Healthy"),
        ]:
            self.card(stats, title, value, desc)

        self.section_title("Quick Actions")
        actions = ctk.CTkFrame(self.main, fg_color="transparent")
        actions.pack(fill="x", padx=26)
        quick = [
            ("⌁", "Network Scan", "Discover devices", self.open_network_scanner),
            ("◌", "Wi-Fi Radar", "Nearby wireless networks", self.open_wifi_scanner),
            ("◉", "Port Scan", "Check open ports", self.open_port_scanner),
            ("◎", "IP Lookup", "Resolve a host", self.open_host_info),
            ("◆", "Password Check", "Assess strength", self.open_password),
            ("◇", "URL Analysis", "Review a URL", self.open_phishing),
            ("□", "File Scan", "Check file integrity", self.open_integrity),
        ]
        for icon, title, desc, cmd in quick:
            tile = ctk.CTkFrame(actions, height=105, corner_radius=13,
                                fg_color="#0b131c", border_width=1, border_color="#17303a")
            tile.pack(side="left", expand=True, fill="both", padx=4)
            tile.pack_propagate(False)
            ctk.CTkLabel(tile, text=icon, font=("Segoe UI", 23, "bold"),
                         text_color=self.teal).pack(pady=(12, 0))
            ctk.CTkButton(tile, text=title, command=cmd, height=25,
                          fg_color="transparent", hover_color="#14212d",
                          font=("Segoe UI", 10, "bold"), text_color="#e5edf5").pack(fill="x", padx=5)
            ctk.CTkLabel(tile, text=desc, font=("Segoe UI", 8),
                         text_color="#68788b").pack()

        lower = ctk.CTkFrame(self.main, fg_color="transparent")
        lower.pack(fill="both", expand=True, padx=30, pady=14)

        activity = ctk.CTkFrame(lower, corner_radius=14, fg_color=self.panel,
                                border_width=1, border_color=self.border)
        activity.pack(side="left", fill="both", expand=True, padx=(0, 7))
        ctk.CTkLabel(activity, text="Recent Activity", font=("Segoe UI", 15, "bold"),
                     text_color="#f5f7fb").pack(anchor="w", padx=16, pady=(12, 7))
        recent = ctk.CTkTextbox(activity, corner_radius=9, fg_color="#070c12",
                                font=self.font_mono, border_width=0)
        recent.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        if self.history:
            for item in self.history[-7:]:
                recent.insert("end", f"✓  {item[1]}  |  {item[0]}  |  {item[2]}\n")
        else:
            recent.insert("end", "No activity yet. Run a scan to populate this panel.\n")
        recent.configure(state="disabled")

        info = ctk.CTkFrame(lower, width=350, corner_radius=14, fg_color=self.panel,
                           border_width=1, border_color=self.border)
        info.pack(side="right", fill="both", padx=(7, 0))
        ctk.CTkLabel(info, text="System Information", font=("Segoe UI", 15, "bold"),
                     text_color="#f5f7fb").pack(anchor="w", padx=16, pady=(12, 12))
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "Unavailable"
        for k, v in [("Hostname", hostname), ("Local IP", local_ip),
                     ("Platform", os.name.upper()), ("Mode", "Defensive")]:
            r = ctk.CTkFrame(info, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=5)
            ctk.CTkLabel(r, text=k, font=("Segoe UI", 9), text_color="#718295").pack(side="left")
            ctk.CTkLabel(r, text=str(v), font=("Segoe UI", 9, "bold"),
                         text_color="#cbd5df").pack(side="right")

    def update_dashboard(self):
        self.build_dashboard()

    def open_settings(self):
        self.clear_main()
        self.add_topbar("Settings", "Application preferences and defensive-mode controls")
        panel = ctk.CTkFrame(self.main, corner_radius=15, fg_color=self.panel,
                             border_width=1, border_color=self.border)
        panel.pack(fill="x", padx=36, pady=12)
        ctk.CTkLabel(panel, text="Appearance", font=("Segoe UI", 16, "bold"),
                     text_color="#f5f7fb").pack(anchor="w", padx=20, pady=(18, 10))
        ctk.CTkLabel(panel, text="Theme", font=("Segoe UI", 10),
                     text_color=self.muted).pack(anchor="w", padx=20)
        theme = ctk.CTkOptionMenu(panel, values=["Dark", "System"],
                                  command=lambda v: ctk.set_appearance_mode(v.lower()),
                                  width=180)
        theme.set("Dark")
        theme.pack(anchor="w", padx=20, pady=(5, 18))
        ctk.CTkLabel(panel, text="Safety", font=("Segoe UI", 16, "bold"),
                     text_color="#f5f7fb").pack(anchor="w", padx=20, pady=(5, 10))
        ctk.CTkLabel(panel, text="Ransomware Simulator is sandbox-only and never encrypts real user files.",
                     font=("Segoe UI", 10), text_color=self.muted).pack(anchor="w", padx=20, pady=(0, 20))

    def open_network_scanner(self):
        self.clear_main()
        self.page_header("Network Scanner", "Discover responsive devices on your local network")
        ctk.CTkButton(self.main, text="START NETWORK SCAN", command=self.run_network_scan,
                      height=45, width=230, corner_radius=10,
                      font=("Arial", 13, "bold")).pack(anchor="w", padx=38, pady=10)
        self.scan_status = ctk.CTkLabel(self.main, text="Ready to scan",
                                        font=("Arial", 13), text_color="#8d98a8")
        self.scan_status.pack(anchor="w", padx=40, pady=(8, 12))
        self.results_box = ctk.CTkTextbox(self.main, corner_radius=12, font=("Consolas", 12))
        self.results_box.pack(fill="both", expand=True, padx=38, pady=(0, 30))
        self.results_box.insert("end", "NETWORK SCANNER\n" + "─" * 55 +
                                "\n\nClick START NETWORK SCAN to begin.\n")

    def run_network_scan(self):
        self.scan_status.configure(text="Scanning local network...")
        self.results_box.delete("1.0", "end")
        self.results_box.insert("end", "Scanning local network...\n")
        self.update()
        try:
            result = scan_network()
            hosts = result.get("hosts", [])
            network = result.get("network", "Unknown")
            self.device_count = len(hosts)
            self.scan_count += 1
            self.history.append(("Network Scan", time.strftime("%Y-%m-%d %H:%M:%S"),
                                 f"{len(hosts)} device(s)"))
            self.results_box.delete("1.0", "end")
            self.results_box.insert("end", f"NETWORK: {network}\nDEVICES FOUND: {len(hosts)}\n")
            self.results_box.insert("end", "─" * 55 + "\n\n")
            for host in hosts:
                self.results_box.insert("end",
                    f"IP       : {host.get('ip', 'Unknown')}\n"
                    f"HOSTNAME : {host.get('hostname', 'Unknown')}\n"
                    f"STATUS   : {host.get('status', 'Unknown')}\n" + "─" * 55 + "\n")
            self.scan_status.configure(text=f"Scan complete • {len(hosts)} device(s) found")
        except Exception as e:
            self.threat_count += 1
            self.scan_status.configure(text="Scan failed")
            self.results_box.insert("end", f"\nERROR:\n{e}\n")

    def tool_page(self, title, subtitle, button_text, callback, placeholder=""):
        self.clear_main()
        self.add_topbar(title, subtitle)
        ctk.CTkFrame(self.main, height=1, fg_color="#202936").pack(fill="x", padx=38, pady=4)
        box = ctk.CTkTextbox(self.main, corner_radius=12, font=("Consolas", 12))
        box.pack(fill="both", expand=True, padx=38, pady=20)
        if placeholder:
            box.insert("end", placeholder)
        return box, ctk.CTkButton(self.main, text=button_text, command=lambda: callback(box),
                                  height=45, corner_radius=10,
                                  font=("Arial", 13, "bold"))

    def open_wifi_scanner(self):
        """Show nearby Wi-Fi metadata plus details for the currently connected network."""
        self.clear_main()
        self.page_header(
            "Wi-Fi Radar",
            "Discover nearby wireless networks and inspect your current connection"
        )

        controls = ctk.CTkFrame(
            self.main, corner_radius=14, fg_color=self.panel,
            border_width=1, border_color=self.border
        )
        controls.pack(fill="x", padx=38, pady=(0, 12))

        ctk.CTkLabel(
            controls, text="WIRELESS ENVIRONMENT",
            font=("Segoe UI", 11, "bold"), text_color=self.teal
        ).pack(side="left", padx=16, pady=14)

        self.wifi_status = ctk.CTkLabel(
            controls, text="READY",
            font=("Consolas", 10, "bold"), text_color=self.green
        )
        self.wifi_status.pack(side="left", padx=10)

        ctk.CTkButton(
            controls, text="SCAN WI-FI", command=self.run_wifi_scan,
            height=36, width=150, corner_radius=9,
            fg_color="#16a673", hover_color="#10845a",
            font=("Segoe UI", 10, "bold")
        ).pack(side="right", padx=10, pady=9)

        ctk.CTkButton(
            controls, text="CLEAR", command=self.clear_wifi_results,
            height=36, width=90, corner_radius=9,
            fg_color="#182331", hover_color="#223244",
            font=("Segoe UI", 10, "bold")
        ).pack(side="right", pady=9)

        self.wifi_results = ctk.CTkTextbox(
            self.main, corner_radius=14, fg_color="#050a10",
            border_width=1, border_color=self.border,
            font=("Consolas", 11), text_color="#c9d5df"
        )
        self.wifi_results.pack(fill="both", expand=True, padx=38, pady=(0, 30))

        self.wifi_results.insert(
            "end",
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║                    CYBERBULLET WI-FI RADAR                  ║\n"
            "╚══════════════════════════════════════════════════════════════╝\n\n"
            "Click SCAN WI-FI to inspect nearby networks and your current\n"
            "connection: router/gateway IP, local IP, adapter MAC, ping,\n"
            "security type, channel, signal and BSSID.\n\n"
            "PASSWORD STATUS: PROTECTED\n"
            "Wi-Fi passwords are not extracted or displayed automatically.\n"
        )

    def clear_wifi_results(self):
        if hasattr(self, "wifi_results"):
            self.wifi_results.delete("1.0", "end")
            self.wifi_results.insert(
                "end",
                "Wi-Fi radar cleared. Click SCAN WI-FI to start.\n"
            )
        if hasattr(self, "wifi_status"):
            self.wifi_status.configure(text="READY", text_color=self.green)

    def _wifi_signal_icon(self, signal):
        try:
            value = int(signal)
        except Exception:
            return "?"
        if value >= 75:
            return "████"
        if value >= 50:
            return "███░"
        if value >= 25:
            return "██░░"
        return "█░░░"

    def _parse_netsh_wifi(self, output):
        """Parse Windows netsh wlan show networks mode=bssid output."""
        networks = []
        current = None

        for raw in output.splitlines():
            line = raw.strip()
            if not line:
                continue

            m = re.match(r"SSID\s+\d+\s*:\s*(.*)$", line, re.I)
            if m:
                if current:
                    networks.append(current)
                current = {
                    "ssid": m.group(1).strip() or "<Hidden SSID>",
                    "auth": "Unknown",
                    "encryption": "Unknown",
                    "signal": "Unknown",
                    "channel": "Unknown",
                    "radio": "Unknown",
                    "bssid": "Unknown",
                }
                continue

            if current is None:
                continue

            for pattern, key in [
                (r"Authentication\s*:\s*(.*)$", "auth"),
                (r"Encryption\s*:\s*(.*)$", "encryption"),
                (r"Signal\s*:\s*(\d+)%", "signal"),
                (r"Channel\s*:\s*(.*)$", "channel"),
                (r"Radio type\s*:\s*(.*)$", "radio"),
                (r"BSSID\s+\d+\s*:\s*(.*)$", "bssid"),
            ]:
                m = re.match(pattern, line, re.I)
                if m:
                    current[key] = m.group(1).strip()
                    break

        if current:
            networks.append(current)

        unique = {}
        for item in networks:
            key = item["ssid"].lower()

            def sig(x):
                try:
                    return int(x["signal"].replace("%", ""))
                except Exception:
                    return -1

            if key not in unique or sig(item) > sig(unique[key]):
                unique[key] = item

        return list(unique.values())

    def _run_netsh(self, args):
        return subprocess.run(
            ["netsh"] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20
        )

    def _get_current_wifi_details(self):
        """Collect non-secret connection details from Windows."""
        details = {
            "ssid": "Unknown",
            "bssid": "Unknown",
            "signal": "Unknown",
            "channel": "Unknown",
            "auth": "Unknown",
            "local_ip": "Unknown",
            "gateway": "Unknown",
            "mac": "Unknown",
            "ping": "Unavailable",
        }

        try:
            show = self._run_netsh(["wlan", "show", "interfaces"])
            if show.returncode == 0:
                lines = [x.strip() for x in show.stdout.splitlines()]
                for line in lines:
                    m = re.match(r"SSID\s*:\s*(.*)$", line, re.I)
                    if m and not re.match(r"BSSID", line, re.I):
                        details["ssid"] = m.group(1).strip()
                    m = re.match(r"BSSID\s*:\s*(.*)$", line, re.I)
                    if m:
                        details["bssid"] = m.group(1).strip()
                    m = re.match(r"Signal\s*:\s*(.*)$", line, re.I)
                    if m:
                        details["signal"] = m.group(1).strip()
                    m = re.match(r"Channel\s*:\s*(.*)$", line, re.I)
                    if m:
                        details["channel"] = m.group(1).strip()
                    m = re.match(r"Authentication\s*:\s*(.*)$", line, re.I)
                    if m:
                        details["auth"] = m.group(1).strip()
        except Exception:
            pass

        # ipconfig gives local IPv4, default gateway and adapter MAC without
        # accessing stored Wi-Fi credentials.
        try:
            ipcfg = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15
            )
            lines = ipcfg.stdout.splitlines()
            wifi_section = False
            for i, raw in enumerate(lines):
                line = raw.strip()
                if "Wireless LAN adapter" in line:
                    wifi_section = True
                    continue
                if wifi_section and line and not raw.startswith(" "):
                    wifi_section = False
                if wifi_section:
                    m = re.search(r"Physical Address[.\s]*:\s*([0-9A-Fa-f:-]{17})", line, re.I)
                    if m:
                        details["mac"] = m.group(1)
                    m = re.search(r"IPv4 Address[.\s]*:\s*([0-9.]+)", line, re.I)
                    if m:
                        details["local_ip"] = m.group(1)
                    m = re.search(r"Default Gateway[.\s]*:\s*([0-9.]+)", line, re.I)
                    if m:
                        details["gateway"] = m.group(1)
        except Exception:
            pass

        # Fallback for local IP.
        if details["local_ip"] == "Unknown":
            try:
                details["local_ip"] = socket.gethostbyname(socket.gethostname())
            except Exception:
                pass

        # Fallback for MAC via UUID-based interface address.
        if details["mac"] == "Unknown":
            try:
                import uuid
                mac_int = uuid.getnode()
                details["mac"] = ":".join(
                    f"{(mac_int >> shift) & 0xff:02X}"
                    for shift in range(40, -1, -8)
                )
            except Exception:
                pass

        if details["gateway"] not in ("Unknown", "", "0.0.0.0"):
            try:
                ping = subprocess.run(
                    ["ping", "-n", "1", "-w", "1000", details["gateway"]],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=3
                )
                m = re.search(r"time[=<]\s*(\d+)\s*ms", ping.stdout, re.I)
                details["ping"] = f"{m.group(1)} ms" if m else (
                    "Reachable" if ping.returncode == 0 else "Timeout"
                )
            except Exception:
                pass

        return details

    def run_wifi_scan(self):
        if not hasattr(self, "wifi_results"):
            return

        self.wifi_status.configure(text="SCANNING...", text_color=self.teal)
        self.wifi_results.delete("1.0", "end")
        self.wifi_results.insert("end", "[*] Reading wireless environment...\n")
        self.update_idletasks()

        try:
            result = self._run_netsh(
                ["wlan", "show", "networks", "mode=bssid"]
            )

            if result.returncode != 0:
                msg = result.stderr.strip() or result.stdout.strip() or \
                      "Windows returned an unknown error."
                raise RuntimeError(msg)

            networks = self._parse_netsh_wifi(result.stdout)
            current = self._get_current_wifi_details()

            self.scan_count += 1
            self.history.append((
                "Wi-Fi Scan",
                time.strftime("%Y-%m-%d %H:%M:%S"),
                f"{len(networks)} network(s)"
            ))

            self.wifi_results.insert(
                "end",
                "╔══════════════════════════════════════════════════════════════╗\n"
                "║                     WI-FI RADAR RESULTS                      ║\n"
                "╚══════════════════════════════════════════════════════════════╝\n\n"
                "CURRENT CONNECTION\n"
                + "─" * 68 + "\n"
                f"ROUTER / SSID : {current['ssid']}\n"
                f"GATEWAY IP    : {current['gateway']}\n"
                f"LOCAL IP      : {current['local_ip']}\n"
                f"MAC ADDRESS   : {current['mac']}\n"
                f"PING          : {current['ping']}\n"
                f"BSSID         : {current['bssid']}\n"
                f"SIGNAL        : {current['signal']}\n"
                f"CHANNEL       : {current['channel']}\n"
                f"SECURITY      : {current['auth']}\n"
                "PASSWORD      : PROTECTED / NOT EXTRACTED\n"
                + "─" * 68 + "\n\n"
                f"NEARBY NETWORKS DETECTED: {len(networks)}\n\n"
            )

            for index, net in enumerate(networks, 1):
                signal = net["signal"]
                try:
                    sig_value = int(signal.replace("%", ""))
                except Exception:
                    sig_value = -1

                if sig_value >= 75:
                    sig_label = "STRONG"
                elif sig_value >= 50:
                    sig_label = "GOOD"
                elif sig_value >= 25:
                    sig_label = "WEAK"
                else:
                    sig_label = "VERY WEAK"

                security_warning = (
                    "  [!] OPEN NETWORK"
                    if net["auth"].lower() == "open" else ""
                )

                self.wifi_results.insert(
                    "end",
                    f"[{index:02d}] {net['ssid']}\n"
                    f"     SIGNAL      : {signal:>8}  "
                    f"{self._wifi_signal_icon(signal)}  {sig_label}\n"
                    f"     SECURITY    : {net['auth']} / "
                    f"{net['encryption']}{security_warning}\n"
                    f"     CHANNEL     : {net['channel']}\n"
                    f"     RADIO       : {net['radio']}\n"
                    f"     BSSID       : {net['bssid']}\n"
                    + "─" * 68 + "\n"
                )

            self.wifi_results.insert(
                "end",
                "\n[OK] Wireless scan complete.\n"
                "[INFO] Router name, IP, MAC and ping are shown locally.\n"
                "[INFO] Wi-Fi passwords remain protected and are not extracted.\n"
            )
            self.wifi_status.configure(
                text=f"{len(networks)} NETWORKS FOUND",
                text_color=self.green
            )

        except FileNotFoundError:
            self.wifi_status.configure(
                text="NETSH UNAVAILABLE", text_color="#ef6b73"
            )
            self.wifi_results.insert(
                "end",
                "\n[ERROR] Windows 'netsh' utility was not found.\n"
            )
        except subprocess.TimeoutExpired:
            self.wifi_status.configure(text="TIMEOUT", text_color="#f0b84b")
            self.wifi_results.insert(
                "end", "\n[ERROR] Wi-Fi scan timed out.\n"
            )
        except Exception as e:
            self.wifi_status.configure(text="SCAN FAILED", text_color="#ef6b73")
            self.wifi_results.insert("end", f"\n[ERROR] {e}\n")

    def open_port_scanner(self):
        box, btn = self.tool_page("Port Scanner", "Scan ports on a host you own or are authorized to test.",
                                  "RUN PORT SCAN", self.run_port_scan,
                                  "Enter a target and optional ports below.\nExample: 127.0.0.1 | 1-100\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))
        box.insert("end", "\nTarget: 127.0.0.1\nPorts: 1-100\n")

    def run_port_scan(self, box):
        text = box.get("1.0", "end")
        target = re.search(r"Target:\s*(\S+)", text)
        ports = re.search(r"Ports:\s*([\d,-]+)", text)
        target = target.group(1) if target else "127.0.0.1"
        ports = ports.group(1) if ports else "1-100"
        try:
            out = subprocess.run(["nmap", "-sT", "-Pn", "-p", ports, target],
                                 capture_output=True, text=True, timeout=90)
            box.insert("end", "\n\n" + (out.stdout or out.stderr))
            self.scan_count += 1
        except FileNotFoundError:
            box.insert("end", "\nNmap not found. Install Nmap and ensure it is in PATH.\n")
        except Exception as e:
            box.insert("end", f"\nERROR: {e}\n")

    def open_host_info(self):
        box, btn = self.tool_page("IP / Host Info", "Resolve and inspect a host name.",
                                  "LOOK UP HOST", self.run_host_info,
                                  "Enter hostname or IP on the first line.\nExample: localhost\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))

    def run_host_info(self, box):
        target = box.get("1.0", "end").strip().splitlines()[1] if len(box.get("1.0", "end").strip().splitlines()) > 1 else "localhost"
        try:
            ip = socket.gethostbyname(target)
            box.insert("end", f"\nResolved IP : {ip}\nHostname    : {socket.getfqdn(target)}\n")
        except Exception as e:
            box.insert("end", f"\nLookup failed: {e}\n")

    def open_password(self):
        box, btn = self.tool_page("Password Analyzer", "Local password-strength assessment. No password is transmitted.",
                                  "ANALYZE PASSWORD", self.run_password,
                                  "Type the test password after: Password:\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))

    def run_password(self, box):
        text = box.get("1.0", "end")
        m = re.search(r"Password:\s*(.*)", text)
        pwd = m.group(1).strip() if m else ""
        score = 0
        score += 25 if len(pwd) >= 12 else 10 if len(pwd) >= 8 else 0
        score += 20 if re.search(r"[A-Z]", pwd) else 0
        score += 20 if re.search(r"[a-z]", pwd) else 0
        score += 20 if re.search(r"\d", pwd) else 0
        score += 15 if re.search(r"[^A-Za-z0-9]", pwd) else 0
        box.insert("end", f"\nStrength Score: {score}/100\n")
        box.insert("end", "Assessment: " + ("Strong" if score >= 80 else "Moderate" if score >= 50 else "Weak") + "\n")

    def open_phishing(self):
        box, btn = self.tool_page("Phishing / URL Analyzer", "Basic local URL-risk heuristics. This does not guarantee a site is safe.",
                                  "ANALYZE URL", self.run_phishing,
                                  "Enter URL after: URL:\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))

    def run_phishing(self, box):
        text = box.get("1.0", "end")
        m = re.search(r"URL:\s*(\S+)", text)
        url = m.group(1) if m else ""
        try:
            p = urlparse(url if "://" in url else "https://" + url)
            flags = []
            if p.scheme != "https": flags.append("not HTTPS")
            if "@" in p.netloc: flags.append("userinfo in URL")
            if len(p.netloc) > 60: flags.append("unusually long host")
            if re.match(r"^\d+\.\d+\.\d+\.\d+$", p.hostname or ""): flags.append("IP-address host")
            box.insert("end", f"\nHost: {p.hostname}\nFlags: {', '.join(flags) if flags else 'No basic heuristic flags'}\n")
        except Exception as e:
            box.insert("end", f"\nInvalid URL: {e}\n")

    def open_integrity(self):
        box, btn = self.tool_page("File Integrity", "Generate and compare SHA-256 hashes for files you control.",
                                  "HASH FILE", self.run_integrity,
                                  "Enter file path after: File:\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))

    def run_integrity(self, box):
        text = box.get("1.0", "end")
        m = re.search(r"File:\s*(.+)", text)
        path = Path(m.group(1).strip()) if m else Path()
        try:
            h = hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            box.insert("end", f"\nSHA-256:\n{h.hexdigest()}\n")
        except Exception as e:
            box.insert("end", f"\nERROR: {e}\n")

    def open_log(self):
        box, btn = self.tool_page("Log Analyzer", "Review a local text log and highlight common security indicators.",
                                  "ANALYZE LOG", self.run_log,
                                  "Enter log file path after: File:\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))

    def run_log(self, box):
        text = box.get("1.0", "end")
        m = re.search(r"File:\s*(.+)", text)
        path = Path(m.group(1).strip()) if m else Path()
        try:
            data = path.read_text(errors="ignore")
            patterns = {
                "Failed login": r"failed|authentication failure|invalid password",
                "Privilege event": r"admin|administrator|sudo|privilege",
                "Network event": r"connection|port|firewall|blocked",
            }
            box.insert("end", "\nLOG FINDINGS\n" + "─" * 40 + "\n")
            for name, pat in patterns.items():
                box.insert("end", f"{name:20} {len(re.findall(pat, data, re.I))}\n")
        except Exception as e:
            box.insert("end", f"\nERROR: {e}\n")

    def open_ransomware(self):
        box, btn = self.tool_page("Safe Ransomware Simulator",
                                  "Defensive training only: creates harmless demo files in a temporary sandbox.",
                                  "RUN SAFE SIMULATION", self.run_ransomware,
                                  "This simulator never encrypts real user files.\n")
        btn.pack(anchor="w", padx=38, pady=(0, 25))

    def run_ransomware(self, box):
        sandbox = Path.cwd() / "CyberBullet_Safe_Sandbox"
        sandbox.mkdir(exist_ok=True)
        for i in range(3):
            (sandbox / f"demo_document_{i+1}.txt").write_text(
                "CYBERBULLET SAFE SIMULATION FILE\nThis file contains no user data.\n")
        box.insert("end", f"\nCreated 3 harmless demo files in:\n{sandbox}\nSimulation complete.\n")

    def open_history(self):
        box, btn = self.tool_page("Scan History", "Recent operations performed in this session.",
                                  "REFRESH", self.run_history)
        btn.pack(anchor="w", padx=38, pady=(0, 25))
        self.run_history(box)

    def run_history(self, box):
        box.delete("1.0", "end")
        if not self.history:
            box.insert("end", "No scans recorded yet.\n")
        else:
            for item in self.history:
                box.insert("end", f"{item[1]} | {item[0]} | {item[2]}\n")

    def open_reports(self):
        box, btn = self.tool_page("Security Reports", "Export a simple local session report.",
                                  "EXPORT REPORT", self.run_reports)
        btn.pack(anchor="w", padx=38, pady=(0, 25))
        box.insert("end", "Click EXPORT REPORT to create CyberBullet_Report.txt\n")

    def run_reports(self, box):
        report = [
            "CYBERBULLET SECURITY REPORT",
            "=" * 40,
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Devices found: {self.device_count}",
            f"Open ports: {self.open_port_count}",
            f"Threat findings: {self.threat_count}",
            f"Scans completed: {self.scan_count}",
            "",
            "Recent activity:",
        ] + [f"{x[1]} | {x[0]} | {x[2]}" for x in self.history]
        Path("CyberBullet_Report.txt").write_text("\n".join(report), encoding="utf-8")
        box.insert("end", "\nReport exported: CyberBullet_Report.txt\n")


if __name__ == "__main__":
    app = CyberBullet()
    app.mainloop()
