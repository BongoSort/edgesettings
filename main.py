import os
import subprocess
import time
from playwright.sync_api import sync_playwright

EDGE_PROFILE = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")

def main():
    subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=EDGE_PROFILE,
            channel="msedge",
            headless=False,
            args=["--no-first-run"],
        )
        page = context.new_page()
        page.goto("edge://flags/#local-network-access-check")
        flag = page.locator("#local-network-access-check")
        value = flag.locator("select").input_value()
        print(f"Flag state before: {value}")
        flag.locator("select").select_option("Enabled")
        value = flag.locator("select").input_value()
        print(f"Flag state after:  {value}")
        page.close()
        context.close()

if __name__ == "__main__":
    main()
