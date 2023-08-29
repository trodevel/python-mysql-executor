SELECT JSON_OBJECT(
    'id', id,
    'firstname', firstname,
    'lastname', lastname,
    'creation_ts', creation_ts
    ) FROM users;
