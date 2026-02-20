@forgot_password
Feature: Forgot Password Functionality

  As a user
  I want to reset my password
  So that I can regain access to my account

  Background:
    Given the user is on the login page


  @positive
  Scenario Outline: Reset password with registered email
    When the user clicks on Forgot Password link
    And the user enters email "<email>"
    And the user clicks on Reset Password button
    Then a success message should be displayed

    Examples:
      | email            |
      | am@yopmail.com   |


  @negative
  Scenario Outline: Reset password with unregistered or invalid email
    When the user clicks on Forgot Password link
    And the user enters email "<email>"
    And the user clicks on Reset Password button
    Then an error message should be displayed

    Examples:
      | email             |
      | invalid@gmail.com |