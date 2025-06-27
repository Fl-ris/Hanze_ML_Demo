create table IF NOT EXISTS vragenlijst_data(
id int AUTO_INCREMENT,
leeftijd int,
gewicht int,
lengte int,
voorspelling_correct boolean

);

insert into vragenlijst_data(leeftijd, gewicht, lengte) values(23, 70, 180)