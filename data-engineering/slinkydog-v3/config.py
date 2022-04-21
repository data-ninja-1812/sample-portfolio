### Tables ###

SNAPSHOT_STAGING =        "EDWCL_TEMP.clifford_in__v0_2h__FRAME_STAGING"
SNAPSHOT_CURRENT =        "EDWCL_TEMP.clifford_in__v0_2h__FRAME_CURRENT"
SNAPSHOT_PREVIOUS =       "EDWCL_TEMP.clifford_in__v0_2h__FRAME_PREVIOUS"
KEYFRAME_TABLE =          "EDWCL_TEMP.clifford_in__v0_2h__KEYFRAME_TABLE"
INTRAFRAME_MEMO_STAGING = "EDWCL_TEMP.clifford_in__v0_2h__INTRAFRAME_MEMO_STAGING"
INTRAFRAME_STAGING =      "EDWCL_TEMP.clifford_in__v0_2h__INTRAFRAME_STAGING"
INTRAFRAME_TABLE =        "EDWCL_TEMP.clifford_in__v0_2h__INTRAFRAME_TABLE"
INDEX_TABLE =             "EDWCL_TEMP.clifford_in__v0_2h__INDEX_TABLE"

PLAYBACK_FRAME   = "EDWCL_TEMP.clifford_in__v0_2h__PLAYBACK_FRAME"
PLAYBACK_APPEND  = "EDWCL_TEMP.clifford_in__v0_2h__PLAYBACK_APPEND"
PLAYBACK_REMOVE  = "EDWCL_TEMP.clifford_in__v0_2h__PLAYBACK_REMOVE"
PLAYBACK_TEMP    = "clifford_in__v0_2h__PLAYBACK_TEMP" #Must be volatile table

### Parameters ###

INTRAFRAME_MAX = 24

