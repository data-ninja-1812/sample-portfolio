SELECT 
Site.[site_code]
, Site.[parent_site_code]
, Facility.[coid]
, Purpose.[purpose_type_name]
, Site.[operating_status_code]
, OpStatus.[operating_status_name]
, Site.[site_name]
, Site.[site_short_name]
, Site.[street_addr_1]
, Site.[street_addr_2]
, Site.[city]
, Site.[county]
, Site.[state_code]
, Site.[postal_code]
, Site.[country_code]
, Site.[geographic_latitude]
, Site.[geographic_longitude]
, Site.[time_zone_code]
, Timezone.[time_zone_name]
, Facility.[unit_num]
, Facility.[corporate_name]
, Facility.[group_name]
, Facility.[division_name]
, Facility.[market_name]
, Facility.[coid_name]
, Facility.[network_mnemonic]
, Facility.[facility_mnemonic]
, Facility.[facility_oid]
, Facility.[facility_npi]
, Site.[effective_date_time]
FROM [RDM_FACILITY].[dbo].[site] Site
--
LEFT JOIN [RDM_FACILITY].[dbo].[ref_purpose_type] Purpose
	ON   Site.[purpose_type_id] = Purpose.[purpose_type_id]
	AND  Purpose.[active_sw] = 1
--
LEFT JOIN [RDM_FACILITY].[dbo].[ref_time_zone] TimeZone
	ON Site.[time_zone_code] = Timezone.[time_zone_code]
	AND  Timezone.[active_sw] = 1
--
LEFT JOIN [RDM_FACILITY].[dbo].[ref_operating_status] OpStatus
	ON Site.[operating_status_code] = OpStatus.[operating_status_code]
	AND  OpStatus.[active_sw] = 1
--
JOIN [RDM_FACILITY].[dbo].[facility] Facility
	ON Site.[company_code] = Facility.[company_code]
	AND Site.[coid] = Facility.[coid]

WHERE Purpose.Purpose_Type_Abrv IN ('HOS','ASC','FSER','UCC')


