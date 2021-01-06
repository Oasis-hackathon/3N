create table if not exists oasis_hackathon_database.article
(
	id int auto_increment
		constraint `PRIMARY`
			primary key,
	title varchar(255) not null,
	submitter binary(16) not null,
	address varchar(255) not null,
	image text null,
	cost int not null,
	content text null,
	remain_time int default 48 not null,
	max_num int default 1 not null,
	article_type varchar(20) not null,
	article_category varchar(20) not null,
	reg_date datetime default CURRENT_TIMESTAMP not null,
	is_visible tinyint default 1 not null,
	views int default 0 not null
);

