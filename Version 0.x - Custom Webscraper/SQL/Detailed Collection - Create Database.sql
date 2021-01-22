DROP TABLE IF EXISTS `Role` ;
DROP TABLE IF EXISTS `Tagline` ;
DROP TABLE IF EXISTS `MovieGenre` ;
DROP TABLE IF EXISTS `MovieProduction` ;

DROP TABLE IF EXISTS `RoleCode` ;
DROP TABLE IF EXISTS `Person` ;
DROP TABLE IF EXISTS `Genre` ;
DROP TABLE IF EXISTS `Production` ;

DROP TABLE IF EXISTS `Movie` ;

CREATE TABLE `Movie` (
  `movie_id` CHAR(9) NOT NULL,
  `movie_title` VARCHAR(200) NULL,
  `movie_year` INT NULL,
  `movie_runtime` INT NULL,
  `movie_boxoffice` BIGINT NULL,
  `movie_budget` INT NULL,
  PRIMARY KEY (`movie_id`))
;
CREATE TABLE  `Production` (
  `production_id` INT NOT NULL,
  `production_name` VARCHAR(45) NULL,
  PRIMARY KEY (`production_id`))
;
CREATE TABLE  `Genre` (
  `genre_id` INT NOT NULL,
  `genre_name` VARCHAR(45) NULL,
  PRIMARY KEY (`genre_id`))
;

CREATE TABLE  `Person` (
  `person_id` INT NOT NULL,
  `person_name` VARCHAR(45) NULL,
  PRIMARY KEY (`person_id`))
;
CREATE TABLE  `RoleCode` (
  `role_code` INT NOT NULL,
  `role_name` VARCHAR(45) NULL,
  PRIMARY KEY (`role_code`))
;

CREATE TABLE  `MovieProduction` (
  `production_id` INT NOT NULL,
  `movie_id` CHAR(9) NOT NULL,
  PRIMARY KEY (`production_id`, `movie_id`),
    FOREIGN KEY (`production_id`)
    REFERENCES `Production` (`production_id`)  ,
    FOREIGN KEY (`movie_id`)
    REFERENCES `Movie` (`movie_id`)
    
    )
;

CREATE TABLE  `MovieGenre` (
  `genre_id` INT NOT NULL,
  `movie_id` CHAR(9) NOT NULL,
  PRIMARY KEY (`genre_id`, `movie_id`),
    FOREIGN KEY (`genre_id`)
    REFERENCES `Genre` (`genre_id`)
    
    ,
    FOREIGN KEY (`movie_id`)
    REFERENCES `Movie` (`movie_id`)
    
    )
;

CREATE TABLE  `Tagline` (
  `tagline_id` INT NOT NULL,
  `tagline_text` VARCHAR(200) NULL,
  `movie_id` CHAR(9) NOT NULL,
  PRIMARY KEY (`tagline_id`),
    FOREIGN KEY (`movie_id`)
    REFERENCES `Movie` (`movie_id`)
    
    )
;
CREATE TABLE  `Role` (
  `movie_id` CHAR(9) NOT NULL,
  `role_code` INT NOT NULL,
  `person_id` INT NOT NULL,
  PRIMARY KEY (`movie_id`, `role_code`, `person_id`),
    FOREIGN KEY (`movie_id`)
    REFERENCES `Movie` (`movie_id`)
    ,
    FOREIGN KEY (`role_code`)
    REFERENCES `RoleCode` (`role_code`)
    ,
    FOREIGN KEY (`person_id`)
    REFERENCES `Person` (`person_id`)
    )
;

