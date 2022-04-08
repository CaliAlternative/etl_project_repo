--CREATE DATABASE etl_capstone_relational
--GO

--USE etl_capstone_relational

--DROP TABLE IF EXISTS Expenses

CREATE TABLE "Expenses"
(
	"date" date,
	"USD" money,
	"rate" DECIMAL(6,5),
	"CAD" money
);