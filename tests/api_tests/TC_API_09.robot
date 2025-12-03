*** Settings ***
Library    ../../libs/api/Api.py


*** Test Cases ***
Verify Login With Delete Request
    [Documentation]    Varmistaa, että /verifyLogin ei onnistu ja DELETE palauttaa 405 ja odotetun virheviestin.
    Verify Login Delete Should Return 405