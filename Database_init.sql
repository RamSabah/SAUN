CREATE DATABASE testing;
USE testing;
CREATE TABLE queries (
graph int,
querynumber int,
description text
);

INSERT INTO queries (graph, querynumber, description) VALUES(1,1,"My Text");
select * from queries;