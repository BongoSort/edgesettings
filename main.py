import os
from playwright.sync_api import sync_playwright

EDGE_PROFILE = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")

def main():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=EDGE_PROFILE,
            channel="msedge",
            headless=False,
        )
        page = context.new_page()
        page.goto("edge://flags/#local-network-access-check")
        flag = page.locator("#local-network-access-check")
        value = flag.locator("select").input_value()
        print(f"Flag state: {value}")
        flag.locator("select").select_option("Enabled")
        value = flag.locator("select").input_value()
        print(f"Flag state: {value}")
        try:
            page.get_by_role("button", name="Restart").click()
        except Exception:
            pass  # Edge restarts and closes the session — expected

if __name__ == "__main__":
    main()
