drop table if exists addresses;
create table addresses (
  id integer primary key autoincrement,
  nickname string not null,
  location string not null,
	latitude string not null,
	longitude string not null
);