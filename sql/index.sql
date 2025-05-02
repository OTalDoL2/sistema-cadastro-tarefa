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

-- Procedure Verifica se a Tarefa foi Encerrada

-- Procedure Listar
CREATE PROCEDURE ListarTarefas
AS
BEGIN
    SELECT *
    FROM Tarefas
END
GO

CREATE PROCEDURE ListarTarefa
    @TarefaId INT
AS
BEGIN
    SELECT *
    FROM Tarefas
    WHERE TarefaId = @TarefaId

END
GO

-- Procedure Buscar Status atual
CREATE PROCEDURE BuscarStatus
    @TarefaId INT
AS
BEGIN
    SELECT Status
    FROM Tarefas
    WHERE TarefaId = @TarefaId
END
GO

-- Procedure Inserir
CREATE PROCEDURE AdicionarNovaTarefa
    @Descricao NVARCHAR(MAX)
AS
BEGIN
    INSERT INTO Tarefas
        (Descricao, Status, DataCriacao)
    VALUES
        (@Descricao, 'Não Iniciada', GETDATE())
END
GO

-- Procedure Atualizar Status
CREATE PROCEDURE AtualizarStatusTarefa
    @Status NVARCHAR(50),
    @TarefaId INT
AS
IF EXISTS(SELECT 1 FROM Tarefas WHERE TarefaId = @TarefaId AND Status != 'Concluída' AND Status != 'Cancelada')
    BEGIN
        UPDATE Tarefas set Status = @Status WHERE TarefaId = @TarefaId
    END
ELSE
    BEGIN
        PRINT 'Tarefa já foi encerrada. Atualização não permitida.'
    END
GO

-- Procedure Tarefa Concluida
CREATE PROCEDURE ConcluirTarefa
    @TarefaId INT
AS
IF EXISTS(SELECT 1 FROM Tarefas WHERE TarefaId = @TarefaId AND Status != 'Concluída' AND Status != 'Cancelada')
    BEGIN
        UPDATE Tarefas set Status = 'Concluída', DataConclusao = GETDATE() WHERE TarefaId = @TarefaId
    END
ELSE
    BEGIN
        PRINT 'Tarefa já está encerrada. Atualização não permitida.'
    END
GO

-- Procedure Excluir Tarefa
CREATE PROCEDURE DeletarTarefa
    @TarefaId INT
AS
IF EXISTS(SELECT 1 FROM Tarefas WHERE TarefaId = @TarefaId AND Status != 'Concluída' AND Status != 'Cancelada')
    BEGIN
        DELETE FROM Tarefas WHERE TarefaId = @TarefaId
    END
ELSE
    BEGIN
        PRINT 'Tarefa já está encerrada. Atualização não permitida.'
    END
GO

-- Procedure Tarefa Cancelada
CREATE PROCEDURE CancelarTarefa
    @TarefaId INT
AS
IF EXISTS(SELECT 1 FROM Tarefas WHERE TarefaId = @TarefaId AND Status != 'Concluída' AND Status != 'Cancelada')
    BEGIN
        UPDATE Tarefas set Status = 'Cancelada', DataConclusao = GETDATE() WHERE TarefaId = @TarefaId
    END
ELSE
    BEGIN
        PRINT 'Tarefa já está encerrada. Atualização não permitida.'
    END
GO

EXEC AdicionarNovaTarefa "Fazer as compras para cozinha do escritório" GO
EXEC AdicionarNovaTarefa "Comprar complemento da mobilia" GO
EXEC AdicionarNovaTarefa "Marcar instalação da internet" GO
EXEC AdicionarNovaTarefa "Fazer orçamento da instalação energia solar" GO


