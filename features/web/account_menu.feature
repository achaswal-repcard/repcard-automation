@account_menu
Feature: Account Menu Navigation

  As a logged-in user
  I want to navigate account menu links
  So that I can access profile pages and log out

  @positive
  Scenario Outline: Account menu links redirect correctly and logout works
    Given the user is logged in to the home page with valid credentials
    When the user opens the account dropdown menu
    And the user selects "<menu_item>" from account dropdown
    Then the system should redirect to "<destination>" page
    When the user navigates back to the admin home page
    And the user opens the account dropdown menu
    And the user logs out from account dropdown
    Then the system should redirect to admin login page

    Examples:
      | menu_item        | destination       |
      | Profile          | profile           |
      | Profile Settings | profile settings  |
      | Change Password  | change password   |
