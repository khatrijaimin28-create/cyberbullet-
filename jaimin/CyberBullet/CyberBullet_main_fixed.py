import customtkinter as ctk
from core.network_scanner import scan_network
import threading


# -----------------------------
# CyberBullet Configuration
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CyberBullet(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("CyberBullet – AI-Assisted Cybersecurity Monitoring Suite")
        self.geometry("1280x760")
        self.minsize(1100, 680)

        self.scan_count = 0
        self.network_devices = 0

        # =========================
        # SIDEBAR
        # =========================
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.sidebar.pack_propagate(False)

        # Logo
        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="CYBERBULLET",
            font=("Arial", 25, "bold")
        )
        self.logo.pack(pady=(35, 2))

        self.logo_subtitle = ctk.CTkLabel(
            self.sidebar,
            text="SECURITY SUITE",
            font=("Arial", 11)
        )
        self.logo_subtitle.pack(pady=(0, 35))

        # Navigation
        menu_items = [
            "◉  Dashboard",
            "⌁  Network Scanner",
            "⌁  Port Scanner",
            "⌁  IP / Host Info",
            "⌁  Password Analyzer",
            "⌁  Phishing Analyzer",
            "⌁  File Integrity",
            "⌁  Log Analyzer",
            "⌁  Ransomware Simulator",
            "⌁  Scan History",
            "⌁  Reports"
        ]

        for item in menu_items:
            if "Dashboard" in item:
                command = self.show_dashboard
            elif "Network Scanner" in item:
                command = self.open_network_scanner
            else:
                command = self.module_not_ready

            button = ctk.CTkButton(
                self.sidebar,
                text=item,
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color=("gray75", "gray20"),
                anchor="w",
                font=("Arial", 13),
                command=command
            )

            button.pack(
                fill="x",
                padx=15,
                pady=3
            )

        # =========================
        # MAIN AREA
        # =========================
        self.main = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    # =========================
    # DASHBOARD
    # =========================
    def show_dashboard(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        # Header
        self.header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        self.header.pack(
            fill="x",
            padx=35,
            pady=(30, 10)
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Security Dashboard",
            font=("Arial", 30, "bold")
        )
        self.title_label.pack(side="left")

        self.status_label = ctk.CTkLabel(
            self.header,
            text="● SYSTEM ONLINE",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(
            side="right",
            pady=10
        )

        # =========================
        # RISK CARD
        # =========================
        self.risk_card = ctk.CTkFrame(
            self.main,
            height=190,
            corner_radius=18
        )
        self.risk_card.pack(
            fill="x",
            padx=35,
            pady=15
        )
        self.risk_card.pack_propagate(False)

        self.risk_heading = ctk.CTkLabel(
            self.risk_card,
            text="THREAT / RISK SCORE",
            font=("Arial", 13, "bold")
        )
        self.risk_heading.pack(pady=(25, 0))

        self.risk_score = ctk.CTkLabel(
            self.risk_card,
            text="0 / 100",
            font=("Arial", 42, "bold")
        )
        self.risk_score.pack(pady=2)

        self.risk_status = ctk.CTkLabel(
            self.risk_card,
            text="SYSTEM SECURE",
            font=("Arial", 14)
        )
        self.risk_status.pack()

        # =========================
        # STAT CARDS
        # =========================
        self.stats_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        self.stats_frame.pack(
            fill="x",
            padx=35,
            pady=15
        )

        self.create_stat_card(
            "NETWORK DEVICES",
            str(self.network_devices),
            "Devices discovered"
        )

        self.create_stat_card(
            "OPEN PORTS",
            "0",
            "Ports detected"
        )

        self.create_stat_card(
            "THREATS",
            "0",
            "Security findings"
        )

        self.create_stat_card(
            "SCANS",
            str(self.scan_count),
            "Total scans"
        )

        # =========================
        # QUICK ACTIONS
        # =========================
        self.quick_title = ctk.CTkLabel(
            self.main,
            text="Quick Security Actions",
            font=("Arial", 19, "bold")
        )
        self.quick_title.pack(
            anchor="w",
            padx=35,
            pady=(20, 10)
        )

        self.actions = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        self.actions.pack(
            fill="x",
            padx=35
        )

        actions = [
            ("Network Scan", self.open_network_scanner),
            ("Port Scan", self.module_not_ready),
            ("Password Check", self.module_not_ready),
            ("URL Analysis", self.module_not_ready)
        ]

        for action, command in actions:
            btn = ctk.CTkButton(
                self.actions,
                text=action,
                height=45,
                corner_radius=10,
                font=("Arial", 13, "bold"),
                command=command
            )

            btn.pack(
                side="left",
                expand=True,
                fill="x",
                padx=5
            )

        # =========================
        # FOOTER
        # =========================
        self.footer = ctk.CTkLabel(
            self.main,
            text="CyberBullet • AI-Assisted Cybersecurity Monitoring Suite",
            font=("Arial", 11)
        )
        self.footer.pack(
            side="bottom",
            pady=18
        )

    # =========================
    # NETWORK SCANNER PAGE
    # =========================
    def open_network_scanner(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main,
            text="Network Scanner",
            font=("Arial", 30, "bold")
        )
        title.pack(
            anchor="w",
            padx=35,
            pady=(35, 5)
        )

        subtitle = ctk.CTkLabel(
            self.main,
            text="Discover responsive devices on your local network",
            font=("Arial", 13)
        )
        subtitle.pack(
            anchor="w",
            padx=35
        )

        controls = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        controls.pack(
            fill="x",
            padx=35,
            pady=25
        )

        self.scan_button = ctk.CTkButton(
            controls,
            text="START NETWORK SCAN",
            height=45,
            width=220,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.run_network_scan
        )
        self.scan_button.pack(side="left")

        self.back_button = ctk.CTkButton(
            controls,
            text="BACK TO DASHBOARD",
            height=45,
            width=180,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.show_dashboard
        )
        self.back_button.pack(side="left", padx=10)

        self.scan_status = ctk.CTkLabel(
            self.main,
            text="Ready to scan",
            font=("Arial", 13)
        )
        self.scan_status.pack(
            anchor="w",
            padx=35,
            pady=(0, 15)
        )

        self.results_box = ctk.CTkTextbox(
            self.main,
            corner_radius=12,
            font=("Consolas", 12)
        )
        self.results_box.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 35)
        )

        self.results_box.insert(
            "end",
            "NETWORK SCANNER\n"
            "────────────────────────────────────────\n\n"
            "Click START NETWORK SCAN to begin.\n"
        )

    # =========================
    # RUN NETWORK SCAN
    # =========================
    def run_network_scan(self):
        if hasattr(self, "scan_button"):
            self.scan_button.configure(
                state="disabled",
                text="SCANNING..."
            )

        self.scan_status.configure(
            text="Scanning local network..."
        )

        self.results_box.delete("1.0", "end")
        self.results_box.insert(
            "end",
            "Scanning local network...\n"
        )

        # Run scan in background so the GUI does not freeze.
        thread = threading.Thread(
            target=self._network_scan_worker,
            daemon=True
        )
        thread.start()

    def _network_scan_worker(self):
        try:
            result = scan_network()

            hosts = result.get("hosts", [])
            network = result.get("network", "Unknown")
            error = result.get("error")

            self.after(
                0,
                self._display_scan_results,
                network,
                hosts,
                error
            )

        except Exception as error:
            self.after(
                0,
                self._display_scan_error,
                str(error)
            )

    def _display_scan_results(self, network, hosts, error=None):
        self.results_box.delete("1.0", "end")

        if error:
            self.results_box.insert(
                "end",
                f"SCAN ERROR:\n{error}\n"
            )
            self.scan_status.configure(
                text="Scan failed"
            )
        else:
            self.results_box.insert(
                "end",
                f"NETWORK: {network}\n"
            )

            self.results_box.insert(
                "end",
                f"DEVICES FOUND: {len(hosts)}\n"
            )

            self.results_box.insert(
                "end",
                "────────────────────────────────────────\n\n"
            )

            if not hosts:
                self.results_box.insert(
                    "end",
                    "No responsive devices found.\n"
                )
            else:
                for host in hosts:
                    self.results_box.insert(
                        "end",
                        f"IP       : {host['ip']}\n"
                    )
                    self.results_box.insert(
                        "end",
                        f"HOSTNAME : {host['hostname']}\n"
                    )
                    self.results_box.insert(
                        "end",
                        f"STATUS   : {host['status']}\n"
                    )
                    self.results_box.insert(
                        "end",
                        "────────────────────────────────────────\n"
                    )

                self.network_devices = len(hosts)

            self.scan_count += 1

            self.scan_status.configure(
                text=f"Scan complete • {len(hosts)} device(s) found"
            )

        if hasattr(self, "scan_button"):
            self.scan_button.configure(
                state="normal",
                text="START NETWORK SCAN"
            )

    def _display_scan_error(self, error):
        self.results_box.delete("1.0", "end")
        self.results_box.insert(
            "end",
            f"ERROR:\n{error}\n"
        )

        self.scan_status.configure(
            text="Scan failed"
        )

        if hasattr(self, "scan_button"):
            self.scan_button.configure(
                state="normal",
                text="START NETWORK SCAN"
            )

    # =========================
    # PLACEHOLDER MODULES
    # =========================
    def module_not_ready(self):
        for widget in self.main.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main,
            text="Module Coming Soon",
            font=("Arial", 30, "bold")
        )
        title.pack(
            anchor="w",
            padx=35,
            pady=(50, 10)
        )

        message = ctk.CTkLabel(
            self.main,
            text="This CyberBullet module will be added in the next development step.",
            font=("Arial", 14)
        )
        message.pack(
            anchor="w",
            padx=35
        )

        back = ctk.CTkButton(
            self.main,
            text="BACK TO DASHBOARD",
            width=200,
            height=45,
            command=self.show_dashboard
        )
        back.pack(
            anchor="w",
            padx=35,
            pady=25
        )

    # =========================
    # STATISTICS CARD
    # =========================
    def create_stat_card(self, title, value, description):
        card = ctk.CTkFrame(
            self.stats_frame,
            height=120,
            corner_radius=15
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold")
        )
        title_label.pack(
            pady=(18, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 27, "bold")
        )
        value_label.pack()

        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 10)
        )
        desc_label.pack()


# =============================
# START APPLICATION
# =============================
if __name__ == "__main__":
    app = CyberBullet()
    app.mainloop()
