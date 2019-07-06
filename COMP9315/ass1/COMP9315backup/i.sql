CREATE FUNCTION intset_in(cstring)
   RETURNS intSet
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION intset_out(intSet)
   RETURNS cstring
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intSet'
   LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE intSet (
   internallength = 40,
   input = intset_in,
   output = intset_out
);


create table mySets (id integer primary key, iset intSet);

insert into mySets values (1, '{1,2,3}');

select * from mySets;

drop type intSet cascade;

drop table mySets;