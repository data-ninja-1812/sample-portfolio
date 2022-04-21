BEGIN;

CREATE OR REPLACE VIEW watchdog_clifford_view AS

SELECT *,
COALESCE(_last_update,_query_timestamp) AS _last_record

FROM watchdog_base_view

WHERE _table IN (
    'EDWCDM_VIEWS.Fact_Encounter',
    'EDWCDM_VIEWS.Clinical_Patient_Appt_Schedule',
    'EDWCDM_VIEWS.Surgical_Case_Proc_Dtl',
    'EDWCDM_VIEWS.Ref_Surgical_Procedure_Group_Dtl',
    'EDWCDM_VIEWS.Standard_Code_Service_Line_Map',
    'EDWCDM_VIEWS.Dim_Vital_Test',
    'EDWCDM_VIEWS.SRG_CASE_DTL',
    'EDWCDM_VIEWS.VITAL_RSLT_DTL',
    'EDWCDM_VIEWS.SRG_TO_ENCNT',
    'EDWCDM_VIEWS.ENCNT_TO_ROLE',
    'EDWCDM_VIEWS.PTNT_DTL',
    'EDWCDM_VIEWS.SRG_ADMN_EV',
    'EDWCL_VIEWS.Clinical_Registration',
    'EDWCL_VIEWS.Clinical_Reg_Surg_Case',
    'EDWCL_VIEWS.Clinical_Health_Care_Provider',
    'EDWCL_VIEWS.Room_Primary_Use',
    'EDWCL_VIEWS.Ref_Surg_Props_Act_Procedure',
    'EDWCL_VIEWS.Ref_Surg_Props_Act_Proc_Group',
    'EDWCDM_PC_Views.Ref_Nomenclature_Code_Map',
    'clifford_dev.scoring_data_s0_base',
    'clifford_dev.predictions_s1_base',
	'WatchdogStatusMessage'
)

AND _query_timestamp > (NOW() - interval '30 days')
AND ((_last_update > (NOW() - interval '30 days')) OR (_last_update is null));

COMMIT;