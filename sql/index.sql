-- Criação do Banco de Dados
CREATE DATABASE SistemaCadastroTarefa
GO

USE SistemaCadastroTarefa;
GO

-- Criação da Tabela
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



