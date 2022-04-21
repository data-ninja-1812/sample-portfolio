BEGIN;

CREATE OR REPLACE VIEW watchdog_base_view AS

SELECT * FROM watchdog_v5_s0

--WHERE _query_timestamp > (NOW() - interval '30 days');

COMMIT;