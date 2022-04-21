BEGIN;

DROP TABLE watchdog_nate_interval_view;

CREATE OR REPLACE VIEW watchdog_nate_interval_view AS

SELECT base.*,
EXTRACT(EPOCH (base._query_timestamp - base._last_update))/60 as _interval_timer
FROM watchdog_nate_view base

INNER JOIN (
	SELECT _table,
	max(_query_timestamp) as _query_timestamp
	FROM watchdog_nate_view
	WHERE _last_update is not null
	GROUP BY 1
) subquery

ON  base._table = subquery._table
AND base._query_timestamp = subquery._query_timestamp;

ROLLBACK;