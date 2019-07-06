CREATE FUNCTION intset_in(cstring)
   RETURNS intset
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION intset_out(intset)
   RETURNS cstring
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE FUNCTION belong(integer, cstring)
	RETURNS bool
	AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE TYPE intset (
   input = intset_in,
   output = intset_out
);

CREATE FUNCTION belong(integer, intset)
   RETURNS bool
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR <@(
   leftarg = integer,
   rightarg = intset,
   procedure = belong);


CREATE FUNCTION count(intset)
   RETURNS integer
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR @(
   rightarg = intset,
   procedure = count);


CREATE FUNCTION subset(intset, intset)
   RETURNS bool
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR @> (
   leftarg = intset,
   rightarg = intset,
   procedure = subset);

CREATE FUNCTION equal(intset, intset)
   RETURNS bool
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR = (
   leftarg = intset,
   rightarg = intset,
   procedure = equal,
   commutator = =
);

CREATE FUNCTION intset_intersection(intset,intset)
   RETURNS intset
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR && (
   leftarg = intset,
   rightarg = intset,
   procedure = intset_intersection,
   commutator = &&
);

CREATE FUNCTION intset_union(intset,intset)
   RETURNS intset
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR || (
   leftarg = intset,
   rightarg = intset,
   procedure = intset_union,
   commutator = ||
);

CREATE FUNCTION intset_disjunction(intset,intset)
   RETURNS intset
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR !!(
   leftarg = intset,
   rightarg = intset,
   procedure = intset_disjunction,
   commutator = !!);

CREATE FUNCTION intset_diff(intset,intset)
   RETURNS intset
   AS '/srvr/z5089358/postgresql-10.4/src/tutorial/intset'
   LANGUAGE C IMMUTABLE STRICT;

CREATE OPERATOR -(
   leftarg = intset,
   rightarg = intset,
   procedure = intset_diff); 


