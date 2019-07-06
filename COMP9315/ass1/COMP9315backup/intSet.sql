drop type intSet cascade;

drop table mySets;

CREATE FUNCTION intset_in(cstring)
   RETURNS intSet
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION intset_out(intSet)
   RETURNS cstring
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE intSet (
   
   input = intset_in,
   output = intset_out
);

CREATE FUNCTION belong(integer, intSet)
	RETURNS bool
	AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

create operator <@(
leftarg = integer,
rightarg = intSet,
procedure = belong);


create table mySets (id integer primary key, iset intSet);

insert into mySets values (2,'{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49}');


insert into mySets values (1, '{1,2,3}');

select * from mySets;

drop type intSet cascade;

/srvr/z5089358/postgresql-10.4/src/tutorial
insert into mySets values (1,'{ }');
insert into mySets values (2,'{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49}');
insert into mySets values (3,'{1, 999, 13, 666, -5}');
insert into mySets values (4,'{    1  ,  3  ,  5 , 7,9 }');
insert into mySets values (5,'{a,b,c}');
insert into mySets values (6,'{1, 2.0, 3}');
insert into mySets values (7,'{1, {2,3}, 4}');
insert into mySets values (8,'{1, 2, 3, 4, five}');
insert into mySets values (9,'{ 1 2 3 4 }');