*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/SignLogin.py
Library     ../libs/pages/HomePage.py
Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Variables ***
&{PERSON1}    title=mr     day=10   month=June   year=1993
...           first=Test   last=User  company=ACME
...           addr1=Main street 1   addr2=Apt 2
...           country=Canada   state=Ontario   city=Toronto   zip=12345
...           newsletter=${True}    special_offers=${False}

&{PERSON2}    title=mrs    day=22   month=March  year=1990
...           first=Maija  last=Meikäläinen
...           addr1=Fleminginkatu 10  addr2=
...           country=Australia  state=Queensland  city=Cairns  zip=00100
...           newsletter=${False}    special_offers=${True}

*** Test Cases ***
TC005 Delete User
    [Documentation]    Sign up new user and delete it
    Delete Account    

TC004 Create New User With Valid Default Values
    [Documentation]    Sign up with default values
    Sign Up New User

TC004 Create New User With Valid Credentials
    [Documentation]    Sign up with given values from dictionary
    Sign Up New User    &{PERSON2}

TC004 Create New User2 With Valid Credentials
    [Documentation]    Sign up with given values from dictionary
    Sign Up New User    &{PERSON1}
    
TC001 Create User With Existing Email
    [Documentation]    Nevative test to sign in with existing invalid credentials
    Click Signup Login Link From Homepage
    Attempt Signup With Existing Email   ${EMAIL}    ${USERNAME}
