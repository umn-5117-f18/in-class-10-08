drop table images;
CREATE TABLE images (
  img_id SERIAL PRIMARY KEY,
  filename varchar(255) not null,
  img bytea not null,
  tstamp timestamp default current_timestamp
);
