*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py

*** Test Cases ***
Sign Up New User
    [Documentation]    Test for signing up a new user
    Open Home Page
    Consent Cookies
    Click Sign Up Login
    
