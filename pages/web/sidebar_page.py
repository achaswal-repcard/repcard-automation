from playwright.sync_api import expect


class SidebarPage:
    def __init__(self, page):
        self.page = page
        self.sidebar_root = "aside.main-sidebar"
        self.topbar_links = {
            "Golden Door Tracker": "a.golden-door-tracker",
            "Help Center": "a.repcard-help",
            "Broadcast Feature": "a.movable-icon[data-label='Broadcast Feature']",
        }

    def click_sidebar_path(self, menu_path):
        if menu_path in self.topbar_links:
            self._click_topbar_link(menu_path)
            return

        parts = [part.strip() for part in menu_path.split(">")]
        if len(parts) == 1:
            self._click_sidebar_link(parts[0])
            return

        parent, child = parts[0], parts[1]
        self._expand_parent_menu_if_needed(parent, child)
        self._click_sidebar_link(child)

    def verify_redirect(self, expected_url_part):
        expected = expected_url_part.strip()

        if self._is_external_destination(expected):
            # Some links open in a new tab (target=_blank), e.g. Help Center / Work hard & Be Kind.
            matched_pages = [p for p in self.page.context.pages if expected in p.url]
            if expected in self.page.url:
                matched_pages.append(self.page)

            assert matched_pages, f"Expected a page with URL containing '{expected}', but none was found."
            for popup in matched_pages:
                if popup != self.page and not popup.is_closed():
                    popup.close()
            return

        self.page.wait_for_url(f"**{expected}*", timeout=10000)
        assert expected in self.page.url

    @staticmethod
    def _is_external_destination(expected):
        return (not expected.startswith("/")) and ("." in expected)

    def go_to_home_page(self, base_url):
        self.page.goto(f"{base_url}/admin/home")
        self.page.wait_for_url("**/admin/home", timeout=10000)
        assert "/admin/home" in self.page.url

    def _expand_parent_menu_if_needed(self, parent, child):
        child_locator = self.page.locator(
            f"{self.sidebar_root} ul.treeview-menu a:has-text('{child}')"
        ).first

        if child_locator.is_visible():
            return

        self._click_sidebar_link(parent)
        expect(child_locator).to_be_visible(timeout=10000)

    def _click_sidebar_link(self, link_text):
        locator = self.page.locator(
            f"{self.sidebar_root} a:has-text('{link_text}')"
        ).first

        expect(locator).to_be_visible(timeout=10000)

        target = locator.get_attribute("target")
        if target == "_blank":
            with self.page.context.expect_page() as popup_info:
                locator.click()
            popup = popup_info.value
            popup.wait_for_load_state("domcontentloaded")
        else:
            locator.click()

    def _click_topbar_link(self, link_text):
        locator = self.page.locator(self.topbar_links[link_text]).first
        expect(locator).to_be_visible(timeout=10000)

        target = locator.get_attribute("target")
        if target == "_blank":
            with self.page.context.expect_page() as popup_info:
                locator.click()
            popup = popup_info.value
            popup.wait_for_load_state("domcontentloaded")
        else:
            locator.click()
