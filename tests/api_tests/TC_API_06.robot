*** Settings ***
Library     ../../libs/api/Api.py


*** Test Cases ***
TC_API_06_POST_Search_Product_Without_Parameter
    [Documentation]    POST ilman search_product-parametria. Odotetaan virhevastausta (400) Python-kirjaston tarkistamana.
    Search Product Without Parameter Should Return 400
