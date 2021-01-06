create table if not exists oasis_hackathon_database.account
(
	uuid binary(16) not null,
	id varchar(255) not null,
	email varchar(255) not null,
	username varchar(100) not null,
	password char(83) not null,
	address varchar(150) not null,
	is_admin tinyint default 1 not null,
	nickname varchar(100) not null,
	image text null,
	rate int default 50 not null
);

