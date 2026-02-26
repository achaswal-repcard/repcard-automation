@sidebar_navigation
Feature: Left Sidebar Navigation

  As an admin user
  I want to navigate all left sidebar links in order
  So that I can verify each link redirects to the correct page

  @positive
  Scenario Outline: Sidebar links redirect correctly in left-panel order
    Given the user is logged in to admin home with valid credentials
    When the user clicks "<menu_path>" from left sidebar
    Then the user should land on URL containing "<expected_url_part>"

    Examples:
      | menu_path                    | expected_url_part         |
      | Golden Door Tracker          | /admin/golden-door-trackers |
      | Help Center                  | repcard.zendesk.com/hc/en-us |
      | Broadcast Feature            | /admin/notification       |
      | Companies                    | /admin/company            |
      | Users                        | /admin/user               |
      | Events                       | /admin/events             |
      | NFC > Link Types             | /admin/nfc-links-types    |
      | NFC > Links                  | /admin/nfc-links          |
      | Shop > Products              | /admin/product            |
      | Shop > Orders                | /admin/product/orders     |
      | Card Assets > Video Library  | /admin/videos             |
      | Card Assets > Calls to Action (CTA) | /admin/call-to-actions |
      | Card Assets > Email Templates | /admin/template          |
      | Training Library - LMS       | /admin/training           |
      | Reviews                      | /admin/review             |
      | Virtual Backgrounds          | /admin/virtual-backgrounds |
      | Settings > Hot Contacts Settings | /admin/hot-contact-settings |
      | Settings > Roles             | /admin/roles              |
      | Settings > App Settings      | /admin/app/settings       |
      | Submit Feedback              | /admin/feedbacks          |
      | Release Notes                | /admin/release-notes      |
      | Work hard & Be Kind.         | shop.repcard.com          |
