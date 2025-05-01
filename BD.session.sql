-- Procedure Excluir Tarefa
CREATE PROCEDURE DeletarTarefa
    @TarefaId INT
AS
IF EXISTS(SELECT 1 FROM Tarefas WHERE TarefaId = @TarefaId)
    BEGIN
        DELETE FROM Tarefas WHERE TarefaId = @TarefaId
    END
ELSE
    BEGIN
        PRINT 'Tarefa já está encerrada. Atualização não permitida.'
    END
GO
