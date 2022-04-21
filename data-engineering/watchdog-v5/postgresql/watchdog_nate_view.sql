BEGIN;

CREATE OR REPLACE VIEW watchdog_nate_view AS

SELECT *,
COALESCE(_last_update,_query_timestamp) AS _last_record

FROM watchdog_base_view

WHERE _table IN (
	'BMAC.vw_All_Beds',
	'EDWCDM_VIEWS.fact_surgical_case_detail',
	'OpenGate_COMMON_ORC.zStagingCases',
	'OpenGate_Common.tbl_EDWidget_Nursing3_New',
	'OpenGate_Sepsis.tbl_MEDITECHEncntrVitalSgnLoad',
	'OpenGate_Sepsis.tbl_MEDITECHPatientEncntrLoad',
	'OpenGate_Common.tbl_EDWidget_Nursing1',
	'OpenGate_Common.tbl_EDWidget_Provider_Pat',
	'OpenGate_Sepsis.tbl_MEDITECHPhrmOrderLoad',
	'OpenGate_Sepsis.tbl_MEDITECHWBCLabRsltLoad',
	'OpenGate_CareAssure.tbl_MEDITECHPatientInsLoad',
	'TrackER.Track_ER_Admit_Order_stg',
	'TrackER.Track_ER_Patient_Census_Now_stg',
	'utp_dev.model_results',
	'WatchdogStatusMessage'
)
AND _query_timestamp > (NOW() - interval '30 days')
AND ((_last_update > (NOW() - interval '30 days')) OR (_last_update is null));

ROLLBACK;