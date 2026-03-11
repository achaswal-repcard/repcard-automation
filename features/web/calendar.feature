@calendar
Feature: Calendar Creation

  As a company user
  I want to create a calendar from the new calendar flow
  So that I can use it for scheduling

  @positive
  Scenario: Company user creates direct assign calendar with default settings
    Given the company user is logged in and on create calendar page
    When the company user completes the calendar creation steps
    Then Calendar should be created

  @positive
  Scenario: Company user creates direct assign calendar with availability settings
    Given the company user is logged in and on create calendar page
    When the company user completes direct assign flow with availability selections
    Then Calendar should be created

  @positive
  Scenario: Company user creates dispatcher calendar calendar with default settings
    Given the company user is logged in and on create calendar page
    When the company user completes the dispatcher calendar creation steps
    Then Calendar should be created

  @positive
  Scenario: Company user creates dispatcher calendar with availability settings
    Given the company user is logged in and on create calendar page
    When the company user completes dispatcher flow with availability selections
    Then Calendar should be created
