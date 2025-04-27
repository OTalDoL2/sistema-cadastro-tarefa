-- Procedure Verifica se a Tarefa foi Encerrada

-- Procedure Inserir
CREATE PROCEDURE ListarTarefas
AS
BEGIN
    SELECT *
    FROM Tarefas
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