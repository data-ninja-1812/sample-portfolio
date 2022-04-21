SELECT
A.COID AS EHR_COID,
C.Facility_Mnemonic AS Facility_Mnemonic,
Trim(Substr(A.Source_System_Original_Code,7,30)) AS Location_Mnemonic,
A.Source_Term_Text,
A.Standard_Code AS Target_Code,
B.COID AS Target_COID,
Coalesce(B.Site_Name, A.Target_Term_Text) AS Target_Term

FROM EDWCL_VIEWS.Ref_Standard_Code_Map A
LEFT JOIN EDW_PUB_Views.Facility_Master_Site B
ON Trim(A.Standard_Code) = Trim(B.Site_Code)
LEFT JOIN EDWCDM_Views.Clinical_Facility C
ON A.COID = C.COID
WHERE Clinical_System_Module_Code = 'UNT'
;