QUERY = """ (
SELECT
    --(Wheels_Out_TS - Wheels_In_TS) DAY(4) TO MINUTE AS Actual_Duration
    
    -- Reference features (Not for training)
    scd.SRG_CASE_SK,
    ste.ENCNT_SK,
    TRIM(apt.Facility_Mnemonic_CS) AS Facility_Mnemonic_CS,
    TRIM(apt.Clinical_Resource_Mnemonic_CS) AS Clinical_Resource_Mnemonic_CS,
    TRIM(apt.Resource_Group_Mnemonic_CS) AS Resource_Group_Mnemonic_CS,
    TRIM(apt.Appointment_Type) AS Proposed_Appt_Mnemonic,
    TRIM(apt.Appointment_URN) AS Appointment_URN,
    apt.Patient_DW_Id,
    TRIM(facte.Medical_Record_Num) AS Medical_Record_Num,
    apt.Appointment_Date_Time,
    TRIM(scd.SRG_CASE_ID_TXT) AS Surg_Case_Seq,
   
    -- Case Durations
    TRIM(apt.Appointment_Duration_Min_Cnt) AS Appt_Duration_w_cleanup_setup, -- Includes cleanup and setup
    TRIM(crsc.Scheduled_Setup_Duration) AS Scheduled_Setup_Duration,
    TRIM(crsc.Scheduled_Cleanup_Duration) AS Scheduled_Cleanup_Duration,
    sae_patin.EV_TS AS Wheels_In_TS,
    sae_patout.EV_TS AS Wheels_Out_TS,

    -- Patient features
    FLOOR(MONTHS_BETWEEN(CAST(apt.Appointment_Date_Time AS DATE), CAST(ptn.BRTH_TS AS DATE))/12) AS Patient_Age, 
    CASE 
        WHEN ptn.SEX_REF_CD IN ('F', 'female') THEN 'F'
        WHEN ptn.SEX_REF_CD IN ('M', 'male') THEN 'M'
        ELSE NULL
        END AS Patient_Sex,  
    TRIM(vitals_w_MRN.VITAL_VAL_NUM) AS Patient_weight,
    TRIM(vitals_w_MRN.VITAL_VAL_UNT_TYPE_CD) AS Patient_weight_units,
     
    -- Facility features
    TRIM(apt.Coid) AS Coid,
    TRIM(ff.Market_Code) AS Market_Code,
    TRIM(apt.Clinical_Resource_Mnemonic_CS) AS Scheduled_Room,
    --rpu.Room_Type_Code,
    
    -- Surgeon features
    scp.National_Provider_Id AS Surgeon_NPI,
    TRIM(rspgd.Procedure_Group_SSK) AS Procedure_Group_SSK,
    TRIM(rspgd.Procedure_Group_Desc) AS Service_Line,
                      
    -- Case Details
    TRIM(facte.Patient_Class_Code) AS Hospital_Care_Status,
    TRIM(facte.Reason_For_Visit_Txt) AS Reason_For_Visit_Txt,
    TRIM(refsurg.Nomenclature_Code) AS Proposed_Appt_IMO,
    TRIM(ref_nom_CPT.Standard_Code) AS Proposed_Appt_CPT,
    TRIM(ref_nom_ICD9.Standard_Code) AS Proposed_Appt_ICD9,
    scd.ANSTH_TYPE_CD AS Proposed_Anesthesia_Type,

    -- Procedures within each case   
    procedures.Proposed_Proc_1_Duration AS Props_Proc_1_Duration,
    procedures.Proposed_Proc_2_Duration AS Props_Proc_2_Duration,
    procedures.Proposed_Proc_3_Duration AS Props_Proc_3_Duration,
    procedures.Proposed_Proc_4_Duration AS Props_Proc_4_Duration

    --Proposed_Proc_1_SK,
    --Proposed_Proc_2_SK,
    --Proposed_Proc_3_SK,
    --Proposed_Proc_4_SK,
    
    --Proposed_Proc_1_CD_SK,
    --Proposed_Proc_2_CD_SK,
    --Proposed_Proc_3_CD_SK,
    --Proposed_Proc_4_CD_SK,
        
    --Proposed_Proc_1_Primary,
    --Proposed_Proc_2_Primary,
    --Proposed_Proc_3_Primary,
    --Proposed_Proc_4_Primary,
        
    --Proposed_Proc_1_Body_Site,
    --Proposed_Proc_2_Body_Site,
    --Proposed_Proc_3_Body_Site,
    --Proposed_Proc_4_Body_Site,
        
    --Proposed_Proc_1_Severity
    --Proposed_Proc_2_Severity,
    --Proposed_Proc_3_Severity,
    --Proposed_Proc_4_Severity,
        

        
    --Proposed_Proc_1_Desc,
    --Proposed_Proc_2_Desc,
    --Proposed_Proc_3_Desc,
    --Proposed_Proc_4_Desc
    
    
FROM 
    (-- Get all planned surgery cases from appointment schedule
    -- N.B. This table has a problem with empty string values ('') instead of NULL,
    -- which is why there are NULLIF()s in the SELECT statement

    SELECT 
        
        Appointment_URN,
        Patient_DW_Id,
        Coid,
        Pat_Acct_Num,
        Appointment_Date_Time,
        Appointment_Made_Date,
        Appointment_Type,
        NULLIF(Facility_Mnemonic_CS, '') AS Facility_Mnemonic_CS,
        NULLIF(Appointment_Status, '') AS Appointment_Status,
        NULLIF(Clinical_Resource_Mnemonic_CS, '') AS Clinical_Resource_Mnemonic_CS,
        NULLIF(Resource_Group_Mnemonic_CS, '') AS Resource_Group_Mnemonic_CS,
        NULLIF(Receiving_Location_Mnemonic_CS, '') AS Receiving_Location_Mnemonic_CS,
        NULLIF(Appointment_Duration_Min_Cnt , '') AS Appointment_Duration_Min_Cnt,
        NULLIF(Surgeon_Mnemonic_CS, '') AS Surgeon_Mnemonic_CS
        --NULLIF(Morning_Admit_Ind, '') AS Morning_Admit_Ind,
        --NULLIF(Network_Mnemonic_CS, '') AS Network_Mnemonic_CS,
        --NULLIF(Facility_Mnemonic_CS, '') AS Facility_Mnemonic_CS

    FROM EDWCDM_VIEWS.Clinical_Patient_Appt_Schedule

    WHERE Surgeon_Mnemonic_CS <> ''
        AND Company_Code = 'H'
        AND CAST(Appointment_Date_Time AS DATE) >= '2014-01-01' -- Choose timeframe
        AND Appointment_Status IN ('ATTENDED', 'BOOKED')
        AND Case_Type_Code NOT IN ('U', 'E')
        AND (Cast(Appointment_Date_Time AS DATE) - Appointment_Made_Date) > 1  -- Filters out 'planned' cases that were scheduled < 24 hrs prior

    ) apt
    
-- Facility
LEFT JOIN edwcdm_Views.fact_facility ff
ON ff.coid = apt.coid
AND ff.Company_Code = 'H'

-- Room location and room type
LEFT JOIN EDWCL_Views.Room_Primary_Use rpu
ON apt.Coid = rpu.Coid
    AND rpu.Company_Code = 'H'
    AND Trim(apt.Clinical_Resource_Mnemonic_CS) = Trim(rpu.Clinical_Resource_Mnemonic_CS)
    AND rpu.Eff_From_Date <= CAST(apt.Appointment_Date_Time AS Date) 
    AND (rpu.Eff_To_Date >= CAST(apt.Appointment_Date_Time AS Date) OR rpu.Eff_To_Date IS NULL)

-- Case detail. This table is transactional    
LEFT JOIN EDWCDM_Views.SRG_CASE_DTL scd
ON TRIM(apt.Appointment_URN) = TRIM(scd.SRG_CASE_APNTMT_ID_TXT)
    AND scd.Company_Code = 'H'
    AND apt.Coid = scd.COID
    AND apt.Patient_DW_Id = scd.PATIENT_DW_ID

LEFT JOIN EDWCL_VIEWS.Clinical_Reg_Surg_Case crsc
ON scd.SRG_CASE_ID_TXT = crsc.Surg_Case_Seq
    AND scd.PATIENT_DW_ID = crsc.Patient_DW_Id
    AND crsc.Active_Case_Sw = 1

-- Get the anesthesia type desc
--LEFT JOIN EDWCL_VIEWS.Ref_Anesthesia_Type anes
--ON scd.ANSTH_TYPE_CD = anes.Anesthesia_Type_Mnemonic
    --AND scd.COID = anes.Coid
    --AND Anesthesia_Type_Active_Ind = 'Y'
    
-- Get the Encounter SK
LEFT JOIN EDWCDM_Views.SRG_TO_ENCNT ste
ON scd.SRG_CASE_SK = ste.SRG_CASE_SK
    AND ste.Company_Code = 'H'

-- Get information about the encounter. Discard any case that does not have an associated encounter.
-- We also use this to filter out cases that are not Meditech 5.6
INNER JOIN EDWCDM_Views.Fact_Encounter facte
ON ste.ENCNT_SK = facte.Encounter_Sk
    AND facte.Company_Code = 'H'
    AND apt.Patient_DW_Id = facte.Patient_DW_Id

LEFT JOIN EDWCDM_Views.ENCNT_TO_ROLE e2role
ON ste.ENCNT_SK = e2role.ENCNT_SK
    AND e2role.Company_Code = 'H'
    AND e2role.RL_TYPE_REF_CD = 'PATIENT'
    AND e2role.VLD_TO_TS = '9999-12-31 00:00:00'
    
-- Patient features    
LEFT JOIN EDWCDM_Views.PTNT_DTL ptn
ON e2role.ROLE_PLYR_SK = ptn.ROLE_PLYR_SK
    AND ptn.VLD_TO_TS = '9999-12-31 00:00:00'

-- IMO Code
LEFT JOIN 
    (select Nomenclature_Code, Coid, Procedure_Code_SSK_CS
    from edwcdm_views.Ref_Surgical_Procedure 
    qualify ROW_NUMBER() over (partition by Coid, Procedure_Code_SSK_CS order by Nomenclature_Code) = 1
    ) refsurg
ON apt.Coid = refsurg.Coid
    AND apt.Appointment_Type = refsurg.Procedure_Code_SSK_CS

-- Service Line
LEFT JOIN  EDWCDM_Views.Ref_Surgical_Procedure_Group_Dtl rspgd
ON apt.COID = rspgd.Coid
    AND apt.Appointment_Type = rspgd.Procedure_Code_SSK_CS
    AND rspgd.Company_Code = 'H'

  
-- Get the individual procedures in the case    
LEFT JOIN
    (SELECT 
        SRG_CASE_SK,
        max(case when seq =1 then SRG_PRCDR_SK end) Proposed_Proc_1_SK,
        max(case when seq =2 then SRG_PRCDR_SK end) Proposed_Proc_2_SK,
        max(case when seq =3 then SRG_PRCDR_SK end) Proposed_Proc_3_SK,
        max(case when seq =4 then SRG_PRCDR_SK end) Proposed_Proc_4_SK,
    
        max(case when seq =1 then PRPSD_PRCDR_CD_SK end) Proposed_Proc_1_CD_SK,
        max(case when seq =2 then PRPSD_PRCDR_CD_SK end) Proposed_Proc_2_CD_SK,
        max(case when seq =3 then PRPSD_PRCDR_CD_SK end) Proposed_Proc_3_CD_SK,
        max(case when seq =4 then PRPSD_PRCDR_CD_SK end) Proposed_Proc_4_CD_SK,
    
        max(case when seq =1 then PRMY_PRCDR_IND end) Proposed_Proc_1_Primary,
        max(case when seq =2 then PRMY_PRCDR_IND end) Proposed_Proc_2_Primary,
        max(case when seq =3 then PRMY_PRCDR_IND end) Proposed_Proc_3_Primary,
        max(case when seq =4 then PRMY_PRCDR_IND end) Proposed_Proc_4_Primary,
    
        max(case when seq =1 then BDY_SITE_CD_SK end) Proposed_Proc_1_Body_Site,
        max(case when seq =2 then BDY_SITE_CD_SK end) Proposed_Proc_2_Body_Site,
        max(case when seq =3 then BDY_SITE_CD_SK end) Proposed_Proc_3_Body_Site,
        max(case when seq =4 then BDY_SITE_CD_SK end) Proposed_Proc_4_Body_Site,
    
        max(case when seq =1 then SVRTY_CD end) Proposed_Proc_1_Severity,
        max(case when seq =2 then SVRTY_CD end) Proposed_Proc_2_Severity,
        max(case when seq =3 then SVRTY_CD end) Proposed_Proc_3_Severity,
        max(case when seq =4 then SVRTY_CD end) Proposed_Proc_4_Severity,
    
        max(case when seq =1 then SRG_PRCDR_DURTN_AMT end) Proposed_Proc_1_Duration,
        max(case when seq =2 then SRG_PRCDR_DURTN_AMT end) Proposed_Proc_2_Duration,
        max(case when seq =3 then SRG_PRCDR_DURTN_AMT end) Proposed_Proc_3_Duration,
        max(case when seq =4 then SRG_PRCDR_DURTN_AMT end) Proposed_Proc_4_Duration,
    
        max(case when seq =1 then SRG_PRCDR_TXT end) Proposed_Proc_1_Desc,
        max(case when seq =2 then SRG_PRCDR_TXT end) Proposed_Proc_2_Desc,
        max(case when seq =3 then SRG_PRCDR_TXT end) Proposed_Proc_3_Desc,
        max(case when seq =4 then SRG_PRCDR_TXT end) Proposed_Proc_4_Desc
    
    FROM
        (SELECT
            SRG_CASE_SK,
            SRG_PRCDR_SK,
            Patient_DW_Id,
            PRPSD_PRCDR_CD_SK,
            PRMY_PRCDR_IND,
            BDY_SITE_CD_SK,
            SVRTY_CD,
            SRG_PRCDR_DURTN_AMT,
            SRG_PRCDR_TXT,
            ROW_NUMBER() OVER (partition by SRG_CASE_SK ORDER BY SRG_PRCDR_SEQ_NBR) SEQ
        FROM
            edwcdm_views.SRG_PRCDR_DTL
        WHERE
            PRCDR_TYPE_CD = 'Proposed Procedure'
            AND VLD_TO_TS = '9999-12-31 00:00:00'
            AND Company_Code = 'H'
        ) details
    GROUP BY SRG_CASE_SK) procedures
ON scd.SRG_CASE_SK = procedures.SRG_CASE_SK
    
    
    
    
-- Get actual outcome data
LEFT JOIN edwcdm_Pc_views.Fact_Surgical_Case_Detail  fscd
on scd.SRG_CASE_ID_TXT = fscd.Surg_Case_Seq
    AND fscd.Company_Code = 'H'
    AND apt.Patient_DW_Id = fscd.Patient_DW_Id
    AND apt.Coid = fscd.Coid
    
LEFT JOIN EDWCDM_views.SRG_ADMN_EV sae_patin
    ON scd.SRG_CASE_SK = sae_patin.SRG_CASE_SK
    AND sae_patin.Company_Code = 'H'
    AND sae_patin.VLD_TO_TS = '9999-12-31 00:00:00'
    AND sae_patin.EV_MAPPED_CD = 'PATIN'
    
LEFT JOIN EDWCDM_views.SRG_ADMN_EV sae_patout
    ON scd.SRG_CASE_SK = sae_patout.SRG_CASE_SK
    AND sae_patout.Company_Code = 'H'
    AND sae_patout.VLD_TO_TS = '9999-12-31 00:00:00'
    AND sae_patout.EV_MAPPED_CD = 'PTOUT'


    
-- From the IMO, get the CPT code for the main procedure
-- N.B. As far as I can tell, there is not a straightforward way to get
-- a 1:1 mapping of IMO -> CPT.  This logic takes the most recent mapping
-- from *whichever* facility most recently updated the mapping
LEFT JOIN (
    SELECT 
        Nomenclature_Code,
        Standard_Code,
        ROW_NUMBER( ) OVER (PARTITION BY Nomenclature_Code
          ORDER BY Code_Last_Update_Date DESC, Coid) AS "Ranking"
    
    FROM EDWCDM_PC_Views.Ref_Nomenclature_Code_Map
    WHERE Standard_Code_Type = 'CPT'
    AND Active_Ind = 'Y'
    QUALIFY Ranking = 1
    ) ref_nom_CPT
ON refsurg.Nomenclature_Code = ref_nom_CPT.Nomenclature_Code
    
-- From the IMO, get the ICD9 code for the main procedure
LEFT JOIN (
    SELECT 
        Nomenclature_Code,
        Standard_Code,
        ROW_NUMBER( ) OVER (PARTITION BY Nomenclature_Code
          ORDER BY Code_Last_Update_Date DESC, Coid) AS "Ranking"
    
    FROM EDWCDM_PC_Views.Ref_Nomenclature_Code_Map
    WHERE Standard_Code_Type = 'ICD9'
    AND Active_Ind = 'Y'
    QUALIFY Ranking = 1
    ) ref_nom_ICD9
ON refsurg.Nomenclature_Code = ref_nom_ICD9.Nomenclature_Code

-- Surgeon info
LEFT JOIN EDWCDM_VIEWS.Consolidated_Health_Care_Provider scp
ON  
apt.Coid = scp.COID    
    AND apt.Surgeon_Mnemonic_CS = scp.HCP_Mnemonic_CS  
    AND scp.Company_Code = 'H'


-- Patient weight
    LEFT JOIN 
        (-- Get all results from the vitals table and for each row, also pull in the patient's MRN and Market Code to join by
        SELECT 
            VITAL_VAL_NUM, 
            VITAL_OCCR_TS, 
            clinreg.Medical_Record_Num, 
            Market_Code, 
            Vital_Test_Desc, 
            VITAL_VAL_UNT_TYPE_CD
        FROM EDWCDM_VIEWS.VITAL_RSLT_DTL vitals
        
        LEFT JOIN EDWCDM_Views.Dim_Vital_Test dim_vitals
        ON vitals.VITAL_CD_SK = dim_vitals.Vital_Test_Sk
        
        LEFT JOIN EDWCL_VIEWS.Clinical_Registration clinreg
        ON vitals.PATIENT_DW_ID = clinreg.Patient_DW_Id
            AND vitals.Coid = clinreg.Coid
            AND clinreg.Company_Code = 'H'
        
        LEFT JOIN edwcdm_Views.fact_facility ff
        ON vitals.COID = ff.Coid
        AND ff.Company_Code = 'H'
        
        -- All possible weight values in kg
        WHERE (VITAL_VAL_UNT_TYPE_CD LIKE '%kg%' OR VITAL_VAL_UNT_TYPE_CD LIKE '%lb%' )  
        AND (Vital_Test_Desc IS NULL OR Vital_Test_Desc NOT IN ('Weight source:', 'WEIGHT SOURCE', 'Body mass index (BMI) [Ratio]', 'BMI', 'BMI:'))
        AND vitals.Company_Code = 'H'
        ) vitals_w_MRN
    ON facte.Medical_Record_Num = vitals_w_MRN.Medical_Record_Num
    AND ff.Market_Code = vitals_w_MRN.Market_Code
    AND apt.Appointment_Date_Time - INTERVAL '5' DAY > vitals_w_MRN.VITAL_OCCR_TS
    AND VITAL_VAL_NUM IS NOT NULL
    
   qualify ROW_NUMBER() over (partition by scd.SRG_CASE_SK order by VITAL_OCCR_TS desc, VITAL_VAL_UNT_TYPE_CD) = 1 --Only consider most recent entry;
  
    
    WHERE  rpu.Room_Type_Code IN ('GEN', 'HEART', 'CYSTO') -- This is via Jon Puncochar
    AND scd.VLD_TO_TS = '9999-12-31 00:00:00'
    AND (scd.CASE_VRFCTN_STS_TXT NOT IN ('DEFERRED', 'CANCEL') OR scd.CASE_VRFCTN_STS_TXT IS NULL)
    AND (facte.Source_System_Txt = 'Meditech 5.6' OR facte.Source_System_Txt IS NULL)
    AND (facte.Patient_Status_Code NOT IN ('cancelle', 'CAN') OR facte.Patient_Status_Code IS NULL)



    
    ) WITH DATA PRIMARY INDEX NUPI (Patient_DW_Id)
"""

