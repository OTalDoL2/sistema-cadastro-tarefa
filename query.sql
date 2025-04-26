CREATE TABLE SistemaCadastroTarefa
GO

USE SistemaCadastroTarefa;
GO

CREATE TABLE Tarefas
(
    TarefaId int IDENTITY(1,1),
    Descricao varchar(250),
    Status varchar(20),
    DataCriacao DATE,
    DataConclusao DATE,
    PRIMARY KEY(TarefaId)
);
GO

