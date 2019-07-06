
-- The first part of the exercise simply involved re-ordering the 
-- data in the data.sql file so that tables were inserted in an
-- order such that there would never be references to keys that
-- were not already inserted into the database.
--
-- Valid orders for populating tables:
--    Employee, Department, Mission, WorksFor
--    Employee, Department, WorksFor, Mission

-- The second part of the exercise required addition of constraints
-- to the original schema. One possible solution for this is given
-- below. (Question 10 excluded)

create table Employees (
	tfn 		char(11)
	            constraint ValidTFN
				check (tfn ~ '[0-9]{3}-[0-9]{3}-[0-9]{3}'),
	givenName   varchar(30) not null,  -- must have a given name
	familyName  varchar(30),           -- some people have only one name
	hoursPweek  float
				check (hoursPweek >= 0 and hoursPweek <= 168), --7*24 
	primary key (tfn)
);

create table Departments (
	id          char(3)                          -- [[:digit:]] == [0-9]
	            constraint ValidDeptId check (id ~ '[[:digit:]]{3}'),
	name        varchar(100) unique,
	manager     char(11) not null unique
	            constraint ValidEmployee references Employees(tfn),
	primary key (id)
);

create table DeptMissions (
	department  char(3)
	            constraint ValidDepartment references Departments(id),
	keyword     varchar(20),
	primary key (department,keyword)
);

create table WorksFor (
	employee    char(11)
		    constraint ValidEmployee references Employees(tfn),
	department  char(3)
		    constraint ValidDepartment references Departments(id),
	percentage  float
	            constraint ValidPercentage
		    check (percentage > 0.0 and percentage <= 100.0),
	primary key (employee,department)
);


create function check_worksfor_insert()
	 returns trigger as $sum_of_percentage$
    declare
	percentage1 float;
	percentage2 float;
    begin
	select into percentage1 sum(percentage) 
	from WorksFor
	where employee = NEW.employee;
	percentage2 = percentage1 + NEW.percentage;
	if percentage2 > 100 then
	    raise exception 'work percentage cannot exceed 100 percent';
	end if;
	return NEW;
    end;
$sum_of_percentage$ language plpgsql;
	
create trigger sum_of_percentage before insert or update on WorksFor
    for each row execute procedure check_worksfor_insert();