### Parameters ###
PRIMARY_KEY = "SRG_CASE_SK"

HASH_VALUE = """HASHROW(SRG_CASE_SK,
ENCNT_SK,
Clinical_Resource_Mnemonic_CS,
Resource_Group_Mnemonic_CS,
Proposed_Appt_Mnemonic,
Appointment_URN,
Patient_DW_Id,
Medical_Record_Num,
Appointment_Date_Time,
Surg_Case_Seq,
Appt_Duration_w_cleanup_setup,
Scheduled_Setup_Duration,
Scheduled_Cleanup_Duration,
Wheels_In_TS,
Wheels_Out_TS,
Patient_Age,
Patient_Sex,
Patient_weight,
Patient_weight_units,
Coid,
Market_Code,
Scheduled_Room,
Surgeon_NPI,
Procedure_Group_SSK,
Service_Line,
Hospital_Care_Status,
Reason_For_Visit_Txt,
Proposed_Appt_IMO,
Proposed_Appt_CPT,
Proposed_Appt_ICD9,
Proposed_Anesthesia_Type,
Props_Proc_1_Duration + 0.01, --Salting for HASHROW work around
Props_Proc_2_Duration + 0.02, --Salting for HASHROW work around
Props_Proc_3_Duration + 0.03, --Salting for HASHROW work around
Props_Proc_4_Duration + 0.04  --Salting for HASHROW work around
)"""