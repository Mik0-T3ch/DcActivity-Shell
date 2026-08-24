import os
import unittest

from dcactivity.detectors.git import detect_git, get_git_context
from dcactivity.detectors.editors import detect_editor
from dcactivity.detectors.packages import detect_packages
from dcactivity.detectors.dev import detect_dev
from dcactivity.detectors.security import detect_security
from dcactivity.detectors.hardware import detect_hardware
from dcactivity.detectors.system import detect_system
from dcactivity.detectors.network import detect_network
from dcactivity.detectors.distro import get_distro_info


class TestDetectors(unittest.TestCase):
    def test_git_detection(self):
        res = detect_git("git commit -m 'initial'")
        self.assertIsNotNone(res)
        self.assertIn("commit", res["state"].lower())
        self.assertEqual(res["asset"], "git")

        res_push = detect_git("git push origin main")
        self.assertIn("push", res_push["state"].lower())

        res_branch = detect_git("git checkout dev")
        self.assertIn("dev", res_branch["state"])

    def test_git_context(self):
        ctx = get_git_context(os.getcwd())
        self.assertIsNotNone(ctx)
        self.assertIn("branch", ctx)
        self.assertIn("repo", ctx)

    def test_editor_detection(self):
        res = detect_editor("nvim main.py")
        self.assertIsNotNone(res)
        self.assertIn("main.py", res["state"])
        self.assertEqual(res["asset"], "neovim")

        res_nano = detect_editor("nano /etc/hosts")
        self.assertIn("hosts", res_nano["state"])
        self.assertEqual(res_nano["asset"], "nano")

    def test_packages_detection(self):
        res = detect_packages("sudo pacman -Syu")
        self.assertIsNotNone(res)
        self.assertIn("pacman", res["state"])

        res_cargo = detect_packages("cargo build --release")
        self.assertIn("Rust", res_cargo["state"])
        self.assertEqual(res_cargo["asset"], "rust")

        res_apt = detect_packages("apt update")
        self.assertIn("apt", res_apt["state"])

    def test_dev_detection(self):
        res = detect_dev("docker compose up -d")
        self.assertIsNotNone(res)
        self.assertIn("docker", res["asset"])

        res_k8s = detect_dev("kubectl get pods")
        self.assertIn("k8s", res_k8s["asset"])

        res_py = detect_dev("python3 script.py")
        self.assertIn("script.py", res_py["state"])

    def test_security_detection(self):
        res = detect_security("nmap -sV 10.0.0.1")
        self.assertIsNotNone(res)
        self.assertIn("nmap", res["state"])

        res_msf = detect_security("msfconsole")
        self.assertIn("Metasploit", res_msf["state"])

    def test_hardware_detection(self):
        res = detect_hardware("tmux attach -t dev")
        self.assertIsNotNone(res)
        self.assertIn("tmux", res["state"])

        res_nv = detect_hardware("nvidia-smi")
        self.assertIn("Nvidia", res_nv["state"])

    def test_system_detection(self):
        res = detect_system("btop")
        self.assertIsNotNone(res)
        self.assertIn("btop", res["state"])

        res_sudo = detect_system("sudo cat /etc/shadow")
        self.assertIn("root", res_sudo["state"])

    def test_network_detection(self):
        res = detect_network("ssh user@server.com")
        self.assertIsNotNone(res)
        self.assertIn("server.com", res["state"])

        res_ping = detect_network("ping 8.8.8.8")
        self.assertIn("8.8.8.8", res_ping["state"])

    def test_distro_info(self):
        info = get_distro_info()
        self.assertIn("id", info)
        self.assertIn("name", info)
        self.assertIn("asset_key", info)


if __name__ == "__main__":
    unittest.main()
