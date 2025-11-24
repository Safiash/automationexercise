*** Settings ***
Library    ../pages/Api.py


*** Test cases ***
Search Product
    [Documentation]    Palauttaa hakulistan hakusanan mukaan ja varmistaa, että haku onnistuu.
    ${result}=    Search Product Should Return Results    top
    Should Be True    ${result['responseCode']} >= 200 and ${result['responseCode']} < 300