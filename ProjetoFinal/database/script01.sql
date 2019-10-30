DROP DATABASE IF EXISTS TAREFAS_DB;
CREATE DATABASE TAREFAS_DB;
USE TAREFAS_DB;

CREATE TABLE tarefas (
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(30) NOT NULL,
    nivel VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO tarefas (nome, nivel) VALUES ("cozinhar", 3);
INSERT INTO tarefas (nome, nivel) VALUES ("limpar casa", 1);
INSERT INTO tarefas (nome, nivel) VALUES ("estudar", 4);