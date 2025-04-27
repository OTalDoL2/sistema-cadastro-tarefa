-- Procedure Inserir
CREATE PROCEDURE ListarTarefas
AS
BEGIN
    SELECT *
    FROM Tarefas
END

-- Procedure Buscar Status atual
CREATE PROCEDURE BuscarStatus
    @TarefaId INT
AS
BEGIN
    SELECT Status
    FROM Tarefas
    WHERE TarefaId = @TarefaId
END

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

-- Procedure Atualizar Status
CREATE PROCEDURE AtualizarStatusTarefa
    @Status NVARCHAR(50),
    @TarefaId INT
AS
BEGIN
    UPDATE Tarefas set Status = @Status WHERE TarefaId = @TarefaId
END

-- Procedure Tarefa Concluida
CREATE PROCEDURE ConcluirTarefa
    @TarefaId INT
AS
BEGIN
    UPDATE Tarefas set Status = 'Concluído', DataConclusao = GETDATE() WHERE TarefaId = @TarefaId
END

-- Procedure Excluir Tarefa
CREATE PROCEDURE DeletarTarefa
    @TarefaId INT
AS
BEGIN
    DELETE FROM Tarefas WHERE TarefaId = @TarefaId
END
