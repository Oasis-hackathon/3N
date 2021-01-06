create table if not exists oasis_hackathon_database.messages
(
	group_id int not null,
	submitter binary(16) not null,
	message text null,
	image text null,
	reg_date datetime default CURRENT_TIMESTAMP not null
);

