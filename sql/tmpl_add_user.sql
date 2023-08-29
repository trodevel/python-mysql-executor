SET autocommit = OFF;

START TRANSACTION;

SET @DEBUG=%QUERY_DEBUG%;

SET @ID='%ID%';

SET @does_exist=( SELECT 1 FROM users WHERE id = @ID );
SET @does_exist=( IF( @does_exist IS NULL, 0, 1 ) );

SELECT 'DEBUG:', 'exists:', @does_exist FROM ( SELECT @DEBUG as DEBUG ) AS DBG WHERE DEBUG=1;

insert into users
    ( id, firstname, lastname  )
SELECT
    '%ID%', '%FIRSTNAME%', '%LASTNAME%'
FROM
    ( SELECT @does_exist AS does_exist ) AS DE
WHERE
    does_exist = 0
;

SELECT IF( @does_exist, 0, 1 );

COMMIT;
