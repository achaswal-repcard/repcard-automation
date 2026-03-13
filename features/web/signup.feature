@signup
Feature: Sign Up navigation and registration

  As a user
  I want to navigate between login and sign up pages and complete registration details
  So that I can create or access my account

  Background:
    Given the user is on the login page


  @positive
  Scenario: Navigate to Sign Up page from Login page
    When the user clicks on Create account button
    Then the Sign Up page should be displayed


  @positive
  Scenario: Navigate back to Login page from Sign Up page
    When the user clicks on Create account button
    And the user clicks on Sign In link on Sign Up page
    Then the Login page should be displayed

  @positive @signup_flow
  Scenario: Complete signup details across all 3 pages up to captcha verification
    When the user clicks on Create account button
    Then the Sign Up page should be displayed
    And the signup step 1 should be displayed
    When the user enters valid signup details on step 1
    And the user proceeds to signup step 2
    And the user enters valid signup details on step 2
    And the user proceeds to signup step 3
    And the user enters signup details on step 3 except captcha
    Then captcha should be displayed before finishing signup
