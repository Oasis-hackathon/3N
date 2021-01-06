create table if not exists oasis_hackathon_database.user_to_group
(
	user_uuid binary(16) not null,
	group_id int not null
);

