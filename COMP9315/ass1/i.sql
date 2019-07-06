drop type intSet cascade;

drop table mySets;

drop function belong cascade;

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

CREATE FUNCTION count(intSet)
   RETURNS integer
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR @(
rightarg = intSet,
procedure = count);

CREATE FUNCTION subset(intSet, intSet)
   RETURNS bool
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR @> (
leftarg = intSet,
rightarg = intSet,
procedure = subset);

CREATE FUNCTION equal(intSet, intSet)
   RETURNS bool
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR = (
   leftarg = intSet,
   rightarg = intSet,
   procedure = equal,
   commutator = =
);

CREATE FUNCTION intSet_intersection(intSet,intSet)
   RETURNS intSet
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR && (
   leftarg = intSet,
   rightarg = intSet,
   procedure = intSet_intersection,
   commutator = &&
);

CREATE FUNCTION intSet_union(intSet,intSet)
   RETURNS intSet
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR || (
   leftarg = intSet,
   rightarg = intSet,
   procedure = intSet_union,
   commutator = ||
);

CREATE FUNCTION intSet_disjunction(intSet,intSet)
   RETURNS intSet
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR !!(
   leftarg = intSet,
   rightarg = intSet,
   procedure = intSet_disjunction,
   commutator = !!);

CREATE FUNCTION intSet_diff(intSet,intSet)
   RETURNS intSet
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR -(
   leftarg = intSet,
   rightarg = intSet,
   procedure = intSet_diff); 


create or replace table mySets (id integer primary key, iset intSet);


insert into mySets values (1, '{3,1,2}');

insert into mySets values (2, '{3,1,3,1}');

insert into mySets values (3, '{4,5,3}');

insert into mySets values (4, '{5, 4}');

select * from mySets;

select * from mySets where id<@ iset;

select *,@iset from mySets;

select '{1,2,3}'::intSet = '{1,2,3}'::intSet;
select '{1,2,3}'::intSet = '{1,2,4}'::intSet;
select '{}'::intSet = '{}'::intSet;
select '{}'::intSet = '{1,2,4}'::intSet;


select a.*, b.* from mySets a, mySets b where (b.iset @> a.iset) and a.id != b.id;
update mySets set iset = iset && '{1,3,4,6}' where id = 4;
update mySets set iset = iset || '{5,6,7,8}' where id = 4;

update mySets set iset = iset !! '{3,4,5}' where id = 1;

update mySets set iset = iset - '{1,2,3}' where id = 3;






drop type intSet cascade;

drop function belong cascade;

update mySets set iset = iset && '{1,3,4,6}' where id = 4;









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