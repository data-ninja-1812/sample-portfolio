-- Watchdog table base schema

-- Watchdog Version 5 Schema s0
-- August 8, 2019

BEGIN;

CREATE TABLE watchdog_v5_s0
--CREATE TABLE watchdog_v5_s0_dev
(
    _column text,
    _db_type text,
    _last_update timestamp without time zone,
    _query_timestamp timestamp without time zone,
    _server text,
    _status text,
    _table text,
    auto_key serial primary key
);

ROLLBACK;
