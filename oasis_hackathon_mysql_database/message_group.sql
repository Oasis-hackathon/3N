create table if not exists oasis_hackathon_database.message_group
(
	id int auto_increment
		constraint `PRIMARY`
			primary key,
	article_id int not null,
	seller_uuid binary(16) not null,
	buyer_uuid binary(16) not null
);

