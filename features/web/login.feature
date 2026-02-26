@login
Feature: Login Functionality

  As a user
  I want to be able to login to the application
  So that I can access my account

  Background:
    Given the user is on the login page


  @smoke @positive
  Scenario Outline: Successful login with valid credentials for each user type
    When the user enters username "<username>"
    And the user enters password "<password>"
    And the user clicks the login button
    Then the user should be redirected to the home page

    Examples:
      | user_type      | username                           | password   |
      | Admin User     | admin@repcard.com                  | Repcard1$  |
      | Company User   | ac@mailinator.com                  | Test@123   |
      | Freemium User  | automationfreemium@mailinator.com  | Test@123   |
      | Premium User   | automationpremium@mailinator.com   | Test@123   |


  @negative
  Scenario Outline: Login fails for invalid or missing credentials
    When the user enters username "<username>"
    And the user enters password "<password>"
    And the user clicks the login button
    Then an error message should be displayed

    Examples:
      | scenario              | username           | password       |
      | invalid credentials   | invaliduser        | wrongpassword  |
      | empty username        | <empty>            | Repcard1$      |
      | empty password        | admin@repcard.com  | <empty>        |
